#Simone
import numpy as np
import random
import matplotlib.pyplot as plt
from Config import Config

DEBUG = False
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
    def __init__(self, nn_layer_list=None, num_pop=None, num_gen=None, mutation_rate=None, n_best=3):
        self.config         = Config()

        self.weights_bounds = self.config.INITIAL_WEIGHT_RANGE #initial weight bounds
        self.nn_layer_list  = nn_layer_list if nn_layer_list != None else self.Config.NN_LAYER_NODES

        self.num_pop        = num_pop if num_pop != None else self.config.POPULATION_SIZE
        self.num_gen        = num_gen if num_gen != None else self.config.GENERATION_COUNT
        self.mutation_rate  = mutation_rate if mutation_rate != None else self.config.MUTATION_RATE
        self.n_best         = Config.N_BEST

        self.h_fmax         = []
        self.h_favg         = []
        self.h_div          = []

    def _create_individual(self, mode='std_sampled'):
        genotype = []
        for l in range(len(self.nn_layer_list)-1):
            if mode == 'std_sampled':
                genotype.append(np.random.normal(self.weight_bounds[0], self.weight_bounds[1], size=(self.nn_layer_list[l], self.nn_layer_list[l+1]))) #probably better
            elif mode == 'uni_sampled':
                genotype.append(np.multiply(np.random.uniform(size=(self.nn_layer_list[l], self.nn_layer_list[l+1])), self.weights_bounds[1]-self.weights_bounds[0])+self.weights_bounds[0])
        return genotype

    def initialization(self, mode='uni_sampled'):
        self.population = []
        for _ in range(self.num_pop):
            self.population.append(self._create_individual(mode))

    def evaluation(self, generation_counter):
        show_graphically = (generation_counter % self.config.SHOW_INCREMENT_DISTANCE) == 0
        self.fit = simulate_episode(self.population, show_graphically, generation_counter)
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
        elif mode == 'rank_proportional':
            rank_proportions = self.config.RANK_PROPRTIONS
            for rank in range(len(rank_proportions)):
                for count in range(rank_proportions[rank]):
                    new_population.append(self.population[rank].copy())
            return new_population

    def Xover(self, p1, p2, mode=0):
        child = []
        if mode == 3:
            for layer_number in range(len(p1)):
                for gene_number in range(p1[layer_number].shape[0]):
                    if random.random() < 0.5:
                        temp_gene                     = p1[layer_number][gene_number]
                        p1[layer_number][gene_number] = p2[layer_number][gene_number]
                        p2[layer_number][gene_number] = temp_gene
            return p1, p2
        else:
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
        for generation_counter in range(self.num_gen):
            self.evaluation(generation_counter)
            self.population = self.selection_reproduction(mode='rank_proportional', n_best=self.n_best)

            if verbose: print('Generation ',generation_counter,' Best: ',self.population[0],' with value: ', self.fit[0])
            self.h_fmax.append(self.fit[0])
            self.h_favg.append(sum(self.fit)/len(self.fit))
            self.h_div.append(self.diversity())

            start = 0 if not mantain_best else self.n_best
            new_generation = []
            while len(self.population) > 0:
                p1 = self.population.pop(random.randint(0, len(self.population) - 1))
                p2 = self.population.pop(random.randint(0, len(self.population) - 1))
                child_1, child_2 = self.Xover(p1, p2, mode=3)
                new_generation.append(child_1)
                new_generation.append(child_2)

            for child_number in range(len(new_generation)):
                if random.random() < self.mutation_rate:
                    new_generation[child_number] = self.mutation(new_generation[child_number])

            for child_number_1 in range(len(new_generation) - 1):
                for child_number_2 in range(child_number_1 +1, len(new_generation)):
                    child_1 = new_generation[child_number_1]
                    child_2 = new_generation[child_number_2]

                    are_identic = True
                    for layer_number in range(len(child_1)):
                        if np.any(child_1[layer_number] != child_2[layer_number]):
                            are_indentic = False
                            break
                    if are_identic:
                        new_generation[child_number_1] = self.mutation(child_1)

                    # if new_generation[child_number_1] == new_generation[child_number_2]:
                    #     new_generation[child_number_1] = self.mutation(new_generation[child_number_1])

            self.population = new_generation

            # for p in range(start, self.num_pop):
            #     self.population[p] = self.Xover(self.population[p], self.population[random.randint(0, self.num_pop-1)], mode=random.randint(0, 2))
            #     if random.random()<self.mutation_rate:
            #         self.population[p] = self.mutation(self.population[p])

    def diversity(self):
        tmp = 0
        for i in range(self.num_pop):
            for j in range(i, self.num_pop):
                for m in range(len(self.population[i])):
                    tmp += np.average(np.power(self.population[i][m]-self.population[j][m],2))
        return tmp


if __name__=='__main__':
    #Run 1 experiment and show the results
    ea = Evolution([15, 2])
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
    print(ea.h_fmax)
    print(ea.h_favg)
    print(ea.h_div)


