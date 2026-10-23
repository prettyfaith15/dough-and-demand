"""Dough & Demand: entry point.

PyScript runs this file in the browser. Importing each module registers its event handlers
(the @when(...) functions), so the page reacts to clicks, typing and form submissions.

Modules
  menu_data.py  menu items, prices and shop settings
  cart.py       the cart (data) and the observer list
  cart_ui.py    cart drawer, header counter and Add / + / - buttons
  menu.py       category tabs and product cards
  combo.py      build-your-student-combo
  order_form.py mini cake, order form, copy message, save as image
  background.py drifting bakery shapes
  helpers.py    small shared functions
"""
import background
import cart_ui
import combo
import menu
import order_form  # noqa: F401  (importing registers its event handlers)
from cart import cart

# Start-up: restore a saved cart, then draw every section once
cart.load()
menu.render_tabs()
combo.render_combo()
cart.notify()  # redraws the menu, cart drawer, order summary and cake card
background.init()
