from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def product_home(request):

    context = {
        'market_name': 'Django Market',
        'product_count': 25,
    }

    return render(
        request,
        'products/home.html',
        context
    )