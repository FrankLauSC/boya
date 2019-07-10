from django.db import models
import django.utils.timezone as timezone


sex_selection = (
    ("M", "男"),
    ("F", "女"),
)

grade_selection = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5),
    ("6", 6),
    ("7", 7),
    ("8", 8),
    ("9", 9),
)

class_type_selection = (
    ("合作", "合作"),
    ("自组", "自组"),
)


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=10, unique=True, verbose_name="姓名")
    sex = models.CharField(max_length=2, choices=sex_selection, verbose_name="性别")
    phone_1 = models.CharField(max_length=11, blank=True, null=True, verbose_name="电话1")
    phone_2 = models.CharField(max_length=11, blank=True, null=True, verbose_name="电话2")

    class Meta:
        verbose_name = '学生'
        verbose_name_plural = "学生"

    def __str__(self):
        return self.name


class Course(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    name = models.CharField(max_length=30, unique=True, verbose_name="课程名称")

    class Meta:
        verbose_name = '课程'
        verbose_name_plural = "课程"

    def __str__(self):
        return self.name


class Term(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    term = models.CharField(max_length=20, unique=True, verbose_name="学期")

    class Meta:
        verbose_name = '学期'
        verbose_name_plural = "学期"

    def __str__(self):
        return self.term


class Classroom(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    student_name = models.ForeignKey("Student", on_delete=models.DO_NOTHING, to_field="name", verbose_name="学生姓名")
    school = models.CharField(max_length=30, blank=True, null=True, verbose_name="就读学校")
    grade = models.IntegerField(blank=True, null=True, verbose_name="年级")
    _class = models.IntegerField(blank=True, null=True, verbose_name="班级")
    course_name_1 = models.ForeignKey("Course", on_delete=models.DO_NOTHING, to_field="name", related_name="course1", verbose_name="课程1")
    course_name_2 = models.ForeignKey("Course", blank=True, null=True, on_delete=models.DO_NOTHING, to_field="name", related_name="course2", verbose_name="课程2")
    course_name_3 = models.ForeignKey("Course", blank=True, null=True, on_delete=models.DO_NOTHING, to_field="name", related_name="course3", verbose_name="课程3")
    course_name_4 = models.ForeignKey("Course", blank=True, null=True, on_delete=models.DO_NOTHING, to_field="name", related_name="course4", verbose_name="课程4")
    course_name_5 = models.ForeignKey("Course", blank=True, null=True, on_delete=models.DO_NOTHING, to_field="name", related_name="course5", verbose_name="课程5")
    course_name_6 = models.ForeignKey("Course", blank=True, null=True, on_delete=models.DO_NOTHING, to_field="name", related_name="course6", verbose_name="课程6")
    class_type = models.CharField(max_length=6, choices=class_type_selection, verbose_name="形式")
    term = models.ForeignKey("Term", on_delete=models.DO_NOTHING, to_field="term", verbose_name="学期")
    price = models.FloatField(max_length=10, verbose_name="费用")
    pay_date = models.DateField(default=timezone.now, verbose_name="缴费日期")
    return_price = models.FloatField(max_length=10, blank=True, default=0, verbose_name="退还费用")
    return_date = models.DateField(blank=True, null=True, verbose_name="退费日期")
    remark = models.TextField(max_length=100, blank=True, null=True, verbose_name="备注")

    class Meta:
        verbose_name = '教室'
        verbose_name_plural = "教室"
