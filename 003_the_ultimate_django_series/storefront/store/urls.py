from django.urls import path, include

from rest_framework.routers import SimpleRouter, DefaultRouter

# from pprint import pprint

from . import views


# router = SimpleRouter()
router = DefaultRouter()
router.register("products", views.ProductViewSet)
router.register("collections", views.CollectionViewSet)
# pprint(router.urls)

urlpatterns = [
    path("", include(router.urls)),
]

# or
# urlpatterns = router.urls
