from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ["id", "title", "products_count"]

    products_count = serializers.IntegerField(read_only=True)


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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "date", "name", "description"]

    def create(self, validated_data):
        product_id = self.context["product_id"]
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(
        read_only=True, method_name="calculate_total_price"
    )

    def calculate_total_price(self, item: CartItem):
        return item.product.unit_price * item.quantity

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(
        read_only=True, method_name="calculate_total_price"
    )

    def calculate_total_price(self, cart: Cart):
        return sum(
            [item.product.unit_price * item.quantity for item in cart.items.all()]
        )

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]
