# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.apps import AppConfig


class CoursesConfig(AppConfig):
    '''要在init去注册'''
    name = 'courses'
    verbose_name = u'课程管理'