from tkinter import *

root = Tk()
root.geometry("800x500")
root.title("BlackJack")
root.config(bg="sea green")

from sys import version_info

if version_info.major == 2:
    import Tkinter as tk
elif version_info.major == 3:
    import tkinter as tk

import tkinter.font

blackjack = Label(root, text="BLACKJACK", font=('goudy stout', 20), bg="dark green", fg="goldenrod3", relief=FLAT,
                  borderwidth=5, padx=20)
blackjack.grid(row=0, column=2, columnspan=1)
# sticky = W:E

x = Label(root, bg="sea green")
x.grid(row=1)

myFont1 = tkinter.font.Font(family="cambria", size=13, weight='bold')

bet = Label(root, text="BET: 50$", font=myFont1, bg="yellow3", fg="white", relief=RAISED)
bet.grid(row=2, column=2)

# bet = Entry (root,  bg="red3", fg="white", relief= RAISED)
# bet.grid(row=3, column=2)

myFont2 = tkinter.font.Font(family="cambria", size=13, slant='italic', underline=2, weight='bold')

yourCards = tk.Label(root, text="Your cards:", font=myFont2, bg="sea green", fg="white", )
yourCards.grid(row=3, column=1)

dealerCards = tk.Label(root, text="Dealer cards:", font=myFont2, bg="sea green", fg="white")
dealerCards.grid(row=3, column=3)

cards = Label(root, text="Miejsce na karty nasze karty", width=15, height=3, bg="gray70", relief=FLAT)
cards.grid(row=4, column=1)

cardsD = Label(root, text="Miejsce na karty dealera ", width=15, height=3, bg="gray70", relief=FLAT)
cardsD.grid(column=3)

hint = Button(root, text="Hint", borderwidth=5, font=('cambria', 13), bg="goldenrod3", fg="white", width=10, pady=5)
hint.grid(row=4, column=2)

stand = Button(root, text="Stand", borderwidth=5, font=('cambria', 13), bg="goldenrod3", fg="white", width=10, pady=5)
stand.grid(row=5, column=2)

changeBet = Button(root, text="Change bet", borderwidth=5, font=('cambria', 13), bg="goldenrod3", fg="white", width=10,
                   pady=5)
changeBet.grid(row=6, column=2)

y = Label(root, bg="sea green")
y.grid(row=7)

yourNumber = Label(root, text="Suma punktów gracza", font=('cambria', 13), bg="green3", fg="white", relief=RIDGE,
                   borderwidth=10)
yourNumber.grid(row=8, column=1)

dealerNumber = Label(root, text="Suma punktów Dealera", font=('cambria', 13), bg="green3", fg="white", relief=RIDGE,
                     borderwidth=10)
dealerNumber.grid(row=8, column=3)

z = Label(root, bg="sea green")
z.grid(row=9)

yourBalance = Label(root, text="BALANCE: 250$", font=myFont1, bg="yellow3", fg="white", relief=RAISED)
yourBalance.grid(row=8, column=2)

score = Label(root, text="Score 1 : 0", font=myFont1)
score.grid(row=10, column=2)

root.mainloop()
