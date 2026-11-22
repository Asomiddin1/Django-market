from decimal import Decimal
from apps.products.models import Product


class Cart:
    """
    Session asosidagi savatcha (Cart).
    Foydalanuvchi tizimga kirgan yoki kirmaganligidan qat'i nazar ishlaydi.
    """
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Mahsulotni savatga qo'shish yoki uning sonini yangilash.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.price)
            }

        if override_quantity:
            self.cart[product_id]['quantity'] = max(1, int(quantity))
        else:
            self.cart[product_id]['quantity'] += int(quantity)

        # Mahsulot zaxirasidan oshib ketmasligi uchun tekshiruv (agar stock mavjud bo'lsa)
        if product.stock and self.cart[product_id]['quantity'] > product.stock:
            self.cart[product_id]['quantity'] = product.stock

        self.save()

    def decrement(self, product):
        """
        Mahsulot sonini 1 taga kamaytirish. Agar 0 bo'lsa, o'chirish.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] -= 1
            if self.cart[product_id]['quantity'] <= 0:
                self.remove(product)
            else:
                self.save()

    def remove(self, product):
        """
        Mahsulotni savatdan butunlay olib tashlash.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        """
        Savatdagi mahsulotlarni ma'lumotlar bazasidagi obyektlar bilan birlashtirib qaytarish.
        """
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            if 'product' in item:
                item['price'] = Decimal(item['price'])
                item['total_price'] = item['price'] * item['quantity']
                yield item

    def __len__(self):
        """
        Savatdagi jami mahsulotlar donasini hisoblash.
        """
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """
        Savatdagi barcha mahsulotlarning umumiy summasi.
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """
        Savatni butunlay tozalash.
        """
        if 'cart' in self.session:
            del self.session['cart']
            self.save()
