from tkinter import *

root = Tk()
root.geometry("600x400")
root.title("BlackJack")
root.config(bg="sea green")

from sys import version_info

if version_info.major == 2:
    import Tkinter as tk
elif version_info.major == 3:
    import tkinter as tk

import tkinter.font

blackjack = Label(root, text="BLACKJACK", font=('goudy stout', 20), bg="dark green", fg="goldenrod3", relief=FLAT,
                  borderwidth=5)
blackjack.grid(row=0, column=2, columnspan=1)

x = Label(root, bg="sea green", width=15)
x.grid(row=1, column=1)

myFont1 = tkinter.font.Font(family="cambria", size=30, weight='bold')

result = Label(root, text="YOU WIN/LOST!", font=myFont1, bg="sea green", fg="white", width=15)
result.grid(row=2, column=2)

y = Label(root, bg="sea green", height=1)
y.grid(row=3, column=1)

balance = Label(root, text="Your balance: 250$", justify=CENTER, padx=30, font=("cambria", 20), bg="sea green",
                fg="white", relief=FLAT)
balance.grid(row=4, column=2, columnspan=4)

z = Label(root, bg="sea green", height=1)
z.grid(row=5, column=1)

playAgain = Button(root, text="Play again", borderwidth=5, font=('cambria', 13), bg="goldenrod3", fg="white", width=12,
                   pady=5)
playAgain.grid(row=6, column=2)

playAgain = Button(root, text="Save and close", borderwidth=5, font=('cambria', 13), bg="goldenrod3", fg="white",
                   width=12, pady=5, command=root.quit)
playAgain.grid(row=7, column=2)

root.mainloop()
