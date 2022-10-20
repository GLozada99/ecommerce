from django.urls import path

from ecommerce.order.views.checkout import (CheckoutView,
                                            add_address_form_view,
                                            add_address_view, get_cities_view,
                                            order_form_view,
                                            order_submit_view, )

app_name = 'order'
urlpatterns = [
    path('', CheckoutView.as_view(),
         name='checkout'),
    path('delivery', order_form_view,
         name='delivery'),
    path('add-address-form', add_address_form_view,
         name='add-address-form'),
    path('add-address', add_address_view,
         name='add-address'),
    path('get-cities', get_cities_view,
         name='get-cities'),
    path('submit', order_submit_view,
         name='submit'),
]
