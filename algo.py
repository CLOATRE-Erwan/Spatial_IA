from tsp_graph_init import Route, Graph, Population, Lieu
import random

random.seed(1)


class TSP_GA:
    def __init__(self, graph, taux_mutation=0.3, taille_tournoi=5, elitiste=True):
        self.graph = graph
        self.taux_mutation = taux_mutation
        self.taille_tournoi = taille_tournoi
        self.elitisme = elitiste

    def evoluer(self, pop):
            nouvellepop = Population(self.graph,len(pop))
            elitismeOffset = 0

            if self.elitisme:
                nouvellepop[0] = pop.trouver_meilleur()
                elitismeOffset = 1

            for i in range(elitismeOffset, len(nouvellepop)):
                parent1 = self.tournoi(pop)
                parent2 = self.tournoi(pop)
                enfant = self.crossover(parent1, parent2)
                nouvellepop[i] = enfant
            
            for i in range(elitismeOffset, len(nouvellepop)):
                nouvellepop[i] = self.mutation(nouvellepop[i])
            
            return nouvellepop

    def crossover(self, parent1, parent2):
        enfant = Route(self.graph)

        startPos = int(random.random() * parent1.taille)
        endPos = int(random.random() * parent1.taille)

        for i in range(enfant.taille):
            if startPos < endPos and i > startPos and i < endPos:
                if not enfant.contient(parent1[i]):
                    enfant[i] = parent1[i]
            elif startPos > endPos:
                if not (i < startPos and i > endPos): 
                   if not enfant.contient(parent1[i]):
                    enfant[i] = parent1[i]
    
        for i in range(parent2.taille):
            if not enfant.contient(parent2[i]):
                for ii in range(enfant.taille):
                    if enfant[ii] == None:
                            enfant[ii] = parent2[i]
                            break
        return enfant
    
    def mutation(self, route):
        for route_pos1 in range(1, route.taille-2):
            if random.random() < self.taux_mutation:
                route_pos2 = random.randint(1, route.taille-2)
                
                lieu1 = route[route_pos1]
                lieu2 = route[route_pos2]
                
                route[route_pos2] = lieu1
                route[route_pos1] = lieu2

        return route

    def tournoi(self, pop):
        tournoi = Population(self.graph, self.taille_tournoi)
        for i in range(self.taille_tournoi):
            randomId = int(random.random() * len(pop))
            tournoi[i] = pop[randomId]
        meilleur = tournoi.trouver_meilleur()
        return meilleur