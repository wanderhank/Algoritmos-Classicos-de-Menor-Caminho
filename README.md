# Algoritmos Clássicos de Menor Caminho

## Grafos
> Grafos são estruturas matemáticas utilizadas para representar relações entre diferentes elementos. Eles são formados por vértices, que representam os pontos ou entidades do problema, e por arestas, que representam as conexões
> existentes entre esses vértices. Dependendo da situação analisada, as arestas podem possuir direção, peso ou outras propriedades.
> <img src="/images/grafo-simples.png" alt="Grafo Direcionado" width="400">

> Em um **grafo direcionado**, cada aresta possui um sentido definido, de modo que uma conexão de um vértice (u) para um vértice (v) não implica necessariamente a existência do caminho inverso.
> 
> <img src="/images/grafo-direcionado.png" alt="Grafo Direcionado" width="400">

> Em um **grafo ponderado**, cada aresta recebe um valor numérico que pode representar distância, custo, tempo, consumo de recursos ou qualquer
> outra medida relevante.
>
> <img src="/images/grafo-ponderado.png" alt="Grafo Direcionado" width="400">

> Também é possível classificar os grafos de acordo com a quantidade de conexões: **grafos esparsos** possuem poucas arestas em relação ao total possível, enquanto **grafos densos** apresentam um número elevado de conexões.
> <table><tr><td><img src="/images/grafo-esparso.png" alt="Grafo Esparso" width="300"></td><td><img src="/images/grafo-denso.png" alt="Grafo Denso" width="300"></td></tr></table>

## Algoritmos de Menor Caminho

> Um algoritmo de menor caminho (ou shortest path algorithm) é um método usado para encontrar o caminho de menor custo entre dois pontos (vértices) em um grafo.
> O objetivo do algoritmo é encontrar a sequência de arestas que liga a origem ao destino com o menor custo total, que pode ser a menor distância, o menor tempo, o menor número de nós visitados.

### Algoritmo de Floyd-Warshall

#### Origem

> O algoritmo de Floyd-Warshall surgiu de duas publicações separadas, no mesmo ano de 1962. Warshall publicou um método para calcular o fecho transitivo de um grafo — basicamente, descobrir quais pares de vértices têm algum caminho entre si, sem se importar com o custo. Floyd, por conta própria, adaptou basicamente a mesma lógica para resolver um problema mais útil aqui: calcular o custo do menor caminho entre cada par de vértices de um grafo ponderado. É por isso que o algoritmo carrega os dois nomes, mesmo eles não tendo trabalhado juntos.

#### Objetivo

> O Floyd-Warshall é um algoritmo utilizado para encontrar as menores distâncias entre **todos** os pares de vértices de um grafo direcionado e ponderado — não parte de uma única origem, como o Dijkstra ou o Bellman-Ford. Na literatura, esse problema é chamado de All-Pairs Shortest Path (APSP): dado um grafo G = (V, E), formalmente, o objetivo é encontrar, para cada par (i, j), o valor do caminho de menor custo entre eles, ou infinito, caso não exista nenhum caminho.
>
> Dava pra resolver isso rodando Dijkstra a partir de cada vértice, um de cada vez. O que o Floyd-Warshall faz de diferente é resolver tudo numa formulação só de programação dinâmica, sem tratar cada vértice como um problema separado.

#### Funcionamento

> A ideia central do algoritmo é testar, para cada par (i, j), se passar por um vértice intermediário k encurta o caminho já conhecido:
>
>> **dist[i][k] + dist[k][j] < dist[i][j]**
>
> Cormen (2009, cap. 25) formaliza isso definindo d_ij^(k) como o menor caminho de i até j usando só os vértices {1, ..., k} como intermediários possíveis. A recorrência sai naturalmente disso: ou o caminho ótimo não passa por k (e o valor não muda em relação à rodada anterior), ou passa por k (e o caminho se quebra em dois pedaços — i até k, e k até j — cada um já resolvido na rodada anterior).
>
> Por exemplo, considere um grafo com as arestas C→A (peso 5) e A→B (peso 3), sem aresta direta de C para B. Ao liberar A como intermediário (k = A), o algoritmo testa:
>
>> **5 + 3 = 8**
>
> Como não existia caminho de C para B antes, esse valor passa a ser a nova distância registrada: dist[C][B] = 8.
>
> O processo se repete para cada vértice do grafo como intermediário (k percorre todos os vértices), sempre atualizando a matriz de distâncias quando um caminho mais curto é encontrado. Um detalhe que exige atenção na implementação é que a matriz é atualizada "em cima dela mesma" — um único `dist`, sendo sobrescrito a cada rodada de k, em vez de uma cópia nova por rodada. Isso só é seguro porque, na hora de atualizar dist[i][j], os valores usados (dist[i][k] e dist[k][j]) nunca foram alterados durante essa mesma rodada — para isso acontecer, seria necessário ter i = k ou j = k, e nesse caso a comparação não muda nada (comparar um caminho com ele mesmo).
>
> A corretude do algoritmo é provada por indução em k: no caso base (k = 0, nenhum intermediário liberado), a matriz reflete só os pesos das arestas diretas — trivialmente correto. Supondo que até k-1 a matriz esteja certa, a rodada de k testa se vale a pena passar por esse vértice novo. Como nenhum caminho simples num grafo de V vértices passa por mais de V vértices intermediários, depois das V rodadas a matriz reflete o menor caminho de verdade, sem restrição de quais vértices podem ser usados no meio.

#### Complexidade

> O algoritmo tem três laços aninhados percorrendo os V vértices do grafo. Sua complexidade de tempo é:
>
>> O(V³)
>
> E a complexidade de espaço, referente ao armazenamento da matriz de distâncias, é:
>
>> O(V²)
>
> Uma característica importante é que essa complexidade **não muda com a quantidade de arestas** — grafo esparso ou denso, o algoritmo realiza a mesma quantidade de operações.

#### Vantagens e Desvantagens

> As principais vantagens do algoritmo de Floyd-Warshall são:
>
>> - resolve todos os pares de vértices numa única execução, sem precisar rodar o algoritmo várias vezes;
>> - funciona mesmo com arestas de peso negativo, desde que não exista ciclo negativo alcançável;
>> - detecta ciclos de peso negativo de graça: se, ao final, algum valor da diagonal principal (dist[i][i]) ficar negativo, é sinal de que existe um ciclo negativo passando por aquele vértice;
>> - desempenho previsível e competitivo em grafos densos, onde o número de arestas se aproxima de V².
>
> Em contrapartida, sua principal limitação é que o custo O(V³) é fixo, independente da densidade do grafo. Em grafos esparsos, algoritmos como Dijkstra ou Bellman-Ford, que exploram apenas as arestas que existem, tendem a ter desempenho melhor.

### Algoritmo de Dijkstra
### Algoritmo de Johnson

### Algoritmo de Bellman-Ford

#### Origem
> O algoritmo de Bellman-Ford recebeu esse nome em referência aos matemáticos Richard Bellman e Lester Randolph Ford Jr., que publicaram trabalhos relacionados ao método em 1958 e 1956, respectivamente. Entretanto, uma ideia semelhante já havia 
> sido apresentada por Alfonso Shimbel, em 1955. Em 1959, Edward F. Moore publicou outra variação, razão pela qual o método também pode ser chamado de algoritmo de Bellman-Ford-Moore.

#### Objetivo
> O Bellman-Ford é um algoritmo utilizado para encontrar as menores distâncias entre um vértice de origem e todos os demais vértices de um grafo direcionado e ponderado. Sua principal vantagem é funcionar mesmo quando algumas arestas possuem pesos 
> negativos, desde que não exista um ciclo de peso negativo alcançável a partir da origem.
> Um ciclo negativo é um caminho fechado cuja soma dos pesos é menor que zero. Quando esse tipo de ciclo existe, não há uma menor distância bem definida, pois seria possível percorrer o ciclo repetidamente e diminuir o custo indefinidamente.

#### Funcionamento
> Inicialmente, o algoritmo atribui distância zero ao vértice de origem e distância infinita aos demais vértices. Em seguida, percorre todas as arestas do grafo e realiza o processo de relaxamento.
> Relaxar uma aresta significa verificar se ela oferece uma forma mais barata de chegar ao seu vértice de destino. Para uma aresta que liga o vértice (u) ao vértice (v), com peso (w), é feita a comparação:
>> **dist[u] + w < dist[v]**
> 
> Se essa condição for verdadeira, a distância de (v) é atualizada:
>> **dist[v] = dist[u] + w**
> 
> Por exemplo, considere que a distância conhecida até o vértice (A) seja 4, a distância conhecida até (B) seja 10 e a aresta (A → B) tenha peso 3. Passar por (A) produziria um custo igual a:
>> **4 + 3 = 7**
> 
> Como 7 é menor que 10, a aresta (A → B) é relaxada e a distância de (B) passa a ser 7.
> O processo de relaxamento de todas as arestas é repetido, no máximo, (V-1) vezes, sendo (V) a quantidade de vértices. Isso ocorre porque um menor caminho simples pode conter, no máximo, (V-1) arestas.
> Depois dessas repetições, o algoritmo percorre novamente todas as arestas. Se alguma distância ainda puder ser reduzida, isso indica a existência de um ciclo de peso negativo alcançável pela origem.
#### Complexidade
> Para uma única origem, o Bellman-Ford percorre todas as (E) arestas até (V-1) vezes. Sua complexidade de tempo é:
>> O(VE)
> 
> Quando o algoritmo é executado a partir de cada vértice para calcular os menores caminhos entre todos os pares, sua complexidade passa a ser:
>> O(V²E)
> 
#### Vantagens e Desvantagens
> As principais vantagens do algoritmo de Bellman-Ford são:
>
>> - aceita arestas com pesos negativos;
>> - detecta ciclos de peso negativo alcançáveis;
>> - possui funcionamento relativamente simples;
>> - permite reconstruir os caminhos por meio dos predecessores;
>> - pode ser adaptado para calcular menores caminhos entre todos os pares.
>
> Em contrapartida, sua principal limitação é o custo computacional elevado. Em grafos que possuem somente pesos positivos, algoritmos como Dijkstra geralmente apresentam desempenho melhor.
Quando Bellman-Ford é executado a partir de todos os vértices, seu custo pode crescer significativamente, sobretudo em grafos grandes e densos.

## O Experimento

### Objetivo

> A ideia do experimento é comparar, na prática, o desempenho dos algoritmos Floyd-Warshall, Johnson, Dijkstra repetido e Bellman-Ford repetido na tarefa de calcular os menores caminhos entre todos os pares de vértices de grafos
> direcionados e ponderados. Para isso, os quatro algoritmos serão submetidos aos mesmos grafos, com pesos positivos, diferentes quantidades de vértices e diferentes níveis de densidade, permitindo analisar como essas características 
> influenciam o tempo de execução, o uso de memória e a quantidade de operações realizadas. O objetivo não é apenas identificar qual algoritmo é mais rápido, mas compreender em quais tipos de grafo cada abordagem apresenta melhor ou
> pior desempenho e verificar se os resultados práticos correspondem às complexidades teóricas estudadas.

### Entradas

> As entradas do experimento serão grafos direcionados e ponderados, representados por uma quantidade de vértices (V), uma quantidade de arestas (E) e pesos inteiros positivos entre 1 e 100. Os grafos não terão laços nem arestas
> duplicadas e serão gerados com sementes fixas para garantir a reprodução dos testes. Serão usados os mesmos grafos para todos os algoritmos, permitindo uma comparação justa entre Floyd-Warshall, Johnson, Dijkstra repetido e Bellman-
> Ford.

### Carga de Trabalho

> A tarefa submetida aos algoritmos será calcular a matriz de menores distâncias entre todos os pares de vértices do grafo. Serão utilizados grafos de diferentes tamanhos, inicialmente com 10, 30 e 100 vértices, e com três níveis de 
> densidade: esparso, intermediário e denso. Dessa forma, será possível observar como o aumento do número de vértices e da quantidade de arestas influencia o comportamento e o desempenho de cada algoritmo.

### Métricas 

> O experimento medirá o tempo de execução necessário para cada algoritmo calcular todos os menores caminhos, além do pico de memória utilizado e da quantidade de operações internas realizadas. Também serão registrados a média, a 
> mediana, o desvio padrão, o menor e o maior tempo de execução. Antes da análise de desempenho, será verificado se todos os algoritmos produziram a mesma matriz de distâncias, garantindo a correção dos resultados.

### Levantamento

> Para cada combinação de tamanho e densidade, o grafo será gerado antes da medição e fornecido igualmente aos quatro algoritmos. Cada algoritmo realizará três execuções de aquecimento e, em seguida, trinta execuções oficiais. A memória será avaliada separadamente, e as operações internas serão contabilizadas por contadores específicos de cada implementação. Os resultados serão armazenados em arquivos CSV para posterior organização em tabelas, gráficos e análise 
> comparativa.


