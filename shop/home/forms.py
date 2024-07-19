from django import forms
from .models import Comment


class SearchHomeView(forms.Form):
    search = forms.CharField(max_length = 255)


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets  = {"body": forms.Textarea(attrs={"palceholder": "write comment..."})}


class CommentReplyForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)


class FilterProductForm(forms.Form):
    chioce = [('1', 'جدید ترین محصولات'), ('2', 'محبوب ترین محصولات'), ('4','پر تخفیف ترین محصولات' ), ('5', "پر فروش ترین محصولات")]
    sort_by = forms.ChoiceField(choices = chioce, required=False, label='مرتب سازی بر اساس')
    name = forms.CharField(max_length=256, required=False, help_text='نام محصول', label='نام')
    description = forms.CharField(max_length=512, required=False, help_text='توضیحات محصول', label='توضیحات')
    category_name = forms.CharField(max_length=256, required=False, help_text='نام دسته بندی', label='دسته بندی')
    min_star = forms.IntegerField(max_value=5, min_value=0, required=False, help_text='ستاره محصول', label='امتیاز')
    max_star = forms.IntegerField(max_value=5, min_value=0, required=False, help_text='ستاره محصول', label='امتیاز')
    min_price = forms.IntegerField( min_value=0, required=False, help_text='قیمت محصول', label='قیمت')
    max_price = forms.IntegerField( min_value=0, required=False, help_text='قیمت محصول', label='قیمت')