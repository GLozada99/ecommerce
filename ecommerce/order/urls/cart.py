from django.urls import path

from ecommerce.order.views.minicart import (MiniCartView,
                                            add_cart_product_view, )

app_name = 'order'
urlpatterns = [
    path('/manage', MiniCartView.as_view(),
         name='manage'),
    path('add/<int:product_id>', add_cart_product_view,
         name='add'),
]
