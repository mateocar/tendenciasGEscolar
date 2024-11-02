from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Role

class RolViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.role = Role.objects.create(
            id=1,
            name="Admin",
            description="todos los permisos"
        )
        
        self.list_url = reverse("roles-list")
        self.detail_url = reverse("roles-detail", kwargs={"pk": self.role.id})

    def test_rol_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)
        self.assertEqual(response.data[0]["id"], 1)
        self.assertEqual(response.data[0]["name"], "Admin")
        self.assertEqual(response.data[0]["description"], "todos los permisos")

    def test_create_rol(self):
        new_role_data = {
            "name": "admin",
            "description": "todos los permisos",
        }
        response = self.client.post(self.list_url, new_role_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Role.objects.count(), 2)

    def test_update_rol(self):
        updated_role_data = {
            "name": "admin",
            "description": "ninguna",
        }
        response = self.client.put(self.detail_url, updated_role_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.role.refresh_from_db()
        self.assertEqual(self.role.description, "ninguna")

    def test_delete_rol(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Role.objects.count(), 0)
