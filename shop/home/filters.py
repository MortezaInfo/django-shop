import django_filters
from .models import Products

class ProductsFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()
    class Meta:
        model = Products
        fields = {
            'category__name':['icontains',],
            'name':['icontains',],
            'slug':['icontains',],
            'description':['icontains',],
            'star':['icontains',],
        }