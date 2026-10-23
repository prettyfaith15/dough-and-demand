"""Order section: mini cake, order form, order message, copy and save-as-image.

Events: form submit makes the message; buttons copy it, save it as a JPG image, or put the
order back in the cart for editing.
"""
import math
from datetime import date, timedelta

from js import Date
from pyscript import document, when

import state
from cart import cart
from helpers import el, js_obj, scroll_to, stepper, toast
from menu_data import BY_ID, CAKE, CAKE_ID, CAKE_NOTICE_DAYS, MESSENGER_URL, peso

last_message = ""
last_order = None
last_cart = {}


# ---------------------------------------------------------------- mini cake + date
def today():
    now = Date.new()  # uses the customer's own clock and time zone
    return date(int(now.getFullYear()), int(now.getMonth()) + 1, int(now.getDate()))


def update_date_min():
    has_cake = cart.qty(CAKE_ID) > 0
    earliest = today() + timedelta(days=CAKE_NOTICE_DAYS if has_cake else 0)
    iso = earliest.isoformat()
    field = el("f-date")
    field.min = iso
    if not field.value or field.value < iso:
        field.value = iso
    el("date-hint").textContent = f"Cakes need {CAKE_NOTICE_DAYS} days notice." if has_cake else ""


def render_cake():
    qty = cart.qty(CAKE_ID)
    if qty:
        el("cake-ctl").innerHTML = stepper(CAKE_ID, qty, "cart")
    else:
        el("cake-ctl").innerHTML = (f'<button class="btn" type="button" data-a="inc" data-src="cart" '
                                    f'data-id="{CAKE_ID}">Add to my order</button>')
    el("cake-msg-field").hidden = not qty
    update_date_min()


# ---------------------------------------------------------------- result panel
def set_status(text):
    el("status").textContent = text


def reset_result():
    """Hide the order message (used when the cart changes after the message was made)."""
    state.placed = False
    el("result").classList.remove("show")
    set_status("")
    el("imgbox").hidden = True
    el("copy-msg").textContent = "Copy message"


def format_date(iso):
    day = date.fromisoformat(iso)
    return f"{day:%A, %B} {day.day}"


@when("submit", "#order-form")
def make_message(event):
    """Customer submitted the form: check the inputs and build the order message."""
    global last_message, last_order, last_cart
    event.preventDefault()
    error = el("form-err")
    error.textContent = ""

    name = el("f-name").value.strip()
    contact = el("f-contact").value.strip()
    pickup_date = el("f-date").value
    pickup_time = el("f-time").value
    occasion = el("f-occ").value
    notes = el("f-notes").value.strip()

    if not cart.items:
        error.textContent = "Your order is empty. Add something from the menu first."
        return
    if not name:
        error.textContent = "Enter your name."
        el("f-name").focus()
        return
    if not contact:
        error.textContent = "Enter a Messenger name or mobile number so we can reach you."
        el("f-contact").focus()
        return
    if not pickup_date or pickup_date < el("f-date").min:
        if cart.qty(CAKE_ID):
            error.textContent = f"Pick a pickup date at least {CAKE_NOTICE_DAYS} days from today."
        else:
            error.textContent = "Pick a pickup date from today onward."
        el("f-date").focus()
        return

    lines = [f"- {qty} x {BY_ID[i]['name']} ({peso(qty * BY_ID[i]['price'])})" for i, qty in cart.items.items()]
    details = [
        f"Name: {name}",
        f"Contact: {contact}",
        f"Pickup: {format_date(pickup_date)}, {pickup_time}",
        f"Occasion: {occasion}",
    ]
    if cart.qty(CAKE_ID):
        details.append("Cake message: " + (el("f-cake").value.strip() or "Happy Birthday"))
    if notes:
        details.append(f"Notes: {notes}")

    total = peso(cart.total())
    last_message = "\n".join(
        ["Hi Dough & Demand! I'd like to order:", ""] + lines + ["", f"Total: {total}", ""] + details
    )
    last_order = {
        "lines": [(f"{qty} x {BY_ID[i]['name']}", peso(qty * BY_ID[i]["price"])) for i, qty in cart.items.items()],
        "total": total,
        "details": details,
    }
    last_cart = dict(cart.items)

    state.placed = True
    cart.clear()  # the order count goes back to 0

    el("result-text").textContent = last_message
    set_status("")
    el("imgbox").hidden = True
    el("copy-msg").textContent = "Copy message"
    el("result").classList.add("show")
    messenger = el("msgr")
    if MESSENGER_URL:
        messenger.href = MESSENGER_URL
        messenger.hidden = False
    else:
        messenger.hidden = True
    toast("Order message ready")
    scroll_to("result", "nearest")


@when("click", "#copy-msg")
async def copy_message(event):
    """Copy the order message to the clipboard."""
    from pyscript import window
    try:
        await window.navigator.clipboard.writeText(last_message)
        set_status("✓ Message copied. Paste it in Messenger and send it to our page to confirm your order.")
        el("copy-msg").textContent = "Copied ✓"
        toast("Message copied")
    except Exception:
        # Some browsers block clipboard access: select the text so the customer can copy it by hand
        box = document.createRange()
        box.selectNodeContents(el("result-text"))
        selection = window.getSelection()
        selection.removeAllRanges()
        selection.addRange(box)
        set_status("Message selected below. Copy it with your keyboard or phone menu, then send it to our page.")


@when("click", "#edit-order")
def edit_order(event):
    """Put the order back in the cart so the customer can change it."""
    cart.replace(last_cart)
    reset_result()
    cart.notify()
    scroll_to("order")
    toast("Your order is back. Make changes, then make the message again.")


# ---------------------------------------------------------------- save as image
def wrap_text(ctx, text, max_width):
    """Split text into lines that fit inside max_width."""
    lines, current = [], ""
    for word in text.split(" "):
        attempt = f"{current} {word}" if current else word
        if ctx.measureText(attempt).width > max_width and current:
            lines.append(current)
            current = word
        else:
            current = attempt
    if current:
        lines.append(current)
    return lines


def draw_receipt(ctx, width, height):
    """Draw the order as a picture. Call once with height=0 to measure, then again to draw."""
    pad = 48
    inner = width - pad * 2
    y = pad + 10
    ink, muted, line, accent = "#2f1d13", "#6f5a49", "#e7d6c2", "#c8325b"

    if height:
        ctx.fillStyle = "#fbf4ea"
        ctx.fillRect(0, 0, width, height)
        ctx.fillStyle = accent
        ctx.fillRect(0, 0, width, 14)

    ctx.textBaseline = "top"
    ctx.textAlign = "left"
    ctx.font = '800 46px "Bricolage Grotesque",Figtree,sans-serif'
    ctx.fillStyle = ink
    ctx.fillText("Dough & Demand", pad, y)
    y += 64
    ctx.font = "600 24px Figtree,sans-serif"
    ctx.fillStyle = muted
    ctx.fillText("Order message", pad, y)
    y += 44

    def rule():
        nonlocal y
        ctx.fillStyle = line
        ctx.fillRect(pad, y, inner, 3)
        y += 22

    rule()
    ctx.font = "600 28px Figtree,sans-serif"
    for label, amount in last_order["lines"]:
        ctx.fillStyle = ink
        for index, text in enumerate(wrap_text(ctx, label, inner - 170)):
            ctx.textAlign = "left"
            ctx.fillText(text, pad, y)
            if index == 0:
                ctx.textAlign = "right"
                ctx.fillText(amount, width - pad, y)
                ctx.textAlign = "left"
            y += 38
        y += 6
    rule()

    ctx.font = "800 34px Figtree,sans-serif"
    ctx.fillStyle = ink
    ctx.textAlign = "left"
    ctx.fillText("Total", pad, y)
    ctx.textAlign = "right"
    ctx.fillText(last_order["total"], width - pad, y)
    ctx.textAlign = "left"
    y += 62

    ctx.font = "500 26px Figtree,sans-serif"
    ctx.fillStyle = ink
    for detail in last_order["details"]:
        for text in wrap_text(ctx, detail, inner):
            ctx.fillText(text, pad, y)
            y += 36
        y += 4

    y += 14
    ctx.font = "700 24px Figtree,sans-serif"
    ctx.fillStyle = accent
    for text in wrap_text(ctx, "Send this to our Facebook page to confirm your order.", inner):
        ctx.fillText(text, pad, y)
        y += 34
    return y + pad


def make_image():
    """Return the receipt as a JPG data URL."""
    width = 900
    measure = document.createElement("canvas")
    measure.width, measure.height = width, 10
    height = math.ceil(draw_receipt(measure.getContext("2d"), width, 0))
    canvas = document.createElement("canvas")
    canvas.width, canvas.height = width, height
    draw_receipt(canvas.getContext("2d"), width, height)
    return canvas.toDataURL("image/jpeg", 0.92)


@when("click", "#save-img")
def save_image(event):
    """Make the receipt image. Browsers cannot always download directly, so show it to press-and-hold."""
    if last_order is None:
        return
    try:
        el("receipt-img").src = make_image()
        el("imgbox").hidden = False
        set_status("✓ Image ready below. Press and hold it to save, then send it to our page to confirm your order.")
        toast("Image ready")
        el("imgbox").scrollIntoView(js_obj({"behavior": "smooth", "block": "nearest"}))
    except Exception:
        set_status("Could not make the image. Use Copy message instead.")


# ---------------------------------------------------------------- wiring
cart.subscribe(render_cake)
cart.on_user_change(lambda: reset_result() if state.placed else None)
