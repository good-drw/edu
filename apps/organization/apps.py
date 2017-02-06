# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals

from django.apps import AppConfig


class OrganizationConfig(AppConfig):
    '''要在init去注册'''
    name = 'organization'
    verbose_name = u'机构管理'
