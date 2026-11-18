from django.shortcuts import render
from .models import Product
from apps.categories.models import Category

def product_list_view(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    category_id = request.GET.get('category')
    selected_category = None
    if category_id:
        products = products.filter(category_id=category_id)
        selected_category = categories.filter(id=category_id).first()

    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(name__icontains=query)

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'selected_category_id': int(category_id) if category_id and category_id.isdigit() else None,
        'query': query,
        'product_count': products.count(),
    }

    return render(request, 'products/list.html', context)
