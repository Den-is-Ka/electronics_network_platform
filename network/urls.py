from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import NetworkNodeViewSet, ProductViewSet

router = DefaultRouter()
router.register("nodes", NetworkNodeViewSet, basename="network-node")
router.register("products", ProductViewSet, basename="product")

urlpatterns = [
    path("", include(router.urls)),
]
