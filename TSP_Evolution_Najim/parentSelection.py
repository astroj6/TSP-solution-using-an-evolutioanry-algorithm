import random




#tournament selection without replacement
def tournament(fitness, mating_pool_size, tournament_size):
    
    selected_to_mate = [] 

    current_member = 0
    while(current_member< mating_pool_size):
        #pick k individuals and compare them and denote best as i
        count = 0 # count is k
        i=0
        chosen = [] # store our k individuals
        while(count < tournament_size):
            index1 = random.randint(0,(len(fitness)-1))
            if(index1 not in chosen):
                chosen.append(index1)
                count = count +1
                for j in range(0,len(chosen)):
                    current = chosen[j]
                    if(fitness[current]>=fitness[i]):
                        i=current;
        selected_to_mate.append(i)
        current_member = current_member + 1
            


    
    return selected_to_mate




