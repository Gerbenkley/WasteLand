RISKS = {
    "low": {
        "damage": 3,
        "loot_amount": 2,
        "bottle_caps": 15,
        "xp": 20
    },
    "medium": {
        "damage": 7,
        "loot_amount": 4,
        "bottle_caps": 35,
        "xp": 40
    },
    "high": {
        "damage": 15,
        "loot_amount": 7,
        "bottle_caps": 55,
        "xp": 65
    }
}


LOCATIONS = {
    "hospital": {
        "name": "Abandoned Hospital",
        "description": "An [blue]Abandoned Hospital[/blue]. There might be some supplies left in there. Or [red]corpses[/red].",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 5,
            "Food": 5,
            "Water": 10,
            "RadRelief": 15
        }
    },

    "gas station": {
        "name": "Abandoned Gas Station",
        "description": "An [blue]old gas station[/blue]. There is no gas left in the pumps. Not like you had a car, [purple]anyway[/purple].",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 5,
        "loot": {
            "Scrap": 10,
            "Food": 5,
            "Water": 10,
            "RadRelief": 1
        }
    },

    "ruined supermarket": {
        "name": "Ruined Supermarket",
        "description": "A [blue]supermarket[/blue] in [red]ruins[/red]. The shelves have been empty for decades, yet it's still popular for [red]scavengers[/red].",
        "risk": "medium",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 5,
            "Food": 15,
            "Water": 15,
            "RadRelief": 3
        }
    },
    
    "nuclear reactor": {
        "name": "Reactor 9",
        "description": "[blue]Reactor 9[/blue] used to be the source of energy for the province. Reactor 9 also caused [red]the apocalypse[/red].",
        "risk": "medium",
        "radiation": 10,
        "scavenge_time": 20,
        "loot": {
            "Scrap": 25,
            "Food": 3,
            "Water": 5,
            "RadRelief": 10
        }
    },
    "dog daycare": {
        "name": "Dog Daycare",
        "description": "A [blue]Dacyare for Doggies™[/blue]. You'll hope to find your [bold blue]soulmate[/bold blue] here, one day...",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 5,
            "Food": 5,
            "Water": 10,
            "RadRelief": 5,
            "Bone": 25,
            "Dog": 1
        }
    },
    "fire station": {
        "name": "Abandoned Fire Station",
        "description": "The [blue]fire station[/blue] is still standing. The only thing left to put out is your [red]existence[/red].",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 15,
            "Food": 3,
            "Water": 5,
            "RadRelief": 1,
        },
    },

    "pharmacy": {
        "name": "Ruined Pharmacy",
        "description": "Most of the shelves are empty. A few [blue]sealed boxes[/blue] remain behind the counter. Check the labels before swallowing anything. [red]Seriously.[/red]",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 5,
        "loot": {
            "Scrap": 3,
            "Food": 1,
            "Water": 1,
            "RadRelief": 15,
        },
    },

    "police station": {
        "name": "Abandoned Police Station",
        "description": "The workforce are long gone. Their paperwork, however, has survived the [red]apocalypse[/red]. Humanity really does have its priorities.",
        "risk": "medium",
        "radiation": 0,
        "scavenge_time": 15,
        "loot": {
            "Scrap": 15,
            "Food": 2,
            "Water": 3,
            "RadRelief": 2,
        },
    },

    "scrapyard": {
        "name": "The Scrap Heap",
        "description": "An enormous [blue]scrapyard[/blue], filled with rusted machinery and twisted metal. Finally, a place where your crippling hoarding tendencies are [green]useful[/green].",
        "risk": "medium",
        "radiation": 2,
        "scavenge_time": 15,
        "loot": {
            "Scrap": 30,
            "Food": 1,
            "Water": 2,
            "RadRelief": 1,
        },
    },

    "water treatment plant": {
        "name": "Water Treatment Plant",
        "description": "The old [blue]treatment plant[/blue] once provided clean water to thousands. Now, you're not entirely sure what the pipes are providing. At least it's [blue]liquid[/blue]",
        "risk": "medium",
        "radiation": 3,
        "scavenge_time": 15,
        "loot": {
            "Scrap": 10,
            "Food": 1,
            "Water": 25,
            "RadRelief": 2,
        },
    },

    "school": {
        "name": "Abandoned Elementary School",
        "description": "Tiny chairs. Faded drawings. A chalkboard that still reads [purple]'See you Monday!'[/purple] It's been a very long weekend.",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 5,
            "Food": 8,
            "Water": 5,
            "RadRelief": 1,
        },
    },

    "train station": {
        "name": "Derelict Train Station",
        "description": "The trains stopped running [red]decades[/red] ago. The timetable still promises a departure at 14:35. [purple]Optimism[/purple] is a strange thing.",
        "risk": "medium",
        "radiation": 1,
        "scavenge_time": 15,
        "loot": {
            "Scrap": 20,
            "Food": 5,
            "Water": 5,
            "RadRelief": 2,
        },
    },

    "military checkpoint": {
        "name": "Military Checkpoint",
        "description": "[blue]Sandbags[/blue], [blue]barricades[/blue], and abandoned [blue]supply crates[/blue]. Whatever the soldiers were guarding, they apparently decided it wasn't worth staying for.",
        "risk": "high",
        "radiation": 1,
        "scavenge_time": 20,
        "loot": {
            "Scrap": 20,
            "Food": 8,
            "Water": 8,
            "RadRelief": 5,
        },
    },

    "underground bunker": {
        "name": "Shelter 17",
        "description": "A sealed [blue]underground bunker[/blue]. Someone tried to scratch a message into the door: [red]'DO NOT OPEN.'[/red] Well, that's practically an invitation.",
        "risk": "high",
        "radiation": 5,
        "scavenge_time": 25,
        "loot": {
            "Scrap": 15,
            "Food": 15,
            "Water": 15,
            "RadRelief": 8,
        },
    },

    "sewer system": {
        "name": "The Sewer System",
        "description": "A maze of [blue]flooded tunnels[/blue] beneath the wasteland. The smell is indescribable. The [blue]water[/blue] is worse. Something just moved in the darkness. [red]Must've been the wind[/red]",
        "risk": "high",
        "radiation": 4,
        "scavenge_time": 20,
        "loot": {
            "Scrap": 12,
            "Food": 2,
            "Water": 10,
            "RadRelief": 3,
            "Bone": 5,
        },
    },
    "amusement park": {
        "name": "Ruined Amusement Park",
        "description": "Welcome to [green]Funland™[/green]! The rides no longer work, the mascots are probably radioactive, and the only thing screaming is the wind. [red]Enjoy your stay.[/red]",
        "risk": "medium",
        "radiation": 2,
        "scavenge_time": 15,
        "loot": {
            "Scrap": 20,
            "Food": 5,
            "Water": 3,
            "RadRelief": 2,
        },
    },

    "library": {
        "name": "Public Library",
        "description": "A [blue]public library[/blue], still standing after the end of civilization. Thousands of books, millions of pages, and absolutely nobody left who knows how to read a map.",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 5,
            "Food": 2,
            "Water": 2,
            "RadRelief": 1,
        },
    },

    "car dealership": {
        "name": "Used Car Dealership",
        "description": "Rows of [blue]luxury vehicles[/blue] frozen in time. Beautiful machines, pristine interiors, and not a single working [blue]engine[/blue]. At least the cup holders survived.",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 20,
            "Food": 1,
            "Water": 2,
            "RadRelief": 1,
        },
    },

    "military depot": {
        "name": "Military Supply Depot",
        "description": "A heavily fortified [blue]supply depot[/blue]. The army abandoned it years ago. Whatever made them leave in such a hurry probably [bold red]isn't[/bold red] gone.",
        "risk": "high",
        "radiation": 3,
        "scavenge_time": 25,
        "loot": {
            "Scrap": 30,
            "Food": 10,
            "Water": 10,
            "RadRelief": 8,
        },
    },

    "abandoned mine": {
        "name": "Collapsed Mine",
        "description": "A dark, unstable [blue]mine shaft[/blue]. The walls are rich in [yellow]minerals[/yellow], the ceiling is rich in structural problems, and your insurance is rich in exclusions.",
        "risk": "high",
        "radiation": 5,
        "scavenge_time": 25,
        "loot": {
            "Scrap": 35,
            "Food": 1,
            "Water": 3,
            "RadRelief": 3,
        },
    },

    "radio station": {
        "name": "Dead Air Radio Station",
        "description": "The old [blue]radio station[/blue] still hums with [yellow]electricity[/yellow]. Somewhere in the static, you swear you hear a voice repeating the same weather forecast from 20 years ago. Cloudy with a chance of [bold yellow]radiation[/bold yellow].",
        "risk": "medium",
        "radiation": 0,
        "scavenge_time": 15,
        "loot": {
            "Scrap": 15,
            "Food": 2,
            "Water": 2,
            "RadRelief": 2,
        },
    },

    "prison": {
        "name": "Blackwater Penitentiary",
        "description": "The gates of [blue]Blackwater Penitentiary[/blue] hang open. The cells are empty. You decide not to investigate why the warden's office is [red]locked[/red] from the inside.",
        "risk": "high",
        "radiation": 0,
        "scavenge_time": 25,
        "loot": {
            "Scrap": 20,
            "Food": 5,
            "Water": 5,
            "RadRelief": 4,
        },
    },

    "cemetery": {
        "name": "Old Memorial Cemetery",
        "description": "A quiet [blue]cemetery[/blue] where the dead have finally stopped complaining about the living. [red]Mostly[/red]. Something is moving beneath the oldest mausoleum.",
        "risk": "medium",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 5,
            "Food": 1,
            "Water": 1,
            "RadRelief": 1,
            "Bone": 20,
        },
    },

    "industrial plant": {
        "name": "Chemical Processing Plant",
        "description": "A sprawling [blue]industrial complex[/blue] filled with rusted pipes and leaking tanks. The [red]warning[/red] signs are faded, but the smell suggests the chemicals are still very much [purple]in business[/purple].",
        "risk": "high",
        "radiation": 8,
        "scavenge_time": 25,
        "loot": {
            "Scrap": 35,
            "Food": 1,
            "Water": 2,
            "RadRelief": 5,
        },
    },

    "drive-in cinema": {
        "name": "Last Picture Show Drive-In",
        "description": "A [blue]drive-in cinema[/blue] frozen in the middle of movie night. The screen is torn, the cars are rusted, and the snack bar has been looted by some bloke named Grup. Humanity's greatest tragedy wasn't [red]the apocalypse[/red].",
        "risk": "low",
        "radiation": 0,
        "scavenge_time": 10,
        "loot": {
            "Scrap": 10,
            "Food": 10,
            "Water": 5,
            "RadRelief": 1,
        },
    },
}