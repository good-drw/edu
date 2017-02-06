# _*_ encoding:utf-8 _*_
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from organization.models import CourseOrg, Teacher
from DjangoUeditor.models import UEditorField

# Create your models here.


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(verbose_name=u'课程名', max_length=50)
    desc = models.TextField(verbose_name=u'课程描述')
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    detail =  UEditorField(verbose_name=u'课程详情',width=600, height=300, imagePath="courses/ueditor/", filePath="courses/ueditor/",default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')
    degree = models.CharField(verbose_name=u'难度', choices=(('cj', u'初级'), ('zj', u'中级'), ('gj', u'高级')), max_length=2)
    learn_times = models.IntegerField(verbose_name=u'学习时长(分钟数)',default=0)
    students = models.IntegerField(verbose_name=u'学习人数', default=0)
    fav_nums = models.IntegerField(verbose_name=u'收藏人数', default=0)
    imgage = models.ImageField(verbose_name=u'封面图', upload_to='courses/%Y/%m', max_length=100)
    click_nums = models.IntegerField(verbose_name=u'课程点击数', default=0)
    category = models.CharField(max_length=20, verbose_name=u'课程类别', null=True, blank=True)
    tag = models.CharField(verbose_name=u'课程标签', default='', max_length=10)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)
    youneed_know = models.CharField(verbose_name=u'课程需知', max_length=300, default='')
    teacher_tell = models.CharField(verbose_name=u'老师告诉你', max_length=300, default='')

    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        '''获取章节数'''
        return self.lesson_set.all().count()
    get_zj_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='https://www.baidu.com'>跳钻</a>")
    go_to.short_description = '跳转'

    def get_learn_users(self):
        '''获得学习用户'''
        return self.usercourse_set.all()[:5]

    def get_course_lesson(self):
        '''获取课程所有章节'''
        return self.lesson_set.all()

    def __unicode__(self):
        return self.name


class BannerCourse(Course):
    '''同一张表,但是可以分开管理不同数据,数据分类管理'''
    class Meta:
        verbose_name = u'轮播课程'
        verbose_name_plural = verbose_name
        proxy = True


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(verbose_name=u'章节名', max_length=100)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_all_video(self):
        '''获得所有视频'''
        return self.video_set.all()

    def __unicode__(self):
        return self.name

class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(verbose_name=u'视频名', max_length=100)
    url = models.CharField(max_length=200, verbose_name=u'访问地址', default='')
    learn_times = models.IntegerField(verbose_name=u'学习时长(分钟数)', default=0)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class CourseResouce(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(verbose_name=u'名称', max_length=100)
    download = models.FileField(verbose_name=u'资源文件', upload_to='course/resource/%Y/%m', max_length=100)
    add_time = models.DateTimeField(verbose_name=u'添加时间', default=datetime.now)

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

