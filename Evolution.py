import numpy as np

class Evolution():

    def __init__(self, nn_layer_list):
        self.weights_bounds =[[-10,10],[10,10]]
        self.nn_layer_list = nn_layer_list

    def _create_individual(self, mode='uni_sampled'):
        genotype = []
        for l in range(len(self.nn_layer_list)-1):
            if mode == 'std_sampled':
                genotype=np.random.standard_normal(2)
            elif mode == 'uni_sampled':
                genotype.append(np.multiply(np.random.uniform(size=(self.nn_layer_list[l], self.nn_layer_list[l+1])), self.weights_bounds[:,1]-self.weights_bounds[:,0])+self.weights_bounds[:,0])
        return genotype

    def initialization(self, mode='uni_sampled'):
        self.population = []
        for _ in range(self.num_pop):
            self.population.append(self._create_individual(mode))
        print('Population inizialized')

    def evaluation(self):
        for i in range(self.num_pop):
            self.fit[i]=self.F(self.population[i])
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
        if mode == 0: #arithmetic
            if random.random()<0.5:
                x = p1 + p2
            else:
                x = p1 - p2
            x[0] = min(self.bounds[0,1], max(self.bounds[0,0], x[0]))
            x[1] = min(self.bounds[1,1], max(self.bounds[1,0], x[1]))
            return x
        elif mode == 1: #uniform
                return np.array([p1[0],p2[1]])
        elif mode == 2: #average
            return (p1 + p2) /2

    def mutation(self, p):
        noise = self.mutation_coef  * random.random()- self.mutation_coef/2
        i = int(random.random())
        x = p[i]+noise
        p[i] = min(self.bounds[i,1], max(self.bounds[i,0], x))
        return p

    def evolution(self, mantain_best=True):
        ##########################
        positions = [[],[]]
        ##########################
        self.initialization()
        for g in range(self.num_gen):
            self.evaluation()
            #########################
            positions[0].append([])
            positions[1].append([])

            for individual in self.population:
                positions[0][g].append(individual[0])
                positions[1][g].append(individual[1])
            #########################
            print('Generation ',g,' Best: ',self.population[0],' with value: ', self.fit[0])
            self.population = self.selection_reproduction(mode='elitism', n_best=self.n_best)
            start = 0 if not mantain_best else self.n_best
            for p in range(start, self.num_pop):
                if random.random()>self.mutation_rate:
                    if random.random()<0.5:
                        self.population[p] = self.Xover(self.population[p], self.population[random.randint(0, self.num_pop-1)], mode=random.randint(0, 2))
                    else:
                        self.population[p] = self.mutation(self.population[p])

        #######################
        return positions

    
if __name__=='__main__':
    ea = Evolution([2,3,4,2])
    ea._create_individual()
  
    
    