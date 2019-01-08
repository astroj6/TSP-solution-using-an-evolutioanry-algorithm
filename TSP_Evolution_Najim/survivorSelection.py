
import random

# (mu+lambda) selection
def mu_plus_lambda(current_pop, current_fitness, offspring, offspring_fitness):   
    population = []
    fitness = []

    total_pop = current_pop + offspring
    total_fitness = current_fitness + offspring_fitness
    current = 0
    maxim = 0
    maxIndex = 0
    chosenIndex = []
    # we then add to our populat the best fitnesses descending down, until we fill up the fitness and population
    for j in range(0,len(current_fitness)):
        current=0
        maxIndex=0
        maxim = 0
        for i in range(0,len(total_fitness)):
            current = total_fitness[i]
            if((current > maxim) and (i not in chosenIndex)):
                maxim = current
                maxIndex = i
        chosenIndex.append(maxIndex)
        fitness.append(maxim)
        population.append(total_pop[maxIndex])
        
        
        


    
    return population, fitness
    


