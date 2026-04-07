from django.urls import path
from . import views

urlpatterns = [
    path('people/', views.people_view, name='people'),
    path('friend-request/<int:user_id>/', views.send_friend_request, name='send_friend_request'),
    path('friend-request/<int:request_id>/decision/', views.friend_request_decision, name='friend_request_decision'),
    path('block/<int:user_id>/', views.block_user, name='block_user'),
    path('report/<int:user_id>/', views.report_user, name='report_user'),
]
