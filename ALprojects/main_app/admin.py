from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import *


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['username', 'email', 'work_place', 'birth_date', 'password']


admin.site.register(CustomUser, CustomUserAdmin)
