from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """Admin personalizat pentru CustomUser"""
    
    list_display = ['username', 'email', 'role', 'is_staff', 'is_active']
    list_filter = ['role', 'is_staff', 'is_active']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    
    fieldsets = UserAdmin.fieldsets + (
        ('Informații suplimentare', {'fields': ('role', 'bio', 'avatar', 'phone')}),
    )
    
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informații suplimentare', {'fields': ('role', 'bio', 'avatar', 'phone')}),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin pentru Profile"""
    
    list_display = ['user', 'total_tours_completed', 'total_reviews', 'joined_date']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['joined_date']
