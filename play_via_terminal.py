from classes import Player, BlackJackGame, print_scores

my_player = Player(input("What is your name?\n"))
pack_number = int(input("How many packs you want to play?\n"))

if input("Do you want to see scoreboard? [y/n] \n") == "y":
    print_scores()

my_game = BlackJackGame(my_player, pack_number)

try:
    my_game.play_a_game()
except Exception as exception:
    print("Try again, something went wrong!")
    print(exception)
