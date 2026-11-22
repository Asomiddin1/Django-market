from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from apps.products.models import Product
from .cart import Cart


def cart_detail_view(request):
    """
    Savatchadagi mahsulotlar ro'yxatini ko'rsatish sahifasi.
    """
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})


def cart_add_view(request, product_id):
    """
    Mahsulotni savatga qo'shish.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1)) if request.method == 'POST' else 1
    cart.add(product=product, quantity=quantity)

    messages.success(request, f"«{product.name}» savatga muvaffaqiyatli qo‘shildi!")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    return redirect(next_url or 'cart:detail')


def cart_decrement_view(request, product_id):
    """
    Savatdagi mahsulot sonini 1 taga kamaytirish.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.decrement(product=product)

    messages.info(request, f"«{product.name}» miqdori kamaytirildi.")
    return redirect('cart:detail')


def cart_remove_view(request, product_id):
    """
    Mahsulotni savatdan butunlay olib tashlash.
    """
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product=product)

    messages.warning(request, f"«{product.name}» savatdan o‘chirildi.")
    return redirect('cart:detail')


def cart_clear_view(request):
    """
    Savatni to'liq tozalash.
    """
    cart = Cart(request)
    cart.clear()
    messages.info(request, "Savat tozalandi.")
    return redirect('cart:detail')
