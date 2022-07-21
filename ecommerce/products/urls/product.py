from django.urls import path

from ecommerce.products.views.product import ProductListView

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(),
         name='products-list'),
]
