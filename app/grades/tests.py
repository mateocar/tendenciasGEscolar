from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Grade
from ..students.models import Student
from ..courses.models import Course
from django.urls import reverse
from ..teachers.models import Teacher
from decimal import Decimal
from datetime import datetime
from django.utils.timezone import make_aware

class GradeViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(
            id=1,
            full_name="Plata",
            date_birth="2024-10-28",
            gendre="mujer",
            address="carrera 123",
            phone="1234567890",
            email="rina@example.com",
            school_grade="segundo"
        )

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
            schedule="2024-03-09"
        )

        self.grade = Grade.objects.create(
            student_id=self.student,
            course_id=self.course,
            qualification=Decimal("5.00"),
            evaluation_date=make_aware(datetime.strptime("2024-03-09", "%Y-%m-%d"))
        )

        self.list_url = reverse("grade-list")
        self.detail_url = reverse("grade-detail", kwargs={"pk": self.grade.id})

    def test_grade_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(Decimal(response.data[0]["qualification"]), Decimal("5.00"))
        self.assertTrue(response.data[0]["evaluation_date"].startswith("2024-03-09"))      
        self.assertEqual(response.data[0]["student_id"], self.student.id)

    def test_create_grade(self):
        new_grade_data = {
            "qualification": "4.50",
            "evaluation_date": "2024-04-10",
            "student_id": self.student.id,
            "course_id": self.course.id  
        }
        response = self.client.post(self.list_url, new_grade_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Grade.objects.count(), 2) 
        self.assertEqual(Grade.objects.last().qualification, Decimal("4.50"))

    def test_update_grade(self):
        updated_grade_data = {
            "qualification": "4.50",
            "evaluation_date": "2024-04-10",
            "student_id": self.student.id,
            "course_id": self.course.id  
        }
        response = self.client.put(self.detail_url, updated_grade_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.grade.refresh_from_db() 
        self.assertEqual(self.grade.qualification, Decimal("4.50"))

    def test_delete_grade(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Grade.objects.count(), 0)
