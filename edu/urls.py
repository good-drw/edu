# _*_ encoding:utf-8 _*_
"""edu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from users import views
import xadmin
from django.views.static import serve #处理静态文件
from edu.settings import MEDIA_ROOT


from users.views import LoginView #引入登陆类
from users.views import RegisterView #引入注册类
from users.views import ActiveUserView #引入激活类
from users.views import ForgetPwdView #引入找回密码类
from users.views import ResetUserView
from users.views import ModifyPwdView
from users.views import LogOutView
from users.views import IndexView




urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),#验证码
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='user_active'),
    url(r'^forgetpwd/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetUserView.as_view(), name='reset_pwd'),
    url(r'^modifypwd/$', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^org/', include('organization.urls', namespace='org')),#课程机构url配置
    url(r'^media/(?P<path>.*)$', serve, {"document_root":MEDIA_ROOT}), #显示后台图片
    # url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}), #生产环境下显示静态文件
    url(r'^course/', include('courses.urls', namespace='course')),#课程相关url配置
    url(r'^user/', include('users.urls', namespace='user')),#课程相关url配置
    url(r'^ueditor/',include('DjangoUeditor.urls' )),#富文本相关url
]


#全局404页面配置
handler404 = 'users.views.page_not_found'
#全局500配置
handler500 = 'users.views.page_error'

















