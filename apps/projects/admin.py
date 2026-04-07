from django.contrib import admin
from .models import Project, ProjectMember, JoinRequest, Message, ProjectTask, ProjectRating

admin.site.register(Project)
admin.site.register(ProjectMember)
admin.site.register(JoinRequest)
admin.site.register(Message)
admin.site.register(ProjectTask)
admin.site.register(ProjectRating)
