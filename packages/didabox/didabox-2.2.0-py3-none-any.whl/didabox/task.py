# -*- coding: utf-8 -*-

"""
@Project : didabox 
@File    : task.py
@Date    : 2023/10/31 13:42:42
@Author  : zhchen
@Desc    : 
"""
from requests import Response

from didabox.utils import MidBox


class TaskBox(MidBox):
    def _task_api(self, data: dict) -> Response:
        response = self.req.post('https://api.dida365.com/api/v2/batch/task', json=data)
        return response

    def add_reminders_task(self, project_id: str, title: str, content: str, trigger_time: str) -> Response:
        trigger_time = self.str2utc(trigger_time)
        json_data = {
            'add': [
                {
                    'items': [],
                    'reminders': [
                        {
                            'id': self.random_int(),
                            'trigger': 'TRIGGER:PT0S',
                        },
                    ],
                    'exDate': [],
                    'dueDate': None,
                    'priority': 0,
                    'isAllDay': False,
                    'repeatFlag': None,
                    'progress': 0,
                    'assignee': None,
                    'sortOrder': -self.random_int(),
                    'startDate': self.shanghai2utc(trigger_time),
                    'isFloating': False,
                    'status': 0,
                    'projectId': project_id,
                    'kind': None,
                    'createdTime': self.shanghai2utc(self.now()),
                    'modifiedTime': self.shanghai2utc(self.now()),
                    'title': title,
                    'tags': [],
                    'timeZone': self.req.tz,
                    'content': content,
                    'id': self.random_str(),
                },
            ],
            'update': [],
            'delete': [],
            'addAttachments': [],
            'updateAttachments': [],
            'deleteAttachments': [],
        }
        return self._task_api(json_data)
