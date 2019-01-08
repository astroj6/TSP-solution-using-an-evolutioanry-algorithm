
import random
from random import shuffle
def permutation (pop_size, cityL):
    
    population = []
    
    for i in range (0,pop_size):
        shuffle(cityL)
        population.append(cityL)
    
    return population   
	

