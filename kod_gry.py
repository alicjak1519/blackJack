import random

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


print('Lets play blackjack! 1 - new game, 2 - scoreboard')  # scoreboard będzie zaimplementowany później
x = int(input())  # x wykorzystuje jako zmienną tylko do sterowania programu
if x == 1:
    money = 500
    print("Zaczynamy grę\nTwoje pieniądze na start to:", money, ", Powodzenia!")
else:
    print("narazie sie nie da, ale możemy zagrać")
    money = 500

print("ile talii od blackjacka? Podaj liczbe całkowitą w zakresie 1-8")
ilosc_talii = int(input())  # można potem zachować do wyników

while ilosc_talii > 8:
    print("Talii nie może być więcej niż osiem, podaj mniejszą ilość talii")
    ilosc_talii = int(input())  # warunki na to, żeby talia była wybrana w zadanych przez nas granicach

while ilosc_talii < 1:
    print("Minimalna liczba talii to jedna talia, podaj więszką liczbe")
    ilosc_talii = int(input())

print('wybrałeś grę', ilosc_talii, 'taliami')
gra = 1
while gra == 1:
    zbiór_gry = n_talie(ilosc_talii)
    dealer = []
    gracz = []

    bet = 0
    bet_modify = 0

    for i in range(2):
        losowanie1 = dealing_cards(zbiór_gry)
        gracz.append(losowanie1[0])
        zbiór_gry = losowanie1[1]
        losowanie2 = dealing_cards(zbiór_gry)
        dealer.append(losowanie2[0])
        zbiór_gry = losowanie2[1]
    wynik = suma_pkt(gracz)

    bet_min: int = 0.1 * money
    print('Ile chcesz postawić? Minimum', bet_min, 'maksimum', money)

    while 1 == 1:
        bet = int(input())
        if bet >= bet_min and bet <= money:
            money = money - bet
            print('Twoja kasa:', money, 'Twoja stawka:', bet)
            print('Twoje karty:', suits(gracz[0]), ',', suits(gracz[1]), 'a twój wynik to', wynik[0])
            print('Dealer: ZAKRYTA,', suits(dealer[1]))

            if money >= 2 * bet:
                print('Podwoić stawkę, potroić stawkę czy zostawić obecną? 1/2/3')
                bet_modify = int(input())
                if bet_modify == 1:
                    money = money - bet
                    bet += bet
                    print('Twoja kasa:', money, 'Twoja stawka:', bet)
                if bet_modify == 2:
                    money = money - 2 * bet
                    bet += 2 * bet
                    print('Twoja kasa:', money, 'Twoja stawka:', bet)
                if bet_modify == 3:
                    print('Zostawiasz obecną stawkę')

            elif money >= bet:
                print('Podwoić stawkę czy nie? 1/2')
                bet_modify = int(input())
                if bet_modify == 1:
                    money = money - bet
                    bet += bet
                    print('Twoja kasa:', money, 'Twoja stawka:', bet)
                if bet_modify == 2:
                    print('Zostawiasz obecną stawkę')

            break
        elif bet < bet_min:
            print('Musisz postawić więcej')
        else:
            print('Nie masz tyle pieniędzy')

    while 1 == 1:
        print('Stand or hit? 1/2')
        x = int(input())
        if x == 1:
            wynik = suma_pkt(gracz)
            print('Twój wynik to', wynik[0])
            result = gra_dilera(dealer, zbiór_gry, gracz)
            print('Odkryte karty dealera:', suits(dealer[0]), ', ', suits(dealer[1]))

            if result[2] == 1:
                print('Dealer dobrał', suits(dealer[2]))

            if result[1] == 1:  # pokazać karty dealera
                money = money + 1.5 * bet
                print('Wygrałeś', 0.5 * bet, '- wynik dealera to:', result[0])
            else:
                print('Przegrałeś', bet, '- wynik dealera to:', result[0])
            break
        else:
            losowanie3 = dealing_cards(zbiór_gry)
            gracz.append(losowanie3[0])
            zbiór_gry = losowanie3[1]
        wynik_g = suma_pkt(gracz)

        if wynik_g[0] < 21:
            print('Twój wynik to', wynik_g[0])

        if wynik_g[0] == 21:
            print('Sprawdzam czy dealer też dostanie 21:')
            result = gra_dilera(dealer, zbiór_gry, gracz)
            print('Odkryte karty dealera:', suits(dealer[0]), ',', suits(dealer[1]))
            if result[2] == 1:
                print('Dealer dobrał', suits(dealer[2]))

            if result[1] == 1:
                money = money + 2 * bet
                print('Wygrałeś', bet, '- wynik dealera to:', result[0])
            else:
                print('Przegrałeś', bet, '- wynik dealera to:', result[0])
            break

        if wynik_g[1] == 1:
            print('Przegrałeś', bet, ' Twoje karty to:')
            for i in gracz:
                print(suits(i))
            print('Dealer:', suits(dealer[0]), ',', suits(dealer[1]))
            wynik_d = suma_pkt(dealer)
            print('Wynik dealera to:', wynik_d[0])
            break
    print("Czy chcesz grać dalej, czy zabierasz kase i lecisz do domu? 1 - gram, 2 - uciekam")
    gra = int(input())
