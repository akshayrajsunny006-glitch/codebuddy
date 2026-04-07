from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
import json


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        return self.create_user(email, password, **extra_fields)


YEAR_CHOICES = [
    ('1st', '1st Year'), ('2nd', '2nd Year'),
    ('3rd', '3rd Year'), ('4th', '4th Year'), ('5th', '5th Year+'),
]

GENDER_CHOICES = [
    ('male', 'Male'), ('female', 'Female'),
    ('non_binary', 'Non-Binary'), ('prefer_not', 'Prefer not to say'),
]


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, blank=True)
    college_name = models.CharField(max_length=300, blank=True)
    year_of_study = models.CharField(max_length=10, choices=YEAR_CHOICES, blank=True)
    skills = models.TextField(blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, default='user')
    is_banned = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    skills_json = models.JSONField(default=list, blank=True)
    preferred_roles = models.JSONField(default=list, blank=True)
    available_now = models.BooleanField(default=False)
    reputation_score = models.FloatField(default=0.0)
    avatar = models.CharField(max_length=10, blank=True)  # emoji avatar

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    def get_avatar_initials(self):
        parts = self.full_name.split()
        if len(parts) >= 2:
            return parts[0][0].upper() + parts[1][0].upper()
        return self.full_name[0].upper() if self.full_name else 'U'

    def get_avatar_color(self):
        colors = ['#6366f1', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981', '#3b82f6', '#ef4444']
        return colors[self.id % len(colors)] if self.id else colors[0]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    certificates = models.TextField(blank=True)
    linkedin = models.URLField(blank=True)
    github = models.URLField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_profiles'


class Notification(models.Model):
    TYPES = [
        ('join_request', 'Join Request'),
        ('request_approved', 'Request Approved'),
        ('request_rejected', 'Request Rejected'),
        ('friend_request', 'Friend Request'),
        ('friend_accepted', 'Friend Accepted'),
        ('message', 'Message'),
        ('general', 'General'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=30, choices=TYPES, default='general')
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True)

    class Meta:
        db_table = 'notifications'
        ordering = ['-created_at']
