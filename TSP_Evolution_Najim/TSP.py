from City import City

import random
import numpy
import math
import time

import initialization
import evaluation
import recombination
import mutation
import parentSelection
import survivorSelection
import concurrent.futures
import multiprocessing as mp
import argparse



def mainTask(exchange,exchangeFit,migrate,migrateFit,procNum,migrateTo,migrateToF,migrateFrom,migrateFromF):
   
    random.seed()
    numpy.random.seed()
    popsize = 400
    mating_pool_size = int(popsize*0.5)
    tournament_size = 10
    mut_rate = 0.2 # our mutation operator improvement is inside the main generation loop where it is updated dynamically according to our improvement formula
    xover_rate = 0.9
    gen_limit = 500
    prevFitness = [] # we store previous fitnesses for past generattions so that if multiple generations start pproducing the same best fitness we can stop the algorithm
    start_time = time.time()  # this is used to calculate the runtime
    iteration =0 # this is a variable used to kkeep count of how many migrations has happened , we use it to makke sure we don't try to go out of bounds when moving to population2

    # initialize population

    cityList = []
    file = open("TSP_Uruguay_734.txt", 'r') # we read the file , this can be changed to any file name (sahara or canada etc)
    words = list(file.read().split())
    for i in range(0,len(words),3):
        cityList.append(City(float(words[i+1]),float(words[i+2]),"City",int(words[i])))
    file.close()
    
    distanceList = [] # this is a list to precalculate distances in order for us to find them instead of calculating every time
    for i in range (0, len(cityList)):
        distToCity =[]
        for j in range(0, len(cityList)):
            distToCity.append(cityList[i].getDistance(cityList[j]))
        distanceList.append(distToCity)
    gen = 0 # initialize the generation counter
    population = initialization.permutation(popsize, cityList)
    fitness = []
    for i in range (0, popsize):
        fitness.append(evaluation.fitness_TSP(population[i],distanceList))
    print("generation", gen, ": best fitness", (1/(max(fitness))), "average fitness", 1/(sum(fitness)/len(fitness)))

    while gen < gen_limit:
        
        # pick parents
        parents_index = parentSelection.tournament(fitness, mating_pool_size, tournament_size)
        random.shuffle(parents_index)
    
        # reproduction
        offspring =[]
        offspring_fitness = []
        i= 0 # initialize the counter for parents in the mating pool
        while len(offspring) < mating_pool_size:
        
            # recombination
            if random.random() < xover_rate:            
                off1,off2 = recombination.order_cross(population[parents_index[i]], population[parents_index[i+1]])
            else:
                off1 = population[parents_index[i]].copy()
                off2 = population[parents_index[i+1]].copy()

            # mutation
            if random.random() < mut_rate:
                off1 = mutation.permutation_swap(off1)
            if random.random() < mut_rate:
                off2 = mutation.permutation_swap(off2)
            offspring.append(off1)
            offspring_fitness.append(evaluation.fitness_TSP(off1,distanceList))
            offspring.append(off2)
            offspring_fitness.append(evaluation.fitness_TSP(off2,distanceList))
            i = i+2  # update the counter

        # survivor selection
        population, fitness = survivorSelection.mu_plus_lambda(population, fitness, offspring, offspring_fitness)
        
        gen = gen + 1
        mut_rate = mut_rate-(0.1*mut_rate*(gen/gen_limit)) # improved mutation operator 
        
        #Island Model
        chosenIndex = []
        if((gen%10) == 0 ):
            for j in range (0,10): # select 10 best individuals 
                current=0
                maxIndex=0
                maxim = 0
                for i in range(0,len(fitness)):
                    current = fitness[i]
                    if((current > maxim) and (i not in chosenIndex)):
                        maxim = current
                        maxIndex = i
                chosenIndex.append(maxIndex)
                if(len(exchange)<10):
                    exchange.append(population[maxIndex])
                    exchangeFit.append(fitness[maxIndex])
                else:
                    exchange.pop(0)
                    exchangeFit.pop(0)
                    exchange.append(population[maxIndex])
                    exchangeFit.append(fitness[maxIndex])
            migrateTo.append(exchange)
            migrateToF.append(exchangeFit)
            if(procNum==2): #we check to see if this is population2 before moving individuals to it , because in population 1 there is no one to migrate yet so there's no need to run this for pop 1
                if(iteration<len(migrateFromF)): #migration start , and check if there's any more migrations left 
                    for i in range (0, popsize):
                        for x in range(0,len(migrateFromF[iteration])):
                            if(migrateFromF[iteration][x]>fitness[i]):
                                population[i] = migrateFrom[iteration][x]
                                fitness[i] = migrateFromF[iteration][x]       
                    migrateFrom[iteration] = []
                    migrateFromF[iteration]= []
                iteration=iteration+1
            #end Island Model
            

        #generation limitation method 
        if(len(prevFitness)<10):
            prevFitness.append((1/(max(fitness))))
        else:
            prevFitness.pop(0)
            prevFitness.append((1/(max(fitness))))
        print("population: ", procNum,"generation", gen, ": best fitness", (1/(max(fitness))), "average fitness", 1/(sum(fitness)/len(fitness)))
        print("--- %s seconds ---" % (time.time() - start_time))
        if(len(prevFitness)>=10):
            count = 0
            for i in range(0,len(prevFitness)):
                if ((1/(max(fitness))) == prevFitness[i]):
                    count = count+1
            if(count == 10):
                gen = gen_limit
        # generationn Limitation end
    return population, fitness

def Main():
    
    start_time1 = time.time()
    exchangePop1=[]
    exchangePop2=[]
    Pop1Fit=[]
    Pop2Fit=[]
    # finalpop and final fit are used to compare population 1 and 2 and retrieve the proper solution
    finalpop1=[]
    finalfit1=[]
    finalpop2=[]
    finalfit2=[]

    migration1=[]
    migration1F=[]
    migration2=[]
    migration2F=[]
    finalpop1,finalfit1 = mainTask(exchangePop1,Pop1Fit,exchangePop2,Pop2Fit,1,migration1,migration1F,migration2,migration2F,)
    finalpop2,finalfit2 = mainTask(exchangePop2,Pop2Fit,exchangePop1,Pop1Fit,2,migration2,migration2F,migration1,migration1F,)
    Found=False
    if((1/(max(finalfit1)))<(1/(max(finalfit2)))):
        print(1/(max(finalfit1)))
        for i in range (0, len(finalfit1)):
                if (finalfit1[i] == max(finalfit1)):
                    if(Found != True):
                        Found=True
                        print("best solution")
                        for j in range(0,len(finalpop1[i])):
                            print("city : ",finalpop1[i][j].num ,"position : (", finalpop1[i][j].x , ",",finalpop1[i][j].y,")")
                            print("fitness :", 1/finalfit1[i])
    else:
        print(1/(max(finalfit2)))
        for i in range (0, len(finalfit2)):
            if (finalfit2[i] == max(finalfit2)):
                if(Found != True):
                    Found=True
                    print("best solution")
                    for j in range(0,len(finalpop2[i])):
                        print("city :",finalpop2[i][j].num ,"position : (", finalpop2[i][j].x , ",",finalpop2[i][j].y,")")
                    print("fitness :", 1/finalfit2[i])
    print("--- %s total seconds for full program ---" % (time.time() - start_time1))
if __name__ == '__main__':
    Main()
