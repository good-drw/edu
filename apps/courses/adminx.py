#!/user/bin/env/python
# -*- coding:utf-8 -*-
__author__ = 'drw'
__date__ = '2017/1/31 21:00'

import xadmin

from .models import Course, Lesson, Video, CourseResouce, BannerCourse
from organization.models import CourseOrg

#使得添加课程时可以添加章节
class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourseInline(object):
    model = CourseResouce
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_zj_nums','go_to', 'fav_nums', 'imgage',
                    'click_nums', 'course_org', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'imgage', 'course_org',
                     'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'imgage', 'click_nums',
                   'course_org', 'add_time']
    ordering = ['-click_nums']#后台显示排序
    readonly_fields = ['fav_nums'] #设置字段不能修改
    list_editable = ['degree', 'desc'] #在列表页可以编辑
    exclude = ['click_nums'] #设置字段不显示
    inlines = [LessonInline, CourseResourseInline]
    refresh_times = [3, 5]#页面多少秒刷新一次
    style_fields = {"detail":"ueditor"}
    import_excel = True

    def queryset(self):
        '''数据过滤'''
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        '''在保存课程时候统计课程机构的课程数'''
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_num = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class BannerCourseAdmin(object):
    '''这里是数据分类管理'''
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_zj_nums','go_to', 'fav_nums', 'imgage', 'click_nums','course_org', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'imgage','course_org', 'click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'fav_nums', 'imgage', 'click_nums','course_org', 'add_time']
    ordering = ['-click_nums']#后台显示排序
    readonly_fields = ['fav_nums'] #设置字段不能修改
    exclude = ['click_nums'] #设置字段不显示
    inlines = [LessonInline, CourseResourseInline]
    style_fields = {"detail": "ueditor"}

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs
    def save_models(self):
        '''在保存课程时候统计课程机构的课程数'''
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_num = Course.objects.filter(course_org=course_org).count()
            course_org.save()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time'] #course__name添加外键后台过滤

class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']

class CourseResouceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'download', 'name']
    list_filter = ['course__name', 'name', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResouce, CourseResouceAdmin)