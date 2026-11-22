import pytest
from apps.products.models import Product
from apps.categories.models import Category
from apps.cart.cart import Cart
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware


def get_request_with_session():
    """Yordamchi funksiya: Sessiyaga ega soxta request yaratish"""
    rf = RequestFactory()
    request = rf.get('/')
    middleware = SessionMiddleware(lambda r: None)
    middleware.process_request(request)
    request.session.save()
    return request


@pytest.mark.django_db
def test_cart_add_and_total_price():
    """
    Savatga mahsulot qo'shish va umumiy summani to'g'ri hisoblash testi.
    """
    category = Category.objects.create(name="Elektronika")
    p1 = Product.objects.create(category=category, name="Telefon", price=500.00, stock=10)
    p2 = Product.objects.create(category=category, name="Naushnik", price=50.00, stock=5)

    request = get_request_with_session()
    cart = Cart(request)

    # 1. Telefon qo'shamiz
    cart.add(p1, quantity=2)
    assert len(cart) == 2
    assert cart.get_total_price() == 1000.00

    # 2. Naushnik qo'shamiz
    cart.add(p2, quantity=1)
    assert len(cart) == 3
    assert cart.get_total_price() == 1050.00


@pytest.mark.django_db
def test_cart_decrement_and_remove():
    """
    Savatdagi mahsulot sonini kamaytirish va o'chirish testi.
    """
    category = Category.objects.create(name="Kiyim")
    product = Product.objects.create(category=category, name="Ko'ylak", price=100.00, stock=10)

    request = get_request_with_session()
    cart = Cart(request)

    cart.add(product, quantity=2)
    assert len(cart) == 2

    # 1 taga kamaytiramiz
    cart.decrement(product)
    assert len(cart) == 1

    # Yana kamaytirsak o'chib ketishi kerak
    cart.decrement(product)
    assert len(cart) == 0


@pytest.mark.django_db
def test_cart_views_add_and_detail(client):
    """
    Savat view'lariga GET/POST so'rovlar yuborib tekshirish.
    """
    category = Category.objects.create(name="Oziq-ovqat")
    product = Product.objects.create(category=category, name="Shokolad", price=25.00, stock=50)

    # 1. Bo'sh savat sahifasini ochish
    response = client.get('/cart/')
    assert response.status_code == 200
    assert "Savatchangiz hozircha bo‘sh" in response.content.decode('utf-8')

    # 2. Mahsulotni savatga qo'shish
    add_response = client.get(f'/cart/add/{product.id}/', follow=True)
    assert add_response.status_code == 200
    content = add_response.content.decode('utf-8')
    assert "Shokolad" in content
    assert "25" in content
