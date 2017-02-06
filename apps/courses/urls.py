#!/user/bin/env/python
# -*- coding:utf-8 -*-


from django.conf.urls import url, include

from .views import CourseListView
from .views import CourseDetailView
from .views import CourseInfoView
from .views import CourseCommentView
from .views import AddCommentsView
from .views import VideoPlayView



urlpatterns = [
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    url(r'^detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(), name='course_detail'),
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    url(r'comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),
    url(r'add_comment/$', AddCommentsView.as_view(), name='add_comment'), #添加课程评论
    url(r'video_play/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play')
]