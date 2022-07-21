from rest_framework import serializers

from ecommerce.products.models import Category


class CategorySerializer(serializers.ModelSerializer):
    icon = serializers.CharField(source="icon.url", read_only=True)

    class Meta:
        model = Category
        fields = (
            'name',
            'icon',
            'slug',
        )
