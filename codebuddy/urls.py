from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.auth_app import views as auth_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('', auth_views.home, name='home'),
    path('dashboard/', auth_views.dashboard, name='dashboard'),
    path('auth/', include('apps.auth_app.urls')),
    path('projects/', include('apps.projects.urls')),
    path('social/', include('apps.social.urls')),
    path('admin-panel/', include('apps.admin_app.urls')),
    path('support/', include('apps.support.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
