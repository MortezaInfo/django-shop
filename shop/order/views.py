from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .cart import Cart
from home.models import Products
from .forms import  CouponApplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Order, OrderItem, Coupon
from django.contrib import messages
import datetime
from django.http import HttpResponse
import requests
import json

class CartView(View):

    def get(self, request):
        cart = Cart(request)
        print(request.session)
        return render(request, 'order/cart.html', {'cart':cart, 'form':CouponApplyForm})
    
    
class CartAddView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        product = get_object_or_404(Products, id = product_id)
        cart.add(product, 1)
        return redirect('order:cart')

class CartRemoveView(View):
    def get(self, request, product_id):
        cart = Cart(request)
        cart.remove(product_id)
        return redirect('order:cart')
    
class OrderDetailView(LoginRequiredMixin,View):
    form_class = CouponApplyForm
    def get(self, request, order_id):
        order = get_object_or_404(Order, id = order_id)
        return render(request, 'order/order.html', {"order":order, 'form':self.form_class})
    

class OrderCreateView(LoginRequiredMixin, View):
    def get(self, request):
        cart = Cart(request)
        if not len(cart):
            messages.error(request, 'لطفا محصولی به سبد خرید خود اضافه کنید', 'danger')
            return redirect('order:cart')

        order = Order.objects.create(user = request.user, discount = cart.cart.get('discount', 0))
        for item in cart:
            OrderItem.objects.create(order= order, product = item['product'], price = item['price'], quantity = item['quantity'])
        
        cart.clear()
        return redirect('order:order_detail', order.id)


class AddQuantityItemView(View):
    def get(self, request, item_id):
        cart = Cart(request)
        cart.add_product_quantity(item_id)
        return redirect('order:cart')


class DelQuantityItemView(View):
    def get(self, request, item_id):
        cart = Cart(request)
        cart.del_product_quantity(item_id)
        return redirect('order:cart')




MERCHANT = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'

class OrderPayView(LoginRequiredMixin, View):
	def get(self, request, order_id):
		order = Order.objects.get(id=order_id)
		request.session['order_pay'] = {
			'order_id': order.id,
		}
		req_data = {
			"merchant_id": MERCHANT,
			"amount": order.get_total_price(),
			"callback_url": CallbackURL,
			"description": description,
			"metadata": {"mobile": request.user.phone_number, "email": request.user.email}
		}
		req_header = {"accept": "application/json",
					  "content-type": "application/json'"}
		req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
			req_data), headers=req_header)
		authority = req.json()['data']['authority']
		if len(req.json()['errors']) == 0:
			return redirect(ZP_API_STARTPAY.format(authority=authority))
		else:
			e_code = req.json()['errors']['code']
			e_message = req.json()['errors']['message']
			return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


class OrderVerifyView(LoginRequiredMixin, View):
	def get(self, request):
		order_id = request.session['order_pay']['order_id']
		order = Order.objects.get(id=int(order_id))
		t_status = request.GET.get('Status')
		t_authority = request.GET['Authority']
		if request.GET.get('Status') == 'OK':
			req_header = {"accept": "application/json",
						  "content-type": "application/json'"}
			req_data = {
				"merchant_id": MERCHANT,
				"amount": order.get_total_price(),
				"authority": t_authority
			}
			req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
			if len(req.json()['errors']) == 0:
				t_status = req.json()['data']['code']
				if t_status == 100:
					order.paid = True
					order.save()
					return HttpResponse('Transaction success.\nRefID: ' + str(
						req.json()['data']['ref_id']
					))
				elif t_status == 101:
					return HttpResponse('Transaction submitted : ' + str(
						req.json()['data']['message']
					))
				else:
					return HttpResponse('Transaction failed.\nStatus: ' + str(
						req.json()['data']['message']
					))
			else:
				e_code = req.json()['errors']['code']
				e_message = req.json()['errors']['message']
				return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
		else:
			return HttpResponse('Transaction failed or canceled by user')





class CouponApplyView(LoginRequiredMixin, View):
	form_class = CouponApplyForm

	def post(self, request, order_id):
		now = datetime.datetime.now()
		form = self.form_class(request.POST)
		if form.is_valid():
			code = form.cleaned_data['code']
			try:
				coupon = Coupon.objects.get(code__exact=code, valid_form__lte=now, valid_to__gte=now, active=True)
			except Coupon.DoesNotExist:
				messages.error(request, 'this coupon does not exists', 'danger')
				return redirect('order:order_detail', order_id)
			order = Order.objects.get(id=order_id)
			order.discount = coupon.discount
			order.save()
		return redirect('order:order_detail', order_id)
	

class ListCartView(LoginRequiredMixin, View):
	def get(self, request):
		orders = Order.objects.filter(user = request.user, paid = False)
		return render(request, 'order/pay_order.html', {'orders':orders})
	

class OrderRemoveView(LoginRequiredMixin, View):
	def get(self, reqeust, order_id):
		try:
			order = Order.objects.get(id = order_id)
		except Order.DoesNotExist:
			messages.error(reqeust, 'سبدی با این ایدی وجود ندارد')
			return redirect('order:list_cart')
		order.delete()
		return redirect('order:list_cart')