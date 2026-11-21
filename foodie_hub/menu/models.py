from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(unique=True)
    def __str__(self):
        return self.name

class FoodItem(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="foods")
    name = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField()
    is_vegetarian = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True)
    prep_time = models.PositiveSmallIntegerField(default=20)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["category__name", "name"]
    def __str__(self):
        return self.name

class Order(models.Model):
    STATUS_CHOICES = [
        ("Placed", "Placed"), ("Preparing", "Preparing"),
        ("Out for delivery", "Out for delivery"), ("Delivered", "Delivered"),
        ("Cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="food_orders")
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=20)
    address = models.TextField()
    payment_method = models.CharField(max_length=30, default="Cash on Delivery")
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="Placed")
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return f"Order #{self.pk} - {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    food = models.ForeignKey(FoodItem, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    def subtotal(self):
        return self.quantity * self.unit_price
    def __str__(self):
        return f"{self.quantity} × {self.food.name}"
