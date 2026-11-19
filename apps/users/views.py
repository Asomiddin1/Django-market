from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from apps.users.forms import RegisterForm, LoginForm, UserUpdateForm, ProfileUpdateForm
from apps.users.models import Profile
from apps.users.utils import verify_recaptcha


def register(request):
    """
    Yangi foydalanuvchini ro'yxatdan o'tkazish.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Akkauntingiz muvaffaqiyatli yaratildi! Endi tizimga kirishingiz mumkin."
            )
            return redirect('users:login')
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    """
    Foydalanuvchini tizimga kiritish.
    Agar 1 marta xato qilsa (failed_attempts >= 1), reCAPTCHA tekshiruvi yoqiladi.
    """
    if request.user.is_authenticated:
        return redirect('core:home')

    failed_attempts = request.session.get('failed_login_attempts', 0)
    show_recaptcha = failed_attempts >= 1
    recaptcha_error = None

    if request.method == 'POST':
        form = LoginForm(request.POST)
        recaptcha_valid = True

        # Agar avval xato qilgan bo'lsa, reCAPTCHA tekshiriladi
        if show_recaptcha:
            recaptcha_token = request.POST.get('g-recaptcha-response', '').strip()
            remote_ip = request.META.get('REMOTE_ADDR')
            valid, err = verify_recaptcha(recaptcha_token, remote_ip)
            if not valid:
                recaptcha_valid = False
                recaptcha_error = err

        if form.is_valid() and recaptcha_valid:
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                auth_login(request, user)
                # Xatoliklar hisoblagichini tozalash
                if 'failed_login_attempts' in request.session:
                    del request.session['failed_login_attempts']
                    request.session.modified = True

                messages.success(
                    request,
                    f"Xush kelibsiz, {user.first_name or user.username}!"
                )
                next_url = request.GET.get('next') or request.POST.get('next')
                if next_url and next_url.startswith('/'):
                    return redirect(next_url)
                return redirect('core:home')
            else:
                # Login yoki parol noto'g'ri bo'lganda urinishlar sonini oshiramiz
                failed_attempts += 1
                request.session['failed_login_attempts'] = failed_attempts
                request.session.modified = True
                show_recaptcha = True
                form.add_error(None, "Username yoki parol noto‘g‘ri kiritildi!")

    else:
        form = LoginForm()

    context = {
        'form': form,
        'show_recaptcha': show_recaptcha,
        'recaptcha_error': recaptcha_error,
        'recaptcha_site_key': getattr(
            settings,
            'RECAPTCHA_SITE_KEY',
            '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
        ),
    }
    return render(request, 'user/login.html', context)


def logout_view(request):
    """
    Foydalanuvchini tizimdan chiqarish.
    """
    auth_logout(request)
    messages.info(request, "Tizimdan muvaffaqiyatli chiqdingiz.")
    return redirect('core:home')


@login_required(login_url='users:login')
def profile_view(request):
    """
    Foydalanuvchi profilini ko'rish va tahrirlash (One-to-One).
    """
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, "Profilingiz muvaffaqiyatli yangilandi!")
            return redirect('users:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=profile)

    favorites_count = request.user.favorite_products.count()

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'profile': profile,
        'favorites_count': favorites_count,
    }
    return render(request, 'user/profile.html', context)
