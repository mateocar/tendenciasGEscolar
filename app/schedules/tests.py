from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Schedule
from ..students.models import Student
from ..teachers.models import Teacher
from ..courses.models import Course
from django.urls import reverse

class ScheduleViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.student = Student.objects.create(
            id=1,
            full_name="Juaquin",
            date_birth="2003-10-05",
            gendre="Hombre",
            address="2024-10-28",
            phone="1233456789",
            email="juaquincito@gmail.com",
            school_grade="8"
        )

        self.teacher = Teacher.objects.create(
            id=1,
            full_name="Andres",
            date_birth="1993-12-13",
            gendre="Hombre",
            address="Carrera 24",
            phone="000000000",
            email="andres@test.com",
            department="Ciencias basicas"
        )

        self.course = Course.objects.create(
            course_name="Matematicas",
            description="Avanzadas, escapa si puedes",
            teacher_id=self.teacher,
            start_date = "2024-10-01",
            end_date = "2024-10-30",
            start_time = "06:00:00",
            end_time = "08:00:00",
        )

        self.course2 = Course.objects.create(
            course_name="Fisica",
            description="Avanzadas, escapa si puedes",
            teacher_id=self.teacher,
            start_date = "2024-11-01",
            end_date = "2024-11-30",
            start_time = "06:00:00",
            end_time = "08:00:00",
        )
        
        self.schedule = Schedule.objects.create(
            student_id=self.student,
            course_id=self.course,
        )
        
        self.uri = reverse("schedule-list")
        self.uri_with_id = reverse("schedule-detail", kwargs={"pk": self.schedule.id})


    def test_course_list(self):
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]["student_id"], self.student.id)
        self.assertEqual(response.data[0]["course_id"], self.course.id)

    def test_create_course(self):
        new_schedule_data = {
            "student_id": self.student.id,
            "course_id": self.course.id,
        }
        response = self.client.post(self.uri, new_schedule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schedule.objects.count(), 2)
        self.assertEqual(response.data['student_id'], self.student.id)
        self.assertEqual(response.data['course_id'], self.course.id)

    def test_update_course(self):
        updated_schedule_data = {
            "student_id": self.student.id,
            "course_id": self.course2.id,
        }
        response = self.client.put(self.uri_with_id, updated_schedule_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["course_id"], self.course2.id)

    def test_delete_course(self):
        response = self.client.delete(self.uri_with_id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.count(), 0)
