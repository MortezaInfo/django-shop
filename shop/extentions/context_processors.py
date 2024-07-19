
from home.models import Category
from order.cart import Cart

def categories(request):
    return {
        'categories': Category.objects.all(),
        'cart': Cart(request)
    }