from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Cohort, Resident

#Register your models here.
class CustomUserAdmin(UserAdmin):
    #display fields in admin list view
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')

    #add role to the user creation and edit forms
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Cohort)
admin.site.register(Resident)



