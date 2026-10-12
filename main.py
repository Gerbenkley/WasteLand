import random

bottle_caps = 0
max_health = 100
health = 100
rest_cost = 50

def scavenge(health, bottle_caps):

    damage = random.randint(0, 19)
    health = max(0, health - damage)
    print(f"You took {damage} damage.")

    if health > 0:
        loot = random.randint(0, 25)
        bottle_caps += loot
        print(f"You found {loot} bottle_caps!")

    return health, bottle_caps

def rest(health, bottle_caps):

    if health == max_health:
        print("You are already at full health.")
    elif bottle_caps < rest_cost:
        print("You don't have enough bottle_caps")
    else:
        old_health = health
        bottle_caps -= rest_cost

        rest_health = random.randint(12,20)
        health = min(max_health, health+rest_health)

        print(f"You regained {health - old_health} health.")

    return health, bottle_caps


player_name = input("What is your name, scavenger? ")

print(f"\nWelcome to the Wasteland, {player_name}!\n")


while True:
    if health <= 0:
        print("You are dead. Until next time... scavenger...")
        break

    print(f"You have {health} health. and {bottle_caps} bottle caps")
    action = input(f"\nWhat do you want to do next? Scavenge, rest {rest_cost}bc or leave?").lower()
    print("")

    if action == "scavenge":
        health, bottle_caps = scavenge(health, bottle_caps)

    elif action == "rest":
        health, bottle_caps = rest(health, bottle_caps)

    elif action == "leave":
        print("Goodbye scavenger...")
        break
    else:
        print("Invalid action. Try again.")
