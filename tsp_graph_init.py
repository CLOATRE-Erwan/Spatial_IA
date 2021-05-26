import numpy as np
import random
import pandas as pd
import tkinter as tk

random.seed(1)
np.random.seed(1)


class Lieu:
    #Definir un objet Lieu avec un point x et y
    def __init__(self, x, y):
        self.x = x
        self.y = y

    #Calcul de distance euclidienne entre deux points, A et B
    @classmethod
    def calcul_distance(cls, a, b):
        A = np.array((a.x ,a.y))
        B = np.array((b.x ,b.y))
        return np.linalg.norm(A - B)


class Graph:
    #Generer des lieux aléatoirement
    def generer_graph(self, largeur, hauteur, nb_lieux):
        self.nb_lieux = nb_lieux
        self.liste_lieux = [Lieu(random.randint(0, largeur), random.randint(0, hauteur)) for _ in range(nb_lieux)]

    #Créer la matrice euclidienne de chaque points
    def calcul_matrice_cout_od(self):
        self.matrice_od = np.zeros((self.nb_lieux, self.nb_lieux))

        for i in range(self.nb_lieux):
            for j in range(self.nb_lieux):
                if i == j: break
                self.matrice_od[i][j] = Lieu.calcul_distance(self.liste_lieux[i], self.liste_lieux[j])
                self.matrice_od[j][i] = self.matrice_od[i][j]

        self.matrice_od = pd.DataFrame(self.matrice_od)

    #Trouver le voisin le plus proche à partir de la matrice
    #visites=True permet d'ajouter une liste de points déjà visités
    def plus_proche_voisin(self, point, visites=None):
        if visites == None:
            voisin = self.matrice_od[self.matrice_od > 0][point].idxmin()
        else:
            filter_ = self.matrice_od.index.isin(visites)
            matrice = self.matrice_od[~filter_][self.matrice_od > 0][point]
            voisin = matrice.idxmin()
        return voisin

    #Permet de charger un graph à partir d'un fichier csv
    def charger_graph(self, file):
        df = pd.read_csv(file)
        self.liste_lieux = [Lieu(x, y) for x, y in zip(df.x, df.y)]
        self.nb_lieux = len(self.liste_lieux)
    
    #Permet de sauvergarder les points dans un fichier csv
    def sauvegarder_graph(self, file):
        df = pd.DataFrame(columns=['x', 'y'])
        for point in self.liste_lieux:
            df = df.append(vars(point), ignore_index=True)

        df.to_csv(file, index=False)


class Route:
    #Permet de créer un objet route. 
    #random:bool permet de générer un ordre aléatoire ou alors utiliser une heurisique plus proche voisin
    def __init__(self, graph, random=False):
        self.graph = graph
        self.ordre = []
        if not random:
            self.generer_route()
        else:
            self.generer_random()

    #permet de définir 'objet.taille' de la longueur de ordre
    @property
    def taille(self):
      return len(self.ordre)

    #Permet d'utiliser 'objet[key] = value' pour définir et changer des valeurs dans ordre
    def __setitem__(self, key, value):
      self.ordre[key] = value

    #Permet d'utiliser 'value = objet[key]' pour récupérer des valeurs de ordre
    def __getitem__(self, index):
        return self.ordre[index]

    def __repr__(self):
        return f'Route({self.ordre})'

    #Permet de générer une route random en partant de finisissant à 0 et en parcourant tous les lieux
    def generer_random(self):
        route = [i for i in range(1, self.graph.nb_lieux)]
        random.shuffle(route)
        route.insert(0,0)
        route.append(0)
        self.ordre = route
        
    #Permet de définir une route de passage en prenant une heuristique du plus proche voisin
    def generer_route(self):
        route = [0]
        for point in range(self.graph.nb_lieux-1):
            voisin = self.graph.plus_proche_voisin(route[point], route)
            route.append(voisin)
        route.append(0)
        self.ordre = route

    #Permet de calculer la distance totale d'une route
    def calcul_distance_route(self):
        distance = 0
        for i in range(len(self.ordre)-1):
            x = self.ordre[i]
            y = self.ordre[i+1]
            distance += self.graph.matrice_od[y][x]
        self.distance = distance
        return distance

    #Retourne un booleen si le lieu fait parti de l'ordre
    def contient(self, lieu):
        condition = lieu in self.ordre
        return condition

class Population:
    #Permet de créer une population avec une taille définie
    def __init__(self, graph, taille):
        self.graph = graph
        self.routes = [None for i in range(taille)]

    #Permet d'itérer sur l'objet depuis la liste routes
    def __iter__(self):
        yield from self.routes

    #Permet d'utiliser 'objet[key] = value' pour définir et changer des valeurs dans routes
    def __setitem__(self, key, value):
      self.routes[key] = value

    #Permet d'utiliser 'value = objet[key]' pour récupérer des valeurs de routes
    def __getitem__(self, index):
        return self.routes[index]

    #Permet de définir 'len(objet)' sur la longueur de la liste routes
    def __len__(self):
        return len(self.routes)

    #Permet de générer une population de taille n en partant d'une heuristique ou non
    def generer_population(self, random=True):
        for i in range(len(self)):
            route = Route(self.graph, random)
            self.routes[i] = route

    #Permet de trouver la meilleur route de la population d'après la longueur de chaque route
    def trouver_meilleur(self):
        meilleur = self.routes[0]
        for i in range(len(self)):
            if meilleur.calcul_distance_route() >= self.routes[i].calcul_distance_route():
                meilleur = self.routes[i]
        self.meilleur = meilleur
        return meilleur


class Affichage(tk.Frame):
    def __init__(self, hauteur, largeur, graph, master=None,):
        super().__init__(master)
        self.master = master
        self.hauteur = hauteur
        self.hauteur_canvas = hauteur-100
        self.largeur = largeur
        self.largeur_canvas = largeur-100
        self.lieux = []
        self.graph = graph
        self.r = 10
        self.test = tk.StringVar()
        
        master.title("Groupe n°1 : Pereg, Jamal, Erwan")
        master.geometry(str(self.hauteur)+'x'+str(self.largeur))

        for lieu in self.graph.liste_lieux:
            coor = (lieu.x,lieu.y)
            self.lieux.append(coor)

        self.label = tk.Label(self.master, text="Simplon Spatial IA")
        self.label.pack()

        self.canvas = tk.Canvas(self.master, width=largeur-150, height=hauteur-150, bg='ivory')
        self.canvas.pack()

        self.create_route(self.canvas, self.lieux)
        self.create_all_circle(self.lieux)
        
        self.label_distance = tk.Label(self.master, textvariable=self.test)
        self.label_distance.pack()

        self.close_button = tk.Button(self.master, text="Close", command=master.quit)
        self.close_button.pack()
    
    def create_circle(self, x, y, r, i, canvas):
        y = int(self.canvas['height']) - y
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        if i == 0:
            canvas.create_oval(x0, y0, x1, y1, fill='red', outline='red')
        else:
            canvas.create_oval(x0, y0, x1, y1, fill='light blue', outline='red')
        canvas.create_text(x0+r,y0+r, text=str(i))

    def create_route(self, canvas, lieux):
        lst_route = Route.generer_route(self.graph)
        self.test.set('Distance : ' + str(Route.calcul_distance_route(self.graph, lst_route)))
        for i in range(len(lst_route)-1):
            A = (lieux[lst_route[i]][0],int(self.canvas['height']) - lieux[lst_route[i]][1])
            B = (lieux[lst_route[i+1]][0],int(self.canvas['height']) - lieux[lst_route[i+1]][1])
            canvas.create_line(A,B,width=3, fill="blue", arrow=tk.LAST)
            canvas.create_text(lieux[lst_route[i]][0],int(self.canvas['height']) - lieux[lst_route[i]][1]-self.r*2,text=str(i))

    def create_all_circle(self, lieux):
        nombre = 0
        for i in lieux:
            self.create_circle(i[0],i[1],self.r,nombre,self.canvas)
            nombre += 1