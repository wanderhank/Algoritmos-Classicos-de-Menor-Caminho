#Algoritmo de Floyd-Warshall - menor caminho entre todos os pares de vertices.


def calcular(grafo):

    n = len(grafo)
    dist = [linha[:] for linha in grafo]

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]

    return dist
