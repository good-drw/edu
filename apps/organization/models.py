# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.


class CityDict(models.Model):
    name = models.CharField(verbose_name=u'城市名', max_length=20)
    desc = models.CharField(verbose_name=u'描述', max_length=200)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class CourseOrg(models.Model):
    name = models.CharField(verbose_name=u'机构名称', max_length=50)
    desc = UEditorField(verbose_name=u'机构描述',width=600, height=300, imagePath="org/ueditor/", filePath="org/ueditor/",default='')
    tag = models.CharField(default=u'全国知名', verbose_name=u'机构标签', max_length=10)
    category = models.CharField(max_length=20, choices=(("pxjg", u"培训机构"), ("gr", u"个人"), ("gx", u"高校")),default='pxjg', verbose_name=u'机构类别')
    click_num = models.IntegerField(verbose_name=u'点击数', default=0)
    fav_num = models.IntegerField(verbose_name=u'收藏数', default=0)
    student_num = models.IntegerField(verbose_name=u'学习人数', default=0)
    course_num = models.IntegerField(verbose_name=u'课程数', default=0)
    image = models.ImageField(verbose_name=u'封面图', upload_to='org/%Y/%m', max_length=100)
    address = models.CharField(verbose_name=u'机构地址', max_length=150, default='')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市',default='')
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name
    def get_teacher_nums(self):
        '''获取课程机构教师数量'''
        return self.teacher_set.all().count()
    def get_course_nums(self):
        return self.course_set.all().count()
    def __unicode__(self):
        return self.name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所属机构')
    name = models.CharField(verbose_name=u'教师名称', max_length=50)
    age = models.IntegerField(verbose_name=u'年龄', default=18)
    work_years = models.IntegerField(verbose_name=u'工作年限', default=0)
    work_company = models.CharField(verbose_name=u'就职公司', max_length=50)
    work_position = models.CharField(verbose_name=u'公司职位', max_length=50)
    points = models.CharField(verbose_name=u'教学特点', max_length=50)
    click_num = models.IntegerField(verbose_name=u'点击数', default=0)
    fav_num = models.IntegerField(verbose_name=u'收藏数', default=0)
    image = models.ImageField(verbose_name=u'头像', upload_to='teacher/%Y/%m', max_length=100, null=True, blank=True)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'讲师'
        verbose_name_plural = verbose_name
    def get_all_course(self):
        '''获得讲师所有课程'''
        return self.course_set.all().count()
    def __unicode__(self):
        return self.name
