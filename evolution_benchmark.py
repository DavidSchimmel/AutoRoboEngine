import numpy as np
import random
import math

class evolution_benchmark():

    def __init__(self, F, bounds, num_pop, num_gen):
        self.F = F #Fit function NB. Best fit = Higher fitnes value, so to find minimum put the - before!
        self.bounds = np.array(bounds) #Function bounds
        self.num_pop = num_pop #Number of individuals in population
        self.fit = np.zeros(num_pop) #evaluation/fit for each indivial
        self.num_gen = num_gen #Number of generations
        self.mutation_rate = 0.5 #Probability that a mutation occour, Xover and Mutation have the same probability
        self.n_best = math.floor(num_pop*0.25) #Number of best individuals allowed to reproduce (where required)
        self.mutation_coef = 0.01 #Magnitude of the mutation

    def _create_individual(self, mode='uni_sampled'):
        if mode == 'std_sampled':
            genotype=np.random.standard_normal(2)
        elif mode == 'uni_sampled':
            genotype=np.random.uniform(size=(2))
        return np.multiply(genotype, self.bounds[:,1]-self.bounds[:,0])+self.bounds[:,0]

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

def benchmark_1(p):
    #Rosenbrock
    x = p[0]
    y = p[1]
    a = 0
    b = 1
    f = pow((a-pow(x, 2)), 2) + b * pow((y-pow(x, 2)), 2)
    return  -f

def benchmark_2(p):
    #Rastrigin
    x = p[0]
    y = p[1]
    n = 2
    f = pow(x, 2) - 10 * math.cos(2 * math.pi * x) + pow(y, 2) - 10 * math.cos(2 * math.pi * y) + 10*n
    return  -f


##################################################################



eb = evolution_benchmark(benchmark_2, [[-10,10],[-10,10]], 50, 30)
positions = eb.evolution()

##################################################################

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pandas as pd
from random import random
import seaborn as sns

AXIS_X_LFT = -10
AXIS_X_RGT =  10
AXIS_Y_BOT = -10
AXIS_Y_TOP =  10


Writer = animation.writers['ffmpeg']
writer = Writer(fps=8, metadata=dict(artist='Me'), bitrate=1800)
#Init of the function graph
fig = plt.figure(figsize=(10,6))
plt.xlim(AXIS_X_LFT, AXIS_X_RGT)
plt.ylim(AXIS_Y_BOT, AXIS_Y_TOP)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('plot')
#Benchmark functions
a = 0; b = 1
x = np.arange(AXIS_X_LFT, AXIS_X_RGT, 0.1)
y = np.arange(AXIS_Y_BOT, AXIS_Y_TOP, 0.1)
xx, yy = np.meshgrid(x, y)

#z = ((a-(xx**2))**2) + b * ((yy - (xx**2))**2) #Rosenbrock
z = 10 * 2 + ((xx**2) - 10 * np.cos(2 * math.pi * xx)) + ((yy**2) - 10 * np.cos(2 * math.pi * yy)) #Rastrigin

df1 = pd.DataFrame(data=z, index=y, columns=x)
df1.style.background_gradient(cmap ='inferno').set_properties(**{'font-size': '20px'})
h = plt.contourf(x,y,z, levels=1000)

#Business logic
#particels=[]
#positions=[[],[]]
#f,pos=search_min(N_PARTICLES, 1, 0.0033, 2, 2, 1.4, 100, 0.001, Rosenbrock, [[AXIS_X_LFT,AXIS_X_RGT],[AXIS_Y_BOT,AXIS_Y_TOP]], animation=True)

positions=np.array(positions)
#print('Value: ', f, 'Position: ', pos)
ln, = plt.plot([], [], 'ro')
def update(f): #Frame's update
    print(f)
    plt.text(2, 3, r'type: elitism', fontsize=12)
    plt.text(2, 4, r'survival rate: 0.75', fontsize=12)
    plt.text(2, 5, r'elite rate: 0.25', fontsize=12)
    plt.text(2, 6, r'mutation rate: 0.25', fontsize=12)
    plt.text(2, 7, r'population count: 50', fontsize=12)
    plt.text(2, 8, r'generations: 30', fontsize=12)
    ln.set_data(positions[0][f], positions[1][f])
    return ln,

ani = matplotlib.animation.FuncAnimation(fig, update, frames=positions.shape[1], interval = 1, blit = False) #to print all the frames frames=positions.shape[1]
ani.save('testrun.mp4', writer=writer)
plt.show()