"""Small helpers shared by every module: DOM lookup, HTML escaping, toast, stepper buttons."""
import html

from js import Object
from pyodide.ffi import create_proxy, to_js
from pyscript import document, window

_toast_timer = None


def el(element_id):
    """Find an element by its id."""
    return document.getElementById(element_id)


def esc(text):
    """Escape text so it is safe to put inside HTML."""
    return html.escape(str(text), quote=True)


def js_obj(data):
    """Turn a Python dict into a plain JavaScript object."""
    return to_js(data, dict_converter=Object.fromEntries)


def scroll_to(element_id, block="start"):
    """Smoothly scroll an element into view (smooth scrolling is set in the CSS)."""
    el(element_id).scrollIntoView(js_obj({"behavior": "smooth", "block": block}))


def toast(message):
    """Show a short message at the bottom of the screen for about two seconds."""
    global _toast_timer
    box = el("toast")
    box.textContent = message
    box.classList.add("show")
    if _toast_timer is not None:
        window.clearTimeout(_toast_timer)
    _toast_timer = window.setTimeout(create_proxy(lambda *args: box.classList.remove("show")), 1800)


def stepper(item_id, qty, source):
    """The  -  1  +  buttons. `source` is "cart" or "combo" so the click knows where to apply."""
    return (
        '<span class="step">'
        f'<button type="button" data-a="dec" data-src="{source}" data-id="{item_id}" aria-label="Remove one">&minus;</button>'
        f"<span>{qty}</span>"
        f'<button type="button" data-a="inc" data-src="{source}" data-id="{item_id}" aria-label="Add one">+</button>'
        "</span>"
    )
