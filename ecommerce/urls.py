from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path, re_path
from django.views.static import serve

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

handler400 = 'ecommerce.core.views.errors.error_400_view'
handler403 = 'ecommerce.core.views.errors.error_403_view'
handler404 = 'ecommerce.core.views.errors.error_404_view'
handler500 = 'ecommerce.core.views.errors.error_500_view'

if not settings.env_settings.S3_STORAGE:
    urlpatterns += re_path(r'^mediafiles/(?P<path>.*)$', serve,
                           {'document_root': settings.MEDIA_ROOT}),
    urlpatterns += re_path(r'^static/(?P<path>.*)$', serve,
                           {'document_root': settings.STATIC_ROOT}),
