from django.contrib import admin

from ecommerce.clients.models import Address, Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('user',)


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('state', 'city', 'first_line', 'second_line')
