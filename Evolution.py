#Simone
import numpy as np
import random
import matplotlib.pyplot as plt

DEBUG = True
if DEBUG:
    def simulate_episode(population): #stupid function that only return the sum of all the elements of all the matrixes
        fit = []
        for m in  range(len(population)):
            tmp = 0
            for n in range(len(population[m])):
                tmp += np.sum(population[m][n])
            fit.append(tmp)
        return fit
else:
    from Environment import *

class Evolution():

    def __init__(self, nn_layer_list, num_pop=10, num_gen=10, mutation_rate=0.2, n_best=3):
        self.weights_bounds =[-1000,1000] #initial weight bounds
        self.nn_layer_list = nn_layer_list

        self.num_pop = num_pop
        self.num_gen = num_gen
        self.mutation_rate = mutation_rate #probability of a mutation
        self.n_best = n_best

        self.h_fmax=[]
        self.h_favg=[]
        self.h_div=[]

    def _create_individual(self, mode='std_sampled'):
        genotype = []
        for l in range(len(self.nn_layer_list)-1):
            if mode == 'std_sampled':
                genotype.append(np.random.normal(0,1000,size=(self.nn_layer_list[l], self.nn_layer_list[l+1]))) #probably better
            elif mode == 'uni_sampled':
                genotype.append(np.multiply(np.random.uniform(size=(self.nn_layer_list[l], self.nn_layer_list[l+1])), self.weights_bounds[1]-self.weights_bounds[0])+self.weights_bounds[0])
        return genotype

    def initialization(self, mode='std_sampled'):
        self.population = []
        for _ in range(self.num_pop):
            self.population.append(self._create_individual(mode))

    def evaluation(self):
        self.fit = simulate_episode(self.population)
        #Ordered population
        tmp = sorted(zip(self.population, self.fit), reverse=True, key = lambda a : a[1])
        self.population = [x[0] for x in tmp]
        self.fit = [x[1] for x in tmp]

    def selection_reproduction(self, mode='trbs', n_best=3):
        new_population = []
        if mode == 'trbs': #Truncated Rank-Based Selection
            n_children = int(self.num_pop/n_best)
            while len(new_population)<self.num_pop:
                for i in range(n_best):
                    new_population.append(self.population[i].copy())
                    if len(new_population)>=self.num_pop: break
            return new_population
        elif mode == 'elitism':
            for i in range(n_best):
                new_population.append(self.population[i].copy())
            k = 0
            for i in range(n_best,len(self.population)):
                if (k >= n_best):
                    k = 0
                if (random.random() > 0.75):
                    new_population.append(self.population[k].copy())
                    k += 1
                else:
                    new_population.append(self.population[i].copy())
            return new_population

    def Xover(self, p1, p2, mode=0):
        child = []
        for m in range(len(p1)):
            if mode == 0: #arithmetic
                if random.random()<0.5:
                    x = p1[m] + p2[m]
                else:
                    x = p1[m] - p2[m]
                child.append(x)
            elif mode == 1: #uniform
               a = p1[m].reshape(p1[m].shape[0]*p1[m].shape[1])
               b = p2[m].reshape(p2[m].shape[0]*p2[m].shape[1])
               x = np.array([])
               step = random.randrange(1, p1[m].shape[0]*p1[m].shape[1])
               for i in range(0, p1[m].shape[0]*p1[m].shape[1],step):
                   if random.random()<0.5:
                        x = np.concatenate((x, a[i:min(i+step, p1[m].shape[0]*p1[m].shape[1])]), axis=0)
                   else:
                        x = np.concatenate((x, b[i:min(i+step, p1[m].shape[0]*p1[m].shape[1])]), axis=0)
               x = x.reshape((p1[m].shape[0],p1[m].shape[1]))
               child.append(x)
            elif mode == 2: #average
                child.append((p1[m] + p2[m]) /2)
        return child

    def mutation(self, p):
        child = []
        for m in range(len(p)):
            noise = np.random.normal(size=(p[m].shape[0], p[m].shape[1]))
            child.append(p[m] + noise)
        return child

    def evolution(self, verbose=True, mantain_best=True):
        self.initialization()
        for g in range(self.num_gen):
            self.evaluation()
            self.population = self.selection_reproduction(mode='elitism', n_best=self.n_best)

            if verbose: print('Generation ',g,' Best: ',self.population[0],' with value: ', self.fit[0])
            self.h_fmax.append(self.fit[0])
            self.h_favg.append(sum(self.fit)/len(self.fit))
            self.h_div.append(self.diversity())

            start = 0 if not mantain_best else self.n_best
            for p in range(start, self.num_pop):
                if random.random()<self.mutation_rate:
                    if random.random()<0.5:
                        self.population[p] = self.Xover(self.population[p], self.population[random.randint(0, self.num_pop-1)], mode=random.randint(0, 2))
                    else:
                        self.population[p] = self.mutation(self.population[p])
        
    def diversity(self):
        tmp = 0
        for i in range(self.num_pop):
            for j in range(i, self.num_pop):
                for m in range(len(self.population[i])):
                    tmp += np.average(np.power(self.population[i][m]-self.population[j][m],2)) 
        return tmp
 

if __name__=='__main__':
    #Run 1 experiment and show the results
    ea = Evolution([2,3,4,2])
    ea.evolution(verbose=False)
    plt.figure()
    plt.title('Max fitness')
    plt.plot(ea.h_fmax)
    plt.show()
    plt.figure('Avg fitness')
    plt.plot(ea.h_favg)
    plt.show()
    plt.figure('Diversity')
    plt.plot(ea.h_div)
    plt.show()
  
    
    