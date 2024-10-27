from django.shortcuts import get_object_or_404
from django.db.models import Count

from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import Product, Collection, OrderItem
from .serializers import ProductSerializer, CollectionSerializer

# CHECK THE GIT HISTORY OF THIS FILE, THERE ARE A LOT OF DIFFERENT WAYS TO IMPLEMENTS ENDPOINTS


class ProductViewSet(ModelViewSet):
    # pylint: disable=no-member
    queryset = Product.objects.select_related("collection").all()
    lookup_field = "id"  # otherwise the rest framework expects `pk`

    # Alternatively can use methods
    # def get_queryset(self):
    #     # pylint: disable=no-member
    #     return Product.objects.select_related("collection").all()

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
