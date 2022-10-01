from typing import Any, Mapping

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView
from django_htmx.http import trigger_client_event

from ecommerce.products.models.models import Category, Product
from ecommerce.products.services.product import ProductListService


class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'products'
    paginate_by = 6

    def get_queryset(self) -> QuerySet:
        products = ProductListService.get_products(
            super().get_queryset(),
            self.request.session.get('current_order_by'),
        )
        if category := self.request.session.get('current_category'):
            products = products.filter(category__slug=category)
        return products

    def get(
            self, request: HttpRequest,
            *args: tuple, **kwargs: dict) -> HttpResponse:
        request.session['current_category'] = self.request.GET.get(
            'category', '')
        request.session['current_order_by'] = self.request.GET.get(
            'order_by', '')

        response = super().get(request, *args, **kwargs)
        trigger_client_event(response, 'get_items', {})
        return response

    def get_context_data(self, **kwargs: Any) -> Mapping:
        context = super().get_context_data(**kwargs)
        context |= ProductListService.get_context(self.request.GET)

        return context


def category_selection_view(request: HttpRequest) -> \
        HttpResponse:
    categories = Category.objects.all().order_by('name')
    context = {
        'categories': categories,
        'current_category': ProductListService.get_current_category(
            request.session.get('current_category'), categories),
        'current_order_by': request.session.get(
            'current_order_by')
    }
    return render(request, 'list/categories_hx.html', context)


def breadcrumb_view(request: HttpRequest) -> HttpResponse:
    context = {
        'current_category': ProductListService.get_current_category(
            request.session.get('current_category'))
    }
    return render(request, 'list/breadcrumb_hx.html', context)


def order_by_view(request: HttpRequest) -> HttpResponse:
    context = {
        'current_category': ProductListService.get_current_category(
            request.session.get('current_category')),
        'current_order_by': request.session.get(
            'current_order_by')
    }
    return render(request, 'list/order_by_hx.html', context)
