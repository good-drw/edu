# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.apps import AppConfig


class OperationConfig(AppConfig):
    '''要在init去注册'''
    name = 'operation'
    verbose_name = u'用户操作'
