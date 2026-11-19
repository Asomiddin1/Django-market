from django.db import models
from django.contrib.auth.models import User
from apps.categories.models import Category


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products'
    )

    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    # Many-to-Many 
    favorites = models.ManyToManyField(
        User,
        related_name='favorite_products',
        blank=True,
        verbose_name="Sevimlilar (Foydalanuvchilar)"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def favorites_count(self):
        return self.favorites.count()
