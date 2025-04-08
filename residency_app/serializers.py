from rest_framework import serializers
from .models import User, Cohort, Resident

# ------------------ User Serializers ------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']

    def create(self, validated_data):
        user = User.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password= validated_data['password'],
            role = validated_data['role'],
        )
        return user
    
# ------------------ Cohort Serializers ------------------
class CohortSerializer(serializers.ModelSerializer):
    coordinator_username = serializers.CharField(source='coordinator.username', read_only=True)
    class Meta:
        model = Cohort
        fields = ['id', 'name', 'year', 'coordinator', 'coordinator_username']


# ------------------ Resident Serializer ------------------
class ResidentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    cohort_name = serializers.CharField(source='cohort.name', read_only=True)
    coach_username = serializers.CharField(source='coach.username', read_only=True)
    class Meta:
        model = Resident
        fields = ['id', 'user_username', 'cohort_name', 'coach_username', 'sending_church', 'plant_name']