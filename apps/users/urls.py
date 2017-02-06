#!/user/bin/env/python
# -*- coding:utf-8 -*-


from django.conf.urls import url, include

from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailCodeView, UpdateEmailView, UserCourseView
from .views import MyfavOrgView, MyfavTeacherView, MyfavCourseView, UserMessageView


urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),#用户信息
    url(r'^image/upload/$',UploadImageView.as_view(), name='image_upload'),#用户头像上传
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'), #用户个人中心修改密码
    url(r'^sendemail_code/$', SendEmailCodeView.as_view(), name='sendemail_code'), #发送邮箱验证码
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'), #修改邮箱
    url(r'^course/$', UserCourseView.as_view(), name='user_course'),#用户课程
    url(r'^myfav/org/$', MyfavOrgView.as_view(), name='myfav_org'),#收藏课程机构
    url(r'^myfav/teacher/$', MyfavTeacherView.as_view(), name='myfav_teacher'),  # 收藏授课教师
    url(r'^myfav/course/$', MyfavCourseView.as_view(), name='myfav_course'),  # 收藏课程
    url(r'^message/$', UserMessageView.as_view(), name='user_message'),#用户消息
]