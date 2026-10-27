from player import Player, clear_console, initLoop, nextAction, type_text

clear_console()

type_text(0.04, "What is your name, [red]scavenger?[/red] ")
init_player_name = input()
clear_console()
player = Player(init_player_name, 0, 0)
type_text(0.04, f"Welcome to the Wasteland, [red]{player.name}[/red]!\n")

while True:
    initLoop(player)    
    nextAction(player)