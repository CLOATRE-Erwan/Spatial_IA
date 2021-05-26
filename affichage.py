import tkinter as tk
from tsp_graph_init import Graph, Population
from algo import TSP_GA


class Affichage(tk.Frame):
    def __init__(self, hauteur, largeur, graph,pop,ga,master=None):
        super().__init__(master=master)
        self.ahhhhhhhhhh = master
        self.hauteur = 700
        self.largeur = 1000
        self.hauteur_canvas = 600
        self.largeur_canvas = 800
        self.distance = tk.StringVar() 

        self.r = 10
        self.graph = graph
        self.pop = pop
        self.ga = ga   

        self.ahhhhhhhhhh.title("Groupe n°1 : Pereg, Jamal, Erwan")
        self.ahhhhhhhhhh.geometry(str(self.largeur)+'x'+str(self.hauteur))

        self.creat_widget(self.ahhhhhhhhhh)

    def test(self):
        nb_iteration = 50
        self.pop = self.ga.evoluer(self.pop)
        meilleur = self.pop.trouver_meilleur().calcul_distance_route()
        iteration = 1
        for i in range(0,nb_iteration):
            self.clear_canvas(self.canvas)
            if self.pop.trouver_meilleur().calcul_distance_route() < meilleur:
                meilleur = self.pop.trouver_meilleur().calcul_distance_route()
                iteration = i
            self.route(self.pop.trouver_meilleur(), 5, 'blue')
            self.create_all_circle(self.graph.liste_lieux)
            self.distance.set("Distance en cours : "+ str(self.pop.trouver_meilleur().calcul_distance_route())+" trouver en : "+ str(iteration) +' iteration   |   ' + str(i)+'/'+str(nb_iteration))
            # print("Distance en cours : ", self.pop.trouver_meilleur().calcul_distance_route())
            self.pop = self.ga.evoluer(self.pop)
            self.master.update()

    def creat_widget(self, master):
        self.label = tk.Label(master, text="Simplon Spatial IA")
        self.label.pack()

        self.canvas = self.create_canvas(master, self.largeur_canvas, self.hauteur_canvas)
        self.canvas.pack()

        self.distance.set('Distance')
        self.label_distance = tk.Label(master, textvariable=self.distance)
        self.label_distance.pack()

        self.button = tk.Button(master, text="start", command=self.test)
        self.button.pack()

        self.close_button = tk.Button(master, text="Close", command=master.quit)
        self.close_button.pack()


    def create_canvas(self, master , largeur, hauteur):
        canvas = tk.Canvas(master,width=largeur, height=hauteur, bg='ivory')
        return canvas


    def clear_canvas(self, canvas):
        canvas.delete('all')


    def route(self, route, width,fill):
        for i in range(route.taille-1):
            A = (self.graph.liste_lieux[route.ordre[i]].x,int(self.canvas['height']) - self.graph.liste_lieux[route.ordre[i]].y)
            B = (self.graph.liste_lieux[route.ordre[i+1]].x,int(self.canvas['height']) - self.graph.liste_lieux[route.ordre[i+1]].y)
            self.canvas.create_line(A,B,width=width,fill=fill)
            self.canvas.create_text(self.graph.liste_lieux[route.ordre[i]].x,int(self.canvas['height']) - self.graph.liste_lieux[route.ordre[i]].y-self.r*2,text=str(i))


    def create_circle(self,x,y,r,i,canvas):
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


    def create_all_circle(self, lieux):
        nombre = 0
        for i in lieux:
            self.create_circle(i.x,i.y,self.r,nombre,self.canvas)
            nombre += 1

    
graph = Graph()

# graph.generer_graph(800, 600, 25)
#graph.sauvegarder_graph('coor.csv')
graph.charger_graph('graph_10.csv')
graph.calcul_matrice_cout_od()

pop = Population(graph, 50)
pop.generer_population()
ga = TSP_GA(graph)

root = tk.Tk()
app = Affichage(800,600,graph,pop,ga,master=root)
app.mainloop()