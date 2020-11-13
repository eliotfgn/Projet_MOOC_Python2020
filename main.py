import turtle
from CONFIGS import *


# Définition des différentes fonctions du jeu

# Affichage du chateau
def lire_matrice(fichier):
    """fonction qui transforme un fichier en matrice"""

    # créaton de la matrice
    matrice = [[int(colonne) for colonne in ligne if colonne.isdigit()] for ligne in open(fichier)]
    return matrice


def calculer_pas(matrice):
    """calcul de la dimension de chaque case pour que le plan contienne la zone d' affichage"""

    pas_largeur = (ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]) // len(matrice[0])
    pas_hauteur = (ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1]) // len(matrice)
    return min(pas_hauteur, pas_largeur)


def coordonnees(case, pas):
    """calcul des coordonnées du coin inférieur gauche de la case passée en argument """

    return -240 + (case[0] * pas), 190 - (case[1] * pas)


def tracer_carre(dimension):
    """tracé d'un carré de dimension donnée. Cette dimension est égale au pas de chaque case"""

    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)


def tracer_case(case, couleur, pas):
    """tracé d'un carré de couleur donnée à un emplacement précis"""
    turtle.speed(0)
    turtle.up()
    turtle.goto(coordonnees(case, pas))
    turtle.down()
    turtle.color('black', couleur)
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()


def afficher_plan(matrice):
    """fonction de tracé du chateau proprement dit."""

    # calcul du pas
    pas_case = calculer_pas(matrice)

    # On commence par atteindre les lignes en sachant que les lignes représentent les ordonnées:
    for y in range(len(matrice)):
        # ensuite on agit sur les colonnes de chaque ligne en sachant que les colonnes représentent les absisces:
        for x in range(len(matrice[0])):
            if matrice[y][x] == 0:
                tracer_case((x, y), COULEUR_CASES, pas_case)
            elif matrice[y][x] == 4:
                tracer_case((x, y), COULEUR_OBJET, pas_case)
            elif matrice[y][x] == 1:
                tracer_case((x, y), COULEUR_MUR, pas_case)
            elif matrice[y][x] == 2:
                tracer_case((x, y), COULEUR_OBJECTIF, pas_case)
            elif matrice[y][x] == 3:
                tracer_case((x, y), COULEUR_PORTE, pas_case)


# Fonctions de déplacement du joueur
def coordonnees_personnage(case, pas):
    """calcul des coordonnees du centre du personnage"""

    return -240 + (case[1] * pas) + pas / 2, 190 + (pas / 2) - (case[0] * pas)


def deplacer(matrice, position, mouvement):
    """Déplacement général du personnage. Cette fonction fera la gestion des collision. Le paramètre position
    actuelle du personnage, et mouvement est sa destination"""

    case_cible = (position[0] + mouvement[0], position[1] + mouvement[1])
    print(case_cible)

    if matrice[case_cible[0]][case_cible[1]] in (0, 2, 4):
        position[0] += mouvement[0]
        position[1] += mouvement[1]
        turtle.undo()
        turtle.up()
        turtle.goto(coordonnees_personnage(position, calculer_pas(matrice)))
        turtle.down()
        print(position)
        turtle.dot(calculer_pas(matrice) * 0.9, 'red')


def colorier_case(case, couleur, pas):
    turtle.undo()
    turtle.up()
    turtle.goto((-240 + pas * case[1]), (190 - pas * case[0]))
    turtle.down()
    turtle.color('black', couleur)
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()


def deplacer_gauche():
    turtle.onkeypress(None, "Left")
    global position, plan
    deplacer(plan, position, (0, -1))
    turtle.onkeypress(deplacer_gauche, "Left")


def deplacer_droite():
    turtle.onkeypress(None, "Right")
    global position, plan
    deplacer(plan, position, (0, 1))
    turtle.onkeypress(deplacer_droite, "Right")


def deplacer_haut():
    turtle.onkeypress(None, "Up")
    global position, plan
    deplacer(plan, position, (-1, 0))
    turtle.onkeypress(deplacer_haut, "Up")


def deplacer_bas():
    turtle.onkeypress(None, "Down")
    global position, plan
    deplacer(plan, position, (1, 0))
    turtle.onkeypress(deplacer_bas, "Down")


# fonctions de collecte des objets
def creer_inventaire(fichier):
    inventaire = {}
    for ligne in open(fichier):
        ligne = str(ligne.strip())
        parts = ligne.split(", ", 2)
        key = ", ".join((parts[0], parts[1]))
        key = tuple(key)
        value = parts[2]
        value = str(value)
        inventaire[key] = value

    print(inventaire)


# Programme principal

# Création et affichage du chateau
creer_inventaire(fichier_objets)

# ouverture du fichier contenant le plan du chateau et transformation en matrice
plan = lire_matrice(fichier_plan)
position = [0, 1]
position_generale = [0, 1]

turtle.hideturtle()
afficher_plan(plan)

# Création et emplacement du personnage
turtle.up()
turtle.goto(coordonnees_personnage((position[0], position[1]), calculer_pas(plan)))
turtle.down()
turtle.dot(calculer_pas(plan) * 0.9, 'red')

# déplacement du personnage
turtle.listen()
turtle.onkeypress(deplacer_haut, "Up")
turtle.onkeypress(deplacer_bas, "Down")
turtle.onkeypress(deplacer_droite, "Right")
turtle.onkeypress(deplacer_gauche, "Left")

# Coloration de la case parcourue


turtle.mainloop()
