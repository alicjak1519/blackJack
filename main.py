import random


class Player():
    def __init__(self, name=""):
        self.name = name
        self.balance = 500
        self.hand = []


class Dealer():
    def __init__(self):
        self.secret_card = []
        self.hand = []


class PackOfCards():
    def __init__(self, number):
        self.number = number
        self.singlePack = ['2 S', '3 S', '4 S', '5 S', '6 S', '7 S', '8 S', '9 S', '10 S', 'J S', 'Q S', 'K S', 'A S',
                           '2 H', '3 H', '4 H', '5 H', '6 H', '7 H', '8 H', '9 H', '10 H', 'J H', 'Q H', 'K H', 'A H',
                           '2 C', '3 C', '4 C', '5 C', '6 C', '7 C', '8 C', '9 C', '10 C', 'J C', 'Q C', 'K C', 'A C',
                           '2 D', '3 D', '4 D', '5 D', '6 D', '7 D', '8 D', '9 D', '10 D', 'J D', 'Q D', 'K D', 'A D', ]

        self.fullPack = self.number * self.singlePack

    def give_random_card(self):
        card_id = random.randint(0, len(self.fullPack) - 1)
        return self.fullPack[card_id]

    def translate_card(self, card):
        colors = {'S': 'pik',
                  'H': 'kier',
                  'C': 'trefl',
                  'D': 'karo'}

        number = card.split()[0]
        color_id = card.split()[1]
        card_pl_name = number + ' ' + colors[color_id]

        return card_pl_name


class BlackJackGame():
    def __init__(self, player, dealer, pack):
        self.player = player
        self.dealer = dealer
        self.pack = pack

    def first_deal(self):
        self.player.hand.append(self.take_card())
        self.player.hand.append(self.take_card())

        self.dealer.hand.append(self.take_card())
        self.dealer.secret_card.append(self.take_card())

    def next_deal(self):
        pass

    def stand(self):
        pass

    def hint(self, participant):
        new_card = self.take_card()
        participant.hand.append(new_card)

    def take_card(self):
        new_card = self.pack.give_random_card()
        return new_card

    def calculate_hand(self, participant, as_value):
        figures = {'1': 1,
                   '2': 2,
                   '3': 3,
                   '4': 4,
                   '5': 5,
                   '6': 6,
                   '7': 7,
                   '8': 8,
                   '9': 9,
                   '10': 10,
                   'J': 10,
                   'Q': 10,
                   'K': 10,
                   'A': as_value}

        result = sum([figures[card.split()[0]] for card in participant.hand])

        return result


my_pack = PackOfCards(2)
my_card = my_pack.give_random_card()
print(my_pack.translate_card(my_card))

my_player = Player("John")
my_dealer = Dealer()

my_game = BlackJackGame(my_player, my_dealer, my_pack)
my_game.first_deal()
print(my_player.hand)
print(my_game.calculate_hand(my_player, 1))
