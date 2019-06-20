import math
import numpy as np
import pandas as pd
df = pd.read_csv('trechos.csv', sep = ';')
#df = pd.read_excel('dados_da_rede.xlsx')

def hazen(x):
    x['j'] = 10.674*((abs(x['q'])/1000)**1.852)/((150**1.852)*((x['D']/1000)**4.871))
    x['h'] = x['j']*x['L']*(x['q']/abs(x['q']))
    x['h_q'] = x['h']/x['q']
    return x

def universal(x):
    x['v'] = x['q']*4/(((x['D']/1000)**2)*math.pi*1000)
    x['rey'] = abs(x['v']*x['D']*10**(3))
    x['f'] = 0.25/(np.log10((x['rug']/(3.7*x['D'])) + (5.74/x['rey']**0.9)))**2
    x['h'] = (x['f']*x['L']*x['v']**2)/((x['D']/1000)*2*9.81)*(x['q']/abs(x['q']))
    x['h_q'] = x['h']/x['q']
    return x

rede = universal(df)

### Agrupamento dos dados por anel
def teste_h(x):
    soma = x.groupby('Anel').sum()
    soma['modulo_h'] = abs(soma['h'])
    soma['delta_q'] = -soma['h']/(1.852*soma['h_q'])
    return soma

def teste_u(x):
    soma = x.groupby('Anel').sum()
    soma['modulo_h'] = abs(soma['h'])
    soma['delta_q'] = -soma['h']/(2*soma['h_q'])
    return soma

soma = teste_u(rede)

### Redistribuição das vazões pelo Método de Hardy-Cross ###
while soma['modulo_h'][1:3].max() >= 0.001:      #para modulo_h< 0.01
   
    for trecho in list(range(1,8)):
        rede.iloc[trecho,7] += soma['delta_q'][1]
        
    for trecho in list(range(8,16)):
        rede.iloc[trecho,7] += soma['delta_q'][2]
    
    for trecho in list(range(16,24)):
        rede.iloc[trecho,7] += soma['delta_q'][3]
        
    #Trechos em mais de um anel
        
    rede.iloc[1,7] -= soma['delta_q'][2]
    rede.iloc[2,7] -= soma['delta_q'][2]
    rede.iloc[8,7] -= soma['delta_q'][1]
    rede.iloc[9,7] -= soma['delta_q'][1]
    rede.iloc[10,7] -= soma['delta_q'][3]
    rede.iloc[11,7] -= soma['delta_q'][3]
    rede.iloc[22,7] -= soma['delta_q'][2]
    rede.iloc[23,7] -= soma['delta_q'][2]
    
    rede = universal(rede)
    soma = teste_u(rede)

rede['q'] = round(rede['q'],3)      ### Arredondamento dos valores de vazão

### Pressões na rede ###
p = pd.read_csv('nos.csv', sep = ';')
p['h'] = float(0)
p.iloc[1,3] = rede['h'][0]
p.iloc[2,3] = p['h'][1] + rede['h'][1]
p.iloc[3,3] = p['h'][2] + rede['h'][2]
p.iloc[8,3] = p['h'][1] + rede['h'][15]
p.iloc[7,3] = p['h'][8] + rede['h'][14]
p.iloc[6,3] = p['h'][7] + rede['h'][13]
p.iloc[5,3] = p['h'][6] + rede['h'][12]
p.iloc[4,3] = p['h'][5] + rede['h'][10]
p.iloc[9,3] = p['h'][1] - rede['h'][7]
p.iloc[10,3] = p['h'][9] - rede['h'][6]
p.iloc[11,3] = p['h'][10] - rede['h'][5]
p.iloc[12,3] = p['h'][11] - rede['h'][4]
p.iloc[13,3] = p['h'][3] + rede['h'][16]
p.iloc[14,3] = p['h'][13] + rede['h'][17]
p.iloc[15,3] = p['h'][14] + rede['h'][18]
p.iloc[16,3] = p['h'][15] + rede['h'][19]
p.iloc[17,3] = p['h'][16] + rede['h'][20]

p['cota_piezometrica'] = p['cota'] + p['h']

### Reservatório com cota de 228m
p['p_d'] = p.iloc[0,1] - p['cota_piezometrica']

### Cálculo de nível mínimo e nível máximo de reservatório

#N_min = p['p_d'][1:17].max() + 10
#N_max = p['Cota'][1:17].min() + 50
#p['cota_piezometrica'] = N_min - p['Cota']

### Cálculo de nível mínimo e nível máximo de reservatório

#N_min = p['p_d'][1:17].max() + 10
#N_max = p['Cota'][1:17].min() + 50
#p['cota_piezometrica'] = N_min - p['Cota']

#Resultado em tela
apresentacao_rede = rede[['Trecho', 'Anel', 'q']]
apresentacao_rede.columns = ['Trecho', 'Anel', 'Vazão (L/s)']
apresentacao_pressao = p[['no', 'p_d']]
apresentacao_pressao.columns = ['no', 'Pressão disponível (m)']

print(apresentacao_rede)
print(apresentacao_pressao)
apresentacao_pressao.to_csv('pressões.txt', header=True, index=False, sep='\t')
apresentacao_rede.to_csv('rede.txt', header=True, index=False, sep='\t')
#print(round(N_min,2))
#print(round(N_max,2))
