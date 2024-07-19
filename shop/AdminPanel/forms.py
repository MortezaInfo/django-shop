from django import forms
from django.core.exceptions import ValidationError
from home.models import Products, ProductFeatures, ProductImageis
from order.models import Coupon

class AdminCreationProductFrom(forms.ModelForm):
    
    class Meta:
        model = Products
        fields = '__all__'



class AdminAddImageNoneProductForm(forms.ModelForm):
    
    class Meta:
        model = ProductImageis
        fields = '__all__'

class AdminAddImageKnowProductForm(forms.ModelForm):
    
    class Meta:
        model = ProductImageis
        fields = ('images',)

        
class AdminCreationFeatureFrom(forms.ModelForm):
    
    class Meta:
        model = ProductFeatures
        fields = '__all__'


class AdminCreationCouponFrom(forms.ModelForm):
    
    class Meta:
        model = Coupon
        fields = '__all__'

        help_texts = {
            "valid_form": ("example: 2024-11-03 22:01:32"),
            "valid_to": ("example: 2028-11-23 00:21:25"),
    }


