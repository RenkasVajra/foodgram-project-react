from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ("first_name", "last_name", "username", "email")
    list_filter = ("email", "username", "first_name")
    search_fields = ("email", "first_name")
