from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import User, UserProfile, Notification
from .forms import LoginForm, SignupForm, ProfileForm
from apps.projects.models import Project, ProjectMember, JoinRequest


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    stats = {
        'users': User.objects.count(),
        'projects': Project.objects.filter(is_active=True).count() if hasattr(Project, 'objects') else 0,
    }
    return render(request, 'home.html', {'stats': stats})


@login_required
def dashboard(request):
    user = request.user
    my_projects = ProjectMember.objects.filter(user=user).select_related('project').order_by('-joined_at')
    active_projects = [pm for pm in my_projects if pm.project.is_active]
    past_projects = [pm for pm in my_projects if not pm.project.is_active]

    # Incoming join requests on owned projects
    owned_projects = Project.objects.filter(owner=user)
    pending_requests = JoinRequest.objects.filter(
        project__in=owned_projects, status='pending'
    ).select_related('user', 'project').order_by('-created_at')[:5]

    notifications = Notification.objects.filter(user=user, is_read=False)[:5]
    days_since_join = (timezone.now() - user.date_joined).days

    context = {
        'active_projects': active_projects,
        'past_projects': past_projects,
        'pending_requests': pending_requests,
        'notifications': notifications,
        'days_since_join': days_since_join,
    }
    return render(request, 'dashboard.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_banned:
                messages.error(request, 'Your account has been banned.')
            else:
                login(request, user)
                return redirect(request.GET.get('next', 'dashboard'))
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f'Welcome to CodeBuddy, {user.full_name}! 🚀')
            return redirect('dashboard')
    else:
        form = SignupForm()
    return render(request, 'auth/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request):
    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            profile.phone = form.cleaned_data.get('phone', '')
            profile.linkedin = form.cleaned_data.get('linkedin', '')
            profile.github = form.cleaned_data.get('github', '')
            profile.certificates = form.cleaned_data.get('certificates', '')
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=user, initial={
            'phone': profile.phone,
            'linkedin': profile.linkedin,
            'github': profile.github,
            'certificates': profile.certificates,
        })

    from .models import YEAR_CHOICES
    my_projects = ProjectMember.objects.filter(user=user).select_related('project')
    return render(request, 'auth/profile.html', {
        'form': form,
        'profile': profile,
        'my_projects': my_projects,
        'year_choices': YEAR_CHOICES,
    })


def view_profile(request, user_id):
    profile_user = get_object_or_404(User, id=user_id)
    profile, _ = UserProfile.objects.get_or_create(user=profile_user)
    my_projects = ProjectMember.objects.filter(user=profile_user).select_related('project')

    # Check friendship / block status
    is_friend = False
    is_blocked = False
    friend_request_sent = False
    if request.user.is_authenticated:
        from apps.social.models import Friendship, Block, FriendRequest
        is_friend = Friendship.objects.filter(
            user1=request.user, user2=profile_user
        ).exists() or Friendship.objects.filter(
            user1=profile_user, user2=request.user
        ).exists()
        is_blocked = Block.objects.filter(user=request.user, blocked_user=profile_user).exists()
        friend_request_sent = FriendRequest.objects.filter(
            from_user=request.user, to_user=profile_user, status='pending'
        ).exists()

    return render(request, 'auth/view_profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'my_projects': my_projects,
        'is_friend': is_friend,
        'is_blocked': is_blocked,
        'friend_request_sent': friend_request_sent,
    })


@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user).order_by('-created_at')
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return render(request, 'auth/notifications.html', {'notifications': notifs})
