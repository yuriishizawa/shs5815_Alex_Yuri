import numpy as np
import math

class HardyCross_rede:
    '''
    O objetivo desse módulo é de gerar dados de pressões após fazer a simulação da rede com o método de Hardy-Cross.
    Válido para apenas o exemplo de rede da SHS5815/2019-1.
    Para não precisar ficar lendo csv toda iteração.
    '''
    def __init__(self, a, p, Q_R1, e):
        '''
        Input:
        a: matriz dos dados dos trechos (após utilizar load.txt)
        p: dataframe (após utilizar read_csv)
        Q_R1: float or int, é o multiplicador para diferentes tipos de vazões
        e: rugosidade dos trechos
        '''
        self.a = a
        self.p = p
        self.Q_R1 = Q_R1
        self.a[:, 3] = self.a[:, 3] * self.Q_R1/7
        self.e_rede = [0 for i in range(24)]
        for i in list(range(8)):
            self.e_rede[i] = e[i]
        for i in list(range(8,21)):
            self.e_rede[i+2] = e[i]
        self.e_rede[8], self.e_rede[9], self.e_rede[22], self.e_rede[23] = e[1], e[2], e[10], e[11]
        
    def universal(self):
        '''
        Função com o objetivo de cálcular a perda de Carga unitária utilizando a fórmula Universal.
        
        Input:
        Q: Vazão (l/s)
        D: Diâmetro (mm)
        e: Rugosidade (mm)
        
        Output:
        Perda de Carga unitária (m/m)
        '''
        v = self.a[:,3]*4/(((self.a[:,2]/1000)**2)*math.pi*1000) #vetor de velocidades
        rey = abs(v*self.a[:,2]*10**(3)) #vetor de numeros de reynolds
        f = 0.25/(np.log10((self.e_rede/(3.7*self.a[:,2])) + (5.74/rey**0.9)))**2 #vetor de f
        h = (f*self.a[:,1]*v**2)/((self.a[:,2]/1000)*2*9.81)*(self.a[:,3]/abs(self.a[:,3])) #vetor de perda de carga
        h_q = h/self.a[:,3] #vetor de delta h sobre delta q
        return h, h_q
   
    def teste_u(self):
        h_q_anel = np.split(self.universal()[1], np.cumsum(np.unique(self.a[:, 0], return_counts=True)[1])[:-1])
        soma_h_q = [h_q_anel[1].sum(axis = 0), h_q_anel[2].sum(axis = 0), h_q_anel[3].sum(axis = 0)]
        h_anel = np.split(self.universal()[0], np.cumsum(np.unique(self.a[:, 0], return_counts=True)[1])[:-1])
        soma_h = [h_anel[1].sum(axis = 0), h_anel[2].sum(axis = 0), h_anel[3].sum(axis = 0)]
        delta_q = [- soma_h[i] / (2 * soma_h_q[i]) for i in range(3)]
        modulo_h = [abs(h_anel[1].sum(axis = 0)), abs(h_anel[2].sum(axis = 0)), abs(h_anel[3].sum(axis = 0))]
        return delta_q, modulo_h
    
    def simular(self):
        #self.e[8], self.e[9], self.e[22], self.e[23] = self.e[1], self.e[2], self.e[10], self.e[11]
        delta_q, modulo_h = self.teste_u()[0], self.teste_u()[1]
        while max(modulo_h) >= 0.001:
            for trecho in list(range(1,8)):
                self.a[trecho,3] += delta_q[0]
        
            for trecho in list(range(8,16)):
                self.a[trecho,3] += delta_q[1]
        
            for trecho in list(range(16,24)):
                self.a[trecho,3] += delta_q[2]
            #Trechos em mais de um anel
        
            self.a[1,3] -= delta_q[1]
            self.a[2,3] -= delta_q[1]
            self.a[8,3] -= delta_q[0]
            self.a[9,3] -= delta_q[0]
            self.a[10,3] -= delta_q[2]
            self.a[11,3] -= delta_q[2]
            self.a[22,3] -= delta_q[1]
            self.a[23,3] -= delta_q[1]
            self.universal()
            delta_q, modulo_h = self.teste_u()[0], self.teste_u()[1]
        return self.a, self.universal()
    
    def p_calc(self):
        carga6 = self.simular()[1][0][0] + self.simular()[1][0][15] + self.simular()[1][0][14] + self.simular()[1][0][13]
        carga11 = self.simular()[1][0][0] - self.simular()[1][0][7] - self.simular()[1][0][6] - self.simular()[1][0][5]
        carga15 = self.simular()[1][0][0] + self.simular()[1][0][15] + self.simular()[1][0][14] + self.simular()[1][0][13] + self.simular()[1][0][12] + self.simular()[1][0][21] + self.simular()[1][0][20] + self.simular()[1][0][19]
        P6 = self.p[0,0] - self.p[6,0] - carga6
        P11 = self.p[0,0] - self.p[11,0] - carga11
        P15 = self.p[0,0] - self.p[15,0] - carga15
        return P6, P11, P15
