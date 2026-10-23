"""Build-your-student-combo section.

Events: click on Add / + / - changes the combo, and "Add combo to my order" moves it to the cart.
The total, meter and message update on every click.
"""
from pyscript import when

from cart import cart
from cart_ui import open_drawer
from helpers import el, esc, stepper, toast
from menu_data import BY_ID, ITEMS, peso

COMBO_MIN = 75
COMBO_MAX = 100

combo = {}  # item id -> quantity


def combo_total():
    return sum(qty * BY_ID[item_id]["price"] for item_id, qty in combo.items())


def verdict_for(total):
    """Return (message, css class) for the current combo total."""
    if not combo:
        return "Add items to start.", ""
    if total < COMBO_MIN:
        return f"Add {peso(COMBO_MIN - total)} more to reach the combo range.", ""
    if total <= COMBO_MAX:
        return "Nice. This combo is inside the ₱75–₱100 range.", "good"
    return f"{peso(total - COMBO_MAX)} over the combo range. Remove an item to bring it down.", "over"


def render_combo():
    picks = []
    for item in ITEMS:
        qty = combo.get(item["id"], 0)
        if qty:
            control = stepper(item["id"], qty, "combo")
        else:
            control = (f'<button class="add" type="button" data-a="inc" data-src="combo" '
                       f'data-id="{item["id"]}" style="padding:6px 14px">Add</button>')
        picks.append(
            f'<div class="pick"><img src="{item["img"]}" alt="">'
            f'<div class="t"><b>{esc(item["name"])}</b><small>{peso(item["price"])}</small></div>{control}</div>'
        )
    el("pick-list").innerHTML = "".join(picks)

    total = combo_total()
    el("combo-total").textContent = peso(total)
    el("combo-fill").style.width = f"{min(100, total)}%"
    message, css = verdict_for(total)
    verdict = el("combo-verdict")
    verdict.className = ("verdict " + css).strip()
    verdict.textContent = message
    el("combo-list").innerHTML = "".join(
        f'<li><span>{qty} × {esc(BY_ID[item_id]["name"])}</span><span>{peso(qty * BY_ID[item_id]["price"])}</span></li>'
        for item_id, qty in combo.items()
    )
    el("combo-add").disabled = not combo


@when("click", "#pick-list")
def change_combo(event):
    """Customer pressed Add, + or - on a combo item."""
    button = event.target.closest("[data-a]")
    if button is None:
        return
    item_id = button.getAttribute("data-id")
    delta = 1 if button.getAttribute("data-a") == "inc" else -1
    qty = max(0, combo.get(item_id, 0) + delta)
    if qty:
        combo[item_id] = qty
    else:
        combo.pop(item_id, None)
    render_combo()


@when("click", "#combo-add")
def add_combo_to_cart(event):
    """Move the combo into the cart and open the drawer."""
    global combo
    cart.add_many(combo)
    combo = {}
    render_combo()
    toast("Combo added to your order")
    open_drawer(True)
