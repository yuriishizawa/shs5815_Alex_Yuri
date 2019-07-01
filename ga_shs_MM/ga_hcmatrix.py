import numpy as np


class genetic_algorithm: 
    '''
    Genetic Algorithm
    '''
    def __init__(self):
        print('Módulo aberto com sucesso!')
        print('a1')
        
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
    
    def funcao_rede(self, dados_nos, dados_trechos, dados_calibracao):
        '''
        Input:
        
        '''
        self.fitness = []
        for c in self.filhos:
#             print(c)
            f1 = []
#             for i,q in enumerate(dados_calibracao['Vazao(l/s)']):
            for i,q in enumerate(dados_calibracao):
                rede = HC_numpy_matrix(dados_nos=dados_nos,
                                       dados_trechos=dados_trechos,
                                       VazaoSaida_reservatorio=q[0],
                                       rugosidade=c)
                rede.simular()
                f1.append(sum(abs(np.array(rede.resultado_pressao()) - q[1:])))
            self.fitness.append(sum(f1))
        print(min(self.fitness))

    def jarvis(self, dados_nos, dados_trechos, dados_calibracao):
        '''
        Loop e analise situação
        '''
        self.initial_pop(size_pop=30,
                         size_cromossomo=20,
                         minimum=0.01,
                         maximum=1)
        geracao = 0
        while geracao < 200:
            self.funcao_rede(dados_nos=dados_nos,dados_trechos=dados_trechos,dados_calibracao=dados_calibracao)
            self.selecting_mating_pool(elitismo=5,
                                       num_filhos=30,
                                       mutation=0.2)
            print()
            geracao += 1
        print('Fim')
                
    def selecting_mating_pool(self, elitismo, num_filhos, mutation):
        '''
        Input:
        elitismo: Quantidade de filhos elitistas (0 até Número max de filhos)
        num_filhos: Número de filhos
        mutation: Chance de multação
        '''
#         print(self.fitness)
        self.elitismo = elitismo
        self.num_filhos = num_filhos        
        self.mutation = mutation
        
        # Criando Filhos Elitistas
        self.sort_pop = np.array([x for _,x in sorted(zip(self.fitness,self.filhos))])
        self.filhos_elitistas = np.array(self.sort_pop[:self.elitismo,:])
        
        # Criando Filhos Crossovers
        self.crossover()
        
        # Filhos Elitistas e Filhos Crossovers
        self.filhos = np.append(self.filhos_elitistas, self.filhos_crossover,axis=0)
        
        # Criando Filhos Aleatórios
        self.num_filhos_random = self.num_filhos-np.shape(self.filhos)[0]
        self.filhos_random = np.random.uniform(low=self.minimum, 
                                           high=self.maximum, 
                                           size=(self.num_filhos_random,self.size_cromossomo))
        
        # Filhos Elitistas, Filhos Crossovers e Filhos Aleatórios
        self.filhos = np.append(self.filhos, self.filhos_random, axis=0)
        print(self.filhos[0])
#         return self.filhos

    def crossover(self):
        '''
        Função tem como objetivo pegar um array com shape de e.g.(7,4) e ter como output um array com shape de mesma forma.
        Pegar metade da população para manter e fazer crossover
        '''
        self.pais_crossover = self.sort_pop[int(len(self.sort_pop)/2):, :]       
        self.filhos_crossover = np.array([])
        
        # Método das médias de Crossover
#         for i, crom in enumerate(self.pais_crossover):
#             if i == 0:
#                 self.filhos_crossover = np.array([(self.pais_crossover[i]+self.pais_crossover[i-1])/2])
#             else:
#                 self.filhos_crossover = np.append(self.filhos_crossover, np.array([(self.pais_crossover[i]+self.pais_crossover[i-1])/2]), axis=0)
        
        # Método de troca de partes de Crossover
        self.filhos_crossover = np.array([])
        pointBreak = np.ceil(np.random.rand(len(self.pais_crossover),1)*self.size_cromossomo)
        for i in range(len(self.pais_crossover)):
            if i == 0:
                self.filhos_crossover = np.array([np.append(self.pais_crossover[i,0:int(pointBreak[i])],self.pais_crossover[i-1,int(pointBreak[i]):])])
            else:
                self.filhos_crossover = np.append(self.filhos_crossover, np.array([np.append(self.pais_crossover[i,0:int(pointBreak[i])],self.pais_crossover[i-1,int(pointBreak[i]):])]),axis=0)
        
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


class HC_numpy_matrix:
    '''
    Módulo de Hardy-Cross para uma rede específica de 3 anéis utilizando a fórmula de perda de carga de Darcy-Weisbach.
    '''
    
    def __init__(self, dados_trechos, dados_nos, VazaoSaida_reservatorio, rugosidade):
        self.VazaoSaida_reservatorio = VazaoSaida_reservatorio
        self.Q0_modulo = np.array([1,0.307666667,0.272666667,0.359,0.086666667,0.155666667,0.211666667,0.266666667,0.307666667,0.277,0.209,0.092,0.021,0,0.083666667,0.054666667,0.181666667,0.227666667,0.258666667,0.307666667])*self.VazaoSaida_reservatorio
        
        self.diametros = dados_trechos[:,1]
        self.comprimentos = dados_trechos[:,0]
        
        self.cota = dados_nos[:]
        
        self.rugosidade = rugosidade
        
        self.Sem_Loop = np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.Loop_123 = np.array([[0,-1,-1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
                                 [0,1,1,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1],
                                 [0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0]])
        
        self.Loop_1_2 = np.array([0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
#         self.Loop_1_3 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.Loop_2_3 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0])
    

        self.Q_r_1 = self.Q0_modulo * self.Sem_Loop
        self.Q_iterativo = self.Q0_modulo * self.Loop_123
        
    def perdaCarga_unitaria_Universal(self,Q, D,e):
        '''
        Função de Perda de carga utilizando a formulação Universal (Darcy-Weisbach)
        
        Input:
        Q: Vazão (l/s)
        D: Diâmetro (mm)
        e: Rugosidade (mm)
        
        Output:
        j: Perda de carga unitária (m/m)
        '''
#         V = abs(Q) * 4/(0.00314 * D**2)
        V = abs(Q) * 4/(0.00314 * D*D)
        
        Rey = (V * D)/(0.001)
#         f = (0.25)/(np.log10(e/(3.7*D)+5.74/(np.power(Rey,0.9))))**2
        a = (np.log10(e/(3.7*D)+5.74/(np.power(Rey,0.9))))
        f = (0.25)/(a*a)

#         return (f * V**2)/(D*0.0196)
        return (f * V*V)/(D*0.0196)
    
    def vazaoCorretiva_Universal(self, h, Q, n):
        '''
        Função de Correção das vazões pelo método iterativo de Hardy-Cross
        
        Input:
        h: Perda de Carga (m)
        Q: Vazão (l/s)
        n: Constante (e.g. =2 para fórmula de Darcy-Weisbach e =1.85 para Hazen-Williams)
        
        Output:
        Delta_Q: delta de vazão para iteração
        '''
        h_Q = h/Q
        h_Q[np.isnan(h_Q)] = 0
        return np.array([-(h.sum(axis=1))/(n*h_Q.sum(axis=1))])
    
    def simular(self):
        '''
        Função tem como objetivo rodar a pelo método iterativo as vazões até quando a diferença de vazão de uma iteração para outra é menor que 0.01 l/s.
        '''
        self.j_0 = self.perdaCarga_unitaria_Universal(Q=self.Q_r_1,
                                                      D=self.diametros,
                                                      e=self.rugosidade)
        j = self.perdaCarga_unitaria_Universal(Q=self.Q_iterativo,
                                               D=self.diametros,
                                               e=self.rugosidade)
        self.h_0 = self.j_0 * self.comprimentos
        self.h = j * self.comprimentos * np.sign(self.Q_iterativo)

        delta_Q = np.array([[10,10,10]])

        while (abs(delta_Q[0,0]) > 0.01) or (abs(delta_Q[0,1]) > 0.01) or (abs(delta_Q[0,2]) > 0.01):
#             print(delta_Q)
            delta_Q = self.vazaoCorretiva_Universal(h=self.h,
                                                    Q=self.Q_iterativo,
                                                    n=2)

            self.Q_iterativo = self.Q_iterativo +delta_Q.T*abs(self.Loop_123)
            
            self.Q_iterativo[0] -= delta_Q[0,1]*self.Loop_1_2
            self.Q_iterativo[1] -= delta_Q[0,0]*self.Loop_1_2
            
            self.Q_iterativo[1] -= delta_Q[0,2]*self.Loop_2_3
            self.Q_iterativo[2] -= delta_Q[0,1]*self.Loop_2_3

            j = self.perdaCarga_unitaria_Universal(Q=self.Q_iterativo,
                                                   D=self.diametros,
                                                   e=self.rugosidade)
            self.h = j * self.comprimentos * np.sign(self.Q_iterativo)
               
#         print(self.Q_iterativo.T)
    def resultado_pressao(self):
        '''
        Função tem como objetivo cálcular as pressões para os nós 6, 11 e 15.
        '''
        nivel_Reservatorio = 228
            
        j_R1 = self.perdaCarga_unitaria_Universal(Q=self.VazaoSaida_reservatorio,
                                                      D=self.diametros[0],
                                                      e=self.rugosidade[0])

        h_R1 = j_R1 * self.comprimentos[0]
        P1 = nivel_Reservatorio - h_R1

        P6 = P1 - self.cota[5] - abs(self.h[1,17]) - abs(self.h[1,18]) - abs(self.h[1,19])
        P11 = P1 - self.cota[10] - abs(self.h[0,8]) - abs(self.h[0,7]) - abs(self.h[0,6])
        P15 = P1 - self.cota[14] - abs(self.h[0,1]) - abs(self.h[0,2]) - abs(self.h[2,3]) - abs(self.h[2,9]) - abs(self.h[2,10])
        return P6, P11, P15
