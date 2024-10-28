from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin,
)
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializers import (
    ProductSerializer,
    CollectionSerializer,
    ReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
)
from .pagination import DefaultPagination

# CHECK THE GIT HISTORY OF THIS FILE, THERE ARE A LOT OF DIFFERENT WAYS TO IMPLEMENTS ENDPOINTS


# pylint: disable=no-member


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    lookup_field = "id"  # otherwise the rest framework expects `pk`
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # pagination_class = PageNumberPagination  # only for products
    pagination_class = DefaultPagination
    filterset_fields = ["collection_id"]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    def get_serializer_class(self):
        return ProductSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(project_id=kwargs["id"]).count() > 0:
            return Response(
                {
                    "error": "Product cannot be deleted because it is associated with an order item"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )

        return super().destroy(request, *args, **kwargs)


class CollectionViewSet(ModelViewSet):
    # pylint: disable=no-member
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def get_serializer_context(self):
        return {"request": self.request}

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs["pk"]).count() > 0:
            return Response(
                {
                    "error": "Collection cannot be deleted because it associated with products"
                },
                status=status.HTTP_405_METHOD_NOT_ALLOWED,
            )
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_id"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_id"]}


class CartViewSet(
    CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet
):
    serializer_class = CartSerializer
    lookup_field = "id"
    queryset = Cart.objects.prefetch_related("items__product").all()


class CartItemViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer

        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs["cart_id"]).select_related(
            "product"
        )

    def get_serializer_context(self):
        return {"cart_id": self.kwargs["cart_id"]}
