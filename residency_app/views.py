from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrCoordinator, IsAdminCoordinatorCoachResident
from .serializers import UserRegistrationSerializer, CohortSerializer, ResidentSerializer
from .models import Cohort, Resident, User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import Prefetch

# Create your views here.
# ------------------ User Views ------------------
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data= request.data)

        if serializer.is_valid():
            #save and create a token
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            # Return a success mesaage with token and user details
            return Response({
                'message': 'User registered successfully',
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }, status=status.HTTP_201_CREATED)
        # Return error is serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)

        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# ------------------ Cohort Views ------------------
class CohortListView(generics.ListAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['year']
    search_fields = ['name', 'coordinator__username']
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class CohortCreateView(generics.CreateAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated, IsAdminOrCoordinator ]

     
class CohortDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAuthenticated(), IsAdminOrCoordinator()]
        return [IsAuthenticated()]

# ------------------ Resident Views ------------------
class ResidentListCreateView(generics.ListCreateAPIView):
    serializer_class = ResidentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cohort', 'coach', 'sending_church']
    search_fields = ['sending_church', 'plant_name', 'user__username']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsAdminOrCoordinator()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user

        if user.role in [User.ADMIN, User.COORDINATOR]:
            return Resident.objects.all()

        if user.role == User.COACH:
            return Resident.objects.filter(coach=user)

        if user.role == User.RESIDENT:
            return Resident.objects.filter(user=user)

        return Resident.objects.none()


class ResidentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Resident.objects.all()
    serializer_class = ResidentSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['PUT', 'DELETE']:
            return [IsAdminOrCoordinator()]
        return [IsAuthenticated()]




# ------------------ Report Views ------------------
class CohortSummaryReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []
        cohorts = Cohort.objects.all()
        for cohort in cohorts:
            resident_count = cohort.resident.count()
            data.append({
                'cohort': cohort.name,
                'year': cohort.year,
                'resident_count': resident_count
            })
        return Response(data)
    

class CoachResidentReportView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = []
        coaches = User.objects.filter(role='Coach')
        for coach in coaches:
            residents = Resident.objects.filter(coach=coach)
            data.append({
                'coach': coach.username,
                'resident_count': residents.count(),
                'residents': [
                    {'name': r.user.username, 'cohort': r.cohort.name} for r in residents
                ]
            })
        return Response(data)





