from classes import Player
from classes import PackOfCards
from classes import BlackJackGame

my_player = Player("John")
my_pack = PackOfCards(number=3)

my_game = BlackJackGame(my_player, my_pack)

try:
    my_game.play_a_game()
except:
    print("Try again, something went wrong!")
