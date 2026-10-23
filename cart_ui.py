"""Cart display: the slide-in drawer, the order summary and the header counter.

Events: open / close the drawer, Add / + / - buttons everywhere, Escape key, "Continue to order form".
"""
from pyscript import when

import state
from cart import cart
from helpers import el, esc, scroll_to, stepper, toast
from menu_data import BY_ID, peso


def lines_html():
    """The list of items in the cart (used in the drawer and in the order section)."""
    if not cart.items:
        if state.placed:
            return '<p class="empty">Your order was turned into the message on the right. Add items from the menu to start a new order.</p>'
        return '<p class="empty">Nothing here yet. Add something from the menu.</p>'
    rows = []
    for item_id, qty in cart.items.items():
        item = BY_ID[item_id]
        rows.append(
            f'<li><img src="{item["img"]}" alt="">'
            f'<div class="nm"><b>{esc(item["name"])}</b><small>{peso(item["price"])} each</small></div>'
            f'<div class="line-ctl">{stepper(item_id, qty, "cart")}'
            f'<small style="font-variant-numeric:tabular-nums">{peso(qty * item["price"])}</small></div></li>'
        )
    return '<ul class="lines">' + "".join(rows) + "</ul>"


def render_cart():
    el("cart-n").textContent = str(cart.count())
    lines = lines_html()
    el("drawer-lines").innerHTML = lines
    summary = ""
    if cart.items:
        summary = f'<div class="sum"><span>Total</span><span>{peso(cart.total())}</span></div>'
    el("order-lines").innerHTML = lines + summary
    el("drawer-total").textContent = peso(cart.total())


def open_drawer(is_open):
    el("drawer").classList.toggle("open", is_open)
    el("scrim").classList.toggle("open", is_open)
    el("drawer").setAttribute("aria-hidden", str(not is_open).lower())


@when("click", "#menu-grid, #drawer-lines, #order-lines, #cake-ctl")
def change_quantity(event):
    """Customer pressed Add, + or - on a menu card, in the cart, or on the cake."""
    button = event.target.closest("[data-a]")
    if button is None:
        return
    item_id = button.getAttribute("data-id")
    delta = 1 if button.getAttribute("data-a") == "inc" else -1
    qty = cart.change(item_id, delta)
    if delta > 0 and qty == 1:
        toast(f'{BY_ID[item_id]["name"]} added')


@when("click", "#open-cart")
def show_drawer(event):
    open_drawer(True)


@when("click", "#close-cart, #scrim")
def hide_drawer(event):
    open_drawer(False)


@when("keydown", "body")
def escape_closes_drawer(event):
    if event.key == "Escape":
        open_drawer(False)


@when("click", "#go-order")
def go_to_order_form(event):
    open_drawer(False)
    scroll_to("order")


cart.subscribe(render_cart)
