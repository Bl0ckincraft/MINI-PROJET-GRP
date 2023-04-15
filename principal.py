import drapeau
import informations
import tkinter as tk

PAYS = [
    'Finland',
    'Czech Republic',
    'Togo'
]


def show(id: int):
    pass


root = tk.Tk("Informations Pays")
root.resizable(False, False)

root.geometry("600x400")

frame = tk.Frame(root)
frame.grid()

for i in range(len(PAYS)):
    tk.Button(frame, text=PAYS[i], command=lambda: show(i)).grid(row=0, col=i)

root.mainloop()

