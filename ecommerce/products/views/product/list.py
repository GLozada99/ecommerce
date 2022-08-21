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

    def get_queryset(self) -> QuerySet:
        products = super(ProductListView, self).get_queryset()
        if category := self.request.session.get('current_category'):
            products = products.filter(category__slug=category)
        return products

    def get_context_data(self, **kwargs: dict) -> Mapping:
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['current_category'] = self.request.GET.get(
            'category', '')
        context['current_order_by'] = self.request.GET.get(
            'order_by', '')
        return context

    def get_ordering(self) -> str | None:
        order_by = 'name'
        if current_order_by := self.request.session.get('current_order_by'):
            order_by = current_order_by
        return order_by

    def get(
            self, request: HttpRequest,
            *args: tuple, **kwargs: dict) -> HttpResponse:
        request.session['current_category'] = self.request.GET.get(
            'category', '')
        request.session['current_order_by'] = self.request.GET.get(
            'order_by', '')
        print(request.session.items())
        response = super(ProductListView, self).get(request, *args, **kwargs)
        trigger_client_event(response, 'get_items', {})
        return response


def category_selection_view(request: HttpRequest) -> \
        HttpResponse:
    context = {
        'categories': Category.objects.all().order_by('name'),
        'current_category': Category.objects.filter(slug=request.session.get(
            'current_category')).values('slug').first(),
        'current_order_by': request.session.get(
            'current_order_by')
    }
    return render(request, 'list/categories_hx.html', context)


def breadcrumb_view(request: HttpRequest) -> HttpResponse:
    context = {
        'current_category': Category.objects.filter(slug=request.session.get(
            'current_category')).values('name', 'slug').first()
    }
    return render(request, 'list/breadcrumb_hx.html', context)


def order_by_view(request: HttpRequest) -> HttpResponse:
    context = {
        'current_category': request.session.get(
            'current_category'),
        'current_order_by': request.session.get(
            'current_order_by')
    }
    return render(request, 'list/order_by_hx.html', context)
