from django.db import models
from django.conf import settings


DIFFICULTY_CHOICES = [
    ('beginner', 'Beginner'),
    ('intermediate', 'Intermediate'),
    ('advanced', 'Advanced'),
]

PRIVACY_CHOICES = [
    ('public', 'Public'),
    ('private', 'Private'),
]

STATUS_CHOICES = [
    ('recruiting', 'Recruiting'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
    ('paused', 'Paused'),
]


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='owned_projects')
    title = models.CharField(max_length=200)
    teaser = models.CharField(max_length=300, blank=True)
    description = models.TextField()
    full_description = models.TextField(blank=True)
    required_skills = models.TextField(blank=True)
    required_skills_json = models.JSONField(default=list, blank=True)
    roles_needed_json = models.JSONField(default=list, blank=True)
    max_team_size = models.IntegerField(default=5)
    deadline = models.DateField(null=True, blank=True)
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='intermediate')
    privacy_level = models.CharField(max_length=20, choices=PRIVACY_CHOICES, default='public')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='recruiting')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'projects'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_member_count(self):
        return self.members.count()

    def is_member(self, user):
        return self.members.filter(user=user).exists()

    def get_difficulty_color(self):
        return {
            'beginner': '#10b981',
            'intermediate': '#f59e0b',
            'advanced': '#ef4444',
        }.get(self.difficulty, '#6366f1')


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='project_memberships')
    role = models.CharField(max_length=100, default='Member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_members'
        unique_together = ('project', 'user')

    def __str__(self):
        return f'{self.user} in {self.project}'


class JoinRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='join_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='join_requests')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True)
    auto_matched = models.BooleanField(default=False)
    viewed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'join_requests'
        unique_together = ('project', 'user')
        ordering = ['-created_at']


class Message(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'messages'
        ordering = ['created_at']


class ProjectTask(models.Model):
    TASK_STATUS = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default='todo')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'project_tasks'
        ordering = ['created_at']


class ProjectRating(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='ratings')
    rater = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_given')
    ratee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ratings_received')
    reliability = models.IntegerField(default=5)
    communication = models.IntegerField(default=5)
    skill = models.IntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'project_ratings'
        unique_together = ('project', 'rater', 'ratee')
