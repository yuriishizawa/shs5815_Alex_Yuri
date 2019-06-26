# shs5815_Alex_Yuri
### Alunos:
- <b>Alex Naoki Asato Kobayashi</b>
- <b>Yuri Batista Ishizawa</b>

### Objetivo:
Repositório de códigos da disciplina SHS5815-2019 para o trabalho 02, envolvendo o desenvolvimento de código para solução utilizando método meta heurística e Hardy-Cross.


#### Problema do Enunciado:
> Os responsáveis estão contentes com o avanço obtido pela construção do modelo para simulação do comportamento hidráulico da rede de distribuição principal da cidade, mas se preocuparam quando você explicou para eles que no modelo estão sendo supostos valores de rugosidade equivalentes a tubos novos, pois os da cidade tem muitos anos de funcionamento e sabe-se que tem mudado suas características.
Com o objetivo de obter a informação necessária para calibrar o modelo são instalados sensores de pressão nos nós 6, 11 e 15, e um sensor de vazão na saída do reservatório. Com isso, são obtidos valores médios em 12 diferentes horas do dia. É preciso supor que a distribuição do consumo total nos nós é constante.
Sua responsabilidade é usar esse conjunto de 12 tuplas de vazão e cargas de pressão para calibrar os valores de rugosidade das tubulações. 
Há uma informação de que o anel que contém o nó 8 foi o primeiro a ser construído, seguido do que contém o nó 9 e por último o que contém o 14. Porém, múltiplas mudanças têm ocorrido na rede, e você deverá avaliar a melhor forma de usar (ou não) essa informação.

#### Método do Enunciado:
>A calibração deve ser encarada como um processo de otimização, que visa minimizar o erro ou diferença entre as respostas (pressões nos nós) conhecidas e simuladas. A simulação será realizada com o modelo desenvolvido na primeira parte do trabalho (e melhorado). O método de otimização será um algoritmo genético. 

