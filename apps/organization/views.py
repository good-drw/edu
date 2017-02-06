# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator,EmptyPage, PageNotAnInteger
from django.http import HttpResponse

from .models import CourseOrg, CityDict, Teacher
from .forms import UserAskForm
from courses.models import CourseOrg
from operation.models import UserFavorite
from courses.models import Course
from django.db.models import Q




# Create your views here.

class OrgListView(View):
    '''
    课程机构列表页
    '''
    def get(self, request):
        #课程机构
        all_orgs = CourseOrg.objects.all()

        #城市
        all_citys = CityDict.objects.all()

        # 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        #获得城市id
        city_id = request.GET.get('city', '')
        #获得类别
        category = request.GET.get('ct', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 排序
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'student_num':
                all_orgs = all_orgs.order_by('-student_num')
            elif sort == 'course_num':
                all_orgs = all_orgs.order_by('-course_num')
        #统计一共多少课程
        org_nums = all_orgs.count()
        #授课机构排名
        hot_orgs = all_orgs.order_by('-click_num')[:3]



        #对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)
        return render(request, "org-list.html", {
            "all_orgs":orgs,
            "all_citys":all_citys,
            "org_nums":org_nums,
            "city_id":city_id,
            "category":category,
            "hot_orgs":hot_orgs,
            "sort":sort
        })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True) #commit=true 就把数据保存到数据库
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail", "msg":"添加出错"}', content_type='application/json')


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num +=1
        course_org.save()
        all_courses = course_org.course_set.all()[:4]
        all_teachers = course_org.teacher_set.all()[:1]
        current_page = 'home'
        has_fav = False #用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html', {
            "all_courses":all_courses,
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class OrgCourseView(View):
    '''
       机构课程
       '''

    def get(self, request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        current_page = 'course'
        has_fav = False  # 用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 1, request=request)
        orgs = p.page(page)

        return render(request, 'org-detail-course.html', {
            "all_courses": orgs,
            "course_org": course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class OrgDescView(View):
    '''
    机构介绍
    '''
    def get(self,request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        current_page = 'detail'
        has_fav = False  # 用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            "course_org":course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class OrgTeacherView(View):
    '''
    机构教师
    '''
    def get(self,request, org_id):
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teachers = course_org.teacher_set.all()
        current_page = 'teacher'
        has_fav = False  # 用户是否收藏
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, 'org-detail-teachers.html', {
            "all_teachers":all_teachers,
            "course_org":course_org,
            "current_page":current_page,
            "has_fav":has_fav
        })


class AddFavView(View):
    '''
    用户收藏,取消收藏
    '''
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)
        #判断用户登录
        if not request.user.is_authenticated():
            #判断用户登录状态
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在,则表示用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                course_org = CourseOrg.objects.get(id=int(fav_id))
                course_org.fav_num -= 1
                if course_org.fav_num < 0:
                    course_org.fav_num = 0
                course_org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_num -= 1
                if teacher.fav_num < 0:
                    teacher.fav_num = 0
                teacher.save()
            return HttpResponse('{"status":"success", "msg":"收藏"}', content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    course_org = CourseOrg.objects.get(id=int(fav_id))
                    course_org.fav_num += 1
                    course_org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_num += 1
                    teacher.save()
                return HttpResponse('{"status":"success", "msg":"已收藏"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail", "msg":"收藏出错"}', content_type='application/json')


class TeacherListView(View):
    '''教师列表页'''
    def get(self, request):
        all_teachers = Teacher.objects.all()

        # 讲师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords)|
                                               Q(work_company__icontains=search_keywords)|
                                               Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        teacher_nums = all_teachers.count()
        hot_teachers = all_teachers.order_by(('-fav_num'))[:3]
        if sort:
            all_teachers = all_teachers.order_by('-fav_num')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 3, request=request)
        all_teachers = p.page(page)
        return render(request, 'teacher/teachers-list.html', {
            'all_teachers':all_teachers,
            'sort':sort,
            'teacher_nums':teacher_nums,
            'hot_teacher':hot_teachers
        })


class TeacherDetailView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.click_num +=1
        teacher.save()
        all_courses = Course.objects.filter(teacher=teacher)
        #讲师排行
        hot_teachers = Teacher.objects.all().order_by(('-fav_num'))[:3]
        has_teacher_fav = False  # 用户是否收藏
        has_org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_teacher_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=2):
                has_org_fav = True
        return render(request, 'teacher/teacher-detail.html', {
            "teacher":teacher,
            'all_courses':all_courses,
            'hot_teachers':hot_teachers,
            'has_teacher_fav':has_teacher_fav,
            'has_org_fav':has_org_fav
        })























