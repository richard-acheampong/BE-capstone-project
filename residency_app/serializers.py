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
    class Meta:
        model = Cohort
        fields = ['id', 'name', 'year', 'coordinator']


# ------------------ Resident Serializer ------------------
class ResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resident
        fields = ['id', 'user', 'cohort', 'sending_church', 'plant_name', 'plant_location']