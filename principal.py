import drapeau
import informations
import tkinter as tk

PAYS = [
    'Finland',
    'Czech Republic',
    'Togo'
]

currentId = -1


def createButtonClickHandler(id):
    def buttonClickHandler():
        show(id)

    return buttonClickHandler


def show(id: int):
    global currentId
    if id != currentId:
        currentId = id
        for widget in dataContainer.winfo_children():
            widget.destroy()

        flag = drapeau.getFlag(PAYS[id])

        if flag is not None:
            label = tk.Label(dataContainer, image=flag)
            label.image = flag
            label.pack()


root = tk.Tk()
root.title("Informations des pays")

buttonBar = tk.Frame(root)
for i in range(len(PAYS)):
    button = tk.Button(buttonBar, text=PAYS[i], command=createButtonClickHandler(i))
    button.grid(row=0, column=i, padx=5)

dataContainer = tk.Frame(root)
emptyLabel = tk.Label(dataContainer, text="Vous pouvez voir les informations d'un pays en cliquant sur le bouton associé juste au dessus.", padx=10)
emptyLabel.pack()

buttonBar.grid(row=0, column=0, pady=20, padx=5)
dataContainer.grid(row=1, column=0, pady=5, padx=5)

root.mainloop()

