from rest_framework import serializers

from .models import NetworkNode, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "network_node",
            "name",
            "model",
            "release_date",
        )


class NetworkNodeListSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    hierarchy_level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "node_type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "supplier_name",
            "debt",
            "created_at",
            "hierarchy_level",
        )


class NetworkNodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "node_type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "debt",
            "created_at",
        )
        read_only_fields = ("id", "created_at")


class NetworkNodeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "node_type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "debt",
            "created_at",
        )
        read_only_fields = ("id", "debt", "created_at")

    def validate(self, attrs):
        if "debt" in self.initial_data:
            raise serializers.ValidationError(
                {"debt": "Обновление задолженности через API запрещено."}
            )
        return super().validate(attrs)


class NetworkNodeDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    supplier_name = serializers.CharField(source="supplier.name", read_only=True)
    hierarchy_level = serializers.IntegerField(read_only=True)

    class Meta:
        model = NetworkNode
        fields = (
            "id",
            "name",
            "node_type",
            "email",
            "country",
            "city",
            "street",
            "house_number",
            "supplier",
            "supplier_name",
            "debt",
            "created_at",
            "hierarchy_level",
            "products",
        )