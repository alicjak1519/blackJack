import random
import pandas as pd
from datetime import date


class Player:
    def __init__(self, name=""):
        self.name = name
        self.balance = 500
        self.hand = []
        self.sum = 0


class Dealer:
    def __init__(self):
        self.secret_card = []
        self.hand = []
        self.sum = 0


class PackOfCards:
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


class BlackJackGame:
    def __init__(self, player, pack_number):
        self.player = player
        self.dealer = Dealer()
        self.pack = PackOfCards(pack_number)
        self.bet = 0
        self.game_result = 0  # 0 - game not end, 1 - player win, 2 - player lost, 3 - draw
        self.player_round_end = 0  # 0 - player round, 1 - dealer round
        self.end_type = 0  # 0 - unknown, 1 - play again, 2 - save and close

    def first_deal(self):
        self.player.hand.append(self.take_card())
        self.player.hand.append(self.take_card())

        self.dealer.hand.append(self.take_card())
        self.dealer.secret_card.append(self.take_card())
        self.print_status()  # ONLY FOR TESTS

    def set_bet_value(self, value):
        if value <= self.player.balance:
            self.player.balance -= value
            self.bet = value

    def raise_bet_value(self, multiplier=2):
        multiplier = int(input("How many times?\n"))
        if (multiplier - 1) * self.bet <= self.player.balance:
            self.player.balance -= (multiplier - 1) * self.bet
            self.bet *= multiplier
            self.hint(self.player)
            self.check_hand_status()
            self.player_round_end = 1

    def player_game(self):
        bet_value = input("How many dollars you bet? ")  # ONLY FOR TESTS
        self.set_bet_value(int(bet_value))
        self.check_hand_status()  # ONLY FOR TESTS
        self.print_status()  # ONLY FOR TESTS
        while self.game_result == 0 and not self.player_round_end:
            self.check_hand_status()
            player_choice = input("What do you want to do? [hint/raise bet/stand]\n")  # ONLY FOR TESTS
            self.set_and_do_player_choice(player_choice)
            self.check_hand_status()
            self.print_status()  # ONLY FOR TESTS

    def dealer_game(self):
        if self.game_result == 0:
            self.secret_card_reverse()
            while self.game_result == 0:
                self.check_hand_status()
                self.hint(self.dealer)
                self.check_hand_status()
                self.print_status()  # ONLY FOR TESTS

    def play_a_game(self):
        self.first_deal()
        self.player_game()
        self.dealer_game()

    def secret_card_reverse(self):
        self.dealer.hand.append(self.dealer.secret_card[0])
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
        self.player.sum = self.calculate_hand(self.player)
        self.dealer.sum = self.calculate_hand(self.dealer)

        if not self.player_round_end:  # player game
            if self.player.sum > 21:
                self.game_result = 2
        else:  # dealer game
            if self.dealer.sum > 21:
                self.player.balance += 2 * self.bet
                self.game_result = 1
            elif self.dealer.sum >= 17:
                if self.dealer.sum == self.player.sum:
                    self.player.balance += self.bet
                    self.game_result = 3
                elif self.player.sum == 21:
                    self.player.balance += 1.5 * self.bet
                    self.game_result = 1
                elif self.dealer.sum < self.player.sum:
                    self.player.balance += 2 * self.bet
                    self.game_result = 1
                else:
                    self.game_result = 2

        if self.game_result:
            self.save_score()
            self.end_type = self.set_end_type()
            if self.end_type == 1:
                self.play_again()
            else:
                exit(0)

    def set_end_type(self, user_choice=1):
        self.print_status()  # ONLY FOR TESTS
        user_input = input("GAME END. Play again? [y/n]\n")  # ONLY FOR TESTS
        if user_input == 'y':  # ONLY FOR TESTS
            user_choice = 1  # ONLY FOR TESTS
        else:  # ONLY FOR TESTS
            user_choice = 0  # ONLY FOR TESTS

        return user_choice

    def set_and_do_player_choice(self, player_choice='hint'):
        if player_choice == 'hint':
            self.hint(self.player)
        elif player_choice == 'raise bet':
            self.raise_bet_value()
        else:
            self.stand()

    def play_again(self):
        self.player.hand = []
        self.player.sum = 0
        self.dealer.hand = []
        self.dealer.secret_card = []
        self.dealer.sum = 0
        self.game_result = 0
        self.play_a_game()

    def save_score(self):
        scores_table = pd.read_csv(r"scores_table.csv")

        if self.player.name in scores_table.values:
            scores_table.loc[scores_table['player_name'] == self.player.name, ['player_score']] += self.player.sum
            scores_table.loc[scores_table['player_name'] == self.player.name, ['last_game_date']] = date.today()

        else:
            game_info = {'player_name': self.player.name, 'player_score': self.player.sum,
                         'last_game_date': date.today()}
            scores_table = scores_table.append(game_info, ignore_index=True)

        scores_table.to_csv(r"scores_table.csv", index=False)

    def print_status(self):
        print(
            f"\n\nYour hand: {self.player.hand}, your points: {self.player.sum} and your balance: {self.player.balance}.\n"  # ONLY FOR TESTS
            f"Dealer hand: {self.dealer.hand}, dealer points: {self.dealer.sum}. Bet is {self.bet}.\n"  # ONLY FOR TESTS
            f"Game status: {self.game_result} (0 - no result now, 1 - you win, 2 - you lost, 3 - draw).")  # ONLY FOR TESTS


def print_scores():
    scores_table = pd.read_csv(r"scores_table.csv")
    print(scores_table)
