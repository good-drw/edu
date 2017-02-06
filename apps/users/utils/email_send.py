#!/user/bin/env/python
# -*- coding:utf-8 -*-
__author__ = 'drw'
__date__ = '2017/2/1 13:44'

from users.models import EmailVerifyRecord
from random import Random
from django.core.mail import send_mail

from edu.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKklLMmNnOoPpQqRrSsTtUuVvWwXxYyZz1234567890'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def send_regiser_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    if send_type == 'update':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ""
    email_body = ""

    if send_type == "register":
            email_title = "教程网注册激活链接"
            email_body = "请点击下面的链接激活账号:http:127.0.0.1:8000/active/{0},链接将在15分钟后失效".format(code)

            send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
            if send_status:
                pass
    elif send_type == "forget":
        email_title = "教程网密码重置链接"
        email_body = "请点击下面的链接重置账号:http:127.0.0.1:8000/reset/{0},链接将在15分钟后失效".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == "update":
        email_title = "教程网邮箱修改验证码"
        email_body = "你的邮箱验证码为: {0}".format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
