from django.contrib import admin
from .models import *
import pandas as pd
import datetime
from course.models import Term, Classroom, Course
from daterange_filter.filter import DateRangeFilter
from django.http import HttpResponse
from io import BytesIO
import numpy as np
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ClassroomAdmin(admin.ModelAdmin):
    actions = ["direct_export", "export_student_by_term", "export_money_by_term", "export_student_by_course"]
    date_hierarchy = 'pay_date'  # 详细时间分层筛选
    list_filter = (('pay_date', DateRangeFilter), "class_type", "pay_date", "grade")
    search_fields = ['student_name__name', 'school', 'grade', '_class', 'course_name_1__name', 'course_name_2__name', 'course_name_3__name', 'course_name_4__name', 'course_name_5__name', 'course_name_6__name', 'term__term', 'class_type', 'return_price', 'remark']  # 设置搜索栏范围，如果有外键，要注明外键的哪个字段，双下划线
    list_display = ('id', 'student_name', 'school', 'grade', '_class', 'course_name_1', 'course_name_2', 'course_name_3', 'course_name_4', 'course_name_5', 'course_name_6', 'term', 'class_type', 'price', 'pay_date', 'return_price', 'return_date', 'remark')  # 在页面上显示的字段，若不设置则显示 models.py 中 __unicode__(self) 中所返回的值
    list_display_links = ('id', 'student_name')  # 设置页面上哪个字段可单击进入详细页面
    # fields = ('category', 'book')  # 设置添加/修改详细信息时，哪些字段显示，在这里 remark 字段将不显示
    raw_id_fields = ('student_name', 'term', 'course_name_1', 'course_name_2', 'course_name_3', 'course_name_4', 'course_name_5', 'course_name_6')
    fieldsets = [
        ("学生", {'fields': ['student_name', 'school', 'grade', '_class']}),
        ('课程', {'fields': ['term', 'class_type', 'course_name_1', 'course_name_2', 'course_name_3']}),
        ('更多课程', {'fields': ['course_name_4', 'course_name_5', 'course_name_6'], 'classes': ['collapse']}),
        ("缴费", {'fields': ['price', 'pay_date', 'return_price', 'return_date']}),
        ("备注", {'fields': ['remark']}),
    ]

    def direct_export(self, request, queryset):
        outfile = BytesIO()
        data = pd.DataFrame(queryset.values())
        data = data.rename(columns={"course_name_1_id": "课程1", "course_name_2_id": "课程2", "course_name_3_id": "课程3", "course_name_4_id": "课程4", "course_name_5_id": "课程5", "course_name_6_id": "课程6", "id": "序号", "pay_date": "缴费日期", "price": "缴费金额", "return_date": "退费日期", "return_price": "退费金额", "student_name_id": "学生姓名", "term_id": "学期", 'school': '学校', 'grade': '年级', '_class': '班级', 'class_type': '形式', "remark": "备注"})
        data = data[["序号", "学生姓名", "学校", "年级", "班级", "课程1", "课程2", "课程3", "课程4", "课程5", "课程6", "学期", "形式", "缴费金额", "缴费日期", "退费金额", "退费日期", "备注"]]
        data = data.sort_values(by=["序号"], ascending=True)
        data = data.fillna("")
        filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="{}"'.format("Direct export " + filename + ".xlsx")
        data.to_excel(outfile, index=False)
        response.write(outfile.getvalue())
        return response

    def export_student_by_term(self, request, queryset):
        outfile = BytesIO()
        data = pd.DataFrame(queryset.values())
        data = data.rename(columns={"course_name_1_id": "课程1", "course_name_2_id": "课程2", "course_name_3_id": "课程3",
                                    "course_name_4_id": "课程4", "course_name_5_id": "课程5", "course_name_6_id": "课程6",
                                    "id": "序号", "pay_date": "缴费日期", "price": "缴费金额", "return_date": "退费日期",
                                    "return_price": "退费金额", "student_name_id": "学生姓名", "term_id": "学期", 'school': '学校',
                                    'grade': '年级', '_class': '班级', 'class_type': '形式', "remark": "备注"})
        data = data[["序号", "学生姓名", "学校", "年级", "班级", "课程1", "课程2", "课程3", "课程4", "课程5", "课程6", "学期", "形式", "缴费金额", "缴费日期", "退费金额", "退费日期", "备注"]]
        data = data.sort_values(by=["序号"], ascending=True)
        data = data.fillna("")
        data = data.drop_duplicates(["学生姓名", "学期"])
        data = pd.pivot_table(data, values=["学生姓名"], index=["学期", "形式", "学校", "年级"], aggfunc=np.count_nonzero)
        data = data.rename(columns={"学生姓名": "学生人数"})
        filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="{}"'.format("Export by date " + filename + ".xlsx")
        data.to_excel(outfile)
        response.write(outfile.getvalue())
        return response

    def export_money_by_term(self, request, queryset):
        outfile = BytesIO()
        data = pd.DataFrame(queryset.values())
        data = data.rename(columns={"course_name_1_id": "课程1", "course_name_2_id": "课程2", "course_name_3_id": "课程3",
                                    "course_name_4_id": "课程4", "course_name_5_id": "课程5", "course_name_6_id": "课程6",
                                    "id": "序号", "pay_date": "缴费日期", "price": "缴费金额", "return_date": "退费日期",
                                    "return_price": "退费金额", "student_name_id": "学生姓名", "term_id": "学期", 'school': '学校',
                                    'grade': '年级', '_class': '班级', 'class_type': '形式', "remark": "备注"})
        data = data[["序号", "学生姓名", "学校", "年级", "班级", "课程1", "课程2", "课程3", "课程4", "课程5", "课程6", "学期", "形式", "缴费金额", "缴费日期", "退费金额", "退费日期", "备注"]]
        data = data.sort_values(by=["序号"], ascending=True)
        data = data.fillna("")
        data = pd.pivot_table(data, values=["缴费金额", "退费金额"], index=["学期", "形式", "学校", "年级"], aggfunc=np.sum)
        data["合计"] = data["缴费金额"] - data["退费金额"]
        filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="{}"'.format("Export by date " + filename + ".xlsx")
        data.to_excel(outfile)
        response.write(outfile.getvalue())
        return response

    def export_student_by_course(self, request, queryset):
        outfile = BytesIO()
        data = pd.DataFrame(queryset.values())
        data = data.rename(columns={"course_name_1_id": "课程1", "course_name_2_id": "课程2", "course_name_3_id": "课程3",
                                    "course_name_4_id": "课程4", "course_name_5_id": "课程5", "course_name_6_id": "课程6",
                                    "id": "序号", "pay_date": "缴费日期", "price": "缴费金额", "return_date": "退费日期",
                                    "return_price": "退费金额", "student_name_id": "学生姓名", "term_id": "学期", 'school': '学校',
                                    'grade': '年级', '_class': '班级', 'class_type': '形式', "remark": "备注"})
        data = data[["序号", "学生姓名", "学校", "年级", "班级", "课程1", "课程2", "课程3", "课程4", "课程5", "课程6", "学期", "形式", "缴费金额", "缴费日期", "退费金额", "退费日期", "备注"]]
        data = data.sort_values(by=["序号"], ascending=True)
        data1 = data[["学生姓名", "学期", "形式", "课程1"]].rename(columns={"课程1": "课程"}).dropna()
        data2 = data[["学生姓名", "学期", "形式", "课程2"]].rename(columns={"课程2": "课程"}).dropna()
        data3 = data[["学生姓名", "学期", "形式", "课程3"]].rename(columns={"课程3": "课程"}).dropna()
        data4 = data[["学生姓名", "学期", "形式", "课程4"]].rename(columns={"课程4": "课程"}).dropna()
        data5 = data[["学生姓名", "学期", "形式", "课程5"]].rename(columns={"课程5": "课程"}).dropna()
        data6 = data[["学生姓名", "学期", "形式", "课程6"]].rename(columns={"课程6": "课程"}).dropna()
        data = pd.concat([data1, data2], axis=0, ignore_index=True)
        data = pd.concat([data, data3], axis=0, ignore_index=True)
        data = pd.concat([data, data4], axis=0, ignore_index=True)
        data = pd.concat([data, data5], axis=0, ignore_index=True)
        data = pd.concat([data, data6], axis=0, ignore_index=True)
        data = data.fillna("")
        data = pd.pivot_table(data, values=["学生姓名"], index=["学期", "形式", "课程"], aggfunc=np.count_nonzero)
        data = data.rename(columns={"学生姓名": "报名人数"})
        filename = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment;filename="{}"'.format("Export by date " + filename + ".xlsx")
        data.to_excel(outfile)
        response.write(outfile.getvalue())
        return response

    direct_export.short_description = '直接导出'
    export_student_by_term.short_description = '按学期统计学生人数'
    export_money_by_term.short_description = '按学期统计缴费金额'
    export_student_by_course.short_description = '按课程统计学生人数'


class StudentAdmin(admin.ModelAdmin):
    list_filter = ('sex', )  # 过滤器
    search_fields = ['name', 'phone_1', 'phone_2']  # 设置搜索栏范围，如果有外键，要注明外键的哪个字段，双下划线
    list_display = ('id', 'name', 'sex', 'phone_1', 'phone_2')  # 在页面上显示的字段，若不设置则显示 models.py 中 __unicode__(self) 中所返回的值
    list_display_links = ('id', 'name')  # 设置页面上哪个字段可单击进入详细页面
    # fields = ('category', 'book')  # 设置添加/修改详细信息时，哪些字段显示，在这里 remark 字段将不显示


admin.site.register(Student, StudentAdmin)
admin.site.register(Course)
admin.site.register(Term)
admin.site.register(Classroom, ClassroomAdmin)