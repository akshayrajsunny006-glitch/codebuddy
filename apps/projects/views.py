from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Project, ProjectMember, JoinRequest, Message, ProjectTask
from .forms import ProjectForm, JoinRequestForm, TaskForm
from apps.auth_app.models import Notification


@login_required
def projects_list(request):
    user = request.user
    query = request.GET.get('q', '')
    difficulty = request.GET.get('difficulty', '')

    projects = Project.objects.filter(is_active=True).prefetch_related('members')

    if query:
        projects = projects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(required_skills__icontains=query)
        )
    if difficulty:
        projects = projects.filter(difficulty=difficulty)

    my_memberships = ProjectMember.objects.filter(user=user).values_list('project_id', flat=True)
    my_requests = JoinRequest.objects.filter(user=user, status='pending').values_list('project_id', flat=True)

    project_data = []
    for p in projects:
        project_data.append({
            'project': p,
            'is_member': p.id in my_memberships,
            'has_requested': p.id in my_requests,
            'member_count': p.members.count(),
        })

    return render(request, 'projects/list.html', {
        'project_data': project_data,
        'query': query,
        'difficulty': difficulty,
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            ProjectMember.objects.create(project=project, user=request.user, role='Owner')
            messages.success(request, f'Project "{project.title}" created! 🎉')
            return redirect('project_room', pk=project.id)
    else:
        form = ProjectForm()
    return render(request, 'projects/create.html', {'form': form})


@login_required
def project_room(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user
    is_member = project.members.filter(user=user).exists()
    is_owner = project.owner == user

    # Only show full_description to members/owner or public projects
    show_full = is_member or is_owner or project.privacy_level == 'public'

    members = project.members.select_related('user').all()
    chat_messages = project.messages.select_related('user').order_by('created_at')
    join_requests = []
    if is_owner:
        join_requests = project.join_requests.filter(status='pending').select_related('user')

    tasks = project.tasks.select_related('assignee').all()
    task_form = TaskForm()
    if is_owner or is_member:
        task_form.fields['assignee'].queryset = project.members.values_list('user', flat=True)

    # Send message
    if request.method == 'POST' and is_member:
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(project=project, user=user, content=content)
            return redirect('project_room', pk=pk)

    context = {
        'project': project,
        'is_member': is_member,
        'is_owner': is_owner,
        'show_full': show_full,
        'members': members,
        'chat_messages': chat_messages,
        'join_requests': join_requests,
        'tasks': tasks,
        'task_form': task_form,
    }
    return render(request, 'projects/room.html', context)


@login_required
def send_join_request(request, pk):
    project = get_object_or_404(Project, pk=pk)
    user = request.user

    if project.members.filter(user=user).exists():
        messages.warning(request, 'You are already a member.')
        return redirect('project_room', pk=pk)

    if JoinRequest.objects.filter(project=project, user=user).exists():
        messages.warning(request, 'You have already requested to join.')
        return redirect('project_room', pk=pk)

    if request.method == 'POST':
        form = JoinRequestForm(request.POST)
        if form.is_valid():
            jr = form.save(commit=False)
            jr.project = project
            jr.user = user
            jr.save()
            Notification.objects.create(
                user=project.owner,
                type='join_request',
                content=f'{user.full_name} requested to join "{project.title}"',
                link=f'/projects/{project.id}/'
            )
            messages.success(request, 'Join request sent! ✉️')
            return redirect('project_room', pk=pk)
    else:
        form = JoinRequestForm()

    return render(request, 'projects/join_request.html', {'project': project, 'form': form})


@login_required
def join_request_decision(request, pk, request_id):
    project = get_object_or_404(Project, pk=pk)
    if project.owner != request.user:
        messages.error(request, 'Permission denied.')
        return redirect('project_room', pk=pk)

    jr = get_object_or_404(JoinRequest, id=request_id, project=project)
    decision = request.POST.get('decision')

    if decision == 'approve':
        jr.status = 'approved'
        jr.save()
        ProjectMember.objects.get_or_create(project=project, user=jr.user, defaults={'role': 'Member'})
        Notification.objects.create(
            user=jr.user,
            type='request_approved',
            content=f'Your request to join "{project.title}" was approved! 🎉',
            link=f'/projects/{project.id}/'
        )
        messages.success(request, f'{jr.user.full_name} has been added to the project.')
    elif decision == 'reject':
        jr.status = 'rejected'
        jr.save()
        Notification.objects.create(
            user=jr.user,
            type='request_rejected',
            content=f'Your request to join "{project.title}" was not approved.',
        )
        messages.info(request, f'Request from {jr.user.full_name} rejected.')

    return redirect('project_room', pk=pk)


@login_required
def add_task(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if not (project.owner == request.user or project.members.filter(user=request.user).exists()):
        messages.error(request, 'Permission denied.')
        return redirect('project_room', pk=pk)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        if title:
            ProjectTask.objects.create(project=project, title=title, description=description)
            messages.success(request, 'Task added!')

    return redirect('project_room', pk=pk)


@login_required
def update_task_status(request, pk, task_id):
    project = get_object_or_404(Project, pk=pk)
    task = get_object_or_404(ProjectTask, id=task_id, project=project)
    new_status = request.POST.get('status')
    if new_status in ['todo', 'in_progress', 'done']:
        task.status = new_status
        task.save()
    return redirect('project_room', pk=pk)
