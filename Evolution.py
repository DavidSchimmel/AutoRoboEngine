import numpy as np

class Evolution():

    def __init__(self, nn, num_pop, num_gen):
        self.nn = nn #neural network
        self.weights = nn.get_weights() #get a list of the weights as genotype
        self.num_layers = len(self.genotype) #keep the number of weights/layers
        #self.population = []
        self.num_pop = num_pop #population size
        self.eval = np.zeros((self.num_pop,0))
        self.num_gen = num_gen #number of generation

    def _create_individual(self, mode):
        # Create a new individual with two tecniques
        genotype = []
        for i in range(self.num_layers):
            if mode == 'std_sampled':
                genotype[i] = np.random.standard_normal(size=(self.weights[i][0],self.weights[i][1]))
            elif mode == 'uni_sampled':
                genotype[i] = np.random.uniform(size=(self.weights[i][0],self.weights[i][1]))
        return genotype

    def initialization(self, mode):
        # Initialize the population
        self.population = []
        for _ in range(self.num_pop):
            self.population.append(self._create_individual(mode))

    def _evaluate_event(self, weight):
        # Calculate the fitness of an individual
        self.nn.set_weights(weight)
        #evaluate using the nn prediction

    def evaluation(self):
        # Set the fitness of every individuals
        for p in range(self.num_pop):
            self.eval[p]=self._evaluate_event(self.population[p])

    def selection(self, mode_selection, num_selected, repl_stategy):
        """
        mode_selection = strategy for selecting the individuals allowed to reproduce
        repl_strategy = stategy for reproduction [gn: generational replacement, el: elitism, gr: generational rollover]
        """
        if mode_selection == 'rws': #Roulette Wheel Selection
            prob = []
            sum_f = np.sum(self.eval)
            for i in range(self.eval.shape[0]):
                prob.append( [i, self.eval[i]/sum_f] )
            prob.sort(reverse=True, key =lambda x : x[1])
            #select num_selected 

        elif mode_selection == 'rbs': #Rank-Based Selection
            pass

        elif mode_selection == 'trbs': #Truncated Rank-Based Selection
            pass

        elif mode_selection == 'ts': #Tournament Selection
            pass


    def reproduction(self):
        pass

    def _crossover (self, mode, p1, p2):
        """
        0 One Point 
        1 Uniform 
        2 Aritmetic
        """
        if mode == 0:
            pass
        elif mode == 1:
            pass
        elif mode == 2: #Aritmetic
            pass

    def _mutation(self, x, mutation_tax=0.5):
        # Real values random noise
        noise = np.random.uniform( (x.shape[0], x.shape[1]) )[np.np.random.uniform( (x.shape[0], x.shape[1]) )>mutation_tax]
        return x + noise 

    

    
    