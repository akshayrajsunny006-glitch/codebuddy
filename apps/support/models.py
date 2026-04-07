from django.db import models
from django.conf import settings


class SupportTicket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
    ]
    CATEGORY_CHOICES = [
        ('bug', 'Bug Report'),
        ('feature', 'Feature Request'),
        ('account', 'Account Issue'),
        ('project', 'Project Issue'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    subject = models.CharField(max_length=300)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='other')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'support_tickets'
        ordering = ['-created_at']

    def __str__(self):
        return self.subject

    def get_status_color(self):
        return {'open': '#f59e0b', 'in_progress': '#6366f1', 'resolved': '#10b981'}.get(self.status, '#6b7280')
