#!/user/bin/env/python
# -*- coding:utf-8 -*-
__author__ = 'drw'
__date__ = '2017/2/1 10:03'

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile

class LoginForm(forms.Form):
    '''登陆表单验证'''
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)

class RegisterForm(forms.Form):
    '''注册表单验证'''
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class ForgetForm(forms.Form):
    '''找回密码表单'''
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid":u"验证码错误"})

class ModifyForm(forms.Form):
    '''修改密码表单验证'''
    password1 = forms.CharField(required=True, min_length=6)
    password2 = forms.CharField(required=True, min_length=6)

class UploadImageForm(forms.ModelForm):
    '''修改头像'''
    class Meta:
        model = UserProfile
        fields = ['img']

class UserInfoForm(forms.ModelForm):
    '''修改个人信息'''
    class Meta:
        model = UserProfile
        fields = ['nickname', 'gender', 'birday', 'address', 'mobile']