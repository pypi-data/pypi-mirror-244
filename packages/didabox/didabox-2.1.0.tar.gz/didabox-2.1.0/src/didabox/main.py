# -*- coding: utf-8 -*-

"""
@Project : didabox 
@File    : main.py
@Date    : 2023/12/1 10:16:44
@Author  : zhchen
@Desc    : 
"""
from requests import Response

from didabox.check import CheckBox
from didabox.request import Request
from didabox.task import TaskBox
from didabox.login import LoginBox


class DidaBox:
    def __init__(self, cookies: dict, headers=None):
        self.req = Request(cookies=cookies, tz='Asia/Shanghai', headers=headers)
        self.check_box = CheckBox(self)
        self.task_box = TaskBox(self)
        self.login_box = LoginBox(self)

    def check_cookie(self) -> Response:
        """检测cookie是否过期"""
        return self.check_box.check_cookie()

    def add_simple_task(self, project_id: str, title: str, content: str, trigger_time: str) -> Response:
        """
        添加简单的任务
        :param project_id: 清单id
        :param title: 任务标题
        :param content: 任务内容
        :param trigger_time: 触发时间, 准时触发. 格式: %Y-%m-%d %H:%M:%S
        :return:
        """
        return self.task_box.add_reminders_task(project_id, title, content, trigger_time)

    def sign_on(self, username, password) -> Response:
        """
        账号密码登录, 登录完成后自动更新cookie
        :param username: 账号
        :param password: 密码
        :return:
        """
        return self.login_box.sign_on(username, password)
