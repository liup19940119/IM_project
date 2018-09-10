from tkinter import *
from tkinter.scrolledtext import ScrolledText

root = Tk()
root.geometry('800x500+300+100')

# f1 = Frame(root, width=600, bg='red', height=300)
# f1.grid(row=0, column=0)
f2 = ScrolledText(root, width=20, bg='green', height=20)
f2.grid(row=0, column=1)
f3 = ScrolledText(root, width=97, bg='black', height=7)
f3.grid(row=1, columnspan=2)
f4 = Frame(root, width=800, bg='white', height=100)
f4.grid(row=2, columnspan=2)

l1 = ScrolledText(root, width=75, height=20)
l1.grid(row=0, column=0)


mainloop()
