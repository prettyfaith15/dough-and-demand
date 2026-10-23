"""cart.py - the cart (data) and the observer list.

Other modules call cart.subscribe(function) to be redrawn whenever the cart changes.
The cart is remembered in the browser (localStorage) between visits.
"""
import json

from pyscript import window

from menu_data import BY_ID

STORAGE_KEY = "dd-cart"


class Cart:
    def __init__(self):
        self.items = {}            # item id -> quantity
        self._subscribers = []     # functions to call after any change (redraw)
        self._user_listeners = []  # functions to call when the customer changes the cart

    # --- observers ----------------------------------------------------
    def subscribe(self, function):
        """Call `function` every time the cart changes."""
        self._subscribers.append(function)

    def on_user_change(self, function):
        """Call `function` when the customer adds, removes or merges items (not on clear/replace)."""
        self._user_listeners.append(function)

    def notify(self):
        """Redraw everything that depends on the cart."""
        for function in self._subscribers:
            function()

    # --- saving and loading -------------------------------------------
    def load(self):
        try:
            saved = json.loads(window.localStorage.getItem(STORAGE_KEY) or "{}")
            self.items = {k: int(v) for k, v in saved.items() if k in BY_ID and int(v) > 0}
        except Exception:
            self.items = {}

    def _save(self):
        try:
            window.localStorage.setItem(STORAGE_KEY, json.dumps(self.items))
        except Exception:
            pass

    def _changed_by_customer(self):
        self._save()
        for function in self._user_listeners:
            function()
        self.notify()

    # --- changing the cart --------------------------------------------
    def change(self, item_id, delta):
        """Add (delta > 0) or remove (delta < 0) one of an item. Returns the new quantity."""
        qty = max(0, self.items.get(item_id, 0) + delta)
        if qty:
            self.items[item_id] = qty
        else:
            self.items.pop(item_id, None)
        self._changed_by_customer()
        return qty

    def add_many(self, items):
        """Add a whole dict of {item id: quantity} (used by the combo builder)."""
        for item_id, qty in items.items():
            self.items[item_id] = self.items.get(item_id, 0) + qty
        self._changed_by_customer()

    def clear(self):
        """Empty the cart (after the order message is made)."""
        self.items = {}
        self._save()
        self.notify()

    def replace(self, items):
        """Put a saved order back (used by "Edit my order"). The caller redraws."""
        self.items = dict(items)
        self._save()

    # --- reading the cart ---------------------------------------------
    def qty(self, item_id):
        return self.items.get(item_id, 0)

    def count(self):
        return sum(self.items.values())

    def total(self):
        return sum(qty * BY_ID[item_id]["price"] for item_id, qty in self.items.items())


cart = Cart()
