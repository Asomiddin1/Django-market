from django.shortcuts import render
from apps.products.models import Product

# Create your views here.
def home_view(request):
    products = Product.objects.all()

    context = {
        'products': products
    }
    return render(request, "core/home.html", context)