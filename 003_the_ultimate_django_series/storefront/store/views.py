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
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .models import (
    Product,
    ProductImage,
    Collection,
    OrderItem,
    Review,
    Cart,
    CartItem,
    Customer,
    Order,
)
from .serializers import (
    ProductSerializer,
    ProductImageSerializer,
    CollectionSerializer,
    ReviewSerializer,
    CartSerializer,
    CartItemSerializer,
    AddCartItemSerializer,
    UpdateCartItemSerializer,
    CustomerSerializer,
    OrderSerializer,
    CreateOrderSerializer,
    UpdateOrderSerializer,
)
from .pagination import DefaultPagination
from .permissions import IsAdminOrReadOnly, FullDjangoModelPermissions

# CHECK THE GIT HISTORY OF THIS FILE, THERE ARE A LOT OF DIFFERENT WAYS TO IMPLEMENTS ENDPOINTS


# pylint: disable=no-member


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.prefetch_related("images").all()
    # queryset = Product.objects.all()  # simlate performance problem for locust
    lookup_field = "id"  # otherwise the rest framework expects `pk`
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # pagination_class = PageNumberPagination  # only for products
    pagination_class = DefaultPagination
    filterset_fields = ["collection_id"]
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]
    permission_classes = [IsAdminOrReadOnly]

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
    permission_classes = [IsAdminOrReadOnly]

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


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    # permission_classes = [FullDjangoModelPermissions]
    permission_classes = [IsAdminUser]

    # detail=False produces /customers/me
    # detail=True produces /customers/:id/me
    @action(detail=False, methods=["GET", "PUT"], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == "PUT":
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)


class OrderViewSet(ModelViewSet):
    http_method_names = ["get", "post", "patch", "delete", "head", "options"]

    def get_permissions(self):
        if self.request.method in ["PATCH", "DELETE"]:
            return [IsAdminUser()]

        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(
            data=request.data, context={"user_id": self.request.user.id}
        )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        elif self.request.method == "PATCH":
            return UpdateOrderSerializer

        return OrderSerializer

    def get_serializer_context(self, *args, **kwargs):
        return {"user_id": self.request.user.id}

    def get_queryset(self):
        current_user = self.request.user

        if current_user.is_staff:
            return Order.objects.all()

        customer = Customer.objects.get(user_id=current_user.id)
        return Order.objects.filter(customer_id=customer.id).all()


class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer

    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs["product_id"])

    def get_serializer_context(self):
        return {"product_id": self.kwargs["product_id"]}
