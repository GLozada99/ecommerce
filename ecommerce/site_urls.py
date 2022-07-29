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
]

site_urlpatterns = (urlpatterns, 'site')
