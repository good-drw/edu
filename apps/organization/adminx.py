#!/user/bin/env/python
# -*- coding:utf-8 -*-
__author__ = 'drw'
__date__ = '2017/1/31 21:22'

import xadmin

from .models import CityDict, CourseOrg, Teacher

class CityDictAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']

class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city', 'course_num', 'add_time']
    search_fields  = ['name', 'desc', 'click_num', 'fav_num', 'image', 'address','course_num', 'city']
    list_filter =  ['name', 'desc', 'click_num', 'fav_num', 'image', 'address', 'city__name','course_num', 'add_time']
    relfield_style = 'fk-ajax'#将这个字段设置为搜索模式
    style_fields = {"desc": "ueditor"}

class TeacherAdmin(object):
    list_display = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']
    search_fields  = ['org', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num']
    list_filter  = ['org__name', 'name', 'work_years', 'work_company', 'work_position', 'points', 'click_num', 'fav_num', 'add_time']

xadmin.site.register(CityDict, CityDictAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(Teacher, TeacherAdmin)
