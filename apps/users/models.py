# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser



# Create your models here.


class UserProfile(AbstractUser):
    nickname = models.CharField(verbose_name=u'昵称', max_length=32, default=u'')
    birday = models.DateField(verbose_name=u'生日', null=True, blank=True)
    gender = models.CharField(verbose_name=u'性别', choices=(('male', u'男'), ('female', u'女')), max_length=6, default='male')
    address = models.CharField(verbose_name=u'地址', max_length=100, default=u'')
    mobile = models.CharField(max_length=30, null=True, blank=True)
    img = models.ImageField(upload_to='images/%Y/%m', default=u'images/default.png', max_length=100)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def get_unread_nums(self):
        #获取用户未读消息数量
        from operation.models import UserMessage #必须在这引用
        return UserMessage.objects.filter(user=self.id, has_read=False).count()
    def __unicode__(self):
        return self.username

class EmailVerifyRecord(models.Model):
    code = models.CharField(verbose_name=u'验证码',max_length=20)
    email = models.EmailField(verbose_name=u'邮箱', max_length=50)
    send_type = models.CharField(verbose_name=u'验证码类型', choices=(('register', u'注册'), ('forget', u'找回密码'), ('update', u'修改邮箱')), max_length=10)
    send_time = models.DateTimeField(verbose_name=u'发送时间', default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

class Banner(models.Model):
    title = models.CharField(verbose_name=u'标题', max_length=100)
    imgage = models.ImageField(verbose_name=u'轮播图', upload_to='banner/%Y/%m', max_length=100)
    url = models.URLField(verbose_name=u'访问地址', max_length=200)
    index = models.IntegerField(verbose_name=u'顺序',default=100)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
