import actions
import player
from functions import type_text, clear_console

clear_console()
player = player.create_player()
type_text(0.04, "What is your name, [red]scavenger?[/red] ")
player["name"] = input()
clear_console()
type_text(0.04, f"Welcome to the Wasteland, [red]{player['name']}[/red]!\n")

while True:
    actions.initLoop(player)    
    actions.nextAction(player)