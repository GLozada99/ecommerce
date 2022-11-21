from typing import Any, Type

from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand

from ecommerce import settings
from ecommerce.clients.models import Client
from ecommerce.core.models import SlideImage, User
from ecommerce.order.models.order import Order, OrderProducts
from ecommerce.products.models.composite_models import (ProductConfiguration,
                                                        ProductPicture, )
from ecommerce.products.models.models import Category, Product
from ecommerce.utils.models import BaseModel

GROUPS_PERMISSIONS: dict[str, dict[Type[BaseModel], list[str]]] = {
    settings.GROUPS_EMPLOYEE: {
        Client: ['view'],
        SlideImage: ['add', 'change', 'delete', 'view'],
        Category: ['add', 'change', 'delete', 'view'],
        Product: ['add', 'change', 'delete', 'view'],
        ProductConfiguration: ['add', 'change', 'delete', 'view'],
        ProductPicture: ['add', 'change', 'delete', 'view'],
        Order: ['view'],
        OrderProducts: ['view'],
    },
    settings.GROUPS_ADMIN: {
        User: ['add', 'change', 'delete', 'view'],
        Client: ['add', 'change', 'delete', 'view'],
        SlideImage: ['add', 'change', 'delete', 'view'],
        Category: ['add', 'change', 'delete', 'view'],
        Product: ['add', 'change', 'delete', 'view'],
        ProductConfiguration: ['add', 'change', 'delete', 'view'],
        ProductPicture: ['add', 'change', 'delete', 'view'],
        Order: ['add', 'change', 'delete', 'view'],
        OrderProducts: ['add', 'change', 'delete', 'view'],
    },
}


class Command(BaseCommand):
    help = ('A command to create groups.\n'
            'This command does not need parameters')

    def handle(self, *args: Any, **kwargs: Any) -> None:
        for group_name, group_models in GROUPS_PERMISSIONS.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            for model_cls, permissions in group_models.items():
                for perm_index, perm_name in enumerate(permissions):
                    codename = perm_name + "_" + model_cls._meta.model_name
                    try:
                        perm = Permission.objects.get(codename=codename)
                        group.permissions.add(perm)
                        self.stdout.write("Adding "
                                          + codename
                                          + " to group "
                                          + group.__str__())
                    except Permission.DoesNotExist:
                        self.stdout.write(codename + " not found")
