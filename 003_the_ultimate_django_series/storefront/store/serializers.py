from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField()


class ProductSerializer(serializers.ModelSerializer):
    # requires `serializers.ModelSerializer`
    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "slug",
            "inventory",
            "description",
            "unit_price",
            "collection",
        ]
        # fields = "__all__" # optionally can include all fields, but that's considered a bad practice

    # Manual way (needs to inherit from `serializers.Serializer`)
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=255)
    # price = serializers.DecimalField(
    #     max_digits=6, decimal_places=2, source="unit_price"
    # )
    # price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    # collection = CollectionSerializer()
    # collection_url = serializers.HyperlinkedRelatedField(
    #     queryset=Collection.objects.all(),  # pylint: disable=no-member
    #     view_name="collection-detail",
    #     source="collection",
    # )

    # def calculate_tax(self, product: Product):
    #     return product.unit_price * Decimal(1.1)

    # The way to override create or update actions
    # def create(self, validated_data):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product

    # def update(self, instance, validated_data):
    #     instance.unit_price = validated_data.get('unit_price')
    #     instance.save()
    #     return instance
