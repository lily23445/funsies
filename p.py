import tkinter 
from tkinter import *

food=['Pizza', 'Burger', 'Pasta', 'Salad', 'Sushi']

window=Tk()
x=IntVar()
for index in range(len(food)):
    radiobutton=Radiobutton(window, text=food[index], value=index)
    radiobutton.grid(row=index, column=0, sticky=W)

window.mainloop()
