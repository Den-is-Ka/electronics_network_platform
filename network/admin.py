from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import NetworkNode, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0
    fields = ("name", "model", "release_date")


@admin.action(description="Очистить задолженность перед поставщиком")
def clear_debt(modeladmin, request, queryset):
    queryset.update(debt=0)


@admin.register(NetworkNode)
class NetworkNodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "node_type",
        "city",
        "country",
        "supplier_link",
        "debt",
        "hierarchy_level_display",
        "created_at",
    )
    list_filter = ("city", "country", "node_type", "created_at")
    search_fields = ("name", "email", "city", "country", "supplier__name")
    readonly_fields = ("created_at", "hierarchy_level_display")
    actions = (clear_debt,)
    inlines = (ProductInline,)

    fieldsets = (
        (
            "Основная информация",
            {
                "fields": ("name", "node_type", "supplier"),
            },
        ),
        (
            "Контакты",
            {
                "fields": ("email", "country", "city", "street", "house_number"),
            },
        ),
        (
            "Финансы и метаданные",
            {
                "fields": ("debt", "hierarchy_level_display", "created_at"),
            },
        ),
    )

    @admin.display(description="Поставщик")
    def supplier_link(self, obj):
        if not obj.supplier:
            return "-"
        url = reverse("admin:network_networknode_change", args=[obj.supplier.pk])
        return format_html('<a href="{}">{}</a>', url, obj.supplier.name)

    @admin.display(description="Уровень иерархии")
    def hierarchy_level_display(self, obj):
        return obj.hierarchy_level


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "model", "network_node", "release_date")
    list_filter = ("release_date", "network_node__city", "network_node__country")
    search_fields = ("name", "model", "network_node__name")
