from rest_framework import serializers

from ecommerce.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    picture = serializers.CharField(source="principal_image_url",
                                    read_only=True)

    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'current_price',
            'slug',
            'picture',
        )
