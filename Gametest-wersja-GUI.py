from tkinter import *
import sqlite3
import random, os
import time
from sys import version_info

if version_info.major == 2:
    import Tkinter as tk
elif version_info.major == 3:
    import tkinter as tk

import tkinter.font

# tutaj wszystkie importy

talia = ['2 S', '3 S', '4 S', '5 S', '6 S', '7 S', '8 S', '9 S', '10 S', 'J S', 'Q S', 'K S', 'A S',
         '2 H', '3 H', '4 H', '5 H', '6 H', '7 H', '8 H', '9 H', '10 H', 'J H', 'Q H', 'K H', 'A H',
         '2 C', '3 C', '4 C', '5 C', '6 C', '7 C', '8 C', '9 C', '10 C', 'J C', 'Q C', 'K C', 'A C',
         '2 D', '3 D', '4 D', '5 D', '6 D', '7 D', '8 D', '9 D', '10 D', 'J D', 'Q D', 'K D', 'A D', ]
# S - spades, piki, H - hearts, kiery, C - clubs, trefle, D - diamonds, karo

dict_values = {'1': 1,
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
# wartość asa może być równa 11 lub 1 w zależności od sytuacji w grze,
# warunki na to czy as jest warty 1 punkt będą oddzielnie rozpatrywane - by default jest 11

dict_suits = {'S': 'pik',
              'H': 'kier',
              'C': 'trefl',
              'D': 'karo'}


def suits(str, dict=dict_suits):
    # zwraca polską nazwe koloru karty
    podzielone = str.split()
    suit = podzielone[0] + ' ' + dict[podzielone[1]]
    return suit


def n_talie(n, talia=talia):
    # tworzy zbiór talii do gry, zwraca tenże zbiór
    zbiór_talii = []
    for i in range(n):
        zbiór_talii = zbiór_talii + talia
    return zbiór_talii


def dealing_cards(lista_kart):
    # będzie losować karte, zwracać krotke (karta, lista_kart bez wylosowanej karty)
    lista_kart1 = lista_kart
    x = len(lista_kart1) - 1  # zakres losowania
    indeks_karty = random.randint(0, x)
    karta = lista_kart1[indeks_karty]
    del lista_kart1[indeks_karty]
    return (karta, lista_kart1)


def suma_pkt(karty_na_ręce, dict_values=dict_values):
    # zwraca krotke: wynik punktowy i wartość true/false czy gracz/dealer bust
    suma = 0
    bust = 1
    ace_present = 0
    for i in karty_na_ręce:
        if i == 'A S' or i == 'A D' or i == 'A H' or i == 'A C':
            ace_present = 1
        podzielone = i.split()
        suma = suma + dict_values[podzielone[0]]
    if suma <= 21:
        bust = 0
    if bust == 1 and ace_present == 1:
        suma = suma - 10
    if suma <= 21:
        bust = 0
    return (suma, bust)


def gra_dilera(dealer, zbiór_gry, gracz):
    ## Zwraca wynik dealera po ewentualnym dobraniu karty i sprawdza czy wygralismy z dealerem (1=TAK, 0=NIE)

    ## DEALER MUSI ODSLONIC KARTY

    losowanie4 = dealing_cards(zbiór_gry)
    wynik_dealer = suma_pkt(dealer)
    wynik_gracz = suma_pkt(gracz)
    wygrana = 0
    dealer_dobral = 0

    if wynik_dealer[0] <= 16:
        dealer.append(losowanie4[0])
        dealer_dobral = 1
        zbiór_gry = losowanie4[1]
        wynik_dealer = suma_pkt(dealer)
        if wynik_dealer[1] == 1:
            wygrana = 1
        else:
            if wynik_dealer[0] < wynik_gracz[0]:
                wygrana = 1
            else:
                wygrana = 0
    elif wynik_dealer[0] < wynik_gracz[0]:
        wygrana = 1
    else:
        wygrana = 0
    return (wynik_dealer[0], wygrana, dealer_dobral)


# ---------------------------------------------------------
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
        self.player = Player()
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


# ---------------------------------------------------------


# ----------- tutaj zaczyna się kod GUI

class Main(Player, Dealer, PackOfCards, BlackJackGame):  # class Main zawiera wszytskie grafiki
    def __init__(self):  # inicjalizacja glownego okna

        self.root = Tk();
        self.root.geometry("500x200")
        self.root.title("BlackJack")
        self.root.config(bg="sea green")
        self.topFrame = Frame(self.root)
        self.topFrame.config(bg="sea green")
        self.topFrame.grid(row=0, column=0)

    def start(self):  # ekran startowy gry
        blackjack = Label(self.topFrame, text="BLACKJACK", font=('goudy stout', 20), bg="sea green", fg="goldenrod3")
        blackjack.grid(row=0, column=1)

        namelabel = Label(self.topFrame, text="Your name:", font=('cambria', 13), bg="sea green", fg="white")
        namelabel.grid(row=1, column=0)

        pack = Label(self.topFrame, text="Pack number:", font=('cambria', 13), bg="sea green", fg="white")
        pack.grid(row=2, column=0)

        e_name = Entry(self.topFrame, borderwidth=3, width=40, justify=CENTER)
        e_name.grid(row=1, column=1, padx=20, pady=(10, 0))

        e_pack = Entry(self.topFrame, borderwidth=3, width=40, justify=CENTER)
        e_pack.grid(row=2, column=1, padx=20, pady=(10, 0))

        # nacisniecie przycisku Play powoduje przejscie do gry oraz zapis imienia i talii
        play = Button(self.topFrame, text="Play", command=lambda: self.game(e_name, e_pack), borderwidth=5,
                      bg="goldenrod3", fg="white")
        play.grid(row=3, column=1, padx=20, pady=10)
        play.config(width=10, height=1, )

        self.root.mainloop()

    def clear(self):  # funkcja czyszczaca ekran
        list = self.topFrame.grid_slaves()
        for l in list:
            l.destroy()

    def game(self, e_name, e_pack):  # ekran rozgrywki z dealerem
        self.name = e_name.get()  # zapisuje w programie, pozniej do pliku trzeba ustawic!!! self.player.name
        self.number = int(e_pack.get())  # zapisuje jako liczbe

        self.clear()

        Player.__init__(self, self.name)
        Dealer.__init__(self)
        PackOfCards.__init__(self, self.number)
        BlackJackGame.__init__(self, self.name, self.number)

        self.root.geometry("550x400")
        self.root.title("BlackJack")
        self.root.config(bg="sea green")

        blackjack2 = Label(self.topFrame, text="BLACKJACK", font=('goudy stout', 20), bg="dark green", fg="goldenrod3",
                           relief=FLAT, borderwidth=5, padx=20)
        blackjack2.grid(row=0, column=2, columnspan=1)
        # sticky = W:E

        x = Label(self.topFrame, bg="sea green")
        x.grid(row=1)

        myFont1 = tkinter.font.Font(family="cambria", size=13, weight='bold')

        self.bet_gui = IntVar()
        bet = Label(self.topFrame, textvariable=self.bet_gui, font=myFont1, bg="yellow3", fg="white", relief=RAISED)
        bet.grid(row=2, column=2)

        def betchange_gui(self, bet):
            betEntry = Entry(self.topFrame, bg="red3", fg="white", relief=RAISED, justify=CENTER)
            betEntry.grid(row=3, column=2)
            betOk = Button(self.topFrame, padx=10, command=lambda: (betOk.destroy(), show_gui(self, betEntry)),
                           text="OK", borderwidth=2, font=('cambria', 8), bg="goldenrod3", fg="white", width=3,
                           height=1)
            betOk.grid(row=3, column=2, sticky=E)

        myFont2 = tkinter.font.Font(family="cambria", size=13, slant='italic', underline=2, weight='bold')

        yourCards = tk.Label(self.topFrame, text="Your cards:", font=myFont2, bg="sea green", fg="white", )
        yourCards.grid(row=3, column=1)

        dealerCards = tk.Label(self.topFrame, text="Dealer cards:", font=myFont2, bg="sea green", fg="white")
        dealerCards.grid(row=3, column=3)

        self.player.hand_gui = StringVar()
        cards = Label(self.topFrame, textvariable=self.player.hand_gui, fg="black", width=15, height=3, bg="gray70",
                      relief=FLAT)
        cards.grid(row=5, column=1)

        self.dealer.hand_gui = StringVar()
        cardsD = Label(self.topFrame, textvariable=self.dealer.hand_gui, width=15, height=3, bg="gray70", relief=FLAT)
        cardsD.grid(row=5, column=3)

        hintbutton = Button(self.topFrame, text="Hint", command=lambda: (show_gui_hint(self)), borderwidth=5,
                            font=('cambria', 13), bg="goldenrod3", fg="white", width=10, pady=5)
        hintbutton.grid(row=4, column=2)

        standbutton = Button(self.topFrame, text="Stand", command=lambda: (show_gui_dealer(self)), borderwidth=5,
                             font=('cambria', 13), bg="goldenrod3", fg="white", width=10, pady=5)
        standbutton.grid(row=5, column=2)

        changeBet = Button(self.topFrame, text="Change bet", command=lambda: betchange_gui(self, self.bet),
                           borderwidth=5, font=('cambria', 13), bg="goldenrod3", fg="white", width=10, pady=5)
        changeBet.grid(row=6, column=2)

        y = Label(self.topFrame, bg="sea green")
        y.grid(row=7)

        self.player.sum_gui = IntVar()
        yourNumber = Label(self.topFrame, textvariable=self.player.sum_gui, font=('cambria', 13), bg="green3",
                           fg="white", relief=RIDGE, borderwidth=10)
        yourNumber.grid(row=8, column=1)

        self.dealer.sum_gui = IntVar()
        dealerNumber = Label(self.topFrame, textvariable=self.dealer.sum_gui, font=('cambria', 13), bg="green3",
                             fg="white", relief=RIDGE, borderwidth=10)
        dealerNumber.grid(row=8, column=3)

        z = Label(self.topFrame, bg="sea green")
        z.grid(row=9)

        self.player.balance_gui = IntVar()
        yourBalance = Label(self.topFrame, textvariable=self.player.balance_gui, font=myFont1, bg="yellow3", fg="white",
                            relief=RAISED)
        yourBalance.grid(row=8, column=2)

        score = Label(self.topFrame, text="Score 0 : 0", font=myFont1)
        score.grid(row=10, column=2)

        hintbutton.config(state=DISABLED)
        standbutton.config(state=DISABLED)

        # BlackJackGame.first_deal(self)
        # BlackJackGame.check_hand_status(self)

        def start_game_gui(self):  # 1  ekran przed wyznaczeniem stawki
            self.player.balance_gui.set("Balance: {0}$".format(self.player.balance))
            self.player.sum_gui.set("Twoje punkty: {0} ".format(self.player.sum))
            self.dealer.sum_gui.set("Punkty dealera: {0} ".format(self.dealer.sum))
            self.bet_gui.set("Bet: {0}$".format(self.bet))

        def show_gui(self, betEntry):  # 2 ekran po zaczeciu gry, pierwsze rozdanie
            BlackJackGame.first_deal(self)
            BlackJackGame.check_hand_status(self)
            hintbutton.config(state=NORMAL)
            standbutton.config(state=NORMAL)
            self.bet = int(betEntry.get())
            self.bet_gui.set("Bet: {0}$".format(self.bet))
            betEntry.destroy()
            changeBet.config(state=DISABLED)

            self.player.hand[0] = PackOfCards.translate_card(self, self.player.hand[0])
            self.player.hand[1] = PackOfCards.translate_card(self, self.player.hand[1])
            self.player.hand_gui.set("{0}\n{1}".format(self.player.hand[0], self.player.hand[1]))

            self.dealer.hand[0] = PackOfCards.translate_card(self, self.dealer.hand[0])
            self.dealer.hand_gui.set("{0}".format(self.dealer.hand[0]))

            self.player.balance_gui.set("Balance: {0}$".format(self.player.balance))
            self.player.sum_gui.set("Twoje punkty: {0} ".format(self.player.sum))
            self.dealer.sum_gui.set("Punkty dealera: {0} ".format(self.dealer.sum))
            self.bet_gui.set("Bet: {0}$".format(self.bet))

        # start_game_gui(self)
        # show_gui(self)

        # def show_gui_bet(self,betEntry):
        # hintbutton.config(state=NORMAL)
        # standbutton.config(state=NORMAL)
        # self.bet=betEntry.get()
        # self.bet_gui.set("Bet: {0}$".format(self.bet))
        # betEntry.destroy()
        # changeBet.config(state=DISABLED)
        # hintbutton.config(state=ACTIVE)
        # standbutton.config(state=ACTIVE)

        def end_game(self):
            #             self.player.sum = self.calculate_hand(self.player)
            #             self.dealer.sum = self.calculate_hand(self.dealer)

            #            if (self.player.sum>self.dealer.sum):
            #                if (self.player.sum>21):            #lose
            #                    self.game_result=2
            #                elif(self.player.sum<+=21):         #win
            #                    self.game_result=1
            #
            #            elif(self.player.sum<self.dealer.sum):
            #                if (self.dealer.sum>21):            #win
            #
            #                elif(self.dealer.sum<+=21):         #lose
            #
            #            elif(self.player.sum==self.dealer.sum): #draw
            # BlackJackGame.check_hand_status(self)
            self.player.sum = self.calculate_hand(self.player)
            self.dealer.sum = self.calculate_hand(self.dealer)

            # if not self.player_round_end:  # player game
            if (self.player.sum > 21):
                self.game_result = 2
            # else:  # dealer game
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

            print(self.bet)
            print(self.game_result)
            # self.game_result_gui = StringVar()

            time.sleep(1)
            self.end_game_view()  # przejscie do ostatniego okna
            # time.sleep(4)

        def show_gui_dealer(self):
            hintbutton.config(state=DISABLED)
            standbutton.config(state=DISABLED)

            BlackJackGame.secret_card_reverse(self)
            BlackJackGame.check_hand_status(self)
            while self.dealer.sum <= 16:
                BlackJackGame.check_hand_status(self)
                BlackJackGame.hint(self, self.dealer)
                BlackJackGame.check_hand_status(self)

            self.dealer.hand[1] = PackOfCards.translate_card(self, self.dealer.hand[
                1])  # podpięte na sztywno, trzeba ogarnąć zeby dzialalo niezaleznie od ilosci kart dealera, tak samo dla playera
            # self.dealer.hand[2]=PackOfCards.translate_card(self,self.dealer.hand[2])
            self.dealer.hand_gui.set(
                "{0}\n{1}".format(self.dealer.hand[0], self.dealer.hand[1]))  # ,self.dealer.hand[2]))
            BlackJackGame.check_hand_status(self)
            self.dealer.sum_gui.set("Punkty dealera: {0} ".format(self.dealer.sum))
            print(self.dealer.hand)

            end_game(self)

        def show_gui_hint(self):

            new_card = BlackJackGame.take_card(self)
            self.player.hand.append(new_card)

            self.player.hand[2] = PackOfCards.translate_card(self, self.player.hand[2])
            self.player.hand_gui.set(
                "{0}\n{1}\n{2}".format(self.player.hand[0], self.player.hand[1], self.player.hand[2]))
            BlackJackGame.calculate_hand(self, self.player)
            self.player.sum_gui.set("Twoje punkty: {0} ".format(self.player.sum))
            if (self.player.sum > 21):
                end_game(self)

        ###
        start_game_gui(self)

        ####

    def end_game_view(self):  # ekran koncowy gry

        self.clear()

        # Player.__init__(self,self.name)
        # Dealer.__init__(self)
        # PackOfCards.__init__(self,self.number)
        # BlackJackGame.__init__(self,self.name,self.number)

        self.root.geometry("550x400")
        self.root.title("BlackJack")
        self.root.config(bg="sea green")

        blackjack = Label(self.topFrame, text="BLACKJACK", font=('goudy stout', 20), bg="dark green", fg="goldenrod3",
                          relief=FLAT, borderwidth=5)
        blackjack.grid(row=0, column=2, columnspan=1)

        x = Label(self.topFrame, bg="sea green", width=15)
        x.grid(row=1, column=1)

        myFont1 = tkinter.font.Font(family="cambria", size=30, weight='bold')

        self.game_result_gui = IntVar()
        result = Label(self.topFrame, textvariable=self.game_result_gui, font=myFont1, bg="sea green", fg="white",
                       width=15)
        result.grid(row=2, column=2)

        y = Label(self.topFrame, bg="sea green", height=1)
        y.grid(row=3, column=1)

        balance = Label(self.topFrame, textvariable=self.player.balance_gui, justify=CENTER, padx=30,
                        font=("cambria", 20), bg="sea green", fg="white", relief=FLAT)
        balance.grid(row=4, column=2, columnspan=4)

        z = Label(self.topFrame, bg="sea green", height=1)
        z.grid(row=5, column=1)

        playAgain = Button(self.topFrame, text="Play again", command=lambda: (self.game()), borderwidth=5,
                           font=('cambria', 13), bg="goldenrod3", fg="white", width=12, pady=5)
        playAgain.grid(row=6, column=2)

        playAgain = Button(self.topFrame, text="Save and close", command=lambda: (self.root.destroy()), borderwidth=5,
                           font=('cambria', 13), bg="goldenrod3", fg="white", width=12, pady=5)
        playAgain.grid(row=7, column=2)

        self.game_result_gui.set("You {0}".format(self.game_result))
        self.player.balance_gui.set("Balance: {0}$".format(self.player.balance))

        # root.mainloop()


# ------------------------------------
if __name__ == '__main__':  # czesc 'wykonywalna' gry w oknie
    gra = Main()
    gra.start()

# ------------------------------------
