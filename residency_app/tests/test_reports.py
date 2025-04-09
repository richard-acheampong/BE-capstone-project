from rest_framework import status
from rest_framework.test import APITestCase

from residency_app.models import Cohort, Resident, User
from rest_framework.authtoken.models import Token
from django.urls import reverse

class ReportViewsTests(APITestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin', password='password', role='Admin')
        self.coordinator_user = User.objects.create_user(username='coordinator', password='password', role='Coordinator')
        self.coach_user = User.objects.create_user(username='coach', password='password', role='Coach')
    
        self.token_admin = Token.objects.create(user=self.admin_user)
        self.token_coordinator = Token.objects.create(user=self.coordinator_user)
    
        self.cohort1 = Cohort.objects.create(name="Cohort 2025", year=2025)
        self.cohort2 = Cohort.objects.create(name="Cohort 2026", year=2026)
    
    # Create residents and assign coach
        self.resident1 = Resident.objects.create(user=self.coach_user, cohort=self.cohort1, sending_church='Church A', plant_name='Plant A')
        self.resident2 = Resident.objects.create(user=self.coordinator_user, cohort=self.cohort2, sending_church='Church B', plant_name='Plant B')
    
    # Assign coach to residents
        self.resident1.coach = self.coach_user
        self.resident2.coach = self.coach_user
        self.resident1.save()
        self.resident2.save()

    def test_cohort_summary_report_authenticated(self):
        """Test that authenticated users can access cohort summary report"""
        url = reverse('cohort-summary')
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  
        self.assertIn('cohort', response.data[0])
        self.assertIn('resident_count', response.data[0])
    
    def test_cohort_summary_report_unauthenticated(self):
        """Test that unauthenticated users cannot access cohort summary report"""
        url = reverse('cohort-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_coach_resident_report_authenticated(self):
        """Test that authenticated users can access the coach-resident report"""
        url = reverse('coach-report')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  
        self.assertIn('coach', response.data[0])
        self.assertIn('resident_count', response.data[0])
        self.assertIn('residents', response.data[0])
    
    def test_coach_resident_report_unauthenticated(self):
        """Test that unauthenticated users cannot access coach-resident report"""
        url = reverse('coach-report')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_coach_resident_report_data(self):
        """Test that the coach-resident report returns correct data"""
        url = reverse('coach-report')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_admin.key)
        response = self.client.get(url)

        coach_data = response.data[0]
        self.assertEqual(coach_data['coach'], 'coach')
        self.assertEqual(coach_data['resident_count'], 2)
        self.assertEqual(len(coach_data['residents']), 2)
        self.assertEqual(coach_data['residents'][0]['name'], 'coach')
        self.assertEqual(coach_data['residents'][0]['cohort'], 'Cohort 2025')
