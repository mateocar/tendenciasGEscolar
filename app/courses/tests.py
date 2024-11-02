from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Course
from ..teachers.models import Teacher
from django.urls import reverse

class CourseViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.teacher = Teacher.objects.create(
            id=1,
            full_name="Rina",
            date_birth="2024-10-28",
            gendre="mujer",
            address="carrera 123",
            phone="1234567890",
            email="rina@example.com",
            department="ciencias"
        )
        
        self.course = Course.objects.create(
            course_name="Fisica",
            description="Curso de 3 semestre",
            teacher_id=self.teacher,
            start_date = "2024-10-01",
            end_date = "2024-10-30",
            start_time = "06:00:00",
            end_time = "08:00:00",
        )
        
        self.list_url = reverse("course-list")
        self.detail_url = reverse("course-detail", kwargs={"pk": self.course.id})

    def test_course_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]["course_name"], "Fisica")
        self.assertEqual(response.data[0]["description"], "Curso de 3 semestre")
        self.assertEqual(response.data[0]["start_date"], "2024-10-01")
        self.assertEqual(response.data[0]["end_date"], "2024-10-30")
        self.assertEqual(response.data[0]["start_time"], "06:00:00")
        self.assertEqual(response.data[0]["end_time"], "08:00:00")
        self.assertEqual(response.data[0]["teacher_id"], self.teacher.id)

    def test_create_course(self):
        new_course_data = {
            "course_name": "Quimica",
            "description": "hii Quimica!!",
            "teacher_id": self.teacher.id,
            "start_date": "2024-10-03"
        }
        response = self.client.post(self.list_url, new_course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)
        self.assertEqual(response.data['start_date'], "2024-10-03")
        self.assertEqual(Course.objects.get(id=2).course_name, "Quimica") 

    def test_update_course(self):
        updated_course_data = {
            "course_name": "Fisica Avanzada",
            "description": "Curso de 4 semestre",
            "teacher_id": self.teacher.id,
            "start_date": "2024-10-03"
        }
        response = self.client.put(self.detail_url, updated_course_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(response.data['start_date'], "2024-10-03")
        self.assertEqual(self.course.course_name, "Fisica Avanzada") 

    def test_delete_course(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)



