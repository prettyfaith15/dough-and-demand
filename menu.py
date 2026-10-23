"""Menu section: category tabs and the product cards.

Events: click on a tab filters the menu. (Add / + / - clicks are handled in cart_ui.py.)
"""
from pyscript import when

import state
from cart import cart
from helpers import el, esc, stepper
from menu_data import CATEGORIES, ITEMS, peso


def render_tabs():
    el("tabs").innerHTML = "".join(
        f'<button class="tab" type="button" data-cat="{key}" aria-pressed="{str(key == state.category).lower()}">{esc(label)}</button>'
        for key, label in CATEGORIES
    )


def render_menu():
    cards = []
    for item in ITEMS:
        if state.category != "all" and item["cat"] != state.category:
            continue
        qty = cart.qty(item["id"])
        badge = f'<span class="badge">{esc(item["tag"])}</span>' if item.get("tag") else ""
        if qty:
            control = stepper(item["id"], qty, "cart")
        else:
            control = f'<button class="add" type="button" data-a="inc" data-src="cart" data-id="{item["id"]}">Add</button>'
        cards.append(
            '<article class="card">'
            f'<div class="ph"><img src="{item["img"]}" alt="{esc(item["name"])}" loading="lazy">{badge}</div>'
            '<div class="body">'
            f'<h3>{esc(item["name"])}</h3><p class="desc">{esc(item["desc"])}</p>'
            f'<div class="row"><span class="price">{peso(item["price"])}</span>{control}</div>'
            "</div></article>"
        )
    el("menu-grid").innerHTML = "".join(cards)


@when("click", "#tabs")
def choose_category(event):
    """Customer clicked a category tab."""
    tab = event.target.closest("[data-cat]")
    if tab is None:
        return
    state.category = tab.getAttribute("data-cat")
    render_tabs()
    render_menu()


# Redraw the menu whenever the cart changes (so Add turns into - 1 +)
cart.subscribe(render_menu)
