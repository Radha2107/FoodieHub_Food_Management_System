from django.core.management.base import BaseCommand
from menu.models import Category, FoodItem

DATA = [
    ("Burgers", "burgers", [
        ("Classic Smash Burger", "Double smashed patty, cheddar, lettuce and our house sauce.", "249", "photo-1568901346375-23c9450c58cd", False, 15),
        ("Crispy Veg Burger", "Golden veggie patty with crunchy greens and creamy dressing.", "179", "photo-1553979459-d2229ba7433a", True, 15),
    ]),
    ("Pizza", "pizza", [
        ("Margherita Pizza", "Wood-fired style pizza with tomato, mozzarella and basil.", "299", "photo-1574071318508-1cdbab80d002", True, 20),
        ("Farmhouse Pizza", "Bell peppers, onion, mushroom, olives and mozzarella.", "349", "photo-1513104890138-7c749659a591", True, 25),
    ]),
    ("Bowls", "bowls", [
        ("Fresh Buddha Bowl", "A colourful bowl of grains, avocado, greens and roasted veggies.", "269", "photo-1512621776951-a57141f2eefd", True, 15),
        ("Paneer Rice Bowl", "Spiced paneer, fragrant rice and fresh crunchy salad.", "229", "photo-1512058564366-18510be2db19", True, 18),
    ]),
    ("Desserts", "desserts", [
        ("Chocolate Brownie", "Warm, fudgy chocolate brownie with a rich cocoa finish.", "129", "photo-1606313564200-e75d5e30476c", True, 10),
        ("Berry Cheesecake", "Creamy cheesecake topped with bright seasonal berries.", "169", "photo-1533134242443-d4fd215305ad", True, 10),
    ]),
    ("Drinks", "drinks", [
        ("Iced Coffee", "Chilled coffee, milk and a little sweetness over ice.", "119", "photo-1461023058943-07fcbe16d735", True, 5),
        ("Fresh Orange Juice", "Freshly squeezed orange juice, served chilled.", "99", "photo-1613478223719-2ab802602423", True, 5),
    ]),
]

class Command(BaseCommand):
    help = "Add sample categories and food items to the database"
    def handle(self, *args, **options):
        for category_name, slug, items in DATA:
            category, _ = Category.objects.get_or_create(name=category_name, defaults={"slug": slug})
            for name, description, price, photo, veg, prep in items:
                if photo == "photo-1606313564200-e75d5e30476c":
                    photo = "photo-1606313564200-e75d5e30476c"
                url = f"https://images.unsplash.com/{photo}?auto=format&fit=crop&w=900&q=85"
                FoodItem.objects.get_or_create(name=name, defaults={
                    "category": category, "description": description, "price": price,
                    "image_url": url, "is_vegetarian": veg, "prep_time": prep,
                })
        self.stdout.write(self.style.SUCCESS("Sample menu added."))
