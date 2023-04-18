import drapeau
import informations
import tkinter as tk

# On entre ici la liste des pays à afficher, par l'utilisation de cette liste, le code est plus maintenable puisqu'il
# suffit d'ajouter son nom ici et de créer une nouvelle fonction dans drapeau.py pour ajouter un nouveau pays.
PAYS = [
    'Finland',
    'Czech Republic',
    'Togo',
    'India',
    'France'
]

currentId = -1


def createButtonClickHandler(id):
    """
    On utilise une autre fonction pour générer le click handler des boutons de sélection des pays car avec une fonction
    lambda, on rencontre un problème.
    Le problème est que puisque le lamba est utilisé dans une boucle for et qu'il utilise l'index de la boucle alors, il
    ne créer pas de copie de l'index et utilise alors la même instance ce qui a pour effet d'utiliser la dernière valeur
    de l'index. (Pour une boucle à trois répétitions d'index "i", lambda: show(i) correspondait à show(2) dans chaque
    répétition car lors de la dernière execution de la boucle, i = 2.)

    :param id: identifiant du pays.
    :return: le click handler du bouton.
    """

    def buttonClickHandler():
        show(id)

    return buttonClickHandler


def show(id: int):
    """
    Cette fonction va afficher les données d'un pays en fonction de son identifiant dans la liste PAYS ci-dessus.

    :param id: identifiant du pays.
    """

    # Import de la variable globale currentId.
    global currentId
    # Si les données du pays ne sont pas affichées alors on les affiche.
    if id != currentId:
        # On change currentId pour savoir que ce sont les données de ce pays qui sont maintenant affichées.
        currentId = id
        # On supprime les widgets déja présent dans le conteneur de données.
        for widget in dataContainer.winfo_children():
            widget.destroy()

        tk.Label(dataContainer, text=PAYS[id], font=("Arial", 14, "bold")).pack()

        # On récupère le drapeau du pays à l'aide du fichier drapeau.py.
        flag = drapeau.getFlag(PAYS[id])

        # Si l'on a le drapeau alors on l'ajoute dans notre conteneur
        if flag is not None:
            label = tk.Label(dataContainer, image=flag)
            label.image = flag
            label.pack(pady=20)

        tk.Label(dataContainer, text=f"Capitale : {informations.capitale(PAYS[id])}").pack()
        tk.Label(dataContainer, text=f"Espérance de vie : {informations.esperances(PAYS[id])} ans").pack()
        tk.Label(dataContainer, text=f"Rang parmis son continent : {informations.classement(PAYS[id])}").pack()
        cities = informations.trois_villes(PAYS[id])
        tk.Label(dataContainer, text=f"Villes les plus peuplées du pays : {''.join([cities[i] + (', ' if i < len(cities) - 2 else (' et ' if i < len(cities) - 1 else '')) for i in range(len(cities))])}").pack()


# On créer notre fenêtre tkinter et on lui donne un nom.
root = tk.Tk()
root.title("Informations des pays")
root.resizable(False, False)

# On créer une barre de boutons avec un bouton pour chaque pays à l'intérieur.
buttonBar = tk.Frame(root)
for i in range(len(PAYS)):
    button = tk.Button(buttonBar, text=PAYS[i], command=createButtonClickHandler(i))
    button.grid(row=0, column=i, padx=5)

# On créer un conteneur pour stocker les données à afficher dont le drapeau, la population...
dataContainer = tk.Frame(root)
emptyLabel = tk.Label(dataContainer, text="Vous pouvez voir les informations d'un pays en cliquant sur le bouton associé juste au dessus.", padx=10)
emptyLabel.pack()

# On ajoute nos conteneurs dans la fenêtre.
buttonBar.grid(row=0, column=0, pady=20, padx=5)
dataContainer.grid(row=1, column=0, pady=5, padx=5)

# On lance la boucle principale de notre fenêtre tkinter.
root.mainloop()

