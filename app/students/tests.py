from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Student
from django.urls import reverse
from datetime import date

class StudentViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.student = Student.objects.create(
            id=1,
            full_name="Salome",
            date_birth=date(2000, 1, 1),
            gendre="femenina",
            address="2024-10-28",
            phone="77777",
            email="salo@gmail.com",
            school_grade="2"
        )
        
        self.list_url = reverse("student-list")
        self.detail_url = reverse("student-detail", kwargs={"pk": self.student.id})

    def test_student_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]["id"], self.student.id)
        self.assertEqual(response.data[0]["full_name"], "Salome")
        self.assertEqual(response.data[0]["date_birth"], "2000-01-01")      
        self.assertEqual(response.data[0]["gendre"], "femenina")
        self.assertEqual(response.data[0]["address"], "2024-10-28")
        self.assertEqual(response.data[0]["phone"], "77777")
        self.assertEqual(response.data[0]["email"], "salo@gmail.com")
        self.assertEqual(response.data[0]["school_grade"], "2")

    def test_create_student(self):
        new_student_data = {
            "id": 2,
            "full_name": "Juan",
            "date_birth": "2000-02-01",
            "gendre": "masculino",
            "address": "2024-10-28",
            "phone": "88888",
            "email": "juan@gmail.com",
            "school_grade": "3"
        }
        response = self.client.post(self.list_url, new_student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)
        self.assertEqual(Student.objects.get(id=2).full_name, "Juan") 

    def test_update_student(self):
        updated_student_data = {
            "id": 1,
            "full_name": "Salome Actualizada",
            "date_birth": "2000-01-01",
            "gendre": "femenina",
            "address": "2024-10-28",
            "phone": "77777",
            "email": "salo@gmail.com",
            "school_grade": "4" 
        }
        response = self.client.put(self.detail_url, updated_student_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.student.refresh_from_db()
        self.assertEqual(self.student.full_name, "Salome Actualizada")

    def test_delete_student(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Student.objects.count(), 0)
