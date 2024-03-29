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
        self.initial_pop(size_pop=100,
                         size_cromossomo=20,
                         minimum=0.01,
                         maximum=1)
        geracao = 0
        while geracao < 3000:
            self.funcao_rede(dados_nos=dados_nos,dados_trechos=dados_trechos,dados_calibracao=dados_calibracao)
            self.selecting_mating_pool(elitismo=5,
                                       num_filhos=100,
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
    
# spec = [('Q',float32[:]),('h',float32[:]),('n',int32),('D',float32[:]),('e',float32[:])]
# @jitclass(spec)
class Hardy_cross_numpy:

    def __init__(self, dados_trechos, dados_nos, VazaoSaida_reservatorio,rugosidade):
        '''
        
        '''
        self.VazaoSaida_reservatorio = VazaoSaida_reservatorio
#         print(self.VazaoSaida_reservatorio)
        # Vazão chute inicial
        self.Q0_modulo = np.array([1,0.307666667,0.272666667,0.359,0.086666667,0.155666667,0.211666667,0.266666667,0.307666667,0.277,0.209,0.092,0.021,0,0.083666667,0.054666667,0.181666667,0.227666667,0.258666667,0.307666667])*self.VazaoSaida_reservatorio
#         print(self.Q0_modulo)
        # Diâmetros/Comprimento
#         self.diametros = np.array(dados_trechos['Diâmetro (mm)'])
#         self.comprimentos = np.array(dados_trechos['Comprimento (m)'])
        
#         self.diametros = np.loadtxt(dados_trechos,delimiter=',',usecols=2,skiprows=1)
#         self.comprimentos = np.loadtxt(dados_trechos,delimiter=',',usecols=1,skiprows=1)
        self.diametros = dados_trechos[:,1]
        self.comprimentos = dados_trechos[:, 0]
        
        # Cota
#         self.cota = np.array(dados_nos['Cota (m)'])
#         self.cota = np.loadtxt(dados_nos, delimiter=',',usecols=1,skiprows=1)
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
#         f = (0.25)/(np.log10((e/1000)/(3.7*D/1000)+5.74/(((1000 * V * D/1000)/(1.003*10**(-3)))**(0.9))))**2

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
#         print(self.j_1, self.j_2, self.j_3)
#         print(self.comprimentos)
#         print(self.Q_iterativo_1)
        self.h_0 = self.j_0 * self.comprimentos
#         self.h_1 = self.j_1 * self.comprimentos * self.Q_iterativo_1/abs(self.Q_iterativo_1)
#         self.h_2 = self.j_2 * self.comprimentos * self.Q_iterativo_2/abs(self.Q_iterativo_2)
#         self.h_3 = self.j_3 * self.comprimentos * self.Q_iterativo_3/abs(self.Q_iterativo_3)
        
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
            # !
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
            
#             self.h_1 = self.j_1 * self.comprimentos * self.Q_iterativo_1/abs(self.Q_iterativo_1)
#             self.h_2 = self.j_2 * self.comprimentos * self.Q_iterativo_2/abs(self.Q_iterativo_2)
#             self.h_3 = self.j_3 * self.comprimentos * self.Q_iterativo_3/abs(self.Q_iterativo_3)
            
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
            break
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
            
    

class HardyCross_rede_pandas:
    '''
    O objetivo desse módulo é de gerar dados de pressões após fazer a simulação da rede com o método de Hardy-Cross.
    Válido para apenas o exemplo de rede da SHS5815/2019-1.
    Para não precisar ficar lendo csv toda iteração.
    '''
    def __init__(self,dados_trechos, dados_nos,VazaoSaida_reservatorio,rugosidade):
        '''
        Input:
        dados_trechos: dataframe (após utilizar read_csv)
        dados_nos: dataframe (após utilizar read_csv)
        Vazao_Saida_reservatorio: float or int, é o multiplicador para diferentes tipos de vazões
        '''
        self.dados_trechos = dados_trechos
        self.dados_nos = dados_nos
        self.VazaoSaida_reservatorio = VazaoSaida_reservatorio

        self.rugosidade = rugosidade
        
        # Vazão chute inicial
        self.dados_trechos.loc[:, 'Q0_modulo'] = np.array([1,0.307666667,0.272666667,0.359,0.086666667,0.155666667,0.211666667,0.266666667,0.307666667,0.277,0.209,0.092,0.021,0,0.083666667,0.054666667,0.181666667,0.227666667,0.258666667,0.307666667])*self.VazaoSaida_reservatorio
        self.dados_trechos.loc[self.dados_trechos['Trecho'].str.contains('R'), 'Q_reserva_0'] = self.dados_trechos['Q0_modulo']
#         self.dados_trechos.loc[0,'Q_reserva_0'] = self.dados_trechos['Q0_modulo']
        
        # Loop sentido
        self.dados_trechos.loc[[1,2], 'Loop_1'] = -1
        self.dados_trechos.loc[[4,5,6,7,8], 'Loop_1'] = 1
        
        self.dados_trechos.loc[[1,2],'Loop_2'] = 1
        self.dados_trechos.loc[[14,15,16,17,18,19], 'Loop_2'] = -1
        
        self.dados_trechos.loc[[3,9,10,11,12,13,14,15], 'Loop_3'] = 1
        
        # Rugosidade
        self.dados_trechos.loc[:,'rugosidade'] = self.rugosidade
        
        # Aplicando o sentido das vazões após determinada a vazão em módulo.
        self.dados_trechos.loc[self.dados_trechos['Loop_1'].notna(), 'Q_iterativo_1'] = self.dados_trechos['Q0_modulo']*self.dados_trechos['Loop_1']
        self.dados_trechos.loc[self.dados_trechos['Loop_2'].notna(), 'Q_iterativo_2'] = self.dados_trechos['Q0_modulo']*self.dados_trechos['Loop_2']
        self.dados_trechos.loc[self.dados_trechos['Loop_3'].notna(), 'Q_iterativo_3'] = self.dados_trechos['Q0_modulo']*self.dados_trechos['Loop_3']

    def perdaCarga_unitaria_Universal(self, Q, D, e):
        '''
        Função com o objetivo de cálcular a perda de Carga unitária utilizando a fórmula Universal.
        
        Input:
        Q: Vazão (l/s)
        D: Diâmetro (mm)
        e: Rugosidade (mm)
        
        Output:
        Perda de Carga unitária (m/m)
        '''
        V = abs(Q/1000 * 4)/(np.pi * (D/1000)**2)
        Rey = abs(1000 * V * D/1000)/(1.003*10**(-3))
        f = (0.25)/(np.log10((e/1000)/(3.7*D/1000)+5.74/(Rey**(0.9))))**2
#         f = ((64/Rey)**8 + 9.5*(np.log(((e/1000/(3.7*D/1000))+5.74/(Rey)**0.9)-(2500/Rey)**6))**-16)**0.125
        return ((f * V**2)/(D/1000 * 2 * 9.81))
    
    def vazaoCorretiva_Universal(self, h, Q, n):
        '''
        Função com o objetivo de parte do processo do Hardy-Cross.
        
        Input:
        h: Perda de Carga (m)
        Q: Vazão (l/s)
        n: 2 (para fórmula Universal de Darcy-Weisbach) ou 1.85 (para Hazen-Williams)
        
        Output:
        q_corretiva: Vazão corretiva para iteração.
        '''
        h_Q = h/Q
        h_sum = h.sum()
        h_Q_sum = h_Q.sum()
        q_corretiva = -(h_sum)/(n*h_Q_sum)
        return q_corretiva

    def simular(self):
        '''
        Utiliza o Hardy-Cross, com a fórmula Universal de Darcy-Weisbach.
        '''
        
        self.dados_trechos['j_0'] = self.perdaCarga_unitaria_Universal(Q=self.dados_trechos['Q_reserva_0'],
                                                                       D=self.dados_trechos['Diâmetro (mm)'],
                                                                       e=self.dados_trechos['rugosidade'])
        
        self.dados_trechos['j_1'] = self.perdaCarga_unitaria_Universal(Q=self.dados_trechos['Q_iterativo_1'],
                                                                       D=self.dados_trechos['Diâmetro (mm)'],
                                                                       e=self.dados_trechos['rugosidade'])
        self.dados_trechos['j_2'] = self.perdaCarga_unitaria_Universal(Q=self.dados_trechos['Q_iterativo_2'],
                                                                       D=self.dados_trechos['Diâmetro (mm)'],
                                                                       e=self.dados_trechos['rugosidade'])
        self.dados_trechos['j_3'] = self.perdaCarga_unitaria_Universal(Q=self.dados_trechos['Q_iterativo_3'],
                                                                       D=self.dados_trechos['Diâmetro (mm)'],
                                                                       e=self.dados_trechos['rugosidade'])
#         print(self.dados_trechos[['j_1','j_2','j_3']])

        self.dados_trechos['h_0'] = self.dados_trechos['j_0'] * self.dados_trechos['Comprimento (m)']
        
        self.dados_trechos['h_1'] = self.dados_trechos['j_1'] * self.dados_trechos['Comprimento (m)'] * self.dados_trechos['Q_iterativo_1']/abs(self.dados_trechos['Q_iterativo_1'])
        self.dados_trechos['h_2'] = self.dados_trechos['j_2'] * self.dados_trechos['Comprimento (m)'] * self.dados_trechos['Q_iterativo_2']/abs(self.dados_trechos['Q_iterativo_2'])
        self.dados_trechos['h_3'] = self.dados_trechos['j_3'] * self.dados_trechos['Comprimento (m)'] * self.dados_trechos['Q_iterativo_3']/abs(self.dados_trechos['Q_iterativo_3'])
        
#         print(self.dados_trechos[['h_1', 'h_2', 'h_3']])
        soma_h1 = self.dados_trechos['h_1'].sum()
        soma_h2 = self.dados_trechos['h_2'].sum()
        soma_h3 = self.dados_trechos['h_3'].sum()
#         print(soma_h1)
        delta_Q1 = self.vazaoCorretiva_Universal(h=self.dados_trechos['h_1'],
                                            Q=self.dados_trechos['Q_iterativo_1'],
                                            n=2)
        delta_Q2 = self.vazaoCorretiva_Universal(h=self.dados_trechos['h_2'],
                                            Q=self.dados_trechos['Q_iterativo_2'],
                                            n=2)
        delta_Q3 = self.vazaoCorretiva_Universal(h=self.dados_trechos['h_3'],
                                            Q=self.dados_trechos['Q_iterativo_3'],
                                            n=2)
        
        while (abs(soma_h1)>0.0001) or (abs(soma_h2)>0.0001) or (abs(soma_h3)>0.0001):
            self.dados_trechos.loc[self.dados_trechos['Loop_1'].notna(), 'Q_iterativo_1'] +=delta_Q1
            self.dados_trechos.loc[self.dados_trechos['Loop_2'].notna(), 'Q_iterativo_2'] +=delta_Q2
            self.dados_trechos.loc[self.dados_trechos['Loop_3'].notna(), 'Q_iterativo_3'] +=delta_Q3
    
            self.dados_trechos.loc[self.dados_trechos['Loop_1'].notna() & self.dados_trechos['Loop_2'].notna(), 'Q_iterativo_1'] -=delta_Q2
            self.dados_trechos.loc[self.dados_trechos['Loop_1'].notna() & self.dados_trechos['Loop_2'].notna(), 'Q_iterativo_2'] -=delta_Q1
    
            self.dados_trechos.loc[self.dados_trechos['Loop_1'].notna() & self.dados_trechos['Loop_3'].notna(), 'Q_iterativo_1'] -=delta_Q3
            self.dados_trechos.loc[self.dados_trechos['Loop_1'].notna() & self.dados_trechos['Loop_3'].notna(), 'Q_iterativo_3'] -=delta_Q1
    
            self.dados_trechos.loc[self.dados_trechos['Loop_2'].notna() & self.dados_trechos['Loop_3'].notna(), 'Q_iterativo_2'] -=delta_Q3
            self.dados_trechos.loc[self.dados_trechos['Loop_2'].notna() & self.dados_trechos['Loop_3'].notna(), 'Q_iterativo_3'] -=delta_Q2

            
            self.dados_trechos['j_1'] = self.perdaCarga_unitaria_Universal(Q=self.dados_trechos['Q_iterativo_1'], 
                                                              e=self.dados_trechos['rugosidade'], 
                                                              D=self.dados_trechos['Diâmetro (mm)'])
            self.dados_trechos['j_2'] = self.perdaCarga_unitaria_Universal(Q=self.dados_trechos['Q_iterativo_2'], 
                                                              e=self.dados_trechos['rugosidade'], 
                                                              D=self.dados_trechos['Diâmetro (mm)'])
            self.dados_trechos['j_3'] = self.perdaCarga_unitaria_Universal(Q=self.dados_trechos['Q_iterativo_3'], 
                                                              e=self.dados_trechos['rugosidade'], 
                                                              D=self.dados_trechos['Diâmetro (mm)'])
            
            self.dados_trechos.loc[self.dados_trechos['Loop_1'].notna(), 'h_1'] = self.dados_trechos['j_1']*(self.dados_trechos['Q_iterativo_1']/abs(self.dados_trechos['Q_iterativo_1']))*self.dados_trechos['Comprimento (m)']
            self.dados_trechos.loc[self.dados_trechos['Loop_2'].notna(), 'h_2'] = self.dados_trechos['j_2']*(self.dados_trechos['Q_iterativo_2']/abs(self.dados_trechos['Q_iterativo_2']))*self.dados_trechos['Comprimento (m)']
            self.dados_trechos.loc[self.dados_trechos['Loop_3'].notna(), 'h_3'] = self.dados_trechos['j_3']*(self.dados_trechos['Q_iterativo_3']/abs(self.dados_trechos['Q_iterativo_3']))*self.dados_trechos['Comprimento (m)']

            
            soma_h1 = self.dados_trechos['h_1'].sum()
            soma_h2 = self.dados_trechos['h_2'].sum()
            soma_h3 = self.dados_trechos['h_3'].sum()
            
            delta_Q1 = self.vazaoCorretiva_Universal(h=self.dados_trechos['h_1'], 
                                                     Q=self.dados_trechos['Q_iterativo_1'], 
                                                     n=2)
            delta_Q2 = self.vazaoCorretiva_Universal(h=self.dados_trechos['h_2'], 
                                                     Q=self.dados_trechos['Q_iterativo_2'], 
                                                     n=2)
            delta_Q3 = self.vazaoCorretiva_Universal(h=self.dados_trechos['h_3'], 
                                                     Q=self.dados_trechos['Q_iterativo_3'], 
                                                     n=2)

        
        print(self.dados_trechos[['Trecho','Q_iterativo_1','Q_iterativo_2','Q_iterativo_3']])
        
    def resultado_pressao(self):
        '''
        Função tem como objetivo gerar os resultados da pressão para os nós 6, 11 e 15.
        '''
        nivel_Reservatorio = 228
        
        # Primeiro definir a perde de pressão de R - 1
        j_R1 = self.perdaCarga_unitaria_Universal(Q=self.VazaoSaida_reservatorio,
                                                  D=self.dados_trechos.loc[0,'Diâmetro (mm)'],
                                                  e=self.dados_trechos.loc[0,'rugosidade'])
        h_R1 = j_R1 * self.dados_trechos.loc[0,'Comprimento (m)']
        P1 = nivel_Reservatorio - h_R1
        
        # Nós 6, 11 e 15 (Cota Piezometrica => Pressão + Nível)
        P6 = P1 - abs(self.dados_trechos.loc[17,'h_2']) - abs(self.dados_trechos.loc[18,'h_2']) - abs(self.dados_trechos.loc[19,'h_2'])
        P11 = P1 - abs(self.dados_trechos.loc[8,'h_1']) - abs(self.dados_trechos.loc[7,'h_1']) - abs(self.dados_trechos.loc[6,'h_1'])
        P15 = P1 - abs(self.dados_trechos.loc[1,'h_1']) - abs(self.dados_trechos.loc[2,'h_1']) - abs(self.dados_trechos.loc[3,'h_3']) - abs(self.dados_trechos.loc[9,'h_3']) - abs(self.dados_trechos.loc[10,'h_3'])
        
        # Subtraindo Cota do terreno
        P6 -= self.dados_nos.loc[5, 'Cota (m)']
        P11 -=self.dados_nos.loc[10, 'Cota (m)']
        P15 -=self.dados_nos.loc[14, 'Cota (m)']
        
        return P6, P11, P15