from django.shortcuts import redirect
from django.shortcuts import render 
from apps.products.models import Product
from apps.categories.models import Category
from .forms import ContactForm
from django.contrib import messages

# Create your views here.
def home_view(request):
    products = Product.objects.all().select_related('category')
    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, "core/home.html", context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Xabaringiz muvaffaqiyatli yuborildi!"
            )

            return redirect('core:contact')

    else:
        form = ContactForm()

    return render(request, 'core/contact.html', {
        'form': form
    })