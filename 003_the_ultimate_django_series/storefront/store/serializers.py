from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title"]


class ProductSerializer(serializers.ModelSerializer):
    # requires `serializers.ModelSerializer`
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price", "collection"]
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
