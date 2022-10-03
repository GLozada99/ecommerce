from django.urls import path

from ecommerce.order.views.full_cart import FullCartView
from ecommerce.order.views.minicart import (MiniCartView,
                                            add_cart_product_view, )

app_name = 'order'
urlpatterns = [
    path('full', FullCartView.as_view(),
         name='full'),
    path('mini', MiniCartView.as_view(),
         name='mini'),
    path('add/<int:product_id>', add_cart_product_view,
         name='add'),
]
