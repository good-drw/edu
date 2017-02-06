# _*_ encoding:utf-8 _*_
import json
from django.shortcuts import render, HttpResponse
from django.contrib.auth import authenticate, login, logout #django提供的验证方法
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.http import HttpResponse, HttpResponseRedirect
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator,EmptyPage, PageNotAnInteger

from datetime import datetime
import time

from .models import UserProfile,EmailVerifyRecord, Banner
from forms import LoginForm, RegisterForm, ForgetForm, ModifyForm
from django.contrib.auth.hashers import make_password #密码加密
from utils.email_send import send_regiser_email #引入邮箱功能
from .forms import UploadImageForm, UserInfoForm
from operation.models import UserCourse, UserFavorite, UserMessage
from organization.models import CourseOrg, Teacher
from courses.models import Course


# Create your views here.


class CustomBackend(ModelBackend):
    '''
    使登陆能验证邮箱或用户名
    '''
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username)) #Q来做"或"
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, 'login.html', {})
    def post(self, request):
        '''登陆'''
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', None)
            pwd = request.POST.get('password', None)
            user = authenticate(username=username, password=pwd)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    from django.core.urlresolvers import reverse
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg":"用户名或密码错误"})
        else:
            return render(request, "login.html", {"login_form":login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm() #实例化
        return render(request, "register.html", {'register_form':register_form})
    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = request.POST.get('email', '')
            if UserProfile.objects.filter(email=username):
                return render(request, "register.html", {"register_form": register_form, "msg":"用户已经存在"})
            pwd = request.POST.get('password',  '')
            user_profile = UserProfile()
            user_profile.username = username
            user_profile.email = username
            user_profile.is_active = False
            user_profile.password = make_password(pwd)
            user_profile.save()

            #写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id
            user_message.message = '欢迎注册'
            user_message.save()

            send_regiser_email(username, "register")
            return render(request, "login.html")
        else:
            return render(request, "register.html", {"register_form":register_form})


class LogOutView(View):
    def get(self, request):
        logout(request)
        #django重定向
        from django.core.urlresolvers import reverse
        return HttpResponseRedirect(reverse('index'))

class ActiveUserView(View):
    '''点击邮件,通过验证'''
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                old_time = str(record.send_time)  #将时间转为字符串
                old_time = old_time.split('.') #以"."分割字符串
                old_time = time.mktime(time.strptime(old_time[0], "%Y-%m-%d %H:%M:%S")) #将第一部分转为时间戳
                now_time = time.time() #现在时间
                if(now_time - old_time >= 15*60):
                    return render(request, "active_fail.html")
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, 'forgetpwd.html', {'forget_form':forget_form})
    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', '')
            send_regiser_email(email, 'forget')
            return render(request, 'send_success.html')
        else:
            return render(request, 'forgetpwd.html', {"forget_form":forget_form})


class ResetUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                old_time = str(record.send_time)  # 将时间转为字符串
                old_time = old_time.split('.')  # 以"."分割字符串
                old_time = time.mktime(time.strptime(old_time[0], "%Y-%m-%d %H:%M:%S"))  # 将第一部分转为时间戳
                now_time = time.time()  # 现在时间
                if (now_time - old_time >= 15 * 60):
                    return render(request, "active_fail.html")
                return render(request, "password_reset.html", {"email":email})
        else:
            return render(request, "active_fail.html")
        return render(request, "login.html")


class ModifyPwdView(View):
    '''修改用户密码'''
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')

            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email":email, "msg":"密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request, "login.html")
        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html", {"email": email, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    '''用户个人信息'''
    def get(self, request):
        return render(request, 'user/usercenter-info.html')
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    '''修改头像'''
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
           image_form.save()
           return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    '''修改个人中心密码'''
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin, View):
    '''发送邮箱验证码'''
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')
        send_regiser_email(email, 'update')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''修改个人邮箱'''
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class UserCourseView(LoginRequiredMixin, View):
    '''我的课程'''
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'user/usercenter-mycourse.html', {
            'user_courses':user_courses
        })


class MyfavOrgView(LoginRequiredMixin, View):
    '''个人中心 收藏机构'''
    def get(self, request):
        org_list = []
        myfav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for myfav_org in myfav_orgs:
            org_id = myfav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'user/usercenter-fav-org.html', {
            'org_list':org_list
        })


class MyfavTeacherView(LoginRequiredMixin, View):
    '''个人中心 授课讲师'''
    def get(self, request):
        teacher_list = []
        myfav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for myfav_teacher in myfav_teachers:
            teacher_id = myfav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, 'user/usercenter-fav-teacher.html', {
            'teacher_list':teacher_list
        })

class MyfavCourseView(LoginRequiredMixin, View):
    '''个人中心 收藏课程'''
    def get(self, request):
        course_list = []
        myfav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for myfav_course in myfav_courses:
            course_id = myfav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'user/usercenter-fav-course.html', {
            'course_list':course_list
        })


class UserMessageView(LoginRequiredMixin, View):
    '''个人中心 我的消息'''
    def get(self, request):
        all_message = UserMessage.objects.filter(user=request.user.id)
        #点进去后把未读消息变为已读
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 3, request=request)
        all_message = p.page(page)
        return render(request, 'user/usercenter-message.html', {
            'all_message':all_message
        })


class IndexView(View):
    def get(self, request):
        #取出轮播图
        all_banners = Banner.objects.all().order_by('index')
        #轮播课程
        course_banners = Course.objects.filter(is_banner=True)[:3]
        #非轮播课程
        courses = Course.objects.filter(is_banner=False)[:6]
        #课程机构
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request, "index.html", {
            'all_banners':all_banners,
            'course_banners':course_banners,
            'courses':courses,
            'course_orgs':course_orgs
        })


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('redirect/404.html', {})
    response.status_code = 404
    return response


def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('redirect/500.html', {})
    response.status_code = 500
    return response






























