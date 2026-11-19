from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Ism",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Ismingizni kiriting'})
    )
    last_name = forms.CharField(
        label="Familiya",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Familiyangizni kiriting'})
    )
    email = forms.EmailField(
        label="Elektron pochta (Email)",
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'example@gmail.com'})
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            'username': 'Foydalanuvchi nomi (Username)',
        }
        help_texts = {
            'username': 'Talab qilinadi. 150 yoki undan kam harf, raqam va @/./+/-/_ belgilar.',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("Ushbu email bilan allaqachon ro‘yxatdan o‘tilgan.")
        return email


class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username kiriting',
            'autocomplete': 'username',
        })
    )
    password = forms.CharField(
        label="Parol",
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Parolingizni kiriting',
            'autocomplete': 'current-password',
        })
    )


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya',
            'email': 'Elektron pochta (Email)',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Ismingizni kiriting'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Familiyangizni kiriting'}),
            'email': forms.EmailInput(attrs={'placeholder': 'example@gmail.com'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip()
        user_id = self.instance.pk
        if User.objects.filter(email__iexact=email).exclude(pk=user_id).exists():
            raise forms.ValidationError("Ushbu email boshqa foydalanuvchi tomonidan band qilingan.")
        return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'phone_number', 'address', 'bio']
        labels = {
            'avatar': 'Profil rasmi',
            'phone_number': 'Telefon raqam',
            'address': 'Yetkazib berish manzili',
            'bio': 'O‘zingiz haqingizda qisqacha',
        }
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': '+998 90 123 45 67'}),
            'address': forms.TextInput(attrs={'placeholder': 'Toshkent sh., Chilonzor tumani, ...'}),
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'O‘zingiz haqingizda ma’lumot...'}),
        }
