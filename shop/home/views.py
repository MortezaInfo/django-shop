from .forms import CommentCreateForm, CommentReplyForm, SearchHomeView, FilterProductForm
from django.shortcuts import render, redirect, get_object_or_404
from django.http.response import HttpResponse as HttpResponse
from django.contrib.postgres.search import TrigramSimilarity
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Products, Comment, Vote
from django.utils.decorators import method_decorator
from extentions.address_product import get_address
from extentions.filter import advanced_filter
from django.db.models.functions import Greatest
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from order.models import OrderItem
from datetime import datetime, timedelta
from django.contrib import messages
from django.http import HttpRequest
from .filters import ProductsFilter
from django.db.models import Q, F
from django.views import View
from typing import Any



class HomeView(View):
    search_form = SearchHomeView
    
    def get(self, request):
        time = datetime.now() - timedelta(weeks=1)
        new_products = Products.objects.filter(created__gte=time)
        return render(request, "home/home.html", {"products": new_products, 'search_form': self.search_form})



class CategoryDetailView(View):
    def setup(self, request, *args, **kwargs):
        self.category = Category.objects.get(slug=kwargs["slug"])
        self.product = self.category.products.filter(category=self.category, access = True)
        return super().setup(request, *args, **kwargs)

    def get(self, request, slug):
        get = f"""sort_by={request.GET.get('sort_by','')}&name={request.GET.get('name','')}&description={request.GET.get('description','')}&category_name={request.GET.get('category_name','')}&min_star={request.GET.get('min_star','')}&max_star={request.GET.get('max_star','')}&min_price={request.GET.get('min_price','')}&max_price={request.GET.get('max_price','')}"""
        product = advanced_filter(request, self.product)
        paginator = Paginator(product, 15)
        page = request.GET.get("page")
        product = paginator.get_page(page)
        address = get_address(self.category)

        return render(
            request,
            "home/products.html",
            {
                "products": product,
                "category": self.category,
                "address": address,
                'get':get
            },
        )



class ProductDeatilView(View):
    form_class = CommentCreateForm
    form_class_reply = CommentReplyForm

    def setup(self, request, *args: Any, **kwargs: Any) -> None:
        self.product = Products.objects.get(id=kwargs["id"])
        self.category = self.product.category.first()
        ip_address = request.user.ip_address
        if ip_address not in self.product.hits.all():
            self.product.hits.add(ip_address)
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, id):
        comments = self.product.comment.filter(is_reply=False).order_by('-created')
        featureis = self.product.pfeature.all()
        clean_features = dict()

        for feature in featureis:
            if clean_features.get(feature.name):
                clean_features[feature.name] = (f"{feature.value}  ,  {clean_features[feature.name]}")
            else:
                clean_features[feature.name] = feature.value

       
        return render(request, "home/detail.html",{
                "product": self.product,
                "features": clean_features,
                "comments": comments,
                'form': self.form_class,
                "reply_form": self.form_class_reply,
                'category':self.category,
            },
        )

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.content_object = self.product
            new_comment.save()
            messages.success(request, "your comment submitted successfully!", "success")
            return redirect(
                "home:product_detail",  self.product.id
            )



class ProductAddReplyView(LoginRequiredMixin, View):
    form_class = CommentReplyForm
    
    def post(self, request, product_id, comment_id):
        product = get_object_or_404(Products, id = product_id)
        comment = get_object_or_404(Comment, id = comment_id)
        form = self.form_class(request.POST)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.content_object = product
            new_form.reply = comment
            new_form.is_reply = True
            new_form.save()
            messages.success(request, 'you reply submitted successfully!', 'success')
        return redirect('home:product_detail', product.id )
    

class SearchRedirectView(View):
    def post(self, request):
        form = SearchHomeView(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search']
            return redirect('home:search', search_query)
        return redirect('home:home')


class HomeSearchView(View):
    def get(self, request, search = None):
        get = f"""sort_by={request.GET.get('sort_by','')}&name={request.GET.get('name','')}&description={request.GET.get('description','')}&category_name={request.GET.get('category_name','')}&min_star={request.GET.get('min_star','')}&max_star={request.GET.get('max_star','')}&min_price={request.GET.get('min_price','')}&max_price={request.GET.get('max_price','')}"""
        if search:
            product = Products.objects.annotate(
                similarity = Greatest(
                    TrigramSimilarity('name', search),
                    TrigramSimilarity('description', search),
                )
            
            ).filter(similarity__gt = 0.1).order_by('-similarity')
        else:
            product = Products.objects.all()  
        convert = {
            '1':'جدید ترین محصولات',
            '2':'محبوب ترین محصولات',
            '4':"پر تخفیف ترین محصولات",
            '5':"پرفروش ترین محصولات",
        }
       
        search = search or convert[request.GET.get('sort_by')]
        products = advanced_filter(request, product)
        count = products.count()
        
        return render(request, 'home/search.html', {'search': search, 'count_products':count,'products':products, 'get':get})
    


class ProductLikeView(LoginRequiredMixin, View):
    def get(self, request, product_id, number):
        product = get_object_or_404(Products, id = product_id)
        model = ContentType.objects.get(model = 'products')
        obj = model.get_object_for_this_type(id = product.id)
        try:
            vote = Vote.objects.get( object_id = obj.id, user = request.user)
            if vote.like and not number:
                vote.like = False
                vote.save()
            elif not vote.like and number:
                vote.like = True
                vote.save()
        except:
            Vote.objects.create(content_object = product, user = request.user, like = bool(number))
            messages.success(request, 'بازخورد شما ثبت شد', 'success')
        return redirect('home:product_detail', product.id)
    


class CommentLikeView(LoginRequiredMixin, View):


    def get(self, request, product_id, comment_id, number):
        product = get_object_or_404(Products, id = product_id)
        comment = get_object_or_404(Comment, id = comment_id)
        model = ContentType.objects.get(model = 'comment')
        obj = model.get_object_for_this_type(id = comment.id)
        try:
            vote = Vote.objects.get( object_id = obj.id, user = request.user)
            if vote.like and not number:
                vote.like = False
                vote.save()
            elif number:
                vote.like = True
                vote.save()
        except:
            Vote.objects.create(content_object = comment, user = request.user, like = bool(number))
            messages.success(request, 'بازخورد شما ثبت شد', 'success')
        return redirect('home:product_detail', product.id)



            
