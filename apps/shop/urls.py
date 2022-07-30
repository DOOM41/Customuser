from django.urls import path
from apps.shop import views

urlpatterns = [
    path('', views.ProductsView.as_view(), name='products'),
    path('product/<slug:pk>/', views.ProductDetail.as_view(), name='product'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('add_to_basket/', views.add_to_basket, name="add_to_basket"),
    path('buy_from_basket/', views.buy_from_basket, name="buy_from_basket"),
    path('in_basket/', views.ProductInBasketList.as_view(), name="in_basket"),
    path('add_comment/', views.add_comment, name="add_comment"),
]
