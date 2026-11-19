from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'get_favorites_count', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('favorites',)

    @admin.display(description="Sevimlilar soni")
    def get_favorites_count(self, obj):
        return obj.favorites.count()
