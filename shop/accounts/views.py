from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from .models import OtpCode, User
from django.views import View
from .forms import (
    UserRegistrationForm,
    VerifyCodeForm,
    UserLoginForm,
    PhoneNumberForm,
    NewPasswordForm,
)
from extentions.utils import send_otp_code
from django.contrib import messages
from random import randint
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.db.models import Q

class UserPasswordResetView(auth_views.PasswordResetView):
	template_name = 'accounts/password_reset_form.html'
	success_url = reverse_lazy('accounts:password_reset_done')
	email_template_name = 'accounts/password_reset_email.html'


class UserPasswordResetDoneView(auth_views.PasswordResetDoneView):
	template_name = 'accounts/password_reset_done.html'


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
	template_name = 'accounts/password_reset_confirm.html'
	success_url = reverse_lazy('accounts:password_reset_complete')


class UserPasswordResetCompleteView(auth_views.PasswordResetCompleteView):
	template_name = 'accounts/password_reset_complete.html'




class UserRegisterView(View):
    form_class = UserRegistrationForm
    templates_name = "accounts/register.html"

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            messages.error(request,'شما در حال حاضر در سایت ثبت نام کرده اید لطفا به منو رفته سپس خارج شوید' ,'danger')
            return redirect('home:user_register')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.templates_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
                
            random_code = randint(1000, 9999)
            print(random_code)
            send_otp_code(cd["phone"], random_code)
            OtpCode.objects.create(phone_number=cd["phone"], code=random_code)
            request.session["user_registration_info"] = {
                "phone_number": cd["phone"],
                "email": cd["email"],
                "full_name": cd["full_name"],
                "password": cd["password"],
            }
            messages.success(request, "برای شما کد ارسال شد", "success")
            return redirect("accounts:verify_code")
        
        return redirect('accounts:user_register')

class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            messages.error(request,'شما در حال حاضر در سایت ثبت نام کرده اید لطفا به منو رفته سپس خارج شوید' ,'danger')
            return redirect('home:user_register')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class
        return render(request, "accounts/verify.html", {"form": form})

    def post(self, request):
        user_session = request.session.get("user_registration_info")
        if not user_session:
            messages.error(request, 'اطلاعات شما در دسترس نیست لطفا دوباره امتحان کنید', 'danger')
            return redirect('accounts:user_register')
        try:
            code_instance = OtpCode.objects.get(phone_number=user_session["phone_number"] )
        except OtpCode.DoesNotExist:
            messages.error(request, 'لطفا چند ثانیه دیگر امتحان کنید', 'danger')
            return redirect('accounts:user_register')
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["code"] == code_instance.code:
                User.objects.create_user( 
                    user_session["phone_number"],
                    user_session["email"],
                    user_session["full_name"],
                    user_session["password"],
                )

                code_instance.delete()
                messages.success(request, "با موفقیت ثبت نام کردید", "success")
                return redirect("home:home")
            else:
                messages.error(request, "کد وارد شده اشتباه است", "danger")
                return redirect("accounts:verify_code")
        return redirect("home:user_login")


class UserLogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "you logged out successfully", "info")
        return redirect("home:home")


class UserLoginPasswordView(View):
    form_class = UserLoginForm
    templates_name = "accounts/login.html"
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)
    
    
    def get(self, request):
        form = self.form_class
        return render(request, self.templates_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, phone_number=cd["phone"], password=cd["password"]
            )
            if user is not None:
                login(request, user)
                messages.success(request, "u loggined successfully", "info")
                if self.next:
                    return redirect(self.next)
                return redirect("home:home")
            messages.error(request, "phone or password is worng", "danger")
        return render(request, self.templates_name, {"form": form})


class CheckPhoneNumberView(View):
    form_class = PhoneNumberForm

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/check_phone_number.html", {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.filter(phone_number=cd["phone"]).first()
            if user:
                random_code = randint(1000, 9999)
                print(random_code)
                send_otp_code(cd["phone"], random_code)
                OtpCode.objects.create(phone_number=cd["phone"], code=random_code)
                request.session["user_forget_password"] = {
                    "phone_number": cd['phone'],
                    "email":user.email,
                    'full_name': user.full_name,
                    'password': user.password
                }
                messages.success(request, "we sent u a code", "success")
                return redirect("accounts:register_verify_code")
            else:
                messages.error(
                    request,
                    "شما در سایت ثبت نام نکرده اید لطفا از طریق <a href = \"{% url 'accounts:user_register' %}\"> این لینک </a> در سایت ثبت نام کنید",
                    "danger",
                )
                return redirect("accounts:user_register")
        return redirect("accounts:check_user_phone")


class UserRegisterForgetVerifyCodeView(View):
    form_class = VerifyCodeForm

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if request.user.is_authenticated:
            messages.error(request,'شما در حال حاضر در سایت ثبت نام کرده اید لطفا به منو رفته سپس خارج شوید' ,'danger')
            return redirect('home:user_register')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, "accounts/verify.html", {"form": form})

    def post(self, request):
        user_session = request.session["user_forget_password"]
        code_instance = OtpCode.objects.get(phone_number=user_session["phone_number"])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd["code"] == code_instance.code:
                messages.success(request, "کد وارد شده درسته", "success")
                return redirect("accounts:new_password")
            else:
                messages.error(request, "کد وارد شده نادرسته", "danger")
                return redirect("accounts:register_verify_code")
        return redirect("home:home")


class UserCreationNewPasswordView(View):
    form_class = NewPasswordForm

    def get(self, request):
        form = self.form_class()
        return render(request, "accounts/new_password.html", {"form": form})

    def post(self, request):
        user_session = request.session.get("user_forget_password")
        if not user_session:
            return redirect('accounts:check_user_phone')
        code_instance = OtpCode.objects.get(phone_number=user_session["phone_number"])
        form = self.form_class(request.POST)
        if form.is_valid():
            if len(form.cleaned_data['password']) < 8:
                messages.success(request, "طول پسورد باید حداقل 9 کارکتر باشد", "success")
                return redirect("accounts:new_password")
            user = User.objects.get(phone_number = user_session["phone_number"])
            login(request, user)
            user.set_password(form.cleaned_data['password']) 
            user.save()
            code_instance.delete()
            messages.success(request, "پسورد شما با موفقیت تغییر یافت", "success")
            return redirect("home:home")
        return redirect("accounts:new_password")


