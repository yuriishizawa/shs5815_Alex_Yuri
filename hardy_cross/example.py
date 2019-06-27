from HardyCross_rede import HardyCross_rede
import numpy as np

## parametros de entrada
a = np.loadtxt('trechos.txt', skiprows=1, usecols=range(1,5))
p = np.loadtxt('nos.txt', skiprows=1, usecols=range(1,3))
Q_R1 = 1 #vazão que sai do reservatório
e = [0.1 for i in range(20)] #rugosidade dos trechos

#hardy-cross
resultados = HardyCross_rede(a, p, Q_R1, e)
P6 = resultados.p_calc()[0]
P11 = resultados.p_calc()[1]
P15 = resultados.p_calc()[2]

#Apresentação dos dados finais
#Retirar comentários quando o algoritmo completo estiver pronto
#import pandas as pd
#df = pd.read_csv('trechos.txt', sep = '\s+')
#rugosidades = pd.Series(e_rede,index =[df['Trecho']]) #e_rede eh a lista com os valores finais de rugosidade
#dados = pd.DataFrame(rugosidades, columns=['Rugosidade'])
#print(dados)
