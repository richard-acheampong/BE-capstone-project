from django.shortcuts import render
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

# Create your views here.
# ------------------ User Views ------------------
class UserRegistrationView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data= request.data)

        if serializer.is_valid():
            #save and create a token
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            # Return a success mesaage with token nd user details
            return Response({
                'message': 'User registered successfully',
                'token': token.key,
                'username': user.username,
                'role': user.role,
            }, status=status.HTTP_201_CREATED)
        # Return error is serializer is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# ------------------ Cohort Views ------------------
class CohortListView(generics.ListAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated]

class CohortCreateView(generics.ListCreateAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated, IsAdminOrCoordinator]

class CohortDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cohort.objects.all()
    serializer_class = CohortSerializer
    permission_classes = [IsAuthenticated, IsAdminOrCoordinator]

# ------------------ Resident Views ------------------
class ResidentListCreateView(generics.ListCreateAPIView):
    serializer_class = ResidentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['cohort', 'coach', 'sending_church']
    search_fields = ['sending_church', 'plant_name', 'user__username']

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
    permission_classes = [IsAuthenticated, IsAdminCoordinatorCoachResident]




