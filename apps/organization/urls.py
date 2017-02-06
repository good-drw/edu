#!/user/bin/env/python
# -*- coding:utf-8 -*-
__author__ = 'drw'
__date__ = '2017/2/3 11:29'

from django.conf.urls import url, include

from .views import OrgListView #引入课程机构首页类
from .views import AddUserAskView
from .views import OrgHomeView
from .views import OrgCourseView
from .views import OrgDescView
from .views import OrgTeacherView
from .views import AddFavView
from .views import TeacherListView
from .views import TeacherDetailView


urlpatterns = [
    url(r'^list/$', OrgListView.as_view(), name='org_list'),    #课程机构首页
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'), #课程咨询提交
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^detail/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_detail'),
    url(r'^org_teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),#机构收藏
    url(r'^teacher/list/$', TeacherListView.as_view(), name='teacher_list'), #讲师列表页
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetailView.as_view(), name='teacher_detail')
]