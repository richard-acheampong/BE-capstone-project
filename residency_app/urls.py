from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserRegistrationView, CohortListView, CohortCreateListView, CohortDetailView, ResidentDetailView, ResidentListCreateView

urlpatterns =[
    #user urls
    path('residency/register/', UserRegistrationView.as_view(), name= 'register'),
    path('residency/login/', obtain_auth_token, name= 'login'),

    #cohort urls
    path('residency/cohorts/', CohortListView.as_view(), name= 'cohort-list-create'),
    path('residency/cohorts/create/', CohortCreateListView.as_view(), name= 'cohort-list-create'),
    path('residency/cohorts/<int:pk>/', CohortDetailView.as_view(), name= 'cohort-detail'),

    #resident urls
    path('residency/residents/', ResidentListCreateView.as_view(), name='resident-list-create'),
    path('residency/residents/<int:pk>/', ResidentDetailView.as_view(), name='resident-detail'),



]