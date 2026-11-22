from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from apps.categories.models import Category


def product_list_view(request):
    # select_related('category') orqali mahsulot bilan birga uning bog'liq kategoriyasi (Foreign Key)
    # bitta SQL JOIN so'rovi orqali olinadi (N+1 query muammosini oldini oladi)
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

    user_favorite_ids = set()
    if request.user.is_authenticated:
        user_favorite_ids = set(
            request.user.favorite_products.values_list('id', flat=True)
        )

    context = {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'selected_category_id': int(category_id) if category_id and category_id.isdigit() else None,
        'query': query,
        'product_count': products.count(),
        'user_favorite_ids': user_favorite_ids,
    }

    return render(request, 'products/list.html', context)


def product_detail_view(request, pk):
    """
    Mahsulotning to'liq ma'lumotlari (Detail) sahifasi.
    """
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)

    # O'xshash mahsulotlar (select_related orqali bog'liq kategoriya bilan birga olinadi)
    related_products = Product.objects.select_related('category').filter(
        category=product.category
    ).exclude(pk=product.pk)[:4]

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = product.favorites.filter(id=request.user.id).exists()

    context = {
        'product': product,
        'related_products': related_products,
        'is_favorite': is_favorite,
    }
    return render(request, 'products/detail.html', context)


@login_required(login_url='users:login')
def toggle_wishlist(request, product_id):
    """
    Mahsulotni sevimlilarga qo'shish yoki o'chirish (Many-to-Many toggle).
    """
    product = get_object_or_404(Product, id=product_id)

    if request.user in product.favorites.all():
        product.favorites.remove(request.user)
        messages.info(request, f"«{product.name}» sevimlilardan olib tashlandi.")
    else:
        product.favorites.add(request.user)
        messages.success(request, f"«{product.name}» sevimlilar ro‘yxatiga qo‘shildi.")

    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('products:wishlist')


@login_required(login_url='users:login')
def wishlist_view(request):
    """
    Foydalanuvchining barcha sevimli mahsulotlarini ko'rsatish sahifasi.
    """
    favorite_products = request.user.favorite_products.select_related('category').all()
    user_favorite_ids = set(favorite_products.values_list('id', flat=True))

    context = {
        'products': favorite_products,
        'user_favorite_ids': user_favorite_ids,
        'product_count': favorite_products.count(),
    }
    return render(request, 'products/wishlist.html', context)
