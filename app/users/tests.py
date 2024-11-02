from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import User
from ..roles.models import Role
from django.urls import reverse

class UserViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.role = Role.objects.create(
            name="Admin",
            description="Admin"
        )
        
        self.uri_register = reverse('usuario-register')
        self.uri_login = reverse('usuario-login')

    def test_create_users(self):
        data_register = {
                "full_name": "pepito",
                "email": "pepito@example.com",
                "phone": "0123456789",
                "date_birth": "2001-11-02",
                "address": "Carretera X",
                "role_id": self.role.id,
                "username": "pepito",
                "password": "12345678"
            }
        response = self.client.post(
            self.uri_register,
            data_register,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(id=1).full_name, "pepito")
        self.assertEqual(response.data["full_name"], "pepito")

    def test_login_user(self):
        user = User.objects.create_user(
            full_name="Alcachofa",
            email="alcachofa@example.com",
            phone="0123456789",
            date_birth="2000-12-28",
            address="Carrera Y",
            role_id=self.role,
            username="alcachofa",
            password="12345678"
        )
        data_login = {
            "username": "alcachofa",
            "password": "12345678"
        }
        response = self.client.post(self.uri_login, data_login, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    
