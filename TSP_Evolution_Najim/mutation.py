import random

# mutate a permutation
def permutation_swap (individual):
    
    mutant = individual.copy()
    
    x = random.randint(0,len(mutant)-1)
    y = random.randint(0,len(mutant)-1)
    val=mutant[x]
    mutant[x]=mutant[y]
    mutant[y]=val
 
    return mutant
