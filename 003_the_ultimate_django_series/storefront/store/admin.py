from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from django.utils.html import format_html, urlencode
from django.urls import reverse

from . import models


class InventoryFilter(admin.SimpleListFilter):
    title = "inventory"
    parameter_name = "inventory"

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [("<10", "Low")]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        if self.value() == "<10":
            return queryset.filter(inventory__lt=10)


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    readonly_fields = ["thumbnail"]

    def thumbnail(self, instance):
        if instance.image.name != "":
            return format_html(f'<img src="{instance.image.url}" class="thumbnail" />')

        return ""


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # fields = ["title"]
    # read_only = ["title"]
    # exclude = ["promotions"]
    prepopulated_fields = {"slug": ["title"]}
    autocomplete_fields = ["collection"]
    actions = ["clear_inventory"]
    list_display = ["title", "collection_title", "unit_price", "inventory_status"]
    list_editable = ["unit_price"]
    list_filter = ["collection", "last_update", InventoryFilter]
    search_fields = ["title"]
    list_per_page = 10
    list_select_related = ["collection"]
    inlines = [ProductImageInline]

    @admin.display(ordering="inventory")
    def inventory_status(self, product):
        if product.inventory < 10:
            return "Low"

        return "OK"

    def collection_title(self, product):
        return product.collection.title

    @admin.action(description="Clear inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)  # real update
        self.message_user(
            request,
            f"{updated_count} products were successfuly updated",
            messages.SUCCESS,
        )

    class Media:
        css = {
            "all": ["store/styles.css"],
        }


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ["title", "products_count"]
    search_fields = ["title"]

    @admin.display(ordering="products_count")
    def products_count(self, collection):
        url = (
            reverse("admin:store_product_changelist")
            + "?"
            + urlencode({"collection__id": str(collection.id)})
        )
        return format_html("<a href='{}'>{}</a>", url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(products_count=Count("products"))


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "membership", "orders_count"]
    list_editable = ["membership"]
    ordering = ["user__first_name", "user__last_name"]
    list_select_related = ["user"]
    list_per_page = 10
    search_fields = ["first_name__istartswith", "last_name__istartswith"]

    def orders_count(self, customer):
        url = (
            reverse("admin:store_order_changelist")
            + "?"
            + urlencode({"customer__id": str(customer.id)})
        )
        return format_html("<a href='{}'>{}</a>", url, customer.orders_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).annotate(orders_count=Count("order"))


class OrderItemInline(admin.TabularInline):  # or admin.StackedInline
    autocomplete_fields = ["product"]
    min_num = 1
    max_num = 10
    model = models.OrderItem
    extra = 2


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ["customer"]
    inlines = [OrderItemInline]
    list_display = [
        "id",
        "customer",
        "payment_status",
        "placed_at",
    ]
    list_per_page = 10
    list_select_related = ["customer"]
