#!/usr/bin/env python
# coding: utf-8


import numpy as np
import random
import copy



class Individual:
    
    def __init__(self, mentoriZauzetost, zeljeStudenata):
        self.mentoriZauzetost = copy.deepcopy(mentoriZauzetost)
        self.zeljeStudenata = copy.deepcopy(zeljeStudenata)
        self.brMentora = len(mentoriZauzetost)
        self.brStudenata = len(zeljeStudenata)
        self.maxBrojStudenata = sum(mentoriZauzetost)
        
        if self.maxBrojStudenata < self.brStudenata:
            print('Kapaciteti popunjeni! Nije moguce dodeliti mentora svakom studentu!')
        
        studenti = [i for i in range(0, self.brStudenata)]
        random.shuffle(studenti)
        mentori = []
        br=0
        for i in range(self.brMentora):
            for j in range(self.mentoriZauzetost[i]):
                if br + j > self.brStudenata:
                    break
                else :
                    mentori.append(i)
            br += j
        self.code = []
        for i in range(self.brStudenata):
            self.code.append((studenti[i], mentori[i]))
        self.fitness = self.fitnessFunction()
        
    def fitnessFunction(self):
        val = 0
        for i in range(self.brStudenata):
            val += self.geneFitness(i)
        return val
    
    def geneFitness(self, i):
        (student, mentor) = self.code[i]
        return self.zeljeStudenata[student][mentor]
    
    def __lt__(self, other):
        return self.fitness < other.fitness





def mutation(individual, mutation_rate):
    
    if random.uniform(0,1) < mutation_rate:
        i = random.randrange(individual.brStudenata)
        j = random.randrange(individual.brStudenata)
        tmp = individual.code[i][0]
        individual.code[i] = (individual.code[j][0], individual.code[i][1])
        individual.code[j] = (tmp, individual.code[j][1])
    




def selection(population, tournament_size):
    val = float('inf')
    bestInd = -1
    for _ in range(tournament_size):
        i = random.randrange(len(population))
        if population[i].fitness < val:
            val = population[i].fitness
            bestInd = i
    return bestInd



def crossover(parent1, parent2, child1, child2):
    
    n = parent1.brStudenata
    dodeljeni1 = set()
    dodeljeni2 = set()
    nisuDodeljenji1 = set()
    nisuDodeljenji2 = set()
    for i in range(n):
        nisuDodeljenji1.add(parent1.code[i][0])
        nisuDodeljenji2.add(parent1.code[i][0])
    for i in range(n):
        child1.code[i] = (-1, child1.code[i][1])
        child2.code[i] = (-1, child2.code[i][1])
    for i in range(n):
        if parent1.geneFitness(i) < parent2.geneFitness(i) and parent1.code[i][0] not in dodeljeni1 and parent1.code[i][0] in nisuDodeljenji1:
            child1.code[i] = (parent1.code[i][0], child1.code[i][1])
            dodeljeni1.add(child1.code[i][0])
            nisuDodeljenji1.remove(child1.code[i][0])
        elif parent1.geneFitness(i) > parent2.geneFitness(i) and parent2.code[i][0] not in dodeljeni1 and parent2.code[i][0] in nisuDodeljenji1:
            child1.code[i] = (parent2.code[i][0], child1.code[i][1])
            dodeljeni1.add(child1.code[i][0])
            nisuDodeljenji1.remove(child1.code[i][0])
    
    k=n-1
    while k>=0:
        if parent1.geneFitness(k) < parent2.geneFitness(k) and parent1.code[k][0] not in dodeljeni2 and parent1.code[k][0] in nisuDodeljenji2:
            child2.code[k] = (parent1.code[k][0], child2.code[k][1])
            dodeljeni2.add(child2.code[k][0])
            nisuDodeljenji2.remove(child2.code[k][0])
        elif parent1.geneFitness(k) > parent2.geneFitness(k) and parent2.code[k][0] not in dodeljeni2 and parent2.code[k][0] in nisuDodeljenji2:
            child2.code[k] = (parent2.code[k][0], child2.code[k][1])
            dodeljeni2.add(child2.code[k][0])
            nisuDodeljenji2.remove(child2.code[k][0])
        k-=1
    
    for i in range(n):
        if child1.code[i][0] == -1:
           
            child1.code[i] = (random.sample(nisuDodeljenji1, 1)[0], child1.code[i][1])
            
            nisuDodeljenji1.remove(child1.code[i][0])
        if child2.code[i][0] == -1:
           
            child2.code[i] = (random.sample(nisuDodeljenji2, 1)[0], child2.code[i][1])
            
            nisuDodeljenji2.remove(child2.code[i][0])
            
    child1.fitness = child1.fitnessFunction()
    child2.fitness = child2.fitnessFunction()
    
    if child1.fitness > parent1.fitness:
        child1 = parent1
    if child1.fitness > parent2.fitness:
        child1 = parent2
    if child2.fitness > parent1.fitness:
        child2 = parent1
    if child2.fitness > parent2.fitness:
        child2 = parent2




def generisiPrimer(brMentora, brStudenata):
    mentoriZauzetost = [random.randint(int(brStudenata/brMentora)-int(brStudenata/(brMentora*4)),int(brStudenata/brMentora)+2*int(brStudenata/(brMentora*4))) for i in range(brMentora)]
    zeljeStudenata = [[int(i) for i in range(brMentora)] for j in range(brStudenata)]

    for i in range(len(zeljeStudenata)):
        random.shuffle(zeljeStudenata[i])
    
    return mentoriZauzetost, zeljeStudenata
    


mentoriZauzetost, zeljeStudenata = generisiPrimer(15, 60)



population_size = 100
mutation_rate = 0.1
tournament_size = 6
max_iter = 1000
elitism_size = 20
population = [Individual(mentoriZauzetost, zeljeStudenata) for _ in range(population_size)]
new_population = [Individual(mentoriZauzetost, zeljeStudenata) for _ in range(population_size)]

for iteration in range(max_iter):
    population.sort()
    
    
    print(iteration,'-ta iteracija, najbolji fitness je: ', population[0].fitness)
    if population[0].fitness == 0:
        print("Svakom studentu je ispunjena prva zelja!")
        break
    for i in range(elitism_size):
        new_population[i] = population[i]
    for i in range(elitism_size, population_size, 2):
        p1 = selection(population, tournament_size)
        p2 = selection(population, tournament_size)
        
        crossover(population[p1], population[p2], new_population[i], new_population[i+1])
        
        mutation(new_population[i], mutation_rate)
        mutation(new_population[i+1], mutation_rate)
        new_population[i].fitness = new_population[i].fitnessFunction()
        new_population[i+1].fitness = new_population[i+1].fitnessFunction()
        
    population = new_population

population.sort()




brPrvihZelja = 0
najgoraZelja = 0
ispunjeneZelje = {}
for i in range(len(population[0].code)):
    print("{}. studentu je dodeljen {}. i ispunjena mu je {}. zelja".format(population[0].code[i][0], population[0].code[i][1], population[0].geneFitness(i)))
    if population[0].geneFitness(i) == 0:
        brPrvihZelja +=1
    if population[0].geneFitness(i) > najgoraZelja:
        najgoraZelja = population[0].geneFitness(i)
    if population[0].geneFitness(i) not in ispunjeneZelje:
        ispunjeneZelje[population[0].geneFitness(i)] = 1
    else:
        ispunjeneZelje[population[0].geneFitness(i)] +=1
print("{}% studenata je ispunjena prva zelja".format((brPrvihZelja*100)/population[0].brStudenata))
print("najgora ispunjena zelja se nalazi u prvih {}% zelja na listi".format((najgoraZelja*100)/population[0].brMentora))

print(ispunjeneZelje)

