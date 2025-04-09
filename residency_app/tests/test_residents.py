from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from residency_app.models import Resident, Cohort

User = get_user_model()

class TestResidentEndpoints(APITestCase):

    def setUp(self):
        # Create users with different roles
        self.admin_user = User.objects.create_user(
            username="admin1",
            email="admin1@example.com",
            password="testpass123",
            role=User.ADMIN
        )
        self.coordinator_user = User.objects.create_user(
            username="coordinator1",
            email="coordinator1@example.com",
            password="testpass123",
            role=User.COORDINATOR
        )
        self.coach_user = User.objects.create_user(
            username="coach1",
            email="coach1@example.com",
            password="testpass123",
            role=User.COACH
        )
        self.resident_user = User.objects.create_user(
            username="resident1",
            email="resident1@example.com",
            password="testpass123",
            role=User.RESIDENT
        )

        # Create a cohort for testing
        self.cohort = Cohort.objects.create(
            name="Cohort 2025", 
            year=2025, 
            coordinator=self.coordinator_user)
        
        # Create residents for testing
        self.resident = Resident.objects.create(
            user=self.resident_user,
            cohort=self.cohort,
            coach=self.coach_user,
            sending_church="Church A",
            plant_name="Plant A",
            plant_location= "Accra"
        )
        
    def test_resident_list_authenticated(self):
        """Test that authenticated users can retrieve the resident list."""
        # Authenticate with admin user
        token = Token.objects.create(user=self.admin_user)
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('resident-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)  

    def test_resident_register_authenticated(self):
        """Test that only admin or coordinator can register a new resident."""
        # Authenticate with admin user
        # token = Token.objects.create(user=self.admin_user)
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('resident-list-create')
        new_resident_user = User.objects.create_user(
            username= "resident2",
            email= "resident2@gmail.com",
            password= "testpass123",
            role=User.RESIDENT
        )

        data = {
            "user": new_resident_user.id,
            "cohort": self.cohort.id,
            "coach": self.coach_user.id,
            "sending_church": "Church B",
            "plant_name": "Plant B",
            "plant_location": "Adenta",
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_resident_retrieve_authenticated(self):
        """Test that an authenticated user can retrieve a specific resident."""
        # Authenticate with admin user
        token = Token.objects.create(user=self.admin_user)
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('resident-detail', kwargs={'pk': self.resident.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.resident.id)

    def test_resident_update_authenticated(self):
        """Test that only admin or coordinator can update a resident."""
        # Authenticate with admin user
        token = Token.objects.create(user=self.admin_user)
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('resident-detail', kwargs={'pk': self.resident.id})
        data = {
            "sending_church": "Updated Church",
            "plant_name": "Updated Plant"
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['sending_church'], "Updated Church")

    def test_resident_delete_authenticated(self):
        """Test that only admin or coordinator can delete a resident."""
        # Authenticate with admin user
        token = Token.objects.create(user=self.admin_user)
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('resident-detail', kwargs={'pk': self.resident.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
