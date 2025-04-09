from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView, LoginView, CohortListView, CohortCreateView, CohortDetailView, ResidentDetailView, ResidentListCreateView, CohortSummaryReportView, CoachResidentReportView

urlpatterns =[
    #user urls
    path('residency/register/', UserRegistrationView.as_view(), name= 'register'),
    path('residency/login/', LoginView.as_view(), name= 'login'),

    #cohort urls
    path('residency/cohorts/', CohortListView.as_view(), name= 'cohort-list'),
    path('residency/cohorts/create', CohortCreateView.as_view(), name= 'cohort-create'),
    path('residency/cohorts/<int:pk>/', CohortDetailView.as_view(), name= 'cohort-detail'),

    #resident urls
    path('residency/residents/', ResidentListCreateView.as_view(), name='resident-list-create'),
    path('residency/residents/<int:pk>/', ResidentDetailView.as_view(), name='resident-detail'),

    #report urls
    path('residency/reports/cohorts/', CohortSummaryReportView.as_view(), name='cohort-summary'),
    path('residency/reports/coaches/', CoachResidentReportView.as_view(), name='coach-report'),



]