from django.urls import path, include

from rest_framework_nested import routers

from pprint import pprint

from . import views


router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")
# pprint(router.urls)
# pprint(products_router.urls)


urlpatterns = [
    path("", include(router.urls)),
    path("", include(products_router.urls)),
]

# or
# urlpatterns = router.urls
