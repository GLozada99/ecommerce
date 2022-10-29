from django.urls import path

from ecommerce.order.views.full_cart import FullCartView
from ecommerce.order.views.minicart import (MiniCartView,
                                            add_cart_product_view, )

app_name = 'order'
urlpatterns = [
    path('', FullCartView.as_view(),
         name='cart'),
    path('full', FullCartView.as_view(template_name='cart/items_hx.html'),
         name='full'),
    path('mini', MiniCartView.as_view(),
         name='mini'),
    path('add/<int:product_id>', add_cart_product_view,
         name='add'),
]
