from tkinter import *
import sqlite3


# def buttom_click():
def myClick():
    playLabel = Label(root, text="CDN :)")
    playLabel.grid(row=4, column=2)


# def show():
# 	myLabel = Label(root, text=var.get()).pack()


root = Tk()
root.geometry("500x200")
root.title("BlackJack")
root.config(bg="sea green")

blackjack = Label(root, text="BLACKJACK", font=('goudy stout', 20), bg="sea green", fg="goldenrod3")
blackjack.grid(row=0, column=1)

name = Label(root, text="Your name:", font=('cambria', 13), bg="sea green", fg="white")
name.grid(row=1, column=0)

pack = Label(root, text="Pack number:", font=('cambria', 13), bg="sea green", fg="white")
pack.grid(row=2, column=0)

e_name = Entry(root, borderwidth=3, width=40, justify=CENTER)
e_name.grid(row=1, column=1, padx=20, pady=(10, 0))

e_pack = Entry(root, borderwidth=3, width=40, justify=CENTER)
e_pack.grid(row=2, column=1, padx=20, pady=(10, 0))

play = Button(root, text="Play", command=myClick, borderwidth=5, bg="goldenrod3", fg="white")
play.grid(row=3, column=1, padx=20, pady=10)
play.config(width=10, height=1)

root.mainloop()
