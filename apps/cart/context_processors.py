from .cart import Cart


def cart(request):
    """
    Har qanday shablonda (template) `{{ cart }}` orqali savatchaga murojaat qilish imkonini beradi.
    """
    return {'cart': Cart(request)}
