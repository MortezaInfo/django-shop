from typing import Any
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from home.models import Products, ProductImageis, Comment, ProductFeatures
from .forms import AdminCreationProductFrom, AdminCreationFeatureFrom, AdminAddImageNoneProductForm, AdminAddImageKnowProductForm, AdminCreationCouponFrom
from django.contrib import messages
from accounts.models import User
from datetime import datetime
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.db.models import F, Q
from order.models import Coupon

class DashbordView(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('accounts:user_login')
        elif not (request.user.is_staff or request.user.is_shoper):
            return redirect("home:home")
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):

        if request.user.is_staff:
            self.products = Products.admin_objects.all()
        elif request.user.is_shoper:
            self.products = request.user.userproducts.all()

        return render(request, "AdminPanel/product.html", {"products": self.products, 'user':request.user.full_name})


class EditProductView(View):
    form_class = AdminCreationProductFrom

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.product = Products.admin_objects.get(id = kwargs['id'])
        self.pricture =  self.product.productimage.all()
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, id):
        form = self.form_class(instance=self.product)
        comments = self.product.comment.all()
        return render(request, 'AdminPanel/edit_product.html', {'form': form, 'images': self.pricture, 'name': 'ادیت محصول', 'comments':comments})
    
    def post(self, request, id):
        form = self.form_class(request.POST,request.FILES, instance = self.product)
        if form.is_valid():
            form.save()
            messages.success(request, 'product edited successfully!', 'success')
            return redirect('admin_panel:dashbord')


class DeleteImageView(View):
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.img = ProductImageis.objects.get(id = kwargs['id'])
        self.product = self.img.product
        return super().setup(request, *args, **kwargs)
    def get(self, request, id):
        self.img.delete()
        messages.success(request, 'imgae deleted successfully', 'success')
        return redirect('admin_panel:edit_product', self.product.id)


class AddProductView(View):
    from_class = AdminCreationProductFrom

    def get(self, request):
        form = self.from_class
        return render(request, "AdminPanel/add_product.html", {"form": form, "name": 'افزودن محصول'})

    def post(self, request):
        form = self.from_class(request.POST, request.FILES)
        if form.is_valid():
            for f in form.cleaned_data['pfeature']:
                if not f.access :
                    messages.error(request, 'some feature not access!', 'danger')
                    return redirect('admin_panel:add_product')
            if request.user.is_staff:
                form = form.save(commit=False)
            else:
                form = form.save(commit=False)
                form.user = request.user
                form.star = 0
            form.image = request.FILES['image']
            form.save()
            messages.success(request, 'your product add to list', 'success')
            return redirect("admin_panel:dashbord")
        messages.info(request, 'your product add to list', 'info')
        return redirect("admin_panel:add_product")


class AddFeatureView(View):
    from_class = AdminCreationFeatureFrom

    def get(self, request):
        form = self.from_class
        return render(request, "AdminPanel/add_feature.html", {"form": form, 'name': 'افزودن افزونه'})

    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect("admin_panel:features")


class AllFeatureView(View):
    def get(self, request):
        features = ProductFeatures.admin_objects.all()
        return render(request, 'AdminPanel/feature.html', {'features':features})


class EditFeatureView(View):
    form_class = AdminCreationFeatureFrom

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.feature = ProductFeatures.objects.get(id = kwargs['fid'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, fid):
        form = self.form_class(instance=self.feature)
        return render(request, 'AdminPanel/edit_feature.html', {'form': form, 'name': 'ادیت فیچر'})
    
    def post(self, request, fid):
        form = self.form_class(request.POST, instance = self.feature)
        if form.is_valid():
            form.save()
            messages.success(request, 'feature edited successfully!', 'success')
            return redirect('admin_panel:features')        


class ConfirmFeatureView(View):
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.feature = ProductFeatures.objects.get(id = kwargs['id'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            return redirect('admin_panel:dashboard')
        return super().dispatch(request, *args, **kwargs)


    def get(self, request, *args, **kwargs):
        if self.feature.access:
            self.feature.access = False
        else:
            self.feature.access = True
        self.feature.save()
        messages.success(request, 'admin this feature publiced')
        return redirect('admin_panel:features')


class AddProductImageView(View):
    
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.product_id = kwargs.get('id') if kwargs.get('id') else None
        if self.product_id:
            self.form_class = AdminAddImageKnowProductForm
        else:
            self.form_class = AdminAddImageNoneProductForm
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class
        select_product = True if self.product_id else False
        return render(request, "AdminPanel/add_photo.html", {"form": form, 'name': 'افزودن عکس', 'select_product': select_product})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            new_pic = form.save(commit=False)
            if self.product_id:
                product = Products.admin_objects.get(id = self.product_id)

                new_pic.product = product
            form.images = request.FILES['images']
            new_pic.save()

            messages.success(request, 'your picture submitted successfully!', 'success')
            return redirect("admin_panel:dashbord")
        if self.product_id:
            return redirect('admin_panel:add_photo', self.product_id)
        return redirect('admin_panel:add_photo')


class ConfirmProductView(View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            return redirect('admin_panel:dashbord')
        return super().dispatch(request, *args, **kwargs)
    
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.product = Products.admin_objects.get(id = kwargs['id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if self.product.access:
            self.product.access = False
        else:
            self.product.access = True
        self.product.save()
        messages.success(request, 'admin this product publiced')
        return redirect('admin_panel:dashbord')
    

class AllCommentProductView(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            return redirect('admin_panel:dashbord')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        comment = Comment.admin_objects.filter(Q(access = False) | Q(created__gte = F('created') - timedelta(days = 1))).order_by('access')
        return render(request, 'AdminPanel/access_comment.html', {'comments':comment})


class ConfirmCommentView(LoginRequiredMixin, View):
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_staff:
            return redirect('admin_panel:dashbord')
        return super().dispatch(request, *args, **kwargs)
    
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.comment = Comment.admin_objects.get(id = kwargs['id'])
        
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        if self.comment.access:
            self.comment.access = False
        else:
            self.comment.access = True
        self.comment.save()
        return redirect('admin_panel:product_comment')
    

class AddCouponView(View):
    from_class = AdminCreationCouponFrom

    def get(self, request):
        form = self.from_class
        return render(request, "AdminPanel/add_coupon.html", {"form": form, 'name': 'افزودن کد تخفیف'})

    def post(self, request):
        form = self.from_class(request.POST)
        if form.is_valid():
            if not request.user.is_staff:
                form = form.save(commit=False)
                form.user = request.user
            form.save()
            return redirect("admin_panel:coupons")
        return redirect('admin_panel:add_coupon')


class AllCouponView(View):
    def get(self, request):
        coupons = Coupon.objects.all()
        return render(request, 'AdminPanel/coupons.html', {'coupons':coupons})


class EditCouponView(View):

    form_class = AdminCreationCouponFrom

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.coupon = Coupon.objects.get(id = kwargs['id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, id):
        form = self.form_class(instance=self.coupon)
        return render(request, 'AdminPanel/edit_coupon.html', {'form': form, 'name': 'ادیت کد تخفیف'})
    
    def post(self, request, id):
        form = self.form_class(request.POST, instance = self.coupon)
        if form.is_valid():
            form.save()
            messages.success(request, 'feature edited successfully!', 'success')
            return redirect('admin_panel:coupons')      
        
    
  