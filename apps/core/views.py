from django.shortcuts import render
from apps.products.models import Product
from apps.categories.models import Category

# Create your views here.
def home_view(request):
    products = Product.objects.all().select_related('category')
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, "core/home.html", context)