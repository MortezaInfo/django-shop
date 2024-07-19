from django.shortcuts import redirect
from django.contrib import messages

LOGIN_EXEMPT_URL = [
    '/order/cart/',
    '/order/create/',
    'detail/<int:order_id>/',
    'cart/add-cart/<int:product_id>/',
    'cart/remove/<int:product_id>/',
    'apply/<int:order_id>/',
]

class OrderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user.is_authenticated and request.path in LOGIN_EXEMPT_URL:
            messages.error(request, 'you should login first', 'danger')
            return redirect('accounts:user_login')

        response = self.get_response(request)
        
        
        return response

""" 
1. add middelware settings
2. create class 
3. use that

 """