from django.urls import path

from ecommerce.products.views.product import ProductDetailView, ProductListView

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(),
         name='products-list'),
    path('<slug:slug>/', ProductDetailView.as_view(),
         name='products-detail'),
]
