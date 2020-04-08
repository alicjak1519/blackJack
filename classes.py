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
        self.player_sum = self.calculate_hand(self.player)
        self.dealer = dealer
        self.dealer_sum = self.calculate_hand(self.dealer)
        self.pack = pack
        self.bet = 0
        self.game_result = 0  # 0 - game not end, 1 - player win, 2 - player lose
        self.player_round_end = 0  # 0 - player round, 1 - dealer round
        self.end_type = 0  # 0 - unknown, 1 - play again, 2 - save and close

    def first_deal(self):
        self.player.hand.append(self.take_card())
        self.player.hand.append(self.take_card())

        self.dealer.hand.append(self.take_card())
        self.dealer.secret_card.append(self.take_card())

    def set_bet_value(self, value):
        if value <= self.player.balance:
            self.player.balance -= value
            self.bet = value

    def raise_bet_value(self, multiplier=2):
        if (multiplier - 1) * self.bet <= self.player.balance:
            self.player.balance -= (multiplier - 1) * self.bet
            self.bet *= multiplier
            self.hint(self.player)
            self.player_round_end = 1

    def player_deal(self):
        while self.game_result == 0 or self.player_round_end:
            self.check_hand_status()
            self.set_and_do_player_choice()
            self.check_hand_status()

    def dealer_deal(self):
        if self.game_result == 0:
            self.secret_card_reverse()
            while self.game_result == 0:
                self.check_hand_status()
                self.hint(self.dealer)
                self.check_hand_status()

    def play_a_game(self):
        self.player_deal()
        self.dealer_deal()

    def secret_card_reverse(self):
        self.dealer.hand.append(self.dealer.secret_card)
        self.dealer.secret_card = []

    def stand(self):
        self.player_round_end = 1

    def hint(self, participant):
        new_card = self.take_card()
        participant.hand.append(new_card)

    def take_card(self):
        new_card = self.pack.give_random_card()
        return new_card

    def calculate_hand(self, participant):
        figures_dict = {'1': 1,
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
                        'A': 11}

        figures_in_hand = [card.split()[0] for card in participant.hand]
        result = sum([figures_dict[figure] for figure in figures_in_hand])

        if 'A' in figures_in_hand:
            if result > 21:
                figures_dict['A'] = 1
                result = sum([figures_dict[figure] for figure in figures_in_hand])

        return result

    def uncover_secret_card(self):
        self.dealer.hand += self.dealer.secret_card
        self.dealer.secret_card = []

    def check_hand_status(self):
        if not self.player_round_end:  # player game
            if self.player_sum > 21:
                self.game_result = 2
            elif self.player_sum == 21:
                self.player.balance += 1.5 * self.bet
                self.game_result = 1
        else:  # dealer game
            if self.dealer_sum > 21:
                self.player.balance += 2 * self.bet
                self.game_result = 1
            elif self.dealer_sum >= 17:
                if self.dealer_sum < self.player_sum:
                    self.player.balance += 2 * self.bet
                    self.game_result = 1
                else:
                    self.game_result = 2

        if self.game_result:
            self.end_type = self.set_end_type()

    def set_end_type(self, user_choice=1):
        return user_choice

    def set_and_do_player_choice(self, player_choice='hint'):
        opt_dict = {
            'hint': self.hint(self.player),
            'stand': self.stand(),
            'raise_bet': self.raise_bet_value()
        }
        return opt_dict[player_choice]

    def play_again(self):
        self.play_a_game()

    def save_and_close(self):
        pass
