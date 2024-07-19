from home.models import Products


CART_SESSION_ID = 'CAR2'
class Cart:
	def __init__(self, request):
		self.session = request.session
		cart = self.session.get(CART_SESSION_ID)
		if not cart:
			cart = self.session[CART_SESSION_ID] = {}
		self.cart = cart
		
	def __iter__(self):
		product_ids = self.cart.keys()
		products = Products.objects.filter(id__in=product_ids)
		cart = self.cart.copy()
		for product in products:
			cart[str(product.id)]['product'] = product

		for item in cart.values():
			item['total_price'] = int(item['price']) * item['quantity']
			yield item

	def __len__(self):
		return sum(item['quantity'] for item in self.cart.values())

	def add(self, product, quantity):
		product_id = str(product.id)
		if product_id not in self.cart:
			self.cart[product_id] = {'quantity':1, 'price':str(product.price)}
		self.cart[product_id]['quantity'] += quantity
		self.save()

	def add_product_quantity(self, product_id):
		product_id = str(product_id)
		self.cart[product_id]['quantity'] += 1
		self.save()

	def del_product_quantity(self, product_id):
		product_id = str(product_id)
		self.cart[product_id]['quantity'] -= 1
		self.save()

	def remove(self, product):
		product_id = str(product)
		if product_id in self.cart:
			del self.cart[product_id]
			self.save()

	def save(self):
		self.session.modified = True

		
	
	def get_total_price(self):
		total =  sum(int(item['price']) * item['quantity'] for item in self.cart.values())
		return total
		
	def clear(self):
		del self.session[CART_SESSION_ID]
		self.save()