from django.contrib import admin
from .models import User, Department

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'is_approved', 'department']
    list_filter = ['role', 'is_approved', 'department']
    search_fields = ['username', 'email']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
