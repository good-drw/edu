#!/user/bin/env/python
# -*- coding:utf-8 -*-
__author__ = 'drw'
__date__ = '2017/1/31 23:00'

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin
from .models import EmailVerifyRecord
from .models import Banner
from .models import UserProfile


# class UserProfileAdmin(UserAdmin):
#     pass


class BaseSetting(object):
    '''开启主题功能'''
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    '''修改后台系统默认字段'''
    site_title = '教育后台管理系统'
    site_footer = '后台管理'
    menu_style = 'accordion' #左侧导航收起

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time'] #后台显示字段
    search_fields = ['code', 'email', 'send_type'] #后台搜索
    list_filter = ['code', 'email', 'send_type', 'send_time'] #过滤器
    model_icon = 'fa fa-address-book-o'

class BannerAdmin(object):
    list_display = ['title', 'imgage', 'url', 'index', 'add_time']
    search_fields = ['title', 'imgage', 'url', 'index']
    list_filter = ['title', 'imgage', 'url', 'index', 'add_time']


'''因为xadmin bug 我们做了修改 所以这里不用注册'''
# from django.contrib.auth.models import User #卸载默认user
# xadmin.site.unregister(User)
# xadmin.site.register(UserProfile, UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting) #注册BaseSetting
xadmin.site.register(views.CommAdminView, GlobalSettings) #注册GlobalSettings