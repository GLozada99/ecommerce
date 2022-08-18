from typing import Mapping

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django_htmx.http import trigger_client_event

from ecommerce.products.models.models import Category, Product


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 1
    ordering = 'name'

    def get_queryset(self) -> QuerySet:
        products = super(ProductListView, self).get_queryset()
        if category := self.request.session.get('current_category'):
            products = products.filter(category__slug=category)

        print(products)
        return products

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get(
            self, request: HttpRequest,
            *args: tuple, **kwargs: dict) -> HttpResponse:
        request.session['current_category'] = self.request.GET.get('category')
        response = super(ProductListView, self).get(request, *args, **kwargs)
        trigger_client_event(response, 'get_items', {})
        return response


def category_selection_view(request: HttpRequest) -> \
        HttpResponse:
    context = {
        'categories': Category.objects.all().order_by('name'),
    }
    return render(request, 'list/categories_hx.html', context)


def breadcrumb_view(request: HttpRequest) -> HttpResponse:
    context = {
        'current_category': Category.objects.filter(slug=request.session.get(
            'current_category')).values('name', 'slug').first()
    }
    return render(request, 'list/breadcrumb_hx.html', context)
