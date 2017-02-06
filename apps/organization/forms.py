#!/user/bin/env/python
# -*- coding:utf-8 -*-
__author__ = 'drw'
__date__ = '2017/2/3 11:25'

from django import forms
from operation.models import UserAsk
import re

#表单验证 继承modelform
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']
    def clean_mobile(self):
        '''
        自定义mobile验证
        :return:
        '''
        mobile = self.cleaned_data['mobile'] #取到mobile
        REGEX_MOBILE = '^1[358]\d{9}$|^147/d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")
