from django.conf.urls.static import static
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

from ecommerce import settings
from ecommerce.site_urls import site_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',
         include(
             site_urlpatterns,
             namespace='site'),
         ),
    path('site/', lambda req: redirect('site:frontpage:frontpage')),
    path('accounts/', include('allauth.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
]

if not settings.env_settings.S3_STORAGE:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
