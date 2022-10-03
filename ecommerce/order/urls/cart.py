from django.urls import path

from ecommerce.order.views.cart import CartView
from ecommerce.order.views.minicart import (MiniCartView,
                                            add_cart_product_view, )

app_name = 'order'
urlpatterns = [
    path('/', CartView.as_view(),
         name='full'),
    path('/manage', MiniCartView.as_view(),
         name='manage'),
    path('add/<int:product_id>', add_cart_product_view,
         name='add'),
]
