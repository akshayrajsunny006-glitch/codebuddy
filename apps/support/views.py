from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import SupportTicket


@login_required
def support_view(request):
    if request.method == 'POST':
        subject = request.POST.get('subject', '').strip()
        category = request.POST.get('category', 'other')
        message = request.POST.get('message', '').strip()
        if subject and message:
            SupportTicket.objects.create(
                user=request.user,
                subject=subject,
                category=category,
                message=message
            )
            messages.success(request, 'Support ticket submitted! We\'ll get back to you soon.')
            return redirect('support')
        else:
            messages.error(request, 'Please fill in all required fields.')

    tickets = SupportTicket.objects.filter(user=request.user)
    return render(request, 'support/support.html', {'tickets': tickets})
