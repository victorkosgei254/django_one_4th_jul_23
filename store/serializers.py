from rest_framework import serializers
from decimal import Decimal

from store.models import Product, Collection, Review


class CollectionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "price", "collection", "price_with_tax"]

    price_with_tax = serializers.SerializerMethodField(method_name='product_with_tax')

    def product_with_tax(self, product: Product):
        return product.price * Decimal(1.3)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_pk = self.context["product_pk"]
        return Review.objects.create(product_id=product_pk, **validated_data)
