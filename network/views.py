from rest_framework.viewsets import ModelViewSet

from .models import NetworkNode, Product
from .serializers import (
    NetworkNodeCreateSerializer,
    NetworkNodeDetailSerializer,
    NetworkNodeListSerializer,
    NetworkNodeUpdateSerializer,
    ProductSerializer,
)


class NetworkNodeViewSet(ModelViewSet):
    queryset = NetworkNode.objects.select_related("supplier").prefetch_related("products")

    def get_serializer_class(self):
        if self.action == "create":
            return NetworkNodeCreateSerializer
        if self.action in ("update", "partial_update"):
            return NetworkNodeUpdateSerializer
        if self.action == "retrieve":
            return NetworkNodeDetailSerializer
        return NetworkNodeListSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("network_node")
    serializer_class = ProductSerializer
    