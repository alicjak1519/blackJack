from classes import Player
from classes import Dealer
from classes import PackOfCards
from classes import BlackJackGame

my_pack = PackOfCards(2)
my_card = my_pack.give_random_card()
print(my_pack.translate_card(my_card))

my_player = Player("John")
my_dealer = Dealer()

my_game = BlackJackGame(my_player, my_dealer, my_pack)
my_game.first_deal()
print(my_player.hand)
print(my_game.calculate_hand(my_player))