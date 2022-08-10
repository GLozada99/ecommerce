from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from ecommerce import settings
from ecommerce.site_urls import site_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('site/',
         include(
             site_urlpatterns,
             namespace='site'),
         ),
    path('', lambda req: redirect('site:frontpage:frontpage')),
    path('accounts/', include('allauth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
