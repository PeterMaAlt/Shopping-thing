import os
from colorama import Fore, Style, init
init(autoreset=True)
import json

settings_file = "settings.json"
# Load settings from file if it exists
if os.path.exists(settings_file):
    with open(settings_file, "r") as f:
        settings.update(json.load(f))


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

filename = "shopping_list.txt"
default_items = [
    "Milk 3.60 1",
    "Eggs 5.80 10",
    "Bread 18.5 3"
]

items = {}
settings = {
    "currency": None,
    "budget_limit": None,
    "red_budget": 100.0
}

def add_item(name, price, amount):
    if name in items:
        items[name]["amount"] += amount
        items[name]["price"] = price
    else:
        items[name] = {"price": price, "amount": amount}

def colorize_total(total):
    if not settings["red_budget"]:
        return f"{total:.2f}"
    ratio = total / settings["red_budget"]
    if ratio >= 1.0:
        return Fore.RED + f"{total:.2f}" + Style.RESET_ALL
    elif ratio >= 0.8:
        return Fore.YELLOW + f"{total:.2f}" + Style.RESET_ALL
    else:
        return f"{total:.2f}"

def colorize_item_cost(cost):
    if not settings["red_budget"]:
        return f"{cost:.2f}"
    ratio = cost / settings["red_budget"]
    if ratio >= 0.3:
        return Fore.RED + f"{cost:.2f}" + Style.RESET_ALL
    elif ratio >= 0.2:
        return Fore.YELLOW + f"{cost:.2f}" + Style.RESET_ALL
    else:
        return f"{cost:.2f}"

if not os.path.exists(filename):
    with open(filename, "w") as f:
        f.write("\n".join(default_items))

with open(filename, "r") as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            name, price, amount = parts[0], float(parts[1]), int(parts[2])
            items[name] = {"price": price, "amount": amount}

print("Welcome to the shopping thing!")
print("Press enter to continue...")
input()
clear_screen()

while True:
    print("What would you like to do?")
    print("--------------------------------")
    print("1 | View shopping list")
    print("2 | Add item to shopping list")
    print("3 | Clear shopping list")
    print("4 | Delete item from shopping list")
    print("s | Settings")
    print("q | Quit")
    print("--------------------------------")
    choice = input("Select an action: ").strip().lower()

    if choice == "1":
        clear_screen()
        print("Shopping list | Price | Amt | Total")
        print("-" * 40)
        total = 0
        for name, data in items.items():
            price = data["price"]
            amount = data["amount"]
            cost = price * amount
            total += cost
            cost_str = colorize_item_cost(cost)
            print(f" - {name:<12} {price:>6.2f}  {amount:>3}  {cost_str:>7}")
        print("-" * 40)
        currency = settings["currency"] or ""
        print(f"Total cost: {currency}{colorize_total(total)}")
        print("Press enter to return to menu...")
        input()
        clear_screen()

    elif choice == "2":
        clear_screen()
        name = input("Enter item name: ").strip()
        try:
            price = float(input("Enter item price: "))
            amount = int(input("Enter item amount: "))
        except ValueError:
            print("Invalid input. Price must be a number, amount must be an integer.")
            input("Press Enter to return to menu...")
            clear_screen()
            continue

        new_total = sum(data["price"] * data["amount"] for data in items.values()) + price * amount
        if settings["budget_limit"] and new_total > settings["budget_limit"]:
            print(f"Cannot add item. Total would exceed budget limit of {settings['budget_limit']}.")
            input("Press Enter to return to menu...")
            clear_screen()
            continue

        add_item(name, price, amount)
        print(f"Added {name} ({price:.2f} x {amount}) to your shopping list.")
        input("Press Enter to return to menu...")
        clear_screen()

    elif choice == "3":
        clear_screen()
        confirm = input("Are you sure you want to clear the shopping list? (y/n): ").strip().lower()
        if confirm == "y":
            items.clear()
            with open(filename, "w") as f:
                f.write("")
            print("Shopping list cleared.")
        else:
            print("Cancelled. Shopping list not cleared.")
        input("Press Enter to return to menu...")
        clear_screen()

    elif choice == "4":
        clear_screen()
        if not items:
            print("Your shopping list is empty.")
            input("Press Enter to return to menu...")
            clear_screen()
            continue

        print("Items in your shopping list:")
        for name in items:
            print(f" - {name}")
        name_to_delete = input("Enter the name of the item to delete: ").strip()

        if name_to_delete in items:
            confirm = input(f"Are you sure you want to delete '{name_to_delete}'? (y/n): ").strip().lower()
            if confirm != "y":
                print("Cancelled. Item not deleted.")
                input("Press Enter to return to menu...")
                clear_screen()
                continue
            del items[name_to_delete]
            print(f"'{name_to_delete}' has been removed from your shopping list.")
        else:
            print(f"'{name_to_delete}' not found in your shopping list.")

        input("Press Enter to return to menu...")
        clear_screen()

    elif choice == "s":
        clear_screen()
        print("Settings")
        print("-" * 40)
        print(f"1 | Currency symbol: {settings['currency'] or 'None'}")
        print(f"2 | Budget limit: {settings['budget_limit'] or 'None'}")
        print(f"3 | Red budget threshold: {settings['red_budget']}")
        print("b | Back to main menu")
        print("-" * 40)
        setting_choice = input("Select a setting to change: ").strip().lower()

        if setting_choice == "1":
            new_currency = input("Enter new currency symbol (or leave blank for none): ").strip()
            settings["currency"] = new_currency if new_currency else None
            print("Currency updated.")

        elif setting_choice == "2":
            try:
                new_limit = float(input("Enter budget limit (0 to disable): "))
                settings["budget_limit"] = new_limit if new_limit > 0 else None
                print("Budget limit updated.")
            except ValueError:
                print("Invalid number.")

        elif setting_choice == "3":
            try:
                new_red = float(input("Enter red budget threshold (e.g. 100): "))
                settings["red_budget"] = new_red
                print("Red budget threshold updated.")
            except ValueError:
                print("Invalid number.")

        input("Press Enter to return to menu...")
        clear_screen()

    elif choice == "q":
        with open(filename, "w") as f:
            for name, data in items.items():
                f.write(f"{name} {data['price']} {data['amount']}\n")
        print("Shopping list saved. Goodbye!")
        break
