from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.HomeView.as_view(), name = 'home'),
    path('search/', views.HomeSearchView.as_view(), name='search'),
    path('search/<str:search>', views.HomeSearchView.as_view(), name='search'),
    path('question/', views.SearchRedirectView.as_view(), name='question'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name = 'category_detail'),
    path("products/<int:id>/", views.ProductDeatilView.as_view(), name = 'product_detail'),
    path('reply/<int:product_id>/<int:comment_id>/', views.ProductAddReplyView.as_view(), name = 'add_reply'),
    path('like/<int:product_id>/<int:number>', views.ProductLikeView.as_view(), name = 'product_like'),
    path('like/<int:product_id>/<int:comment_id>/<int:number>/', views.CommentLikeView.as_view(), name = 'comment_like'),

]