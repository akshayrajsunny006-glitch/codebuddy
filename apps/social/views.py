from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import FriendRequest, Friendship, Block, Report
from apps.auth_app.models import User, Notification


@login_required
def people_view(request):
    user = request.user
    query = request.GET.get('q', '')

    # Friends
    friendships = Friendship.objects.filter(
        Q(user1=user) | Q(user2=user)
    ).select_related('user1', 'user2')
    friends = []
    for f in friendships:
        friends.append(f.user2 if f.user1 == user else f.user1)

    # Incoming friend requests
    incoming = FriendRequest.objects.filter(to_user=user, status='pending').select_related('from_user')

    # Outgoing
    outgoing_ids = FriendRequest.objects.filter(from_user=user, status='pending').values_list('to_user_id', flat=True)

    # Blocked users
    blocked_ids = Block.objects.filter(user=user).values_list('blocked_user_id', flat=True)

    # Search
    search_results = []
    if query:
        blocked_me_ids = Block.objects.filter(blocked_user=user).values_list('user_id', flat=True)
        results = User.objects.filter(
            Q(full_name__icontains=query) | Q(email__icontains=query) | Q(skills__icontains=query)
        ).exclude(id=user.id).exclude(id__in=blocked_me_ids)[:20]

        friend_ids = [f.id for f in friends]
        for u in results:
            search_results.append({
                'user': u,
                'is_friend': u.id in friend_ids,
                'is_blocked': u.id in blocked_ids,
                'request_sent': u.id in outgoing_ids,
            })

    context = {
        'friends': friends,
        'incoming_requests': incoming,
        'search_results': search_results,
        'query': query,
        'blocked_ids': list(blocked_ids),
    }
    return render(request, 'social/people.html', context)


@login_required
def send_friend_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    user = request.user
    if to_user == user:
        messages.error(request, "You can't befriend yourself.")
        return redirect('people')

    if Block.objects.filter(user=user, blocked_user=to_user).exists():
        messages.error(request, 'You have blocked this user.')
        return redirect('people')

    _, created = FriendRequest.objects.get_or_create(from_user=user, to_user=to_user)
    if created:
        Notification.objects.create(
            user=to_user,
            type='friend_request',
            content=f'{user.full_name} sent you a friend request.',
            link='/social/people/'
        )
        messages.success(request, f'Friend request sent to {to_user.full_name}!')
    else:
        messages.info(request, 'Request already sent.')
    return redirect(request.META.get('HTTP_REFERER', 'people'))


@login_required
def friend_request_decision(request, request_id):
    fr = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    decision = request.POST.get('decision')

    if decision == 'accept':
        fr.status = 'accepted'
        fr.save()
        Friendship.objects.get_or_create(user1=request.user, user2=fr.from_user)
        Notification.objects.create(
            user=fr.from_user,
            type='friend_accepted',
            content=f'{request.user.full_name} accepted your friend request! 🎉',
            link='/social/people/'
        )
        messages.success(request, f'You are now friends with {fr.from_user.full_name}!')
    elif decision == 'reject':
        fr.status = 'rejected'
        fr.save()
        messages.info(request, 'Request rejected.')

    return redirect('people')


@login_required
def block_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    user = request.user

    existing = Block.objects.filter(user=user, blocked_user=target).first()
    if existing:
        existing.delete()
        messages.success(request, f'{target.full_name} unblocked.')
    else:
        Block.objects.create(user=user, blocked_user=target)
        # Cancel pending friend requests
        FriendRequest.objects.filter(
            Q(from_user=user, to_user=target) | Q(from_user=target, to_user=user),
            status='pending'
        ).update(status='rejected')
        messages.success(request, f'{target.full_name} has been blocked.')

    return redirect(request.META.get('HTTP_REFERER', 'people'))


@login_required
def report_user(request, user_id):
    target = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        description = request.POST.get('description', '')
        if reason:
            Report.objects.create(
                reporter=request.user,
                reported_user=target,
                reason=reason,
                description=description
            )
            messages.success(request, 'Report submitted. We will review it.')
    return redirect(request.META.get('HTTP_REFERER', 'people'))
