from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.categories.models import Category
from apps.products.models import Product


class ProductDetailAndWishlistTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='alimardon',
            email='alimardon@example.com',
            password='Password123!'
        )
        self.category = Category.objects.create(name='Smartfonlar')
        self.product = Product.objects.create(
            category=self.category,
            name='iPhone 15 Pro',
            description='A17 Pro chip va titan korpus',
            price=1199.00,
            stock=10
        )
        self.related_product = Product.objects.create(
            category=self.category,
            name='iPhone 15',
            description='A16 Bionic chip',
            price=799.00,
            stock=5
        )

    def test_direct_many_to_many_relationship(self):
        # 1. Productga foydalanuvchini sevimlilarga qo'shish
        self.product.favorites.add(self.user)
        self.assertIn(self.user, self.product.favorites.all())
        self.assertIn(self.product, self.user.favorite_products.all())
        self.assertEqual(self.product.favorites.count(), 1)

        # 2. Sevimlilardan olib tashlash
        self.product.favorites.remove(self.user)
        self.assertNotIn(self.user, self.product.favorites.all())
        self.assertNotIn(self.product, self.user.favorite_products.all())
        self.assertEqual(self.product.favorites.count(), 0)

    def test_toggle_wishlist_requires_login(self):
        response = self.client.get(
            reverse('products:toggle_wishlist', kwargs={'product_id': self.product.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('users:login'), response.url)

    def test_toggle_wishlist_view_add_and_remove(self):
        self.client.login(username='alimardon', password='Password123!')

        # Qo'shish (Add)
        toggle_url = reverse('products:toggle_wishlist', kwargs={'product_id': self.product.id})
        resp1 = self.client.get(toggle_url, follow=True)
        self.assertEqual(resp1.status_code, 200)
        self.assertTrue(self.product.favorites.filter(id=self.user.id).exists())

        # O'chirish (Remove)
        resp2 = self.client.get(toggle_url, follow=True)
        self.assertEqual(resp2.status_code, 200)
        self.assertFalse(self.product.favorites.filter(id=self.user.id).exists())

    def test_wishlist_page(self):
        self.client.login(username='alimardon', password='Password123!')
        self.product.favorites.add(self.user)

        response = self.client.get(reverse('products:wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15 Pro')
        self.assertEqual(response.context['product_count'], 1)

    def test_product_detail_view_success(self):
        detail_url = reverse('products:detail', kwargs={'pk': self.product.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'iPhone 15 Pro')
        self.assertContains(response, '1199')
        self.assertContains(response, 'A17 Pro chip va titan korpus')
        self.assertEqual(response.context['product'], self.product)
        # O'xshash mahsulotlar mavjudligini tekshirish
        self.assertIn(self.related_product, response.context['related_products'])

    def test_product_detail_view_404(self):
        detail_url = reverse('products:detail', kwargs={'pk': 999999})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 404)

    def test_product_detail_is_favorite_flag(self):
        detail_url = reverse('products:detail', kwargs={'pk': self.product.pk})

        # Kirilmagan holatda
        r1 = self.client.get(detail_url)
        self.assertFalse(r1.context['is_favorite'])

        # Kirgan va mahsulot sevimli qilingan holatda
        self.client.login(username='alimardon', password='Password123!')
        self.product.favorites.add(self.user)
        r2 = self.client.get(detail_url)
        self.assertTrue(r2.context['is_favorite'])
