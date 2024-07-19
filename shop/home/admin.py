from django.contrib import admin
from .models import Category, Products, ProductFeatures, ProductImageis, Comment , Brands

admin.site.register(Comment)
admin.site.register(Brands)

@admin.register(ProductImageis)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('parent',)
    raw_id_fields = ('product',)

    def parent(self, obj):
        return obj.product
    
@admin.register(ProductFeatures)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')

    
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_sub", "sub_categories", 'parent_categories')
    raw_id_fields = ("sub_category",)

    def sub_categories(self, obj):
        return ", ".join([cat.name for cat in obj.scategory.all()])

    def parent_categories(self, obj):
        cat = obj.sub_category
        try:
            if cat.sub_category:
                return f'{cat.sub_category} > {cat}'
            return cat
        except:
            return cat
        


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    raw_id_fields = ('user',"category", "pfeature")
    list_display = ("name",) 


