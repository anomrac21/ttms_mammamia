#!/usr/bin/env python3
"""Generate Hugo menu content from MammaMia 2026 menu data."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1] / "content"

ICON = {
    "antipasti": "https://cdn.ttmenus.com/icons/food/icon-salads.webp",
    "pasta": "https://cdn.ttmenus.com/icons/food/icon-pasta.webp",
    "mains": "https://cdn.ttmenus.com/icons/food/icon-beef.webp",
    "pizza": "https://cdn.ttmenus.com/icons/food/icon-pizza.webp",
    "pizza_rosse": "https://cdn.ttmenus.com/icons/food/icon-sauce.webp",
    "pizza_seafood": "https://cdn.ttmenus.com/icons/food/icon-shrimp.webp",
    "breakfast": "https://cdn.ttmenus.com/icons/food/icon-eggs.webp",
    "lunch": "https://cdn.ttmenus.com/icons/food/icon-lunchspecial.webp",
    "drinks": "https://cdn.ttmenus.com/icons/drink/icon-drinks.webp",
    "wine": "https://cdn.ttmenus.com/icons/drink/icon-wine.webp",
    "beer": "https://cdn.ttmenus.com/icons/drink/icon-beerglass.webp",
    "kids": "https://cdn.ttmenus.com/icons/activities/icon-joystick.svg",
}

SECTIONS = [
    ("antipasti-salads", "Antipasti & Salads", 1, ICON["antipasti"],
     "Starters, soups, and salads with house vinaigrette."),
    ("pasta", "Pasta (Fatta a Mano)", 2, ICON["pasta"],
     "Handmade pasta — cooked al dente the Italian way."),
    ("secondi-burgers", "Secondi Piatti & Burgers", 3, ICON["mains"],
     "Mains, steaks, seafood, and handmade burgers with house chips."),
    ("pizza", "Pizza", 4, ICON["pizza"],
     "Classic, white, meat, and seafood pizzas from our wood-fired oven."),
    ("pizza-rosse", "Pizza Rosse", 5, ICON["pizza_rosse"],
     "Red pizzas with tomato sauce."),
    ("pizza-seafood-special", "Seafood & Special Pizza", 6, ICON["pizza_seafood"],
     "Seafood red pizzas, calzone-style favourites, and the Vulcano."),
    ("kids", "Kids Corner", 7, ICON["kids"],
     "Per i più piccoli — pasta, pizza shapes, and sliders."),
    ("breakfast-panini", "Breakfast & Panini", 8, ICON["breakfast"],
     "Farm-fresh eggs and panini, served 10am–5pm."),
    ("special-lunch", "Special Lunch", 9, ICON["lunch"],
     "Weekday lunch specials, Mon–Fri 11am–3pm."),
    ("drinks-desserts", "Drinks & Desserts", 10, ICON["drinks"],
     "Soft drinks, smoothies, house desserts, and caffetteria."),
    ("wines", "Wine List", 11, ICON["wine"],
     "Imported Italian wines — glass and bottle."),
    ("beer", "Beer", 12, ICON["beer"],
     "Premium Italian and European beers."),
]

# slug, title, description, tags, types, prices: [(v1, v2, price), ...]
Item = tuple[str, str, str, list[str], list[str], list[tuple[str, str, int]]]

def slugify(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")

def yaml_list(key: str, values: list[str], indent: int = 0) -> str:
    pad = " " * indent
    if not values:
        return f"{pad}{key}: []"
    lines = [f"{pad}{key}:"]
    for v in values:
        lines.append(f'{pad}  - {v}')
    return "\n".join(lines)

def render_item(item: Item, weight: int) -> str:
    slug, title, body, tags, types, prices = item
    lines = [
        "---",
        f"title: {title}",
        f"weight: {weight}",
        "prices:",
    ]
    for v1, v2, price in prices:
        lines.append(f'  - variable1: "{v1}"')
        lines.append(f'    variable2: "{v2}"')
        lines.append(f"    price: {price}")
    lines.append(yaml_list("tags", tags))
    lines.append(yaml_list("types", types))
    lines.append("additions: []")
    lines.append("modifications: []")
    lines.append("side_categories: []")
    lines.append("---")
    lines.append("")
    if body:
        lines.append(body)
        lines.append("")
    return "\n".join(lines)

def write_section(section_slug: str, title: str, weight: int, icon: str, desc: str, items: list[Item]) -> None:
    section_dir = ROOT / section_slug
    section_dir.mkdir(parents=True, exist_ok=True)
    index = f"""---
title: {title}
weight: {weight}
icon: {icon}
---

{desc}
"""
    (section_dir / "_index.md").write_text(index, encoding="utf-8")
    for i, item in enumerate(items, start=1):
        (section_dir / f"{slugify(item[0])}.md").write_text(render_item(item, i), encoding="utf-8")

ITEMS: dict[str, list[Item]] = {}

def I(slug, title, body, tags, types, price):
    return (slug, title, body, tags, types, [("-", "-", price)])

def V(slug, title, body, tags, types, *variants):
    return (slug, title, body, tags, types, list(variants))

# --- ANTIPASTI & SALADS ---
ITEMS["antipasti-salads"] = [
    I("bruschetta-pomodoro", "Bruschetta al Pomodoro",
      "2 slices house bread with fresh tomatoes, oregano, and basil.",
      ["Starter", "Vegetarian"], ["Starter"], 32),
    I("crostini", "Crostini",
      "2 slices house bread — one with grilled zucchini, mozzarella, oregano and basil; one with mushroom & mozzarella.",
      ["Starter", "Vegetarian"], ["Starter"], 44),
    I("caprese", "Caprese",
      "Slices of mozzarella and fresh tomato, extra virgin olive oil, balsamic vinegar, basil.",
      ["Starter", "Vegetarian"], ["Starter"], 59),
    I("impepata-cozze", "Impepata di Cozze",
      "Peppered (black) mussels and clams in extra virgin olive oil, parsley, flaked pepper garlic. Served with toasted house bread.",
      ["Starter", "Seafood"], ["Starter"], 152),
    I("salmone-affumicato", "Salmone Affumicato",
      "2 slices house bread, smoked salmon with arugula and goat cheese.",
      ["Starter", "Seafood"], ["Starter"], 98),
    I("tartara-tonno", "Tartara di Tonno",
      "Yellowfin tuna tartare seasoned with extra virgin olive oil and fresh herbs on thinly sliced potato crisps.",
      ["Starter", "Seafood"], ["Starter"], 104),
    I("zuppa-zucca", "Zuppa di Zucca",
      "Heartwarming pumpkin soup with toasted pumpkin seed. Served with homemade bread.",
      ["Starter", "Soup", "Vegetarian"], ["Starter"], 52),
    I("polpetta-mac-cheese", "Polpetta di Mac & Cheese",
      "Golden crisp four cheese ball delights.",
      ["Starter", "Vegetarian"], ["Starter"], 58),
    I("lite-salad", "Lite Salad",
      "Gourmet lettuce, cabbage, carrot, tomato, corn. Served with house vinaigrette.",
      ["Salad", "Vegetarian"], ["Starter"], 48),
    I("pollo-salad", "Pollo Salad",
      "Gourmet lettuce, arugula, carrot, tomato, black olives, grapes, chicken, mushroom, corn.",
      ["Salad"], ["Starter"], 82),
    I("salmone-salad", "Salmone Salad",
      "Gourmet lettuce, arugula, black olives, smoked salmon, zucchini, balsamic pearl, pineapple, grapes.",
      ["Salad", "Seafood"], ["Starter"], 149),
    I("warm-lentil", "Warm Lentil",
      "Earthy lentils served on a bed of mixed greens.",
      ["Salad", "Vegetarian"], ["Starter"], 58),
    I("wild-greens", "Wild Greens",
      "Gourmet lettuce mix, cranberries, pickled pumpkin, and roasted walnuts.",
      ["Salad", "Vegetarian"], ["Starter"], 58),
    I("couscous", "Couscous",
      "Tender couscous served on a bed of mixed greens.",
      ["Salad", "Vegetarian"], ["Starter"], 58),
    I("quinoa-bowl", "Quinoa Bowl",
      "Quinoa, chickpeas, cherry tomatoes, spinach, cucumber, black olives, pickled red onion. Served with tangy Greek yogurt or vinaigrette.",
      ["Salad", "Vegetarian"], ["Starter"], 62),
    V("salad-add-ons", "Salad Add-Ons", "Add protein to any salad.",
      ["Salad"], ["Side"],
      ("Grilled Salmon Steak", "-", 98),
      ("Grilled Shrimp", "-", 45),
      ("Grilled Fish", "-", 25),
      ("Grilled Chicken", "-", 28),
      ("Grilled Goat Cheese", "-", 34)),
]

# --- PASTA ---
ITEMS["pasta"] = [
    I("ravioli-carne-mascarpone", "Ravioli di Carne e Mascarpone",
      "Ravioli filled with minced beef and mascarpone cheese served in pink sauce.",
      ["Pasta", "Meat"], ["Main"], 155),
    I("beef-lasagna", "Beef Lasagna",
      "Layers of homemade pasta, ragù, béchamel, parmesan and mozzarella.",
      ["Pasta", "Meat"], ["Main"], 114),
    V("pappardelle-ragu", "Pappardelle al Ragù",
      "Hearty ragù, cream, parmesan cheese.",
      ["Pasta", "Meat"], ["Main"],
      ("Minced Beef Ragù", "-", 136),
      ("Pulled Lamb Ragù", "-", 152)),
    V("gnocchi", "Gnocchi",
      "Potato gnocchi in hearty ragù and parmesan cheese.",
      ["Pasta"], ["Main"],
      ("Minced Beef Ragù", "-", 104),
      ("Pulled Lamb Ragù", "-", 122),
      ("Cheese (cream, gorgonzola, parmesan)", "-", 118)),
    I("tagliatelle-pollo-toscano", "Tagliatelle al Pollo Toscano",
      "Roasted chicken, cream, spinach, parmesan cheese, cherry tomato.",
      ["Pasta", "Poultry"], ["Main"], 144),
    I("tagliatelle-pollo-formaggio", "Tagliatelle Pollo e Formaggio",
      "Chicken, cream, parsley, parmesan cheese.",
      ["Pasta", "Poultry"], ["Main"], 136),
    I("tagliatelle-pollo-peperoni", "Tagliatelle Pollo e Peperoni",
      "Chicken, mushroom, sweet peppers, cream, parsley, black pepper, parmesan cheese.",
      ["Pasta", "Poultry"], ["Main"], 142),
    I("tagliatelle-salsiccia-funghi", "Tagliatelle Salsiccia e Funghi",
      "Sausage, mushroom, fresh tomato, cream, parmesan cheese, parsley.",
      ["Pasta", "Meat"], ["Main"], 150),
    I("ravioli-ricotta", "Ravioli Ricotta",
      "Ravioli filled with spinach & ricotta, parmesan in creamy sauce topped with roasted walnuts.",
      ["Pasta", "Vegetarian"], ["Main"], 148),
    I("tagliatelle-vegetariane", "Tagliatelle Vegetariane",
      "Fresh tomato, sweet peppers, zucchini, mushroom, black olives and green peas.",
      ["Pasta", "Vegetarian"], ["Main"], 114),
    I("spaghetti-pomodoro", "Spaghetti al Pomodoro",
      "Fresh tomato, extra virgin olive oil.",
      ["Pasta", "Vegetarian"], ["Main"], 80),
    I("parmigiana-melanzane", "Parmigiana di Melanzane",
      "Layers of roasted eggplant, tomato sauce, mozzarella, basil & parmesan with side salad.",
      ["Pasta", "Vegetarian"], ["Main"], 94),
    I("pasta-di-mare", "Pasta di Mare",
      "Spaghetti, shrimp, mussels, white fish, calamari, lobster in tomato sauce.",
      ["Pasta", "Seafood"], ["Main"], 242),
    I("ravioli-pesce", "Ravioli di Pesce",
      "Ravioli filled with shrimp, white fish, ricotta in marinara sauce.",
      ["Pasta", "Seafood"], ["Main"], 175),
    I("tagliatelle-salmone", "Tagliatelle Salmone",
      "Smoked salmon, gorgonzola dop, chive, cream, red onion.",
      ["Pasta", "Seafood"], ["Main"], 168),
    I("tagliatelle-mammamia", "Tagliatelle Mammamia!",
      "Shrimp, mushroom, spinach, cream, parmesan cheese, onion.",
      ["Pasta", "Seafood"], ["Main"], 168),
    V("pasta-bimbo", "Pasta Bimbo",
      "Half portion short pasta — mozzarella cheese or pink sauce. Add bacon or chicken +14.",
      ["Pasta", "Kids"], ["Main"],
      ("Mozzarella or Pink Sauce", "-", 48)),
]

# --- SECONDI & BURGERS ---
ITEMS["secondi-burgers"] = [
    I("il-siciliano", "Il Siciliano",
      "9 oz premium beef patty with fresh tomato, lettuce, marinated eggplant, pickled onions & gouda on herb-infused buttered bun. House chips.",
      ["Burger", "Meat"], ["Main"], 109),
    I("il-padrino", "Il Padrino (The Godfather)",
      "9 oz premium beef patty with fresh tomato, lettuce, gouda, pickled onion on herb-infused buttered bun. Bacon optional (pork or turkey).",
      ["Burger", "Meat"], ["Main"], 109),
    I("il-pastore", "Il Pastore (The Shepherd)",
      "9 oz premium juicy lamb patty with fresh tomato, lettuce, cucumber, onion, tomato on mint aioli. Herb-infused buttered bun.",
      ["Burger", "Meat"], ["Main"], 118),
    I("mamma-burger", "Mamma Burger (Vegetarian)",
      "Blend of black beans, lentils & corn with sweet caramelized onion, lettuce, tomatoes and marinara on house-made bun.",
      ["Burger", "Vegetarian"], ["Main"], 89),
    V("burger-add-ons", "Burger Add-Ons", "",
      ["Burger"], ["Side"],
      ("Sauté Mushroom", "-", 14),
      ("Bacon", "-", 14),
      ("Cheese", "-", 10),
      ("Egg", "-", 8)),
    I("bistecca-manzo", "Bistecca di Manzo",
      "Ribeye steak (14 oz) with baked/mashed potato, mushroom, spinach & cherry tomato.",
      ["Steak", "Meat"], ["Main"], 354),
    I("coste-agnello", "Coste di Agnello",
      "Lamb rack (4) with mashed potato and vegetable medley.",
      ["Lamb", "Meat"], ["Main"], 259),
    I("stinco-agnello", "Stinco di Agnello",
      "Lamb shank with mashed potato and vegetable medley.",
      ["Lamb", "Meat"], ["Main"], 249),
    I("pollo-arrosto", "Pollo Arrosto",
      "Half chicken marinated in herbs and rosemary butter, slowly roasted. Creamy mashed potato, tomato confit.",
      ["Poultry"], ["Main"], 189),
    I("cotoletta-pollo", "Cotoletta di Pollo",
      "Panko breaded chicken breast with herbed house mayo. Side of mixed salad or potato mashed/oven baked.",
      ["Poultry"], ["Main"], 138),
    I("grilled-salmon-fillet", "Grilled Salmon Fillet",
      "Oven baked/mashed potato, mushroom, spinach & cherry tomato.",
      ["Seafood"], ["Main"], 246),
    I("tuscan-chicken", "Tuscan Chicken",
      "Herb marinated grilled chicken, sundried tomatoes, cherry tomatoes, spinach, cream, parmesan. Herb parsley rice and side salad.",
      ["Poultry"], ["Main"], 144),
    I("zuppa-di-mare", "Zuppa di Mare",
      "Seafood soup in mild spicy tomato sauce — shrimp, mussels, whitefish, calamari, lobster. Housemade bread.",
      ["Seafood", "Soup"], ["Main"], 228),
]

# --- PIZZA (classics, bianche, carne, pesce white) ---
PIZZA_BASE = ["Pizza"]
pizza_items = [
    ("classico", "Classico", "Tomato sauce, mozzarella, ham, mushroom.", 114),
    ("vegetariano", "Vegetariano", "Tomato sauce, mozzarella, mushroom, artichoke, sweet peppers, onion, black olives.", 114),
    ("fuoco", "Fuoco", "Tomato sauce, mozzarella, salami, onion, hot sauce, jalapeño.", 114),
    ("maialona", "Maialona", "Mozzarella, spicy sausage, mortadella, ham.", 128),
    ("peperino", "Peperino", "Tomato sauce, mozzarella, gorgonzola, sweet peppers, chicken.", 128),
    ("focaccia", "Focaccia", "White pizza drizzled with olive oil and rosemary sea salt. No tomato sauce.", 50),
    ("campagnola", "Campagnola", "Mozzarella, sweet peppers, mushroom, artichoke, garlic oil.", 118),
    ("quattro-formaggi-bianca", "4 Formaggi Bianca", "Mozzarella, goat cheese, gorgonzola, parmesan. No tomato sauce.", 135),
    ("tricolore", "Tricolore", "Mozzarella, spinach, fresh mozzarella, fresh tomato.", 148),
    ("coccodé", "Coccodé", "Mozzarella, chicken, black olives, mushroom.", 109),
    ("carbonara", "Carbonara", "Mozzarella, pancetta, red onion, eggs, parmesan & pecorino, black pepper.", 150),
    ("gallina", "Gallina", "Mozzarella, chicken, corn.", 105),
    ("pesto", "Pesto", "Mozzarella, pesto sauce, bacon, goat cheese, fresh tomato.", 150),
    ("marina-05", "05 Marina", "Mozzarella, shrimp, sweet peppers, grapes.", 138),
    ("ss-carina", "S.S. Carina", "Mozzarella, smoked salmon, black olives, arugula, fresh tomato.", 144),
    ("piccante", "Piccante", "Mozzarella, shrimp, pepper flakes, garlic oil, sweet pepper, red onion.", 145),
    ("rocket", "Rocket", "Mozzarella, smoked salmon, zucchini, arugula, cherry tomato, parmesan, lemon, olive oil.", 160),
]
ITEMS["pizza"] = [
    I(slug, title, desc, PIZZA_BASE + (["Vegetarian"] if "Veget" in title or slug == "focaccia" else []), ["Main"], price)
    for slug, title, desc, price in pizza_items
]

# --- PIZZA ROSSE ---
rosse = [
    ("caprina", "Caprina", "Tomato sauce, goat cheese, gorgonzola, zucchini, mushroom, onion.", 130),
    ("cinque-formaggi", "Cinque Formaggi", "Tomato sauce, mozzarella, gorgonzola, goat cheese, parmesan, mascarpone.", 155),
    ("marinara", "Marinara", "Tomato sauce, oregano, basil, garlic oil.", 70),
    ("margherita", "Margherita", "Tomato sauce, mozzarella.", 75),
    ("veggy", "Veggy", "Tomato sauce, mozzarella, fresh tomato, artichoke, sweet peppers, black olives, mushroom, onion.", 140),
    ("capricciosa", "Capricciosa", "Tomato sauce, mozzarella, ham, black olives, artichoke, mushroom.", 136),
    ("contadina", "Contadina", "Tomato sauce, mozzarella, chicken, zucchini, onion, mushroom, sweet peppers, corn.", 140),
    ("cow-boy", "Cow-Boy", "Tomato sauce, mozzarella, salami, bacon, mushroom, sweet peppers, parmesan.", 140),
    ("diavola", "Diavola", "Spicy: tomato sauce, mozzarella, spicy salami, spicy oil.", 120),
    ("prosciutto", "Prosciutto", "Tomato sauce, mozzarella, prosciutto.", 140),
    ("prosciutto-funghi", "Prosciutto & Funghi", "Tomato sauce, mozzarella, prosciutto, mushroom.", 144),
    ("ham", "Ham", "Tomato sauce, mozzarella, ham.", 112),
    ("ham-funghi", "Ham & Funghi", "Tomato sauce, mozzarella, ham, mushroom.", 115),
    ("hannibal", "Hannibal", "Tomato sauce, mozzarella, mortadella, salami, bacon, ham.", 158),
    ("hawaii", "Hawaii", "Tomato sauce, mozzarella, ham, pineapple.", 114),
    ("inferno", "Inferno", "Hot & spicy: tomato sauce, mozzarella, spicy sausage, onion, jalapeño, hot sauce.", 124),
    ("meat-forever", "Meat Forever", "Tomato sauce, mozzarella, ham, salami, bacon, spicy sausage, chicken.", 164),
    ("paella", "Paella", "Tomato sauce, mozzarella, chicken, mushroom, sweet peppers, zucchini, shrimp, pine.", 189),
    ("pepperoni", "Pepperoni", "Tomato sauce, mozzarella, pepperoni.", 105),
    ("pollo", "Pollo", "Tomato sauce, mozzarella, chicken, pineapple.", 110),
    ("primavera", "Primavera", "Tomato sauce, mozzarella, arugula, prosciutto, fresh tomato, mascarpone.", 142),
    ("quattro-stagioni", "Quattro Stagioni", "Tomato sauce, mozzarella, salami, ham, mushroom, artichoke.", 138),
    ("rustica", "Rustica", "Tomato sauce, mozzarella, spicy sausage, salami, onion, black olives.", 142),
    ("salame", "Salame", "Tomato sauce, mozzarella, salami.", 108),
    ("amore-in-citta", "Amore in Città", "Tomato sauce, mozzarella, chicken, ham, pineapple.", 134),
    ("mammamia-pizza", "Mammamia", "Tomato sauce, mozzarella, mascarpone, mushroom, spicy sausage.", 154),
]
ITEMS["pizza-rosse"] = [
    I(slug, title, desc, PIZZA_BASE, ["Main"], price) for slug, title, desc, price in rosse
]

# --- SEAFOOD & SPECIAL ---
seafood_special = [
    ("scoglio", "Scoglio", "Tomato sauce, shrimp, mussel, white fish, calamari, lobster.", 224),
    ("diamante", "Diamante", "Tomato sauce, mozzarella, smoked salmon, balsamic glaze, goat cheese.", 214),
    ("gamberetti", "Gamberetti", "Tomato sauce, mozzarella, shrimp, zucchini.", 150),
    ("mare-monti", "Mare & Monti", "Tomato sauce, mozzarella, smoked salmon, shrimp, artichoke, mushroom.", 198),
    ("napoli", "Napoli", "Tomato sauce, mozzarella, anchovies, oregano, garlic oil, basil.", 105),
    ("oceano", "Oceano", "Tomato sauce, mozzarella, smoked salmon, shrimp, zucchini, black olives, pine.", 188),
    ("siciliana", "Siciliana", "Tomato sauce, mozzarella, anchovies, capers, black olives, oregano.", 120),
    ("tobago", "Tobago", "Tomato sauce, mozzarella, shrimp, jalapeño, pepper flake, pineapple.", 144),
    ("trinidad", "Trinidad", "Tomato sauce, mozzarella, smoked salmon, capers, anchovies.", 150),
    ("vulcano", "Vulcano", "Double dough volcano shape with tomato sauce, mozzarella, ham, spicy sausage, salami, onion. Served with flame (* not for takeaway).", 195),
    ("slider-pizza", "Slider", "3 oz beef burger patty with cheese, lettuce, tomato and house-made potato chips.", 35),
]
ITEMS["pizza-seafood-special"] = [
    I(slug, title, desc, PIZZA_BASE + (["Seafood"] if slug not in ("vulcano", "slider-pizza") else ["Burger"]), ["Main"], price)
    for slug, title, desc, price in seafood_special
]

# --- KIDS ---
ITEMS["kids"] = [
    I("kids-pizza", "Kids Pizza Shape",
      "Choose your shape: Topolino (mouse), Pesciolino (fish), Cuoricino (heart), Caramellina (candy). Tomato sauce & mozzarella plus 1 topping: ham, salami, chicken, mushroom, or spinach.",
      ["Kids", "Pizza"], ["Main"], 65),
    V("pizza-toppings-8", "Pizza Toppings ($8)", "Black olives, corn, cream, jalapeño, egg, capers, fresh tomatoes.",
      ["Kids", "Pizza"], ["Side"],
      ("Each topping", "-", 8)),
    V("pizza-toppings-18", "Pizza Toppings ($18)", "Arugula, bacon, artichoke, chicken, extra cheese, ham, mortadella, mushroom, parmesan, pineapple, salami, sweet peppers, zucchini, anchovy.",
      ["Kids", "Pizza"], ["Side"],
      ("Each topping", "-", 18)),
    V("pizza-toppings-24", "Pizza Toppings ($24)", "Gorgonzola, mascarpone, prosciutto crudo, shrimp, smoked salmon, spicy sausage, fresh mozzarella, goat cheese.",
      ["Kids", "Pizza"], ["Side"],
      ("Each topping", "-", 24)),
]

# --- BREAKFAST & PANINI ---
ITEMS["breakfast-panini"] = [
    V("eggs-any-way", "Eggs Any Way", "Choose pork or turkey bacon & toast.",
      ["Breakfast"], ["Main"],
      ("Poached", "-", 75),
      ("Scrambled", "-", 70),
      ("Over Easy", "-", 70),
      ("Sunny Side", "-", 70),
      ("Omelette", "-", 75)),
    I("dutch-baby", "Dutch Baby", "Golden brown baked European pancake topped with fresh fruit compote and Devonshire cream.", ["Breakfast"], ["Main"], 95),
    I("egg-benedict", "Egg Benedict", "Rustic house baked bread, fresh spinach, smoked salmon, poached eggs, house Hollandaise.", ["Breakfast"], ["Main"], 122),
    I("steak-and-eggs", "Steak and Eggs", "Marinated steak, sunny side eggs, potatoes & side salad.", ["Breakfast"], ["Main"], 116),
    I("english-fry-up", "Classic English Fry Up", "Baked beans, roasted tomatoes, sunny side eggs, spicy sausage, bacon, mushroom and potatoes. Toast.", ["Breakfast"], ["Main"], 120),
    I("pancakes", "Pancakes", "Three house-made buttermilk pancakes with Devonshire cream, berry compote and syrup.", ["Breakfast"], ["Main"], 60),
    I("french-toast", "French Toast", "Rustic house baked Italian bread with fresh fruit and Devonshire cream, berry compote.", ["Breakfast"], ["Main"], 74),
    I("eggs-in-purgatory", "Eggs in Purgatory", "Tomato sauce, onion, eggs, mild spicy, parmesan, rustic slice house bread. Add mozzarella or pepper jack +15.", ["Breakfast"], ["Main"], 74),
    V("breakfast-coffee", "Breakfast Coffee", "Hausbrandt coffee.",
      ["Breakfast", "Coffee"], ["Beverage"],
      ("Espresso", "-", 18),
      ("Double Espresso", "-", 25),
      ("Caffè Latte", "-", 24),
      ("Americano", "-", 18),
      ("Cappuccino Reg.", "-", 20),
      ("Cappuccino Large (double shot)", "-", 30),
      ("Cappuccino To Go", "-", 20),
      ("Cappuccino Shakerato (cold)", "-", 25),
      ("Hot Chocolate", "-", 22),
      ("Tea Selection", "-", 18),
      ("Extra Shot", "-", 9)),
    I("pollo-blt-panini", "Pollo BLT Panini", "Grilled chicken breast, crispy bacon, tomatoes, lettuce & garlic aioli. In-house chips or salad.", ["Panini"], ["Main"], 58),
    I("caprese-panini", "Caprese Panini", "Fresh mozzarella and tomatoes with basil and olive oil.", ["Panini", "Vegetarian"], ["Main"], 58),
    I("fish-panini", "Fish Panini", "White fish with mayo, pineapple, basil pesto, onion.", ["Panini", "Seafood"], ["Main"], 55),
    I("steak-panini", "Steak Panini", "Grilled steak with caramelized onions, dried tomatoes, cheese and house steak sauce.", ["Panini", "Meat"], ["Main"], 70),
    I("slider-panini", "Slider Panini", "2 × 3 oz beef burgers with cheese, lettuce, tomato and house potato chips.", ["Panini"], ["Main"], 64),
    I("giardino-panini", "Giardino Panini", "Grilled veggy with caramelized onion.", ["Panini", "Vegetarian"], ["Main"], 55),
    I("slider-shrimp-panini", "Slider Shrimp Panini", "Shrimp in saffron mayo on 2 brioche buns, lettuce & side salad.", ["Panini", "Seafood"], ["Main"], 55),
    I("shrimp-panini", "Shrimp Panini", "Grilled shrimp, tomatoes, lettuce & garlic aioli.", ["Panini", "Seafood"], ["Main"], 70),
]

# --- SPECIAL LUNCH ---
ITEMS["special-lunch"] = [
    V("pizzetta-lunch", "Pizzetta Lunch Special", "Small pizza + bottle water. Mon–Fri 11am–3pm.",
      ["Lunch"], ["Main"],
      ("Salami & Bacon", "-", 60),
      ("Chicken & Corn", "-", 60),
      ("Veggy", "-", 60)),
    V("pasta-lunch", "Pasta Lunch Special", "Housemade fusilli + bottle water.",
      ["Lunch"], ["Main"],
      ("Chicken Tomato Mozzarella Garlic", "-", 60),
      ("Ham Mushroom Peas & Cream", "-", 60),
      ("Veggy", "-", 60),
      ("Ragù (beef)", "-", 75)),
    I("lunch-grilled-chicken-veg", "Grilled Chicken & Vegetable Medley", "Lunch special with bottle water — $99.", ["Lunch"], ["Main"], 99),
    I("lunch-grilled-fish-veg", "Grilled White Fish & Vegetable Medley", "Lunch special with bottle water — $99.", ["Lunch", "Seafood"], ["Main"], 99),
    I("lunch-tuscan-chicken", "Tuscan Chicken Lunch", "Herb marinated grilled chicken, sundried tomatoes, cherry tomatoes, spinach, cream, parmesan. Herb parsley rice — $99 with bottle water.", ["Lunch"], ["Main"], 99),
    I("lunch-shrimp-potatoes", "Grilled Shrimp & Pan Tossed Potatoes", "Red onions, house dressing — $75 with bottle water.", ["Lunch", "Seafood"], ["Main"], 75),
    I("lunch-chicken-potatoes", "Grilled Chicken & Pan Tossed Potatoes", "Red onions, house dressing — $75 with bottle water.", ["Lunch"], ["Main"], 75),
]

# --- DRINKS & DESSERTS ---
ITEMS["drinks-desserts"] = [
    V("italian-water-still", "Italian Bottle Water (Still)", "",
      ["Beverage"], ["Beverage"],
      ("0.5 L", "-", 18), ("0.75 L", "-", 38)),
    V("italian-water-sparkling", "Italian Bottle Water (Sparkling)", "",
      ["Beverage"], ["Beverage"],
      ("0.5 L", "-", 20), ("0.75 L", "-", 40)),
    I("san-pellegrino-arancia", "San Pellegrino Red Orange", "330ml.", ["Beverage"], ["Beverage"], 18),
    I("soft-drinks", "Coke / Diet Coke / Sprite / Club Soda", "By glass.", ["Beverage"], ["Beverage"], 10),
    I("juices", "Juices", "Orange or fruit punch by glass.", ["Beverage"], ["Beverage"], 15),
    I("llb", "LLB", "By glass.", ["Beverage"], ["Beverage"], 14),
    V("lemonade", "Lemonade / Flavored", "",
      ["Beverage"], ["Beverage"],
      ("Regular", "-", 18), ("Flavored", "-", 22)),
    I("smoothie", "Smoothie", "Strawberry, mango, colada, peach, or watermelon.", ["Beverage"], ["Beverage"], 42),
    I("tiramisu", "Tiramisù", "Coffee & cocoa.", ["Dessert"], ["Dessert"], 54),
    I("panna-cotta", "Panna Cotta", "", ["Dessert"], ["Dessert"], 40),
    V("gelato", "Gelato", "2 scoops.",
      ["Dessert"], ["Dessert"],
      ("Single scoop", "-", 28), ("2 scoops", "-", 40)),
    I("affogato", "Affogato al Caffè", "1 shot espresso & 1 scoop gelato.", ["Dessert", "Coffee"], ["Dessert"], 38),
    V("caffetteria", "Caffetteria", "",
      ["Coffee"], ["Beverage"],
      ("Espresso", "-", 18),
      ("Americano / Tea Selection", "-", 18),
      ("Cappuccino", "-", 20),
      ("Caffè Latte / Hot Chocolate", "-", 22),
      ("Extra Shot", "-", 9)),
    V("limoncello-grappa", "Limoncello & Grappa", "",
      ["Spirits"], ["Beverage"],
      ("Limoncello", "-", 44),
      ("Grappa", "-", 50)),
]

# --- WINES (glass / bottle from PDF) ---
WINES = [
    ("prosecco-il-soller", "Prosecco Superiore Il Soller", "Valdobbiadene DOCG Extra Dry. Fresh, delicate, hints of ripe fruit.", 90, 470),
    ("prosecco-ruiol-castei", "Prosecco Ruiol Castei", "Valdobbiadene Prosecco Superiore DOCG Extra Dry 2019.", 90, 495),
    ("prosecco-torri-credazzo", "Prosecco Torri di Credazzo", "Valdobbiadene Prosecco Superiore Millesimato DOCG Extra Dry.", None, 525),
    ("rose-primitivo-puglia", "Duca di Saragnano Rosato Puglia", "Primitivo IGT Rosato.", 65, 305),
    ("rose-vecciano-toscana", "Duca di Saragnano Vecciano Rosato", "Toscana Rosato IGT.", None, 305),
    ("white-levantae", "Duca di Saragnano Levantae Bianco", "Vino Bianco.", 65, 305),
    ("white-chardonnay-sicilia", "Barbanera Chardonnay Sicilia", "Terre Siciliane Vino Bianco.", 65, 305),
    ("white-fiano-salento", "Masso Antico Fiano del Salento", "IGT da uve legg. appassite.", 70, 315),
    ("white-casali-langhe", "Casali del Barone Langhe Chardonnay Arneis", "DOC white.", None, 335),
    ("white-vecciano-toscana", "Duca di Saragnano Vecciano Bianco", "Toscana Bianco IGT.", None, 330),
    ("red-sangiovese-toscana", "Duca di Saragnano Sangiovese", "Sangiovese di Toscana IGT.", 65, 300),
    ("red-opera", "Duca di Saragnano Operà Rosso", "Vino Rosso.", 65, 295),
    ("red-sir-passo", "Duca di Saragnano Sir Passo", "Toscana Rosso IGT.", 70, 310),
    ("red-governo-toscana", "Duca di Saragnano Governo", "Toscana Rosso IGT.", None, 305),
    ("red-aglianico-primitivo", "Duca di Saragnano Aglianico Primitivo", "Puglia IGT.", None, 325),
    ("red-passone", "Passone Rosso", "Vino ottenuto da uve appassite.", None, 395),
    ("red-ripasso-valpolicella", "Ripasso Valpolicella DOC", "", None, 315),
    ("red-primitivo-salento", "Masso Antico Primitivo del Salento", "IGT da uve legg. appassite.", None, 360),
    ("red-vecciano-toscana", "Duca di Saragnano Vecciano Rosso", "Toscana Rosso IGT.", None, 395),
    ("white-gigino", "Barbanera Gigino Bianco", "Toscana IGT.", None, 405),
    ("red-amarone", "Cantine Amarone della Valpolicella", "DOCG.", None, 495),
    ("red-gigino-rosso", "Barbanera Gigino Rosso", "Toscana IGT.", None, 545),
    ("red-gigino-grande", "Barbanera Gigino Grande Rosso", "Toscana IGT.", None, 610),
    ("red-il-potere", "Masso Antico Il Potere Rosso", "Puglia IGT.", None, 395),
    ("red-ngudra-primitivo", "Barbanera Ngudrà Primitivo", "Salento IGT.", None, 520),
]
ITEMS["wines"] = []
for slug, title, desc, glass, bottle in WINES:
    prices = []
    if glass:
        prices.append(("Glass", "-", glass))
    if bottle:
        prices.append(("Bottle", "-", bottle))
    if not prices:
        continue
    ITEMS["wines"].append((slug, title, desc, ["Wine", "Alcoholic"], ["Beverage"], prices))

ITEMS["beer"] = [
    I("pilsner", "Pilsner",
      "Pale and brilliant — dry finish with fresh malt and hops. Alcohol 5.0%. Serve 6–8°C.",
      ["Beer", "Alcoholic"], ["Beverage"], 42),
    I("vienna", "Vienna Lager",
      "Perfect balance of malt and hops. Fruity notes and hints of caramel. Alcohol 5.3%. Serve 8–10°C.",
      ["Beer", "Alcoholic"], ["Beverage"], 45),
    I("strong-ale", "Strong Ale",
      "Smooth flavour with hints of liquorice, nuts and coffee. Deep amber. Alcohol 8.5%.",
      ["Beer", "Alcoholic"], ["Beverage"], 45),
    I("pilsner-gluten-free", "Pilsner Gluten Free",
      "Premium lager taste, gluten-free unfiltered. Alcohol 4.9%.",
      ["Beer", "Alcoholic"], ["Beverage"], 46),
]

def main() -> None:
    for section_slug, title, weight, icon, desc in SECTIONS:
        items = ITEMS.get(section_slug, [])
        write_section(section_slug, title, weight, icon, desc, items)
        print(f"  {section_slug}: {len(items)} items")

    home = """---
title: "MammaMia"
image: /branding/favicon192.webp
images:
    - image: /branding/favicon192.webp
slideshow: []
---

<p>Benvenuti — authentic Italian restaurant & pizzeria at Grand Bazaar, Arima, Maraval, and Valpark. Handmade pasta, wood-fired pizza, and the full Italian experience.</p>
"""
    (ROOT / "_index.md").write_text(home, encoding="utf-8")
    print("Updated content/_index.md")

if __name__ == "__main__":
    print("Generating MammaMia menu content...")
    main()
    print("Done.")
