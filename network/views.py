from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import NetworkNodeFilter
from .models import NetworkNode, Product
from .permissions import IsActiveStaffPermission
from .serializers import (
    NetworkNodeListSerializer,
    NetworkNodeDetailSerializer,
    NetworkNodeCreateSerializer,
    NetworkNodeUpdateSerializer,
    ProductSerializer,
)


class NetworkNodeViewSet(ModelViewSet):
    queryset = NetworkNode.objects.select_related("supplier").prefetch_related("products")
    permission_classes = [IsActiveStaffPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = NetworkNodeFilter

    def get_serializer_class(self):
        if self.action == "list":
            return NetworkNodeListSerializer
        if self.action == "retrieve":
            return NetworkNodeDetailSerializer
        if self.action == "create":
            return NetworkNodeCreateSerializer
        if self.action in ("update", "partial_update"):
            return NetworkNodeUpdateSerializer
        return NetworkNodeDetailSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("network_node")
    serializer_class = ProductSerializer
    permission_classes = [IsActiveStaffPermission]
