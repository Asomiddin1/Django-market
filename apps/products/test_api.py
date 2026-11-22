import pytest
from apps.products.models import Product
from apps.categories.models import Category


@pytest.mark.django_db
def test_product_list_api(client):
    """
    Yangi yaratilgan /api/products/ endpointini tekshirish uchun test.
    """
    # 1. Test uchun kategoriya va mahsulot yaratamiz
    category = Category.objects.create(name="Elektronika")
    product = Product.objects.create(
        category=category,
        name="Samsung Galaxy S24",
        price=900.00,
        stock=10
    )

    # 2. API manziliga GET so'rov yuboramiz
    response = client.get('/api/products/')

    # 3. Natijalarni assert orqali tekshiramiz
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]['name'] == product.name
