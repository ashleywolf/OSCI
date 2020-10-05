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


class Project:
    def __init__(self, json_payload: dict = None):
        json_payload = json_payload or dict()
        self.id = json_payload.get('id')
        self.description = json_payload.get('description')
        self.name = json_payload.get('name')
        self.created_at = json_payload.get('created_at')
        self.web_url = json_payload.get('web_url')
        self.readme_url = json_payload.get('readme_url')
        self.forks_count = json_payload.get('forks_count')
        self.star_count = json_payload.get('star_count')
        self.last_activity_at = json_payload.get('last_activity_at')
