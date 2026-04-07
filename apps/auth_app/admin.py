from django.contrib import admin
from .models import User, UserProfile, Notification

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'full_name', 'role', 'is_banned', 'date_joined']
    search_fields = ['email', 'full_name']
    list_filter = ['role', 'is_banned', 'available_now']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'linkedin']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'type', 'is_read', 'created_at']
    list_filter = ['type', 'is_read']
