from django.urls import path

from ecommerce.order.views.cart import ManageCartView, get_cart_view

app_name = 'order'
urlpatterns = [
    path('manage/<int:product_id>', ManageCartView.as_view(),
         name='manage'),
    path('', get_cart_view,
         name='show'),
]
