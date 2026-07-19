# Algoritmos Clássicos de Menor Caminho

## Grafos
> Grafos são estruturas matemáticas utilizadas para representar relações entre diferentes elementos. Eles são formados por vértices, que representam os pontos ou entidades do problema, e por arestas, que representam as conexões
> existentes entre esses vértices. Dependendo da situação analisada, as arestas podem possuir direção, peso ou outras propriedades. 

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

> Os grafos são estruturas matemáticas utilizadas para representar relações entre diferentes elementos. Eles são formados por vértices, que representam os pontos ou entidades do problema, e por arestas, que representam as conexões existentes 
> entre esses vértices. Dependendo da situação analisada, as arestas podem possuir direção, peso ou outras propriedades. Em um grafo direcionado, cada aresta possui um sentido definido, de modo que uma conexão de um vértice (u) para um 
> vértice (v) não implica necessariamente a existência do caminho inverso. Em um grafo ponderado, cada aresta recebe um valor numérico que pode representar distância, custo, tempo, consumo de recursos ou qualquer outra medida relevante.
> Também é possível classificar os grafos de acordo com a quantidade de conexões: grafos esparsos possuem poucas arestas em relação ao total possível, enquanto grafos densos apresentam um número elevado de conexões. No experimento proposto,
> serão utilizados grafos direcionados, ponderados, simples e fortemente conectados, com pesos positivos, sem laços e sem arestas duplicadas. Essa escolha permite representar diferentes cenários de redes e, ao mesmo tempo, garantir que 
> exista pelo menos um caminho entre todos os pares de vértices, tornando possível comparar os algoritmos de forma uniforme.

### Algoritmo de Floyd-Warshall
### Algoritmo de Dijkstra
### Algoritmo de Johnson
### Algoritmo de Bellman-Ford

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

> Para cada combinação de tamanho e densidade, o grafo será gerado antes da medição e fornecido igualmente aos quatro algoritmos. Cada algoritmo realizará três execuções de aquecimento e, em seguida, trinta execuções oficiais. A memória > será avaliada separadamente, e as operações internas serão contabilizadas por contadores específicos de cada implementação. Os resultados serão armazenados em arquivos CSV para posterior organização em tabelas, gráficos e análise 
> comparativa.


