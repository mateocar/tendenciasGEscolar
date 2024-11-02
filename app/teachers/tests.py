from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Teacher
from django.urls import reverse
from datetime import date


class TeacherViewSetTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.teacher = Teacher.objects.create(id=1,
                                              full_name="Jacinto",
                                              date_birth=date(1983, 6, 18),
                                              gendre="masculino",
                                              address="Cl 44 # 65 - 28",
                                              phone="6666666666",
                                              email="jaci@gmail.com",
                                              department="Ciencias")
        
        self.list_url = reverse("teacher-list")
        self.detail_url = reverse("teacher-detail", kwargs={"pk": self.teacher.id})

    def test_get_teacher(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]["id"], self.teacher.id)
        self.assertEqual(response.data[0]["full_name"], "Jacinto")
        self.assertEqual(response.data[0]["date_birth"], "1983-06-18")
        self.assertEqual(response.data[0]["gendre"], "masculino")
        self.assertEqual(response.data[0]["address"], "Cl 44 # 65 - 28")
        self.assertEqual(response.data[0]["phone"], "6666666666")
        self.assertEqual(response.data[0]["email"], "jaci@gmail.com")
        self.assertEqual(response.data[0]["department"], "Ciencias")

    def test_create_teacher(self):
        new_teacher = {
            "id": 2,
            "full_name": "Ana",
            "date_birth": "1986-09-08",
            "gendre": "femenino",
            "address": "Cl 30 # 80 - 39",
            "phone": "9999999999",
            "email": "ana@gmail.com",
            "department": "Sociales"
        }
        response = self.client.post(self.list_url, new_teacher, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 2)
        self.assertEqual(Teacher.objects.get(id=2).full_name, "Ana")

    def test_update_teacher(self):
        update_teacher = {
            "id": 1,
            "full_name": "Jacinto Correa",
            "date_birth": "1983-06-18",
           "gendre": "masculino",
           "address": "Cl 44 # 65 - 28",
            "phone": "6666666666",
            "email": "jaci@gmail.com",
            "department": "Tecnologia"
        }
        response = self.client.put(self.detail_url, update_teacher, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.teacher.refresh_from_db()
        self.assertEqual(self.teacher.full_name, "Jacinto Correa")

    def test_delete_teacher(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Teacher.objects.count(), 0)
