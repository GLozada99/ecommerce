from django.urls import path

from ecommerce.core.views.frontpage import FrontPageView

app_name = 'core'
urlpatterns = [
    path('', FrontPageView.as_view(),
         name='frontpage'),
]
