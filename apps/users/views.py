from apps.users.forms import LoginForm
from django.contrib import messages
from django.shortcuts import render, redirect
from apps.users.forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Akkauntingiz muvaffaqiyatli yaratildi!"
            )
            return redirect('users:register')
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Akkauntingizga kirdingiz!"
            )
            return redirect('users:login')
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})