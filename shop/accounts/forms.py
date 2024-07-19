from django import forms
from .models import User, OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    pass1 = forms.CharField(label="password", widget=forms.PasswordInput)
    pass2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name", 'pass1', 'pass2')

    def clean_pass2(self):
        cd = self.cleaned_data
        if cd["pass1"] and cd["pass2"] and cd["pass1"] != cd["pss2"]:
            raise ValidationError("password dont match!")
        return cd["pass2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["pass1"])
        if commit:
            user.save()
        return user


class UserChangeFrom(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text='you can change password using <a href = "../password/">this form</a>'
    )

    class Meta:
        model = User
        fields = ("email", "phone_number", "full_name", "password", "last_login")


class UserRegistrationForm(forms.Form):
    email = forms.CharField()
    full_name = forms.CharField()
    phone = forms.CharField(max_length=11)
    password = forms.CharField()
    password1 = forms.CharField()

    # widgets={'email': forms.Textarea(attrs={ 'palceholder': 'write comment...'})}

    def clean_password1(self):
        cd = self.cleaned_data
        if cd["password1"] and cd["password"] and cd["password1"] != cd["password"]:
            raise ValidationError("password dont match!")
        return cd["password1"]

    def clean_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError("this email already exists")
        return email

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError("this phone number is already exists")
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone


class UserLoginForm(forms.Form):  # for login
    phone = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput)


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class PhoneNumberForm(forms.Form):
    phone = forms.CharField(max_length=11)


class NewPasswordForm(forms.Form):
    password = forms.CharField()
