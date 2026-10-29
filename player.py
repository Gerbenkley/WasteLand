import os
import random
import sys
import time
from collections import Counter

import questionary
from rich.console import Console
from rich.text import Text

import items
import theme
from factory import FACTORY_MACHINES
from items import CONSUMABLE_EFFECTS
from locations import DIRECTIONS, LOCATIONS, RISKS

BASE_HEALTH = 100
HEALTH_PER_LEVEL = 10
FIRST_LEVEL_XP = 500
XP_STEP_PER_LEVEL = 500

MAX_NEED = 100
HUNGER_PER_TRIP = 5
THIRST_PER_TRIP = 10
STARVATION_DAMAGE = 10

SLEEP_COST = 20
SLEEP_HEAL_RANGE = (12, 20)

FACTORY_SPACE_PER_LEVEL = 15
HP_BAR_LENGTH = 20

console = Console()

def type_text(delay, text):
    styled_text = Text.from_markup(text)

    for i, char in enumerate(styled_text.plain):
        char_style = styled_text.get_style_at_offset(console, i)

        console.print(
            Text(char, style=char_style),
            end="",
            markup=False,
            highlight=False,
        )

        time.sleep(delay)

    console.print()

def clear_console():
    os.system("cls" if os.name == "nt" else "clear")

def ask(question: str, choices: list[str]):
    return questionary.select(question, choices=choices, style=theme.custom_style,).ask()

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
    print()
    
    if action == "leave":
        type_text(0.08, "Goodbye [red]scavenger[/red]...")
        sys.exit()

    clear_console()

    commands = {
        "inventory": player.inventory_menu, 
        "scavenge": player.scavenge, 
        "sleep": player.sleep,
        "status": player.status,
        "factory": player.factory_menu
    }
    commands[action]()  

def initLoop(player):

    if player.health["hunger"] >= 100:
        type_text(0.08, "You are [bold red]starving[/bold red]...")
    elif player.health["hunger"] > 50:
        type_text(0.08, "You are [red]hungry[/red]...")

    if player.health["thirst"] >= 100:
        type_text(0.08, "You are [bold blue]dehydrated[/bold blue]...")
    elif player.health["thirst"] > 50:
        type_text(0.08, "You are [blue]thirsty[/blue]...")


    type_text(0.02,
        f"You have [bold green]{player.health['hitpoints']} health[/bold green] "
        f"and have [bold yellow]{player.bottle_caps} bottle capsu[/bold yellow]."
        )



class Character:
    def __init__(self, name: str, total_xp: int, bottle_caps: int):
        self.name = name
        self.total_xp = total_xp
        self.bottle_caps = bottle_caps

        self.level = self.calculate_level()
        self.max_health = self.calculate_max_health()

        self.health = {
            "max_health": self.max_health,
            "hitpoints": self.max_health,
            "thirst": 0,
            "hunger": 0,
            "radiation": 0
        }

        self.inventory = {
            "Water": 1,
            "Food": 1,
            "Scrap": 0
        }

    def calculate_level(self) -> int:
        level = 1
        xp_required = FIRST_LEVEL_XP

        while self.total_xp >= xp_required:
            level += 1
            xp_required += level * XP_STEP_PER_LEVEL

        return level

    def calculate_max_health(self) -> int:
        return BASE_HEALTH + (self.level - 1) * HEALTH_PER_LEVEL

    def update_level(self) -> bool:
        old_level = self.level
        self.level = self.calculate_level()
        self.max_health = self.calculate_max_health()
        self.health["max_health"] = self.max_health
        return self.level > old_level

    def take_damage(self, damage: int) -> None:
        self.health["hitpoints"] = max(0, self.health["hitpoints"] - damage)
        if self.health["hitpoints"] == 0:
            self.on_death()

    def on_death(self) -> None:
        pass



class Player(Character):
    def __init__(self, name: str, total_xp: int, bottle_caps: int):
        super().__init__(name, total_xp, bottle_caps)

        self.factory_level = 1
        self.factory = {            
            "Bottle Cap Press": 0,
            "Scrap Producer": 0
        }



    def on_death(self) -> None:
        type_text(0.08, "You are [bold red]dead[/bold red]. Until next time... [red]scavenger[/red]...")
        sys.exit()



    def scavenge(self):
        location = self._pick_location()
        if location is None:
            return

        self._show_location(location)
        if not self._confirm_entry():
            return

        self._apply_survival_damage()
        self._tick_survival_needs()

        type_text(0.15, "You go inside...")
        type_text(0.40, "[bold red]. . . [/bold red]")

        risk_settings = RISKS[location["risk"]]
        self._take_trip_damage(risk_settings["damage"])
        self._take_radiation(location["radiation"])
        self._collect_loot(location["loot"], risk_settings["loot_amount"])
        self._collect_rewards(risk_settings["bottle_caps"], risk_settings["xp"])

    def _pick_location(self):
        type_text(0.02, "You venture on a scavenger hunt.")
        type_text(0.15, "[bold red]. . .[/bold red]")

        names = random.sample(list(LOCATIONS), 3)
        for (direction, speed), name in zip(DIRECTIONS, names):
            type_text(speed, f"{direction}, you see a [bold blue]{name}[/bold blue]")
        type_text(0.04, "Where would you like to go?")

        chosen = ask("", names + ["Head back"])
        print()
        clear_console()

        if chosen is None or chosen == "Head back":
            type_text(0.01, "You [red]stumble[/red] on a rock and you find yourself somewhere unfamiliar.")
            return None

        return LOCATIONS[chosen]

    def _show_location(self, location: dict):
        type_text(0.02, location["description"])
        type_text(0.06, f"The risk is [bold red]{location['risk']}[/bold red] and there is [yellow]{location['radiation']}[/yellow] radiation.")
        type_text(0.02, f"It takes [purple]{location['scavenge_time']} seconds[/purple] to scavenge.")
        type_text(0.04, "\nLoot contains:")
        for loot, amount in location["loot"].items():
            type_text(0.01, f"[blue]{loot}[/blue] x[green]{amount}[/green]")

    def _confirm_entry(self) -> bool:
        type_text(0.06, "\nDo you want to go in?")
        answer = ask("", ["Yes", "Not really..."])
        print()
        clear_console()
        return answer == "Yes"

    def _take_trip_damage(self, damage: int):
        type_text(0.03, f"You took [bold red]{damage} damage[/bold red]!")
        self.take_damage(damage)

    def _take_radiation(self, radiation: int):
        if radiation <= 0:
            return
        radiation_damage = random.randint(0, radiation)
        self.health["radiation"] += radiation_damage
        type_text(0.03, f"You suffered [yellow]{radiation_damage} radiation[/yellow]!")

    def _collect_loot(self, loot_table: dict, loot_amount: int):
        found = random.choices(
            list(loot_table.keys()),
            weights=list(loot_table.values()),
            k=loot_amount,
        )

        # Counter turns ["Scrap", "Water", "Scrap"] into {"Scrap": 2, "Water": 1}
        summary = Counter(found)
        for item, amount in summary.items():
            self.inventory[item] = self.inventory.get(item, 0) + amount

        loot_text = ", ".join(
            f"[blue]{item}[/blue] x[green]{amount}[/green]"
            for item, amount in summary.items()
        )
        type_text(0.02, f"\nYou gained: {loot_text}!")

    def _collect_rewards(self, caps: int, xp: int):
        self.bottle_caps += caps
        type_text(0.05, f"You also gained [bold yellow]{caps} bottle caps[/bold yellow]!")

        self.total_xp += xp
        type_text(0.02, f"You also gained [bold yellow]{xp} xp[/bold yellow].\n")

        if self.update_level():
            type_text(0.01, f"You reached [bold green]level {self.level}[/bold green]!")

    def _apply_survival_damage(self):
        health = self.health

        if health["hunger"] >= MAX_NEED:
            type_text(0.08, f"You are [yellow]starving[/yellow]... you take [red]{STARVATION_DAMAGE} damage[/red].")
            self.take_damage(STARVATION_DAMAGE)

        if health["thirst"] >= MAX_NEED:
            type_text(0.08, f"You are [yellow]dehydrated[/yellow]... you take [red]{STARVATION_DAMAGE} damage[/red].")
            self.take_damage(STARVATION_DAMAGE)

        if health["radiation"] > 0:
            type_text(0.08, f"You suffer from [yellow]radiation[/yellow] and take [red]{health['radiation']} radiation damage[/red].")
            self.take_damage(health["radiation"])

    def _tick_survival_needs(self):
        """Every trip makes you a bit hungrier and thirstier."""
        health = self.health
        health["hunger"] = min(MAX_NEED, health["hunger"] + HUNGER_PER_TRIP)
        health["thirst"] = min(MAX_NEED, health["thirst"] + THIRST_PER_TRIP)



    def status(self):
        health = self.health
        hp = max(0, health["hitpoints"])
        max_hp = health["max_health"]

        filled = round(HP_BAR_LENGTH * hp / max_hp)
        bar = "[red]#[/red]" * filled + "[dim]-[/dim]" * (HP_BAR_LENGTH - filled)

        type_text(0.02, f"[bold yellow]=== {self.name}'s STATUS ===[/bold yellow]")
        type_text(0.02, f"[yellow]HP:[/yellow] \\[{bar}] {hp}/{max_hp}")
        type_text(0.02, f"[yellow]XP: {self.total_xp}        LVL: {self.level}[/yellow]")
        type_text(0.02, f"[yellow]Bottle caps: {self.bottle_caps}[/yellow]")
        type_text(0.02, f"[blue]Hunger: {health['hunger']}/{MAX_NEED}[/blue]")
        type_text(0.02, f"[blue]Thirst: {health['thirst']}/{MAX_NEED}[/blue]")
        type_text(0.02, f"[blue]Radiation: {health['radiation']}[/blue]\n")



    def inventory_menu(self):
        while True:
            # Only show items you actually have (before, used-up items
            # stayed in the list as "Food (x0)").
            owned = {name: amount for name, amount in self.inventory.items() if amount > 0}

            if not owned:
                clear_console()
                type_text(0.01, "Your inventory is empty.")
                return

            choices = [f"{name} (x{amount})" for name, amount in owned.items()]
            choices.append("Back")

            selected = ask("Select your item:", choices)
            if selected is None or selected == "Back":
                clear_console()
                return

            item = selected.split(" (x")[0]

            action = ask(f"What do you want to do with {item}?", ["Use", "Examine", "Cancel"])
            clear_console()

            # No .strip().lower() chain here: that crashed when action was
            # None (player pressed Ctrl+C) because None has no .strip().
            if action == "Examine":
                self._examine_item(item)
            elif action == "Use":
                self._use_item(item)

    def _examine_item(self, item: str):
        data = items.ITEMS.get(item)
        if data is None:
            type_text(0.02, f"You can't make out anything special about [bold blue]{item}[/bold blue].")
            return
        type_text(0.02, f"[purple]{data['name']}[/purple].")
        type_text(0.02, data["description"])

    def _use_item(self, item: str):
        data = items.ITEMS.get(item)

        if self.inventory.get(item, 0) <= 0:
            type_text(0.02, f"You don't have any more [bold blue]{item}[/bold blue] to use.")
            return

        effect = CONSUMABLE_EFFECTS.get(data["effect"]) if data and data["type"] == "consumable" else None
        if effect is None:
            type_text(0.02, f"You don't know how to use [bold blue]{item}[/bold blue].")
            return

        need = effect["need"]
        current = self.health[need]
        if current <= 0:
            type_text(0.02, effect["not_needed"])
            return

        if data is not None:
            reduction = current if effect.get("cures_all") else data["effect_amount"]
            self.inventory[item] -= 1
            self.health[need] = max(0, current - reduction)
            actually_reduced = current - self.health[need]

            type_text(0.02, effect["message"].format(item=item, amount=actually_reduced))

        if "flavor" in effect:
            type_text(0.02, effect["flavor"])



    def sleep(self):
        hitpoints = self.health["hitpoints"]
        max_health = self.health["max_health"]

        if hitpoints >= max_health:
            type_text(0.02, "You are already at full [red]health[/red].")
            return

        if self.bottle_caps < SLEEP_COST:
            type_text(0.02, "You don't have enough [yellow]bottle caps[/yellow].")
            return

        self.bottle_caps -= SLEEP_COST
        self.health["hitpoints"] = min(max_health, hitpoints + random.randint(*SLEEP_HEAL_RANGE))
        health_regained = self.health["hitpoints"] - hitpoints

        type_text(0.02, f"You go to sleep. You also wake up with [yellow]{SLEEP_COST}[/yellow] fewer [yellow]bottle caps[/yellow]...")
        type_text(0.02, f"You regained [red]{health_regained} health[/red].")



    def _factory_space(self) -> int:
        return self.factory_level * FACTORY_SPACE_PER_LEVEL

    def factory_menu(self):
        while True:
            space = self._factory_space()
            used = sum(self.factory.values())
            scrap = self.inventory["Scrap"]

            type_text(0, f"Your factory is level [green]{self.factory_level}[/green]. Machines: [green]{used}/{space}[/green].")
            type_text(0, f"You have [bold yellow]bottle caps[/bold yellow] x[bold yellow]{self.bottle_caps}[/bold yellow] and [bold blue]scrap[/bold blue] x[bold blue]{scrap}[/bold blue]")

            choices = [f"{machine} (x{amount})" for machine, amount in self.factory.items()]
            choices.append("Back")

            selected = ask("Select your machine:", choices)
            if selected is None or selected == "Back":
                clear_console()
                return

            machine = selected.split(" (x")[0]

            action = ask(f"What do you want to do with {machine}?", ["Buy", "Sell", "Examine", "Cancel"])
            clear_console()

            if action == "Examine":
                self._examine_machine(machine)
            elif action == "Buy":
                self._buy_machine(machine)
            elif action == "Sell":
                self._sell_machine(machine)

    def _examine_machine(self, machine: str):
        data = FACTORY_MACHINES[machine]
        type_text(0.02, f"[purple]{data['name']}[/purple].")
        type_text(0.02, data["description"])
        type_text(0.02, f"It costs [bold yellow]{data['cost_bottle_caps']} bottle caps[/bold yellow] and [bold blue]{data['cost_scrap']} scrap[/bold blue].")

    def _buy_machine(self, machine: str):
        data = FACTORY_MACHINES[machine]

        if sum(self.factory.values()) >= self._factory_space():
            type_text(0.02, f"You don't have any space for more [purple]{machine}[/purple].")
            return
        if self.bottle_caps < data["cost_bottle_caps"]:
            type_text(0.02, "You don't have enough [bold yellow]bottle caps[/bold yellow].")
            return
        if self.inventory["Scrap"] < data["cost_scrap"]:
            type_text(0.02, "You don't have enough [bold blue]scrap[/bold blue].")
            return

        self.bottle_caps -= data["cost_bottle_caps"]
        self.inventory["Scrap"] -= data["cost_scrap"]
        self.factory[machine] += 1
        type_text(0.02, f"You bought a [purple]{machine}[/purple].")

    def _sell_machine(self, machine: str):
        data = FACTORY_MACHINES[machine]

        if self.factory[machine] <= 0:
            type_text(0.02, f"You don't have any [purple]{machine}[/purple] to sell.")
            return

        self.factory[machine] -= 1
        self.bottle_caps += data["sell_bottle_caps"]
        self.inventory["Scrap"] += data["sell_scrap"]
        type_text(0.02, f"You sold a [purple]{machine}[/purple] for [bold yellow]{data['sell_bottle_caps']} bottle caps[/bold yellow] and [bold blue]{data['sell_scrap']} scrap[/bold blue].")
