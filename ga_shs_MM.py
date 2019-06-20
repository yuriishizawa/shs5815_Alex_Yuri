import numpy as np

class genetic_algorithm:
    def __init__(self):
        print('Módulo aberto com sucesso!')
        
    def initial_pop(self,size_pop,size_cromossomo,minimum,maximum):
        '''
        Função cria uma população inicial
        Input:
        size_pop: determina o número de cromossomos
        size_cromossomo: determina o tamanho de cada cromossomo
        minumum: valor mínimo de parte do cromossomo
        maximum: valor máximo de parte do cromossomo
        
        Output:
        self.filhos: populaçao de cromossomos
        '''
        self.size_pop = size_pop
        self.size_cromossomo = size_cromossomo
        self.minimum = minimum
        self.maximum = maximum
        
        self.init_pop = np.random.uniform(low=self.minimum, 
                                           high=self.maximum, 
                                           size=(self.size_pop,self.size_cromossomo))
        self.filhos = self.init_pop
        return self.filhos
    
    def funcao_obj(self):
        self.fitness = np.zeros((self.size_pop, 1))
        for i,crom in enumerate(self.filhos):
#             print(i, crom)
            self.fitness[i] = 5.1*crom[0] - crom[1]*crom[0] + crom[2]*1.4 - crom[2]*crom[2]*2.1 + 3*crom[0]
        
        print(self.fitness)
        
    def funcao_obj_rede(self, pressoes_simuladas, pressoes_reais):
        '''
        Essa função é a função objetivo da rede, ou seja, o self.fitness deve ser o mínimo possível
        
        Input:
        pressoes_simuladas: Pressões dos nós após realizada simulação (array-like)
        pressoes_reais: Pressões dos nós dados (array-like)
        
        '''
        self.pressoes_simuladas = pressoes_simuladas
        self.pressoes_reais = pressoes_reais
        
        
        
                
    def selecting_mating_pool(self, elitismo, num_filhos, mutation):
        '''
        
        Input:
        elitismo: Quantidade de filhos elitistas (0 até Número max de filhos)
        num_filhos: Número de filhos
        mutation: Chance de multação
        '''
        
        self.elitismo = elitismo
        self.num_filhos = num_filhos        
        self.mutation = mutation
        # Criando Filhos Elitistas
        self.sort_pop = np.array([x for _,x in sorted(zip(self.fitness,self.filhos))])
        self.filhos_elitistas = np.array(self.sort_pop[-self.elitismo:,:])
        print(self.filhos_elitistas)
        
        # Criando Filhos Crossovers
        self.crossover()
        
        # Filhos Elitistas e Filhos Crossovers
        self.filhos = np.append(self.filhos_elitistas, self.filhos_crossover,axis=0)
        print(np.shape(self.filhos))
        
        # Criando Filhos Aleatórios
        self.num_filhos_random = self.num_filhos-np.shape(self.filhos)[0]
        self.filhos_random = np.random.uniform(low=self.minimum, 
                                           high=self.maximum, 
                                           size=(self.num_filhos_random,self.size_cromossomo))
        print(self.filhos_crossover)
        
        # Filhos Elitistas, Filhos Crossovers e Filhos Aleatórios
        self.filhos = np.append(self.filhos, self.filhos_random, axis=0)
        print(self.filhos)

    def crossover(self):
        '''
        Função tem como objetivo pegar um array com shape de e.g.(7,4) e ter como output um array com shape de mesma forma.
        Pegar metade da população para manter e fazer crossover
        '''
        self.pais_crossover = self.sort_pop[-int(len(self.sort_pop)/2):, :]       
        self.filhos_crossover = np.array([])
        for i, crom in enumerate(self.pais_crossover):
            if i == 0:
                self.filhos_crossover = np.array([(self.pais_crossover[i]+self.pais_crossover[i-1])/2])
            else:
                self.filhos_crossover = np.append(self.filhos_crossover, np.array([(self.pais_crossover[i]+self.pais_crossover[i-1])/2]), axis=0)
        self.funcao_mutation()

    def funcao_mutation(self):
        '''
        Função tem como objetivo pegar os filhos e gerar uma porcentagem para cada parte do cromossomo, se for maior que uma porcentagem é alterado para um novo valor(dentro do limite).
        '''
        self.roll_the_dices = np.random.rand(np.shape(self.filhos_crossover)[0],np.shape(self.filhos_crossover)[1])
        for i in range(len(self.roll_the_dices)):
            for j in range(len(self.roll_the_dices[i])):
                if self.roll_the_dices[i,j] <= self.mutation:
                    self.filhos_crossover[i,j] = np.random.uniform(low=self.minimum, high=self.maximum, size=1)
                else:
                    pass
    
