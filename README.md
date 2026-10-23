# Dough & Demand

A bakery website for students, built for the Event-Driven Programming final project
(CEBU EASTERN COLLEGE, College of Information Technology, Free Elective 1 business concept).

Customers can browse the menu, build a combo, add items to an order, and turn the order into a
message to send to the bakery's Facebook page. **All of the interactive behavior is written in
Python with PyScript.** There is no JavaScript logic in this project.

## Group members

- Concepcion, Jasper Joy H.
- Lapez, Shaina May M.
- Ordiz, Cherryl Faith D.
- Tangpos, Jhon Kevin
- Quinanola, Rohan

## How to run it in Visual Studio Code

PyScript loads the Python files with the browser, so the page must be served by a web server.
Double-clicking `index.html` will not work.

1. Open this folder in VS Code.
2. Install the **Live Server** extension (Ritwick Dey).
3. Right-click `index.html`, then choose **Open with Live Server**.
4. Wait a few seconds the first time. The browser downloads the Python runtime (internet needed).

No Live Server? In a terminal inside this folder run `python -m http.server 8000`, then open
`http://localhost:8000`.

## Project files

| File | What it does |
| --- | --- |
| `index.html` | The page structure (sections, forms, buttons) and the PyScript script tag |
| `style.css` | The design: colors, layout, mobile view, animations |
| `pyscript.toml` | PyScript settings: lists the Python files to load |
| `main.py` | Entry point. Imports every module and draws the page the first time |
| `menu_data.py` | Menu items, prices, categories, shop settings |
| `state.py` | Small shared state (selected category, whether an order message was made) |
| `helpers.py` | Shared helpers: find an element, escape text, toast message, +/- buttons |
| `cart.py` | The cart: items, quantities, totals, saving, and the observer list |
| `cart_ui.py` | Cart drawer, header counter, Add / + / - buttons, Escape key |
| `menu.py` | Category tabs and product cards |
| `combo.py` | Build-your-student-combo with the price meter |
| `order_form.py` | Mini cake, order form, order message, copy, save as image, edit order |
| `background.py` | Drifting bakery shapes in the background |
| `img/` | Product photos |

## Event-driven programming in this project

Each handler uses PyScript's `@when(event, selector)` decorator. The page waits for the customer
to do something, and the matching Python function runs.

| Event | Where | What happens |
| --- | --- | --- |
| `click` on a category tab | `menu.py` | Filters the menu cards |
| `click` on Add, +, - | `cart_ui.py`, `combo.py` | Changes quantities and updates totals |
| `click` on "Your order" / close / dark area | `cart_ui.py` | Opens and closes the cart drawer |
| `keydown` (Escape) | `cart_ui.py` | Closes the cart drawer |
| `click` on "Add combo to my order" | `combo.py` | Moves the combo into the cart |
| `submit` on the order form | `order_form.py` | Checks the inputs and builds the order message |
| `click` on Copy message | `order_form.py` | Copies the message to the clipboard |
| `click` on Save as image | `order_form.py` | Draws the order on a canvas and shows a JPG |
| `click` on Edit my order | `order_form.py` | Puts the order back in the cart |

**Observer pattern:** `cart.py` keeps a list of functions. When the cart changes it calls all of
them (`cart.subscribe(render_cart)`, `cart.subscribe(render_menu)`, ...), so the counter, drawer,
menu cards and order summary stay in sync without each handler updating everything by hand.

## Setting the Messenger button

Open `menu_data.py` and set `MESSENGER_URL` to the Facebook page link, for example
`"https://m.me/yourpagename"`. The "Open Messenger" button appears after an order message is made.

## Publishing on GitHub Pages (optional)

Push the folder to a public repository, then in the repository open **Settings > Pages**, choose the
`main` branch and the root folder, and save.
