from django.db import models
from ..users.models import User
from ..courses.models import Course

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)