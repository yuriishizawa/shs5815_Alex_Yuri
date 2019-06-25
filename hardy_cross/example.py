from HardyCross_rede import HardyCross_rede
import numpy as np

## parametros de entrada
a = np.loadtxt('trechos.txt', skiprows=1, usecols=range(1,5))
p = np.loadtxt('nos.txt', skiprows=1, usecols=range(1,3))
Q_R1 = 1 #vazão que sai do reservatório
e = [0.1 for i in range(24)] #rugosidade dos trechos

#hardy-cross
resultados = HardyCross_rede(a, p, Q_R1, e)
P6 = resultados.p_calc()[0]
P11 = resultados.p_calc()[1]
P15 = resultados.p_calc()[2]