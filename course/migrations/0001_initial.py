# Generated by Django 2.2.3 on 2019-07-07 13:26

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='课程名称')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=10, unique=True, verbose_name='姓名')),
                ('sex', models.CharField(choices=[('M', '男'), ('F', '女')], max_length=2, verbose_name='性别')),
                ('phone_1', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话1')),
                ('phone_2', models.CharField(blank=True, max_length=11, null=True, verbose_name='电话2')),
            ],
        ),
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('term', models.CharField(max_length=20, unique=True, verbose_name='学期')),
            ],
        ),
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('school', models.CharField(blank=True, max_length=30, null=True, verbose_name='就读学校')),
                ('grade', models.IntegerField(blank=True, null=True, verbose_name='年级')),
                ('_class', models.IntegerField(blank=True, null=True, verbose_name='班级')),
                ('class_type', models.CharField(choices=[('合作', '合作班'), ('自主', '自主班')], max_length=6, verbose_name='形式')),
                ('price', models.FloatField(max_length=10, verbose_name='费用')),
                ('pay_date', models.DateField(default=django.utils.timezone.now, verbose_name='缴费日期')),
                ('return_price', models.FloatField(blank=True, default=0, max_length=10, verbose_name='退还费用')),
                ('return_date', models.DateField(blank=True, null=True, verbose_name='退费日期')),
                ('remark', models.TextField(blank=True, max_length=100, null=True, verbose_name='备注')),
                ('course_name_1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='course1', to='course.Course', to_field='name', verbose_name='课程1')),
                ('course_name_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='course2', to='course.Course', to_field='name', verbose_name='课程2')),
                ('course_name_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='course3', to='course.Course', to_field='name', verbose_name='课程3')),
                ('course_name_4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='course4', to='course.Course', to_field='name', verbose_name='课程4')),
                ('course_name_5', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='course5', to='course.Course', to_field='name', verbose_name='课程5')),
                ('course_name_6', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='course6', to='course.Course', to_field='name', verbose_name='课程6')),
                ('student_name', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.Student', to_field='name', verbose_name='学生姓名')),
                ('term', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='course.Term', to_field='term', verbose_name='学期')),
            ],
        ),
    ]
