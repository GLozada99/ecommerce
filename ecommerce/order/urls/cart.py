from django.urls import path

from ecommerce.order.views.cart import ManageCartView

app_name = 'order'
urlpatterns = [
    path('manage/<int:product_id>', ManageCartView.as_view(),
         name='manage'),
]
