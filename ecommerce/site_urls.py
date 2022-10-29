from django.urls import include, path

urlpatterns = [
    path('',
         include('ecommerce.core.urls.frontpage',
                 namespace='frontpage'
                 )
         ),
    path('products/',
         include('ecommerce.products.urls.product',
                 namespace='products'
                 )
         ),
    path('cart/',
         include('ecommerce.order.urls.cart',
                 namespace='cart'
                 )
         ),
    path('checkout/',
         include('ecommerce.order.urls.checkout',
                 namespace='checkout'
                 )
         ),
]

site_urlpatterns = (urlpatterns, 'site')
