from django.urls import path

from ecommerce.order.views.checkout import CheckoutView, order_form_view

app_name = 'order'
urlpatterns = [
    path('', CheckoutView.as_view(),
         name='checkout'),
    path('delivery/<int:delivery>', order_form_view,
         name='delivery'),
]
