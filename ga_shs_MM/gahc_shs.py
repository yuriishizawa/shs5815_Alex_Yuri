import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# from numba import jitclass
# from numba import float32, int32

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
    
    ##### Apagar?
#     def funcao_obj(self):
#         '''
#         Função para teste, apagar depois.
#         '''
#         self.fitness = np.zeros((self.size_pop, 1))
#         for i,crom in enumerate(self.filhos):
# #             print(i, crom)
#             self.fitness[i] = 5.1*crom[0] - crom[1]*crom[0] + crom[2]*1.4 - crom[2]*crom[2]*2.1 + 3*crom[0]
        
#         print(self.fitness)
    #####
    
    def funcao_rede(self, dados_nos, dados_trechos, dados_calibracao):
        '''
        Função com o objetivo de fazer o loop?
        Input:
        
        '''
        self.fitness = []
        for c in self.filhos:
#             print(c)
            f1 = []
#             for i,q in enumerate(dados_calibracao['Vazao(l/s)']):
            for i,q in enumerate(dados_calibracao):
                
#                 rede = HardyCross_rede(dados_nos=dados_nos, dados_trechos=dados_trechos,VazaoSaida_reservatorio=q,rugosidade=c)
#                 rede.simular()
#                 print(type(q[0]))
                rede = Hardy_cross_numpy(dados_nos=dados_nos,
                                         dados_trechos=dados_trechos,
                                         VazaoSaida_reservatorio=q[0],rugosidade=c)
                rede.simular()
                
#                 f1.append(sum(abs(np.array(rede.resultado_pressao()) - np.array(dados_calibracao.loc[i,['P_no6(m)','P_no11(m)','P_no15(m)']]))))
                f1.append(sum(abs(np.array(rede.resultado_pressao()) - q[1:])))
            self.fitness.append(sum(f1))
        print(min(self.fitness))
#             print(self.fitness)

    def jarvis(self, dados_nos, dados_trechos, dados_calibracao):
        '''
        Loop e analise situação
        '''
        self.initial_pop(size_pop=50,
                         size_cromossomo=20,
                         minimum=0.01,
                         maximum=1)
        geracao = 0
        while geracao < 500:
            self.funcao_rede(dados_nos=dados_nos,dados_trechos=dados_trechos,dados_calibracao=dados_calibracao)
            self.selecting_mating_pool(elitismo=5,
                                       num_filhos=50,
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
#         print(self.filhos_elitistas)
        
        # Criando Filhos Crossovers
        self.crossover()
        
        # Filhos Elitistas e Filhos Crossovers
        self.filhos = np.append(self.filhos_elitistas, self.filhos_crossover,axis=0)
#         print(np.shape(self.filhos))
        
        # Criando Filhos Aleatórios
        self.num_filhos_random = self.num_filhos-np.shape(self.filhos)[0]
        self.filhos_random = np.random.uniform(low=self.minimum, 
                                           high=self.maximum, 
                                           size=(self.num_filhos_random,self.size_cromossomo))
#         print(self.filhos_crossover)
        
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
        for i, crom in enumerate(self.pais_crossover):
            if i == 0:
                self.filhos_crossover = np.array([(self.pais_crossover[i]+self.pais_crossover[i-1])/2],dtype=np.float32)
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

class Hardy_cross_numpy:

    def __init__(self, dados_trechos, dados_nos, VazaoSaida_reservatorio,rugosidade):
        '''
        
        '''
        self.VazaoSaida_reservatorio = VazaoSaida_reservatorio

        # Vazão chute inicial
        self.Q0_modulo = np.array([1,0.307666667,0.272666667,0.359,0.086666667,0.155666667,0.211666667,0.266666667,0.307666667,0.277,0.209,0.092,0.021,0,0.083666667,0.054666667,0.181666667,0.227666667,0.258666667,0.307666667])*self.VazaoSaida_reservatorio

        self.diametros = dados_trechos[:,1]
        self.comprimentos = dados_trechos[:, 0]
        
        # Cota
        self.cota = dados_nos[:]
        
        # Loop sentido
        self.Sem_Loop = np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.Loop_1 = np.array([0,-1,-1,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0])
        self.Loop_2 = np.array([0,1,1,0,0,0,0,0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1])
        self.Loop_3 = np.array([0,0,0,1,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0])

        self.Loop_1_2 = np.array([0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.Loop_1_3 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
        self.Loop_2_3 = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0])
        
        # Rugosidade
        self.rugosidade = rugosidade
        
        self.Q_r_1 = self.Q0_modulo * self.Sem_Loop
        self.Q_iterativo_1 = self.Q0_modulo * self.Loop_1
        self.Q_iterativo_2 = self.Q0_modulo * self.Loop_2
        self.Q_iterativo_3 = self.Q0_modulo * self.Loop_3
        
    def perdaCarga_unitaria_Universal(self,Q, D,e):
        '''
        
        '''
        V = abs(Q/1000 * 4)/(np.pi * (D/1000)**2)
        Rey = (1000 * V * D/1000)/(1.003*10**(-3))
        f = (0.25)/(np.log10((e/1000)/(3.7*D/1000)+5.74/(Rey**(0.9))))**2
        return (f * V**2)/(D/1000 * 2 * 9.81)
    
    def vazaoCorretiva_Universal(self, h, Q, n):
        '''
        
        '''
#         print(h)
        h_Q = h/Q
#         h_sum = np.sum(h)
#         print(np.nan_to_num(h_Q))
        
#         h_Q_sum = np.sum(h_Q)
#         print(h)
        h_sum = h.sum()
        h_Q_sum = np.nan_to_num(h_Q).sum()
#         print(h_Q_sum)
        q_corretiva = -(h_sum)/(n*h_Q_sum)
        return q_corretiva
    def simular(self):
        '''
        
        '''
#         print('simuladno')
        self.j_0 = self.perdaCarga_unitaria_Universal(Q=self.Q_r_1,
                                                      D=self.diametros,
                                                      e=self.rugosidade)
        j_1 = self.perdaCarga_unitaria_Universal(Q=self.Q_iterativo_1,
                                                 D=self.diametros,
                                                 e=self.rugosidade)
        j_2 = self.perdaCarga_unitaria_Universal(Q=self.Q_iterativo_2,
                                                 D=self.diametros,
                                                 e=self.rugosidade)
        j_3 = self.perdaCarga_unitaria_Universal(Q=self.Q_iterativo_3,
                                                 D=self.diametros,
                                                 e=self.rugosidade)

        self.h_0 = self.j_0 * self.comprimentos
        
        self.h_1 = j_1 * self.comprimentos * np.sign(self.Q_iterativo_1)
        self.h_2 = j_2 * self.comprimentos * np.sign(self.Q_iterativo_2)
        self.h_3 = j_3 * self.comprimentos * np.sign(self.Q_iterativo_3)
        
#         print(self.h_1)
        soma_h1 = self.h_1.sum()
        soma_h2 = self.h_2.sum()
        soma_h3 = self.h_3.sum()
#         print(soma_h1,soma_h2,soma_h3)

        delta_Q1 = self.vazaoCorretiva_Universal(h=self.h_1,
                                                 Q=self.Q_iterativo_1,
                                                 n=2)
        delta_Q2 = self.vazaoCorretiva_Universal(h=self.h_2,
                                                 Q=self.Q_iterativo_2,
                                                 n=2)
        delta_Q3 = self.vazaoCorretiva_Universal(h=self.h_3,
                                                 Q=self.Q_iterativo_3,
                                                 n=2)
#         print(delta_Q1)
        while (abs(soma_h1)>0.001) or (abs(soma_h2)>0.001) or (abs(soma_h3)>0.001):
            self.Q_iterativo_1 += delta_Q1*abs(self.Loop_1)
            self.Q_iterativo_2 += delta_Q2*abs(self.Loop_2)
            self.Q_iterativo_3 += delta_Q3*abs(self.Loop_3)
            
            self.Q_iterativo_1 -= delta_Q2*self.Loop_1_2
            self.Q_iterativo_2 -= delta_Q1*self.Loop_1_2
            
#             self.Q_iterativo_1 -= delta_Q3*self.Loop_1_3
#             self.Q_iterativo_3 -= delta_Q1*self.Loop_1_3
            
            self.Q_iterativo_2 -= delta_Q3*self.Loop_2_3
            self.Q_iterativo_3 -= delta_Q2*self.Loop_2_3
            
            j_1 = self.perdaCarga_unitaria_Universal(Q=self.Q_iterativo_1,
                                                     D=self.diametros,
                                                     e=self.rugosidade)
            j_2 = self.perdaCarga_unitaria_Universal(Q=self.Q_iterativo_2,
                                                     D=self.diametros,e=self.rugosidade)
            j_3 = self.perdaCarga_unitaria_Universal(Q=self.Q_iterativo_3,
                                                     D=self.diametros,
                                                     e=self.rugosidade)
            

            self.h_1 = j_1 * self.comprimentos * np.sign(self.Q_iterativo_1)
            self.h_2 = j_2 * self.comprimentos * np.sign(self.Q_iterativo_2)
            self.h_3 = j_3 * self.comprimentos * np.sign(self.Q_iterativo_3)
            
            
            soma_h1 = self.h_1.sum()
            soma_h2 = self.h_2.sum()
            soma_h3 = self.h_3.sum()
            
            delta_Q1 = self.vazaoCorretiva_Universal(h=self.h_1,
                                                     Q=self.Q_iterativo_1,
                                                     n=2)
            delta_Q2 = self.vazaoCorretiva_Universal(h=self.h_2,
                                                     Q=self.Q_iterativo_2,
                                                     n=2)
            delta_Q3 = self.vazaoCorretiva_Universal(h=self.h_3,
                                                     Q=self.Q_iterativo_3,
                                                     n=2)
        
#         print(self.Q_iterativo_1)
#         print(self.Q_iterativo_2)
#         print(self.Q_iterativo_3)
    def resultado_pressao(self):
        '''
            
        '''
        nivel_Reservatorio = 228
            
        j_R1 = self.perdaCarga_unitaria_Universal(Q=self.VazaoSaida_reservatorio,
                                                      D=self.diametros[0],
                                                      e=self.rugosidade[0])
#         print(j_R1)
        h_R1 = j_R1 * self.comprimentos[0]
        P1 = nivel_Reservatorio - h_R1
#         print(P1)
        P6 = P1 - self.cota[5] - abs(self.h_2[17]) - abs(self.h_2[18]) - abs(self.h_2[19])
        P11 = P1 - self.cota[10] - abs(self.h_1[8]) - abs(self.h_1[7]) - abs(self.h_1[6])
        P15 = P1 - self.cota[14] -abs(self.h_1[1]) - abs(self.h_1[2]) - abs(self.h_3[3]) - abs(self.h_3[9]) - abs(self.h_3[10])
#         print(P6)
        return P6, P11, P15
