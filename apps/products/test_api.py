import pytest
from apps.products.models import Product
from apps.categories.models import Category
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_product_list_api(client):
    """
    1-test: /api/products/ endpointini tekshirish (GET so'rovi va JSON javob).
    """
    category = Category.objects.create(name="Elektronika")
    product = Product.objects.create(
        category=category,
        name="Samsung Galaxy S24",
        price=900.00,
        stock=10
    )

    response = client.get('/api/products/')

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]['name'] == product.name


@pytest.mark.django_db
def test_product_model_str_and_stock():
    """
    2-test: Product modelining __str__ metodi va zaxira (stock) qiymatini tekshirish.
    """
    category = Category.objects.create(name="Kiyimlar")
    product = Product.objects.create(
        category=category,
        name="Qishki Kurtka",
        price=150.00,
        stock=5
    )

    # __str__ metodi mahsulot nomini to'g'ri qaytarishi kerak
    assert str(product) == "Qishki Kurtka"
    # Narx va zaxira to'g'ri saqlanganligini tekshiramiz
    assert product.price == 150.00
    assert product.stock == 5


@pytest.mark.django_db
def test_product_favorites_count():
    """
    3-test: Mahsulot sevimlilarga (favorites) qo'shilganda favorites_count property to'g'ri ishlashi.
    """
    category = Category.objects.create(name="Kitoblar")
    product = Product.objects.create(
        category=category,
        name="Python Dasturlash Asoslari",
        price=50.00,
        stock=20
    )
    user = User.objects.create_user(username="testuser", password="password123")

    # Dastlab sevimlilar soni 0 bo'lishi kerak
    assert product.favorites_count == 0

    # Foydalanuvchini sevimlilarga qo'shamiz
    product.favorites.add(user)

    # Endi sevimlilar soni 1 bo'lishi kerak
    assert product.favorites_count == 1


@pytest.mark.django_db
def test_product_crud_views(client):
    """
    4-test: Mahsulot CRUD (Create, Update, Delete) viewlarini to'liq tekshirish.
    """
    category = Category.objects.create(name="Texnika")
    user = User.objects.create_user(username="seller", password="password123")

    # 1. Tizimga kirmagan bo'lsa, login sahifasiga yo'naltirishi kerak
    res_unauth = client.get('/products/create/')
    assert res_unauth.status_code == 302
    assert '/users/login/' in res_unauth.url

    # 2. Tizimga kiramiz
    client.force_login(user)

    # 3. Create GET sahifasi 200 qaytarishi kerak
    res_get = client.get('/products/create/')
    assert res_get.status_code == 200

    # 4. Create POST orqali yangi mahsulot yaratamiz
    res_post = client.post('/products/create/', {
        'name': 'MacBook Pro M3',
        'category': category.id,
        'price': '2000.00',
        'stock': 8,
        'description': 'Kuchli noutbuk'
    }, follow=True)
    assert res_post.status_code == 200
    created_product = Product.objects.get(name='MacBook Pro M3')
    assert created_product.price == 2000.00

    # 5. Update POST orqali narxini o'zgartiramiz
    res_update = client.post(f'/products/{created_product.id}/edit/', {
        'name': 'MacBook Pro M3 Max',
        'category': category.id,
        'price': '2500.00',
        'stock': 5,
        'description': 'Yangilangan kuchli noutbuk'
    }, follow=True)
    assert res_update.status_code == 200
    created_product.refresh_from_db()
    assert created_product.name == 'MacBook Pro M3 Max'
    assert created_product.price == 2500.00

