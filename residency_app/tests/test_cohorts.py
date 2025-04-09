from rest_framework.test import APITestCase
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from residency_app.models import Cohort

User = get_user_model()

class TestCohortEndpoints(APITestCase):

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

        self.resident_user = User.objects.create_user(
            username="resident1",
            email="resident1@example.com",
            password="testpass123",
            role=User.RESIDENT
        )

        # Create cohorts for testing
        Cohort.objects.create(name="Cohort 2025", year=2025, coordinator=self.coordinator_user)
        Cohort.objects.create(name="Cohort 2026", year=2026, coordinator=self.coordinator_user)

    def test_cohort_list_authenticated(self):
        """Test that authenticated users can access the cohort list."""
        # Authenticate with admin user
        token = Token.objects.create(user=self.admin_user)
        print("Admin token:", token.key)
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('cohort-list')
        response = self.client.get(url)

        print("Response status code:", response.status_code)
        print('Authorization Header:', self.client.defaults.get('HTTP_AUTHORIZATION', 'No header'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  

    def test_cohort_create_authenticated_coordinator(self):
        """Test that a coordinator can create a new cohort."""
        # Authenticate with coordinator user
        token = Token.objects.create(user=self.coordinator_user)
        self.client.force_authenticate(user=self.coordinator_user)
        url = reverse('cohort-create') 
        data = {"name": "Cohort 2025", "year": 2025}
        response = self.client.post(url, data)
        print("Response status code:", response.status_code)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Cohort.objects.filter(name="Cohort 2025").exists())

    def test_cohort_create_authenticated_resident(self):
        """Test that a resident cannot create a new cohort."""
        # Authenticate with resident user
        token = Token.objects.create(user=self.resident_user)
        self.client.force_authenticate(user=self.resident_user)
        url = url = reverse('cohort-create')
        data = {"name": "Cohort 2027", "year": 2028}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cohort_create_unauthenticated(self):
        """Test that unauthenticated users cannot create a new cohort."""
        url = reverse('cohort-create')
        data = {"name": "Cohort 2029", "year": 2029}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cohort_retrieve_authenticated(self):
        """Test that an authenticated user can retrieve a cohort."""
        # Authenticate with admin user
        token = Token.objects.create(user=self.admin_user)
        self.client.force_authenticate(user=self.admin_user)
        cohort = Cohort.objects.first()
        url = reverse('cohort-detail', kwargs={'pk': cohort.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], cohort.id)

    def test_cohort_update_authenticated_coordinator(self):
        """Test that a coordinator can update a cohort."""
        # Authenticate with coordinator user
        token = Token.objects.create(user=self.coordinator_user)
        self.client.force_authenticate(user=self.coordinator_user)
        cohort = Cohort.objects.first()
        url = reverse('cohort-detail', kwargs={'pk': cohort.id})
        data = {"name": "Updated Cohort Name", "year": 2025}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        cohort.refresh_from_db()
        self.assertEqual(cohort.name, "Updated Cohort Name")

    def test_cohort_update_authenticated_resident(self):
        """Test that a resident cannot update a cohort."""
        # Authenticate with resident user
        token = Token.objects.create(user=self.resident_user)
        self.client.force_authenticate(user=self.resident_user)
        cohort = Cohort.objects.first()
        url = reverse('cohort-detail', kwargs={'pk': cohort.id})
        data = {"name": "Updated Cohort Name", "year": 2025}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cohort_delete_authenticated_coordinator(self):
        """Test that a coordinator can delete a cohort."""
        # Authenticate with coordinator user
        token = Token.objects.create(user=self.coordinator_user)
        self.client.force_authenticate(user=self.coordinator_user)
        cohort = Cohort.objects.first()
        url = reverse('cohort-detail', kwargs={'pk': cohort.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Cohort.objects.filter(id=cohort.id).exists())

    def test_cohort_delete_authenticated_resident(self):
        """Test that a resident cannot delete a cohort."""
        # Authenticate with resident user
        token = Token.objects.create(user=self.resident_user)
        self.client.force_authenticate(user=self.resident_user)
        cohort = Cohort.objects.first()
        url = url = reverse('cohort-detail', kwargs={'pk': cohort.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
