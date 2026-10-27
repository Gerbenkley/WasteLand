CONSUMABLE_EFFECTS = {
    "reduce_hunger": {
        "need": "hunger",
        "not_needed": "You are not hungry.",
        "message": "You eat some {item}. Your [yellow]hunger[/yellow] decreased by {amount}.",
        "flavor": "It tastes like the [red]empty wasteland[/red] you find yourself wandering in.",
    },
    "reduce_thirst": {
        "need": "thirst",
        "not_needed": "You are not thirsty.",
        "message": "You drink some {item}. Your [yellow]thirst[/yellow] decreased by {amount}.",
        "flavor": "It tastes like the [red]empty wasteland[/red] you find yourself wandering in.",
    },
    "reduce_radiation": {
        "need": "radiation",
        "not_needed": "You are not radiated.",
        "message": (
            "You inject the [yellow]RadRelief[/yellow] into your veins. "
            "It is invigorating. You feel [bold green]normal[/bold green]."
        ),
        "cures_all": True,
    },
}


ITEMS = {
    "Scrap": {
        "name": "Scrap Metal",
        "description": "Useful for crafting and creating machinery.",
        "type": "material",
        "sell_price": 2,
    },

    "Food": {
        "name": "Canned Food",
        "description": "Reduces hunger. But not by much.",
        "type": "consumable",
        "effect": "reduce_hunger",
        "effect_amount" : 10,
        "sell_price": 5,
    },

    "Water": {
        "name": "Clean Water",
        "description": "Reduces thirst. On the label it says it's clean, yet it doesn't look like it.",
        "type": "consumable",
        "effect": "reduce_thirst",
        "effect_amount": 20,
        "sell_price": 4,
    },

    "RadRelief": {
        "name": "RadRelief",
        "description": "Fully removes radiation. Does some other stuff, but you don't know what.",
        "type": "consumable",
        "effect": "reduce_radiation",
        "effect_amount": 100,
        "sell_price": 10,
    },

    "Bone": {
        "name": "Dog Bone",
        "description": "Give this to a dog to make it very happy. The bone is good for its teeth.",
        "type": "item",
        "sell_price": 1,
    },

    "Dog": {
        "name": "Dog",
        "description": "Your life companion. You are both verey happy you have found each other.",
        "type": "item",
        "sell_price": 1,
    },
}
