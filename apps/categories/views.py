from django.shortcuts import render
from .models import Category

def category_list_view(request):
    query = request.GET.get('q', '').strip()
    categories = Category.objects.prefetch_related('products').all()
    if query:
        categories = categories.filter(name__icontains=query)

    context = {
        "categories": categories,
        "query": query,
    }
    return render(request, "categories/list.html", context)
