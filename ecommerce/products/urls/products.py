from django.urls import path

from ecommerce.products.views.products import ProductListView

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(),
         name='products-list'),
]
