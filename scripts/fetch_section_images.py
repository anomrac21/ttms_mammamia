#!/usr/bin/env python3
"""Update content/*/_index.md to icon + images.primary (client-owned assets)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
IMAGES_DIR = ROOT / "static" / "images"

SECTIONS: dict[str, str] = {
    "promotions": "mammamia-promo.webp",
    "antipasti-salads": "mammamia-antipasti.webp",
    "pasta": "mammamia-pasta.webp",
    "secondi-burgers": "mammamia-steak.webp",
    "pizza": "a-pizza-with-cheese-and-basil.webp",
    "pizza-rosse": "mammamia-pizza-rosse.webp",
    "pizza-seafood-special": "mammamia-seafood-pizza.webp",
    "kids": "mammamia-kids-pizza.webp",
    "breakfast-panini": "mammamia-breakfast.webp",
    "special-lunch": "mammamia-lunch.webp",
    "drinks-desserts": "mammamia-dessert.webp",
    "wines": "mammamia-wine.webp",
    "beer": "mammamia-beer.webp",
}


def img(name: str) -> str:
    return f"images/{name}"


def body_after_frontmatter(raw: str) -> str:
    if raw.count("---") < 2:
        return raw.strip()
    return raw.split("---", 2)[2].strip()


def update_section_index(section: str, image_file: str) -> None:
    path = CONTENT / section / "_index.md"
    if not path.exists():
        return
    raw = path.read_text(encoding="utf-8")
    title_m = re.search(r"^title:\s*(.+)$", raw, re.M)
    weight_m = re.search(r"^weight:\s*(.+)$", raw, re.M)
    title = title_m.group(1).strip() if title_m else section.replace("-", " ").title()
    weight = weight_m.group(1).strip().strip('"') if weight_m else "1"
    body = body_after_frontmatter(raw)

    lines = [
        "---",
        f"title: {title}",
        f"weight: {weight}",
        f"icon: {img(image_file)}",
        "images:",
        f"    primary: {img(image_file)}",
        "---",
    ]
    if body:
        lines.extend(["", body])
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def update_home_index() -> None:
    path = CONTENT / "_index.md"
    body = body_after_frontmatter(path.read_text(encoding="utf-8"))
    if not body.strip():
        body = (
            "<p>Benvenuti — authentic Italian restaurant & pizzeria at Grand Bazaar, "
            "Arima, Maraval, and Valpark. Handmade pasta, wood-fired pizza, and the full "
            "Italian experience.</p>"
        )
    text = (
        "---\n"
        'title: "MammaMia"\n'
        f"image: {img('a-pizza-with-cheese-and-basil.webp')}\n"
        "images:\n"
        f"    - image: {img('a-pizza-with-cheese-and-basil.webp')}\n"
        f"    - image: {img('mammamia-hero-spread.webp')}\n"
        "slideshow:\n"
        f"    - image: {img('mammamia-pasta.webp')}\n"
        f"    - image: {img('a-pizza-with-cheese-and-basil.webp')}\n"
        f"    - image: {img('mammamia-wine.webp')}\n"
        f"    - image: {img('mammamia-dessert.webp')}\n"
        "---"
    )
    text += f"\n\n{body}\n"
    path.write_text(text, encoding="utf-8")


def main() -> None:
    for section, image_file in SECTIONS.items():
        if (IMAGES_DIR / image_file).exists():
            update_section_index(section, image_file)
        else:
            print(f"WARN: missing {image_file} for {section}")

    update_home_index()

    credits = ["Client-owned section images:\n"] + [
        f"- {section} — {file}" for section, file in SECTIONS.items()
    ]
    credits.append("- Home slideshow uses mammamia-* and a-pizza-with-cheese-and-basil.webp")
    (IMAGES_DIR / "IMAGE_CREDITS.txt").write_text("\n".join(credits) + "\n", encoding="utf-8")
    print("Section headers updated.")


if __name__ == "__main__":
    main()
