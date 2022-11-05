from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _


def error_400_view(
        request: HttpRequest,
        exception: Any = None) -> HttpResponse:
    context = {
        'page_name': _('400 Error'),
        'page_title': _('400 - BAD REQUEST'),
        'message': _("The request made may have some incorrect data.")
    }
    return render(request, 'errors/../templates/error.html', context)


def error_403_view(
        request: HttpRequest,
        exception: Any = None) -> HttpResponse:
    context = {
        'page_name': _('403 Error'),
        'page_title': _('403 - FORBIDDEN PAGE'),
        'message': _("You do not have the necessary permissions to go to "
                     "that page")
    }
    return render(request, 'errors/../templates/error.html', context)


def error_404_view(
        request: HttpRequest,
        exception: Any = None) -> HttpResponse:
    context = {
        'page_name': _('404 Error'),
        'page_title': _('404 - PAGE NOT FOUND'),
        'message': _("We can't seem to find page you are looking for.")
    }
    return render(request, 'errors/../templates/error.html', context)


def error_500_view(
        request: HttpRequest,
        exception: Any = None) -> HttpResponse:
    context = {
        'page_name': _('500 Error'),
        'page_title': _('500 - INTERNAL ERROR'),
        'message': _("There's been an error processing your request, "
                     "try again later or contact the administrators.")
    }
    return render(request, 'errors/../templates/error.html', context)
