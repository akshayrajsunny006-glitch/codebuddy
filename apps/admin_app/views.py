from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apps.auth_app.models import User
from apps.projects.models import Project
from apps.social.models import Report
from apps.support.models import SupportTicket


def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'admin':
            messages.error(request, 'Admin access required.')
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return login_required(wrapper)


@admin_required
def admin_panel(request):
    tab = request.GET.get('tab', 'users')
    context = {
        'tab': tab,
        'user_count': User.objects.count(),
        'project_count': Project.objects.count(),
        'report_count': Report.objects.count(),
        'ticket_count': SupportTicket.objects.filter(status='open').count(),
    }

    if tab == 'users':
        context['users'] = User.objects.all().order_by('-date_joined')
    elif tab == 'projects':
        context['projects'] = Project.objects.all().select_related('owner').order_by('-created_at')
    elif tab == 'reports':
        context['reports'] = Report.objects.all().select_related('reporter', 'reported_user').order_by('-created_at')
    elif tab == 'tickets':
        context['tickets'] = SupportTicket.objects.all().select_related('user').order_by('-created_at')

    return render(request, 'admin/panel.html', context)


@admin_required
def ban_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_banned = not user.is_banned
    user.save()
    action = 'banned' if user.is_banned else 'unbanned'
    messages.success(request, f'User {user.full_name} has been {action}.')
    return redirect('admin_panel')


@admin_required
def deactivate_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.is_active = False
    project.save()
    messages.success(request, f'Project "{project.title}" deactivated.')
    return redirect('admin_panel')


@admin_required
def update_ticket(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id)
    status = request.POST.get('status')
    if status in ['open', 'in_progress', 'resolved']:
        ticket.status = status
        ticket.save()
        messages.success(request, 'Ticket status updated.')
    return redirect('admin_panel')
