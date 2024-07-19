from django.urls import path
from . import views


app_name = "admin_panel"
urlpatterns = [
    path('', views.DashbordView.as_view(), name = 'dashbord'),
    path('edit-product/<int:id>/', views.EditProductView.as_view(), name = 'edit_product'),
    path('add-product/', views.AddProductView.as_view(), name = 'add_product'),
    path('add-feature/', views.AddFeatureView.as_view(), name = 'add_feature'),
    path('features/', views.AllFeatureView.as_view(), name = 'features'),
    path('edit-feature/<int:fid>/', views.EditFeatureView.as_view(), name = 'edit_feature'),
    path('confirm-feature/<int:id>/', views.ConfirmFeatureView.as_view(), name = 'confirm_feature'),
    path('add-photo/', views.AddProductImageView.as_view(), name = 'add_photo'),
    path('add-photo/<int:id>/', views.AddProductImageView.as_view(), name = 'add_photo'),
    path('delete-photo/<int:id>/', views.DeleteImageView.as_view(), name = 'delete_photo'),
    path('confirm-product/<int:id>/', views.ConfirmProductView.as_view(), name = 'confirm_product'),
    path('product-comment', views.AllCommentProductView.as_view(), name = 'product_comment'),
    path('confirm-comment/<int:id>/', views.ConfirmCommentView.as_view(), name = 'confirm_comment'),
    path('add-otpcode/', views.AddCouponView.as_view(), name = 'add_coupon'),
    path('edit-otpcode/<int:id>', views.EditCouponView.as_view(), name = 'edit_coupon'),
    path('coupons/', views.AllCouponView.as_view(), name = 'coupons'),
]