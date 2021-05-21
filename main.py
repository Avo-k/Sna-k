from tkinter import *


root = Tk()

l1 = Label(root, text="Hello World!")
l2 = Label(root, text="my name is Avo")

l1.grid(row=0, column=0)
l2.grid(row=1000, column=1)

root.mainloop()
