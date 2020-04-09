from classes import Player
from classes import BlackJackGame

my_player = Player("John2")
pack_number = 3

my_game = BlackJackGame(my_player, pack_number)

try:
    my_game.save_score()
except Exception as exception:
    print("Try again, something went wrong!")
    print(exception)
