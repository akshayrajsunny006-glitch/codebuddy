from apps.auth_app.models import Notification


def unread_notifications(request):
    if request.user.is_authenticated:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
        return {'unread_notif_count': count}
    return {'unread_notif_count': 0}


def global_context(request):
    """Global context processor for all templates"""
    context = {}
    if request.user.is_authenticated:
        context['user'] = request.user
        context['unread_notif_count'] = Notification.objects.filter(user=request.user, is_read=False).count()
    return context
