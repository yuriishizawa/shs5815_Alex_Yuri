import numpy as np
import pandas as pd

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
    
    def funcao_obj(self):
        '''
        Função para teste, apagar depois.
        '''
        self.fitness = np.zeros((self.size_pop, 1))
        for i,crom in enumerate(self.filhos):
#             print(i, crom)
            self.fitness[i] = 5.1*crom[0] - crom[1]*crom[0] + crom[2]*1.4 - crom[2]*crom[2]*2.1 + 3*crom[0]
        
        print(self.fitness)
        
    def fitness(self, pressoes_simuladas, pressoes_reais):
        '''
        Essa é a função fitness, onde é utilizado após passar pela função objetivo (para dados de pressões). 
        Tem o objetivo de determinar o fitness.
        Atualmente ele pega dados externos ao módulo, ou seja, tem que inserir dados.
        
        Input:
        pressoes_simuladas: Pressões dos nós após realizada simulação (array-like, ou seja, array de array de preferência)
        pressoes_reais: Pressões dos nós dados (array-like, ou seja, array de array de preferência)
        '''
        self.pressoes_simuladas = pressoes_simuladas
        self.pressoes_reais = pressoes_reais
        self.fitness = np.zeros((self.size_pop, 1))

        # Quanto menor, melhor!
        for i,simulado in enumerate(self.pressoes_simuladas):
            self.fitness[i] = sum(abs(simulado - self.pressoes_reais))
        
        print(self.fitness)
        return self.fitness
        
        
                
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
        self.filhos_elitistas = np.array(self.sort_pop[:self.elitismo,:])
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
        return self.filhos

    def crossover(self):
        '''
        Função tem como objetivo pegar um array com shape de e.g.(7,4) e ter como output um array com shape de mesma forma.
        Pegar metade da população para manter e fazer crossover
        '''
        self.pais_crossover = self.sort_pop[int(len(self.sort_pop)/2):, :]       
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
    


class HardyCross_rede:
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
        return (f * V**2)/(D/1000 * 2 * 9.81)
    
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
        self.dados_trechos['h_0'] = self.dados_trechos['j_0'] * self.dados_trechos['Comprimento (m)']
        
        self.dados_trechos['h_1'] = self.dados_trechos['j_1'] * self.dados_trechos['Comprimento (m)'] * self.dados_trechos['Q_iterativo_1']/abs(self.dados_trechos['Q_iterativo_1'])
        self.dados_trechos['h_2'] = self.dados_trechos['j_2'] * self.dados_trechos['Comprimento (m)'] * self.dados_trechos['Q_iterativo_2']/abs(self.dados_trechos['Q_iterativo_2'])
        self.dados_trechos['h_3'] = self.dados_trechos['j_3'] * self.dados_trechos['Comprimento (m)'] * self.dados_trechos['Q_iterativo_3']/abs(self.dados_trechos['Q_iterativo_3'])
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
        
        while (abs(soma_h1)>0.00001) or (abs(soma_h2)>0.00001) or (abs(soma_h3)>0.00001):
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