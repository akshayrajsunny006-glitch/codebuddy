from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_panel, name='admin_panel'),
    path('ban/<int:user_id>/', views.ban_user, name='ban_user'),
    path('projects/<int:project_id>/deactivate/', views.deactivate_project, name='deactivate_project'),
    path('tickets/<int:ticket_id>/update/', views.update_ticket, name='update_ticket'),
]
