from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import Category, FoodItem, Order, OrderItem
from .forms import SignUpForm, CheckoutForm

def home(request):
    foods = FoodItem.objects.filter(is_available=True).select_related("category")
    category = request.GET.get("category", "")
    query = request.GET.get("q", "").strip()
    if category:
        foods = foods.filter(category__slug=category)
    if query:
        foods = foods.filter(name__icontains=query)
    return render(request, "menu/home.html", {
    "foods": foods,
    "categories": Category.objects.all(),
    "active_category": category,
    "query": query,
    "food_count": FoodItem.objects.filter(is_available=True).count(),
    })

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to FoodieHub! Your account is ready.")
            return redirect("home")
    else:
        form = SignUpForm()
    return render(request, "menu/auth.html", {"form": form, "heading": "Create your account", "signup": True})

def login_view(request):
    from django.contrib.auth import authenticate
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get("username"), password=request.POST.get("password"))
        if user:
            login(request, user)
            return redirect("home")
        messages.error(request, "Username or password is incorrect.")
    return render(request, "menu/auth.html", {"heading": "Welcome back", "signup": False})

def logout_view(request):
    from django.contrib.auth import logout
    if request.method == "POST":
        logout(request)
    return redirect("home")

def cart_data(request):
    cart = request.session.get("cart", {})
    rows, total, count = [], Decimal("0.00"), 0
    for food_id, quantity in cart.items():
        food = FoodItem.objects.filter(pk=food_id, is_available=True).first()
        if food and int(quantity) > 0:
            subtotal = food.price * int(quantity)
            rows.append({"food": food, "quantity": int(quantity), "subtotal": subtotal})
            total += subtotal
            count += int(quantity)
    return rows, total, count

@login_required
@require_POST
def add_to_cart(request, food_id):
    food = get_object_or_404(FoodItem, pk=food_id, is_available=True)
    cart = request.session.get("cart", {})
    key = str(food.id)
    cart[key] = min(int(cart.get(key, 0)) + 1, 20)
    request.session["cart"] = cart
    messages.success(request, f"{food.name} added to your basket.")
    return redirect(request.META.get("HTTP_REFERER", "home"))

@login_required
def cart_view(request):
    rows, total, count = cart_data(request)
    return render(request, "menu/cart.html", {"rows": rows, "total": total, "count": count})

@login_required
@require_POST
def update_cart(request, food_id):
    cart = request.session.get("cart", {})
    quantity = int(request.POST.get("quantity", 1))
    if quantity <= 0:
        cart.pop(str(food_id), None)
    else:
        cart[str(food_id)] = min(quantity, 20)
    request.session["cart"] = cart
    return redirect("cart")

@login_required
@transaction.atomic
def checkout(request):
    rows, total, count = cart_data(request)
    if not rows:
        messages.info(request, "Your basket is empty.")
        return redirect("home")
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user, total=total, **form.cleaned_data)
            for row in rows:
                OrderItem.objects.create(order=order, food=row["food"], quantity=row["quantity"], unit_price=row["food"].price)
            request.session["cart"] = {}
            messages.success(request, f"Order #{order.id} placed successfully!")
            return redirect("order_detail", order_id=order.id)
    else:
        form = CheckoutForm()
    return render(request, "menu/checkout.html", {"form": form, "rows": rows, "total": total})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).prefetch_related("items__food")
    return render(request, "menu/orders.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items__food"), pk=order_id, user=request.user)
    return render(request, "menu/order_detail.html", {"order": order})

def staff_required(user):
    return user.is_authenticated and user.is_staff

@login_required
@user_passes_test(staff_required)
def dashboard(request):
    return render(request, "menu/dashboard.html", {
        "food_count": FoodItem.objects.count(), "order_count": Order.objects.count(),
        "orders": Order.objects.select_related("user")[:8],
    })
