"""Copyright since 2020, EPAM Systems

   This file is part of OSCI.

   OSCI is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   OSCI is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with OSCI.  If not, see <http://www.gnu.org/licenses/>."""

import asyncio
import json
import logging
import re
import ssl

import aiohttp
import certifi
import tqdm as tqdm
from aiohttp import ClientTimeout
from bs4 import BeautifulSoup

from gitlab_crawler.base import Project

log = logging.getLogger(__name__)
ssl_context = ssl.create_default_context(cafile=certifi.where())

BASE_API_URL = 'https://gitlab.com/api/v4'
SEMAPHORE_VALUE = 2
MAX_ALLOWED_PAGINATION_OFFSET = 500
MAX_ALLOWED_ITEMS_PER_PAGE = 100


async def fetch(sem, session, url):
    async with sem:
        try:
            response = await session.get(url, ssl=ssl_context, timeout=ClientTimeout())
        except (asyncio.TimeoutError,
                aiohttp.ServerDisconnectedError,
                aiohttp.ClientConnectionError) as ex:
            log.error(ex)
            log.error(url)
            return ""
        if response.status == 200:
            return await response.text()
        if response.status == 404:
            log.warning(f'404 code: {url}')
            return ""
        else:
            log.warning(f'unavailable url: {url} - {response.status} code')
            return ""


async def get_projects_list(id_before: int, after, before):
    """Loads projects for required time period

    :param id_before: Limit results to projects with IDs less than the specified ID
    :param after: Limit results to projects with last_activity after specified time. Format: ISO 8601
    :param before: Limit results to projects with last_activity before specified time. Format: ISO 8601
    :return:
    """
    # Offset pagination has a maximum allowed offset of 50000 for requests that return objects of type Project
    sem = asyncio.Semaphore(SEMAPHORE_VALUE)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(sem=sem, session=session, url=__get_projects_url(id_before=id_before,
                                                                        page=page,
                                                                        last_activity_after=after,
                                                                        last_activity_before=before))
                 for page in range(1, MAX_ALLOWED_PAGINATION_OFFSET+1)]
        concat_projects = []
        for item in [await f for f in tqdm.tqdm(asyncio.as_completed(tasks),
                                                total=len(tasks), desc='get_projects_list: ')]:
            try:
                concat_projects += json.loads(item)
            except json.JSONDecodeError as ex:
                log.error(ex)
        return concat_projects


def __get_projects_url(id_before: int,
                       page: int,
                       last_activity_after,
                       last_activity_before,
                       order_by: str = 'last_activity_at',
                       sort: str = 'desc',
                       per_page: int = MAX_ALLOWED_ITEMS_PER_PAGE):
    """Collects a list of projects

    :param page: required page
    :param order_by: projects ordered by id, name, path, created_at, updated_at, or last_activity_at fields.
    :param sort: projects sorted in asc or desc order.
    :param per_page: an amount of projects per page
    :return: url
    """
    return f'{BASE_API_URL}/projects?order_by={order_by}' \
           f'&sort={sort}' \
           f'&page={page}' \
           f'&per_page={per_page}' \
           f'&id_before={id_before if id_before is not None else ""}' \
           f'&last_activity_before={last_activity_before if last_activity_before is not None else ""}' \
           f'&last_activity_after={last_activity_after if last_activity_after is not None else ""}'


async def fetch_project_commits(sem, session, project: Project, since: str, until: str):
    commits = await fetch(sem=sem, session=session,
                          url=__get_commits_url(project=project, since=since, until=until))
    try:
        commits = json.loads(commits)
    except json.JSONDecodeError as ex:
        log.error(ex)
    return project, commits


async def get_project_commits(projects, since: str, until: str):
    sem = asyncio.Semaphore(SEMAPHORE_VALUE)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_project_commits(sem=sem,
                                       session=session,
                                       project=Project(project),
                                       since=since, until=until)
                 for project in projects]
        commits = []
        for project, data in [await f for f in tqdm.tqdm(asyncio.as_completed(tasks),
                                                         total=len(tasks),
                                                         desc='get_project_commits: ')]:
            project_id = project.id
            if len(data) > 0:
                for item in data:
                    item['project_id'] = project_id
                    commits.append(item)
    return commits


def __get_commits_url(project: Project, since, until):
    return f'{BASE_API_URL}/projects/{project.id}/repository/commits?' \
           f'since={since if since is not None else ""}' \
           f'&until={until if until is not None else ""}'


async def fetch_projects_pages(sem, session, project: Project):
    page = await fetch(sem=sem, session=session, url=project.web_url)
    return project, page


async def get_info_about_projects(projects):
    sem = asyncio.Semaphore(SEMAPHORE_VALUE)
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_projects_pages(sem=sem, session=session, project=Project(project)) for project in projects]
        projects_info = []
        for project, page in [await f for f in
                              tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks), desc='get_project_page: ')]:
            projects_info.append({'project_id': project.id,
                                  'project_license': get_project_license(page),
                                  'project_mirrored': get_project_type(page)})
    return projects_info


def get_project_license(response) -> str:
    soup = BeautifulSoup(response, 'html.parser')
    ui_project_buttons = soup.find('div', {'class': 'project-buttons gl-mb-3 js-show-on-project-root'})
    try:
        for ui_button in ui_project_buttons.find_all_next('a'):
            if re.findall('/LICENSE$', ui_button.get('href')):
                return ui_button.text
    except AttributeError:
        pass


def get_project_type(response) -> str:
    soup = BeautifulSoup(response, 'html.parser')
    home_panel = soup.find('div', {'class': 'home-panel-home-desc mt-1'})
    try:
        for block in home_panel.find_all_next('p'):
            paragraph = block.text.lower()
            if re.findall('pull mirror', paragraph):
                return paragraph
    except AttributeError:
        pass
