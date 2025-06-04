from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.core.mail import send_mail

from config import settings
from .forms import RegisterForm

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            try:
                send_mail(
                    'Добро пожаловать в MyDiary!',
                    'Спасибо за регистрацию на нашем сайте.',
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
                return redirect('registration_success')
            except Exception as e:
                messages.error(request, 'Не удалось отправить письмо. Попробуйте войти.')
                return redirect('entry_list')
    else:
        form = RegisterForm()

    return render(request, 'registration/register.html', {'form': form})

def registration_success_view(request):
    return render(request, 'registration/registration_success.html')

