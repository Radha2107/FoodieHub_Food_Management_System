# FoodieHub — Food Management & Food Ordering System

A beginner-friendly Python Full Stack Development project built with **Python, Django, HTML, CSS and SQLite**.

## Features
- Responsive, food-themed interface with food photography
- Food menu with categories and search
- User registration, login and logout
- Add food to basket and update quantities
- Checkout with delivery details (Cash on Delivery demo)
- Order history and order details
- Staff dashboard
- Django admin to manage categories, food items and order statuses
- SQLite database (created automatically by Django migrations)

## Requirements
- Python 3.10 or newer
- VS Code
- Internet connection for Google Fonts and the Unsplash food photos

## Run in VS Code (Windows)

1. Extract the ZIP file.
2. Open the extracted **foodie_hub** folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   py -m venv venv
   ```

5. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run this once in that terminal and activate again:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\venv\Scripts\Activate.ps1
   ```

6. Install Django:

   ```powershell
   py -m pip install -r requirements.txt
   ```

7. Create the database tables:

   ```powershell
   py manage.py makemigrations menu
   py manage.py migrate
   ```

8. Add the sample food menu:

   ```powershell
   py manage.py seed_food
   ```

9. Start the website:

   ```powershell
   py manage.py runserver
   ```

10. Open this address in your browser:

   **http://127.0.0.1:8000/**

Keep the terminal running while using the website. Press `Ctrl + C` to stop the server.

## Create a staff/admin account

Open a **second terminal** in the same project folder. Activate the virtual environment again, then run:

```powershell
py manage.py createsuperuser
```

Enter a username, email (optional if prompted), and password. Then visit:

**http://127.0.0.1:8000/admin/**

Use the superuser login to manage menu items, categories and orders. The staff dashboard is at **http://127.0.0.1:8000/dashboard/**.

## Demo flow
1. Open the home page and browse categories.
2. Create a normal account using **Join us**.
3. Add dishes to the basket.
4. Open Basket → Continue to checkout.
5. Enter delivery details and place the order.
6. Open **My orders** to see the saved order.
7. Log in to Django admin as the superuser to change an order status or edit the menu.

## Database design

- **Category**: category name and slug
- **FoodItem**: category, name, description, price, image URL, veg/non-veg, availability and preparation time
- **Order**: customer, delivery details, payment method, total, status and order date
- **OrderItem**: order, selected food, quantity and unit price

Relationship overview:
- One Category has many FoodItems.
- One User can have many Orders.
- One Order has many OrderItems.
- Each OrderItem refers to one FoodItem.

## Notes
- This is an educational demo. Checkout records orders in SQLite; it does not process real payments or connect to a delivery service.
- Food photos are loaded from Unsplash URLs, so an internet connection is needed to display them.
- Do not use the included development `SECRET_KEY` or `DEBUG=True` settings for a public production deployment.
