# Algoritmos Clássicos de Menor Caminho

## Grafos

## Algoritmos de Menor Caminho

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


