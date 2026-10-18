import random
import sys
import questionary
import theme
import items
from factory import FACTORY_MACHINES
from functions import type_text, clear_console
from locations import LOCATIONS, RISKS

def roll_damage(player):
    health = player["health"]

    if health["hunger"] >= 100:
        health["hunger"] = 100
        health["hitpoints"] -= 10
        type_text(0.08, "You are [yellow]starving[/yellow]... you take [red]10 damage[/red].")

    check_death(player)

    if health["thirst"] >= 100:
        health["thirst"] = 100
        health["hitpoints"] -= 10
        type_text(0.08, "You are [yellow]dehydrated[/yellow]... you take [red]10 damage[/red].")

    check_death(player)

    if health["radiation"] > 0:
        health["hitpoints"] -= health["radiation"]
        type_text(0.08, f"You suffer from [yellow]radiation[/yellow] and take [red]{health['radiation']} radiation damage[/red].")

    check_death(player)

def check_death(player):
    if player["health"]["hitpoints"] <= 0:
        type_text(0.08, "You are [bold red]dead[/bold red]. Until next time... [red]scavenger[/red]...")
        sys.exit()

def get_hungry(player):
    health = player["health"]
    health["hunger"] = min(100, health["hunger"] + 5)
    health["thirst"] = min(100, health["thirst"] + 10)

def levelup(player):
    while player["xp"] >= player["level"] * 500:
        player["xp"] -= player["level"] * 500
        player["level"] += 1
        type_text(0.01, f"You reached [bold green]level {player['level']}[/bold green]!")

def scavenge(player):
    type_text(0.02, "You venture on a scavenger hunt.")
    type_text(0.15, "[bold red]. . .[/bold red]")

    random_locations = random.sample(list(LOCATIONS.keys()), 3)
    type_text(0.04, f"On your [bold blue]left[/bold blue], you see a [bold blue]{random_locations[0]}[/bold blue]")
    type_text(0.06, f"On your [bold blue]right[/bold blue], you see a [bold blue]{random_locations[1]}[/bold blue]")
    type_text(0.04, f"Straight [bold blue]ahead[/bold blue], you see a [bold blue]{random_locations[2]}[/bold blue]")
    type_text(0.04, "Where would you like to go?")


    chosen_location = questionary.select(
        "",
        choices=[
            random_locations[0],
            random_locations[1],
            random_locations[2],
            "Head back"
        ],
        style=theme.custom_style,
    ).ask()
    print("")

    if chosen_location == "Head back":
        clear_console()
        type_text(0.01, "You [red]stumble[/red] on a rock and you find yourself somewhere unfamiliar.")
        return

    clear_console()
    location = LOCATIONS[chosen_location]
    type_text(0.02, f"{location["description"]}")
    type_text(0.06, f"The risk is [bold red]{location["risk"]}[/bold red] and there is [yellow]{location["radiation"]}[/yellow] radiation.")
    type_text(0.02, f"It takes [purple]{location["scavenge_time"]} seconds[/purple] to scavenge.")
    type_text(0.04, f"\nLoot contains:")
    for loot, amount in location["loot"].items():
        type_text(0.01, f"[blue]{loot}[/blue] x[green]{amount}[/green]")

    type_text(0.06, "\nDo you want to go in?")



    yes_no = questionary.select(
        "",
        choices=[
            "Yes",
            "Not really...",
        ],
        style=theme.custom_style,
    ).ask()
    print("")

    if yes_no == "Not really...":
        clear_console()
        return

    clear_console()
    roll_damage(player)
    get_hungry(player)

    type_text(0.15, "You go inside...")
    type_text(0.40, "[bold red]. . . [/bold red]")


    risk = location["risk"]
    risk_settings = RISKS[risk]

    health = player["health"]
    loot_amount = risk_settings["loot_amount"]
    caps = risk_settings["bottle_caps"]
    damage = risk_settings["damage"]
    xp = risk_settings["xp"]
    radiation = location["radiation"]

    health["hitpoints"] -= damage
    type_text(0.03, f"You took [bold red]{damage} damage[/bold red]!")

    check_death(player)

    if radiation > 0:
        radiation_damage = random.randint(0, radiation)
        health["radiation"] += radiation_damage
        type_text(0.03, f"You suffered [yellow]{radiation_damage} radiation[/yellow]!")


    loot_table = location["loot"]
    random_loot = random.choices(
        list(loot_table.keys()),
        weights=list(loot_table.values()),
        k=loot_amount
    )

    loot_summary = {}
    for item in random_loot:
        player["inventory"][item] = player["inventory"].get(item, 0) + 1
        loot_summary[item] = loot_summary.get(item, 0) + 1

    loot_text = ", ".join(
        f"[blue]{item}[/blue] x[green]{amount}[/green]"
        for item, amount in loot_summary.items()
    )

    type_text(0.02, f"\nYou gained: {loot_text}!")

    player["bottle_caps"] += caps
    type_text(0.05, f"You also gained [bold yellow]{caps} bottle caps[/bold yellow]!")

    player["xp"] += xp
    type_text(0.02, f"You also gained [bold yellow]{xp} xp[/bold yellow].\n")

    levelup(player)

def use_item(player, item):
    inventory = player["inventory"]
    hunger = player["health"]["hunger"]
    thirst = player["health"]["thirst"]
    radiation = player["health"]["radiation"]

    if inventory[item] <= 0:
        type_text(0.02, f"You don't have any more [bold blue]{item}[/bold blue] to use.")

    if items.ITEMS[item]["type"] != "consumable":
        type_text(0.02, f"You don't know how to use [bold blue]{item}[/bold blue].")
        return
    
    if items.ITEMS[item]["effect"] == "reduce_hunger":
        if hunger <= 0:
            type_text(0.01, "You are not hungry.")
            return
        player["inventory"][item] -= 1
        player["health"]["hunger"] = max(0, hunger - items.ITEMS[item]["effect_amount"])
        hunger_reduced = hunger - player["health"]["hunger"]
        
        type_text(0.02, f"You eat some {item}. Your [yellow]hunger[/yellow] decreased by {hunger_reduced}.")
        type_text(0.02, f"It tastes like the [red]empty wasteland[/red] you find yourself wandering in.")

    if items.ITEMS[item]["effect"] == "reduce_thirst":
        if thirst <= 0:
            type_text(0.01, "You are not thirsty.")
            return
        player["inventory"][item] -= 1
        player["health"]["thirst"] = max(0, thirst - items.ITEMS[item]["effect_amount"])
        thirst_reduced = thirst - player["health"]["thirst"]
        
        type_text(0.02, f"You drink some {item}. Your [yellow]thirst[/yellow] decreased by {thirst_reduced}.")
        type_text(0.02, f"It tastes like the [red]empty wasteland[/red] you find yourself wandering in.")

    if items.ITEMS[item]["effect"] == "reduce_radiation":
        if radiation <= 0:
            type_text(0.01, "You are not radiated.")
            return
        player["inventory"][item] -= 1
        player["health"]["radiation"] = 0

        type_text(0.02, f"You inject the [yellow]RadRelief[/yellow] into your veins. It is invigorating. You feel [bold green]normal[/bold green].")

def sleep(player):
    hitpoints = player["health"]["hitpoints"]
    max_health = player["max_health"]
    caps = player["bottle_caps"]

    if hitpoints >= max_health:
        player["health"]["hitpoints"] = max_health
        type_text(0.02, "You are already at full [red]health[/red].")
    elif caps < 20:
        type_text(0.02, "You don't have enough [yellow]bottle_caps[/yellow]")
    else:
        rest_health = random.randint(12,20)
        player["bottle_caps"] -= 20
        player["health"]["hitpoints"] = min(max_health, hitpoints + rest_health)

        health_regained = player["health"]["hitpoints"] - hitpoints

        type_text(0.02, f"You go to sleep. You also wake up with [yellow]20[/yellow] fewer [yellow]bottle_caps[/yellow]...")
        type_text(0.02, f"You regained [red]{health_regained} health[/red].")
    
def status(player):
    health = player["health"]
    hp = max(0, health["hitpoints"])
    max_hp = player["max_health"]

    bar_length = 20
    filled = round(bar_length * hp / max_hp)
    bar = "[red]#[/red]" * filled + "[red]-[/red]" * (bar_length - filled)

    type_text(0.02, f"[bold yellow]=== {player['name']}'s STATUS ===[/bold yellow]")
    type_text(0.02, f"[yellow]HP:[/yellow] [{bar}] {hp}/{max_hp}")
    type_text(0.02, f"[yellow]XP: {player['xp']}[/yellow]")
    type_text(0.02, f"[yellow]Bottle caps: {player['bottle_caps']}[/yellow]")
    type_text(0.02, f"[blue]Hunger: {health['hunger']}/100[/blue]")
    type_text(0.02, f"[blue]Thirst: {health['thirst']}/100[/blue]")
    type_text(0.02, f"[blue]Radiation: {health['radiation']}[/blue]\n")

def inventory(player):

    inventory = player["inventory"]

    if not any(amount > 0 for amount in inventory.values()):
        clear_console()
        type_text(0.01, "Your inventory is empty.")
        return

    while True:
        choices = [
            f"{item} (x{amount})"
            for item, amount in inventory.items()
        ]

        choices.append("Back")

        selected = questionary.select(
            "Select your item:",
            choices=choices,
            style=theme.custom_style,
        ).ask()

        if selected is None or selected == "Back":
            clear_console()
            break

        item = selected.split(" (x")[0]


        action = questionary.select(
            f"What do you want to do with {item}?",
            choices=["Use", "Examine", "Cancel"],
            style=theme.custom_style,
        ).ask().strip().lower()

        if action == "examine":
            clear_console()
            type_text(0.02, f"[purple]{items.ITEMS[item]["name"]}[/purple].")
            type_text(0.02, f"{items.ITEMS[item]["description"]}")

        elif action == "use":
            clear_console()
            use_item(player, item)

        elif action == "cancel" or action is None:
            clear_console()
            continue

def buy_machine(player, machine):
    factory = player["factory"]
    factory_level = player["factory_level"]
    factory_space = factory_level * 0 + 15

    count = 0
    for machines, amount in factory.items():
        count += amount
    if count >= factory_space:
        type_text(0.02, "You don't have any space for more [purple]{machine}[/purple].")
        return

    if player["bottle_caps"] < FACTORY_MACHINES[machine]["cost_bottle_caps"]:
        type_text(0.02, "You don't have enough [bold yellow]bottle caps[/bold yellow].")
        return
    if player["inventory"]["Scrap"] < FACTORY_MACHINES[machine]["cost_scrap"]:
        type_text(0.02, "You don't have enough [bold blue]scrap[/bold blue].")
        return

    player["bottle_caps"] -= FACTORY_MACHINES[machine]["cost_bottle_caps"]
    player["inventory"]["Scrap"] -= FACTORY_MACHINES[machine]["cost_scrap"]
    player["factory"][machine] += 1

def sell_machine(player, machine):
    if player["factory"][machine] <= 0:
        type_text(0.02, f"You don't have any [purple]{machine}[/purple] to sell.")
        return

    player["factory"][machine] -= 1
    player["bottle_caps"] += FACTORY_MACHINES[machine]["sell_bottle_caps"]
    player["inventory"]["Scrap"] += FACTORY_MACHINES[machine]["sell_scrap"]

def factory(player):

    while True:
        factory_level = player["factory_level"]
        factory_space = factory_level * 0 + 15
        factory = player["factory"]
        bottle_caps = player["bottle_caps"]
        scrap = player["inventory"]["Scrap"]
        type_text(0, f"Your factory is level [green]{factory_level}[/green]. You have space for [green]{factory_space} machines[/green].")
        type_text(0, f"You have [bold yellow]bottle_caps[/bold yellow] x[bold yellow]{bottle_caps}[/bold yellow] and [bold blue]scrap[/bold blue] x[bold blue]{scrap}[/bold blue]")
        
        choices = [
            f"{machine} (x{amount})"
            for machine, amount in factory.items()
        ]
        choices.append("Back")

        selected = questionary.select(
            "Select your machine:",
            choices=choices,
            style=theme.custom_style,
        ).ask()

        if selected is None or selected == "Back":
            clear_console()
            break

        machine = selected.split(" (x")[0]
        
        action = questionary.select(
            f"What do you want to do with {machine}?",
            choices=["Buy", "Sell", "Examine", "Cancel"],
            style=theme.custom_style,
        ).ask().strip().lower()

        if action == "examine":
            clear_console()
            type_text(0.02, f"[purple]{FACTORY_MACHINES[machine]["name"]}[/purple].")
            type_text(0.02, f"{FACTORY_MACHINES[machine]["description"]}")
            type_text(0.02, f"It costs [bold yellow]{FACTORY_MACHINES[machine]["cost_bottle_caps"]} bottle caps[/bold yellow] and [bold blue]{FACTORY_MACHINES[machine]["cost_scrap"]} scrap[/bold blue].")

        elif action == "buy":
            clear_console()
            buy_machine(player, machine)

        elif action == "sell":
            clear_console()
            sell_machine(player, machine)

        elif action == "cancel" or action is None:
            clear_console()
            continue

def nextAction(player):
    type_text(0.02, "What do you want to do next?     ")
    action = questionary.select(
        "",
        choices=[
            "Scavenge",
            "Sleep",
            "Inventory",
            "Status",
            "Factory",
            "Leave"
        ],
        style=theme.custom_style,
    ).ask().strip().lower()
    print("")
    
    if action == "leave":
        type_text(0.08, "Goodbye [red]scavenger[/red]...")
        sys.exit()

    clear_console()

    commands = {
        "inventory": inventory, 
        "scavenge": scavenge, 
        "sleep": sleep,
        "status": status,
        "factory": factory
    }
    commands[action](player)  

def initLoop(player):
    health = player["health"]

    check_death(player)

    if health["hunger"] >= 100:
        type_text(0.08, "You are [bold red]starving[/bold red]...")
    elif health["hunger"] > 50:
        type_text(0.08, "You are [red]hungry[/red]...")

    if health["thirst"] >= 100:
        type_text(0.08, "You are [bold blue]dehydrated[/bold blue]...")
    elif health["thirst"] > 50:
        type_text(0.08, "You are [blue]thirsty[/blue]...")


    type_text(0.02,
        f"You have [bold green]{health['hitpoints']} health[/bold green] "
        f"and have [bold yellow]{player['bottle_caps']} bottle capsu[/bold yellow]."
        )