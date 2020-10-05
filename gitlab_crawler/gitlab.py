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
import logging
import time

from gitlab_crawler.async_crawler import get_projects_list, get_project_commits, get_info_about_projects
from gitlab_crawler.utils import save_data

log = logging.getLogger(__name__)
loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)


def dump_gitlab_page(work_dir: str, start_date=None, end_date=None, start_id: int = None):
    current_id = start_id
    while True:
        projects = asyncio.get_event_loop() \
            .run_until_complete(get_projects_list(id_before=current_id, after=start_date, before=end_date))

        if len(projects) == 0:
            log.info(f'All projects data from {start_date} to {end_date} are loaded')
            break

        last_project_id = projects[-1].get('id')
        save_data(path=f'{work_dir}/projects/', file_name=f'{current_id}_{last_project_id}_project.json', data=projects)

        commits = asyncio.get_event_loop() \
            .run_until_complete(get_project_commits(projects=projects, since=start_date, until=end_date))
        save_data(path=f'{work_dir}/commits/',
                  file_name=f'{current_id}_{last_project_id}_project_commits.json', data=commits)

        metadata = asyncio.get_event_loop().run_until_complete(get_info_about_projects(projects=projects))
        save_data(path=f'{work_dir}/meta/', file_name=f'{current_id}_{last_project_id}_project_meta.json',
                  data=metadata)

        current_id = last_project_id
        log.info('sleep for 8 minutes..')
        time.sleep(480)


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    dump_gitlab_page(work_dir='dump_gitlab')
