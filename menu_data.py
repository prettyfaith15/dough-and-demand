"""Menu data and shop settings for Dough & Demand.

Edit prices, descriptions and settings here. The rest of the site reads from this file.
"""

# Paste your Facebook page link here (example: "https://m.me/yourpagename")
# to show an "Open Messenger" button after an order message is made.
MESSENGER_URL = ""

# Cakes must be ordered this many days ahead.
CAKE_NOTICE_DAYS = 2

CAKE_ID = "mini-birthday-cake"

# Menu categories: (key, label shown on the tab)
CATEGORIES = [
    ("all", "All"),
    ("cookies", "Cookies & Brownies"),
    ("pastries", "Sweet Pastries"),
    ("savory", "Savory Breads"),
    ("cakes", "Cakes & Cupcakes"),
]

ITEMS = [
    {"id": "oatmeal-cookie", "cat": "cookies", "name": "Oatmeal Cookie", "price": 30,
     "img": "img/oatmeal-cookie.jpg", "desc": "Chewy and hearty, with whole oats and a hint of brown sugar."},
    {"id": "chocolate-chip-cookie", "cat": "cookies", "name": "Chocolate Chip Cookie", "price": 35,
     "img": "img/chocolate-chip-cookie.jpg", "desc": "Golden edges, soft middle, plenty of chocolate chips.",
     "tag": "Student favorite"},
    {"id": "double-chocolate-cookie", "cat": "cookies", "name": "Double Chocolate Cookie", "price": 40,
     "img": "img/double-chocolate-cookie.jpg", "desc": "Cocoa dough packed with melty chocolate chunks."},
    {"id": "fudgy-brownie", "cat": "cookies", "name": "Fudgy Brownie", "price": 45,
     "img": "img/fudgy-brownie.jpg", "desc": "Dense, glossy and rich, with a sprinkle of sea salt.",
     "tag": "Student favorite"},
    {"id": "glazed-donut", "cat": "pastries", "name": "Glazed Donut", "price": 30,
     "img": "img/glazed-donut.jpg", "desc": "Soft ring donut with a sweet, shiny glaze."},
    {"id": "ensaymada", "cat": "pastries", "name": "Ensaymada", "price": 35,
     "img": "img/ensaymada.jpg", "desc": "Fluffy brioche roll with buttery filling and grated cheese."},
    {"id": "cinnamon-roll", "cat": "pastries", "name": "Cinnamon Roll", "price": 40,
     "img": "img/cinnamon-roll.jpg", "desc": "Warm spiral with cinnamon sugar and sweet icing."},
    {"id": "almond-danish", "cat": "pastries", "name": "Almond Danish", "price": 50,
     "img": "img/almond-danish.jpg", "desc": "Flaky layers, creamy custard, sliced almonds and powdered sugar."},
    {"id": "garlic-bread", "cat": "savory", "name": "Garlic Bread", "price": 30,
     "img": "img/garlic-bread.jpg", "desc": "Toasted slices brushed with garlic butter and herbs."},
    {"id": "spanish-bread", "cat": "savory", "name": "Spanish Bread", "price": 30,
     "img": "img/spanish-bread.jpg", "desc": "Soft roll with a sweet buttery filling and a crumb coat.",
     "tag": "Sweet-savory"},
    {"id": "cheese-bread", "cat": "savory", "name": "Cheese Bread", "price": 40,
     "img": "img/cheese-bread.jpg", "desc": "Golden bun with a gooey melted cheese center."},
    {"id": "ham-cheese-roll", "cat": "savory", "name": "Ham & Cheese Roll", "price": 50,
     "img": "img/ham-cheese-roll.jpg", "desc": "Baked roll stuffed with ham and stretchy cheese. The most filling pick."},
    {"id": "vanilla-cupcake", "cat": "cakes", "name": "Vanilla Cupcake", "price": 40,
     "img": "img/vanilla-cupcake.jpg", "desc": "Light vanilla cake with swirled frosting and sprinkles."},
    {"id": "chocolate-cake-slice", "cat": "cakes", "name": "Chocolate Cake Slice", "price": 50,
     "img": "img/chocolate-cake-slice.jpg", "desc": "Two moist chocolate layers with creamy chocolate frosting."},
]

# Pre-order only item (not shown in the regular menu grid)
CAKE = {"id": CAKE_ID, "name": "Mini Birthday Cake", "price": 250, "img": "img/mini-birthday-cake.jpg"}

# Look up any item (including the cake) by its id
BY_ID = {item["id"]: item for item in ITEMS + [CAKE]}


def peso(amount):
    """Format a number as pesos, for example 1250 -> ₱1,250."""
    return "₱" + format(int(amount), ",")
