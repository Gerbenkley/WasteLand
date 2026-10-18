def create_player():

    return {
        "name": "",

        "level": 1,
        "xp": 0,
        
        "max_health": 100,
        "bottle_caps": 0,

        "health": {
            "hitpoints": 100,
            "thirst": 0,
            "hunger": 0,
            "radiation": 0
            },   

        "inventory": {
            "Water": 1,
            "Food": 1,
            "Scrap": 0
        },

        "factory_level": 1,
        "factory": {
            "Bottle Cap Press": 0,
            "Scrap Producer": 0
        }

    }