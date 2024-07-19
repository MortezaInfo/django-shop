from django.urls import path
from . import views

app_name = 'order'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name = 'cart'),
    path('create/', views.OrderCreateView.as_view(), name = 'order_create'),
    path('detail/<int:order_id>/', views.OrderDetailView.as_view(), name = 'order_detail'),
    path('cart/add-cart/<int:product_id>/', views.CartAddView.as_view(), name = 'cart_add' ),
    path('cart/remove/<int:product_id>/', views.CartRemoveView.as_view(), name = 'cart_remove'),
	path('apply/<int:order_id>/', views.CouponApplyView.as_view(), name='apply_coupon'),
    path('pay/<int:order_id>/', views.OrderPayView.as_view(), name='order_pay'),
	path('verify/', views.OrderVerifyView.as_view(), name='order_verify'),
    path('add-quantity/<int:item_id>/', views.AddQuantityItemView.as_view(), name = 'add_quantity'),
    path('del-quantity/<int:item_id>/', views.DelQuantityItemView.as_view(), name = 'del_quantity'),
    path('list-cart/', views.ListCartView.as_view(), name = 'list_cart'),
    path('list-cart/remove/<int:order_id>', views.OrderRemoveView.as_view(), name = 'order_remove'),
]