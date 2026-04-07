from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects_list, name='projects'),
    path('create/', views.project_create, name='project_create'),
    path('<int:pk>/', views.project_room, name='project_room'),
    path('<int:pk>/join/', views.send_join_request, name='send_join_request'),
    path('<int:pk>/requests/<int:request_id>/decision/', views.join_request_decision, name='join_request_decision'),
    path('<int:pk>/tasks/add/', views.add_task, name='add_task'),
    path('<int:pk>/tasks/<int:task_id>/status/', views.update_task_status, name='update_task_status'),
]
