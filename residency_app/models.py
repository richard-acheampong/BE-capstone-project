from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.

# ------------------ User Model ------------------
class User(AbstractUser):
    ADMIN = 'admin'
    COORDINATOR = 'coordinator'
    COACH = 'coach'
    RESIDENT = 'resient'

    role_choices = [
        (ADMIN, 'Administrator'),
        (COORDINATOR, 'Coordinator'),
        (COACH, 'Coach'),
        (RESIDENT, 'Resident'),
    ]

#Adding role as choice field
    role = models.CharField(max_length=20, choices=role_choices)

    def __str__(self):
        return self.username

# ------------------ Cohort Model ------------------
class Cohort(models.Model):
    name = models.CharField(max_length=100)
    year = models.IntegerField()
    coordinator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null= True,
        limit_choices_to= {'role': User.COORDINATOR},
        related_name= 'cohorts'
    )

    def __str__(self):
        return f'{self.name} ({self.year})'
    
# ------------------ Cohort Model ------------------
class Resident(models.Model):
    user =  models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete= models.CASCADE,
        limit_choices_to= {'role': User.RESIDENT},
        related_name= 'resident_profile'
    )
    cohort = models.ForeignKey(
        Cohort,
        on_delete= models.CASCADE,
        related_name= 'residents'
    )
    coach = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete= models.SET_NULL,
        null= True,
        blank= True,
        limit_choices_to= {'role':User.COACH},
        related_name= 'assigned_residents'  
    )
    sending_church = models.CharField(max_length=255)
    plant_name = models.CharField(max_length=255)
    plant_location = models.CharField(max_length=255)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

    
