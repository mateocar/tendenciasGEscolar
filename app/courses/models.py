from django.db import models
from ..teachers.models import Teacher
import datetime

class Course(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    teacher_id = models.ForeignKey(Teacher, null=False, on_delete=models.CASCADE)
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(default=datetime.date.today)
    start_time = models.TimeField(default=datetime.time())
    end_time = models.TimeField(default=datetime.time())