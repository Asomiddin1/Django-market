from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product
from .forms import ProductForm
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


@login_required(login_url='users:login')
def product_create_view(request):
    """
    Yangi mahsulot qo'shish sahifasi (Create).
    """
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"«{product.name}» muvaffaqiyatli qo‘shildi!")
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm()

    return render(request, 'products/product_form.html', {
        'form': form,
        'title': "Yangi mahsulot qo‘shish",
        'btn_text': "Mahsulotni saqlash",
    })


@login_required(login_url='users:login')
def product_update_view(request, pk):
    """
    Mavjud mahsulotni tahrirlash sahifasi (Update).
    """
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"«{product.name}» ma’lumotlari yangilandi!")
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)

    return render(request, 'products/product_form.html', {
        'form': form,
        'product': product,
        'title': f"«{product.name}»ni tahrirlash",
        'btn_text': "O‘zgarishlarni saqlash",
        'is_edit': True,
    })


@login_required(login_url='users:login')
def product_delete_view(request, pk):
    """
    Mahsulotni o'chirish (Delete).
    """
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.warning(request, f"«{name}» mahsuloti o‘chirildi.")
        return redirect('products:list')

    return render(request, 'products/product_confirm_delete.html', {'product': product})

