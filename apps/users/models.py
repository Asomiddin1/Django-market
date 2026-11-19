from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """
    Foydalanuvchi profili uchun One-to-One model.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name="Foydalanuvchi"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name="Profil rasmi"
    )
    phone_number = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name="Telefon raqami"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Yetkazib berish manzili"
    )
    bio = models.TextField(
        max_length=500,
        blank=True,
        null=True,
        verbose_name="O'zi haqida"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} profili"


@receiver(post_save, sender=User)
def create_or_save_user_profile(sender, instance, created, **kwargs):
    """
    Yangi foydalanuvchi yaratilganda avtomatik Profile (One-to-One) obyektini yaratish.
    """
    if created:
        Profile.objects.create(user=instance)
    else:
        # Mavjud bo'lmasa yaratish, bo'lsa saqlash
        Profile.objects.get_or_create(user=instance)
