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
