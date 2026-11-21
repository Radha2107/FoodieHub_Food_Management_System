from django.contrib import admin
from .models import Category, FoodItem, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(FoodItem)
class FoodItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "is_vegetarian", "is_available")
    list_filter = ("category", "is_vegetarian", "is_available")
    search_fields = ("name", "description")

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("food", "quantity", "unit_price")

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "total", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "phone", "user__username")
    inlines = [OrderItemInline]
