"""Decorative background: faint line-art bakes that drift slowly upward (animation is in the CSS)."""
import random

from pyscript import document

from helpers import el

SHAPES = ["donut", "cupcake", "cookie", "loaf", "slice", "croissant"]
SVG_NS = "http://www.w3.org/2000/svg"
COUNT = 14


def init():
    box = el("bg")
    for i in range(COUNT):
        svg = document.createElementNS(SVG_NS, "svg")
        use = document.createElementNS(SVG_NS, "use")
        svg.setAttribute("viewBox", "0 0 64 64")
        use.setAttribute("href", "#i-" + SHAPES[i % len(SHAPES)])
        svg.appendChild(use)

        duration = 48 + random.random() * 48
        sign = -1 if random.random() < 0.5 else 1
        svg.setAttribute("class", "f" + (" a" if i % 3 == 0 else ""))
        svg.style.left = f"{i * 100 / COUNT + random.random() * 4}%"
        svg.style.width = f"{44 + round(random.random() * 44)}px"
        svg.style.setProperty("--dx", f"{round(random.random() * 160 - 80)}px")
        svg.style.setProperty("--rot", f"{sign * round(120 + random.random() * 200)}deg")
        svg.style.setProperty("--y0", f"{round(random.random() * 90)}vh")
        svg.style.setProperty("--r0", f"{round(random.random() * 60 - 30)}deg")
        svg.style.animationDuration = f"{duration}s"
        svg.style.animationDelay = f"-{random.random() * duration}s"
        box.appendChild(svg)
