from django.urls import path

from ecommerce.products.views.product.detail import (ProductDetailView,
                                                     selected_picture_view, )
from ecommerce.products.views.product.list import (ProductListView,
                                                   breadcrumb_view,
                                                   category_selection_view,
                                                   order_by_view, )

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(
        template_name='list.html'),
         name='list'),
    path('search/', ProductListView.as_view(
        template_name='list/items_hx.html'),
         name='search'),
    path('current_category/', category_selection_view,
         name='current-category'),
    path('breadcrumb/', breadcrumb_view,
         name='breadcrumb'),
    path('order_by/', order_by_view,
         name='order_by'),
    path('<slug:slug>/', ProductDetailView.as_view(
        template_name='detail.html'),
         name='detail'),
    path('<slug:slug>/config', ProductDetailView.as_view(
        template_name='detail/product.html'),
         name='detail-config'),
    path('<slug:slug>/<str:type>/<int:id>', selected_picture_view,
         name='detail-picture'),
    path('<slug:slug>/la', ProductDetailView.as_view(
        template_name='product-layout1.html'),
         name='detail2'),
]
