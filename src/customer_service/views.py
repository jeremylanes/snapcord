from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from customer_service.models import Message


def about(request):
    return render(request, 'customer_service/about.html')


def message(request):
    if request.method == 'POST':

        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if request.user.is_authenticated:
            Message.objects.create(name=name, email=email, subject=subject, content=message, author=request.user)
        else:
            Message.objects.create(name=name, email=email, subject=subject, content=message)

        return redirect('store:store')

    return render(request, 'customer_service/message.html')


@login_required
def thanks(request):
    return render(request, 'customer_service/thanks.html')
