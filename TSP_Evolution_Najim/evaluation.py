from City import City
def fitness_TSP (individual,dist): 
    
    fitness = 0
    
    distance = 1
    for i in range (0,len(individual)):
        origin = individual[i]
        if((i+1)<len(individual)):
            destination = individual[i+1]
        else:
            destination = individual[0]
        #distance = distance + origin.getDistance(destination)
        distance = distance + dist[origin.num-1][destination.num-1]
    fitness = 1/distance
    
    return fitness


