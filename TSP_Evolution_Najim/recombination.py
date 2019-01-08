from City import City
import random
def order_cross (parent1, parent2):
    
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1))
    geneB = int(random.random() * len(parent1))
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    
    
    child2 = []
    child2P1 = []
    child2P2 = []

    for i in range(startGene, endGene):
        child2P1.append(parent2[i])
        
    child2P2 = [item for item in parent1 if item not in child2P1]

    child2 = child2P1 + child2P2
    
    return child, child2

def contains(city,individual):
    contains = False
    for i in range(0,len(individual)):
        if(not(individual[i]==-1)):
            if(individual[i].name == city.name):
                contains= True
    return contains
