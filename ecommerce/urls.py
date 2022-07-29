from django.conf.urls.static import static
from django.contrib import admin
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
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
