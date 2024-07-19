from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path('register/', views.UserRegisterView.as_view(), name = 'user_register'),
    path('verify_register/', views.UserRegisterVerifyCodeView.as_view(), name = 'verify_code'),
    path('check_user/', views.CheckPhoneNumberView.as_view(), name = 'check_user_phone'),
    path('password_verify_register/', views.UserRegisterForgetVerifyCodeView.as_view(), name = 'register_verify_code'),
    path('new_password/', views.UserCreationNewPasswordView.as_view(), name = 'new_password'),
    path('login/', views.UserLoginPasswordView.as_view(), name = 'user_login'),
    path('logout/', views.UserLogoutView.as_view(), name = 'user_logout'),
    path('reset/', views.UserPasswordResetView.as_view(), name='reset_password'),
	path('reset/done/', views.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
	path('confirm/<uidb64>/<token>/', views.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
	path('confirm/complete', views.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
