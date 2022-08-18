from django.urls import path

from ecommerce.products.views.product.list import (ProductListView,
                                                   breadcrumb_view,
                                                   category_selection_view, )

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(template_name='list/list.html'),
         name='list'),
    path('search/', ProductListView.as_view(
        template_name='list/items_hx.html'),
         name='search'),
    path('current_category/', category_selection_view,
         name='current-category'),
    path('breadcrumb/', breadcrumb_view,
         name='breadcrumb'),
]
