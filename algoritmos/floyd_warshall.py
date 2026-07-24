from __future__ import annotations

from math import inf

from algoritmos.comum import Aresta, MatrizDistancias, validar_grafo


def floyd_warshall(
    numero_vertices: int,
    arestas: list[Aresta],
) -> MatrizDistancias:
    validar_grafo(numero_vertices, arestas)

    distancias: MatrizDistancias = [
        [inf] * numero_vertices for _ in range(numero_vertices)
    ]

    for i in range(numero_vertices):
        distancias[i][i] = 0

    for u, v, peso in arestas:
        if peso < distancias[u][v]:
            distancias[u][v] = peso

    for k in range(numero_vertices):
        for i in range(numero_vertices):
            distancia_ik = distancias[i][k]
            if distancia_ik == inf:
                continue

            for j in range(numero_vertices):
                distancia_kj = distancias[k][j]
                if distancia_kj == inf:
                    continue

                nova_distancia = distancia_ik + distancia_kj
                if nova_distancia < distancias[i][j]:
                    distancias[i][j] = nova_distancia

    for i in range(numero_vertices):
        if distancias[i][i] < 0:
            raise ValueError("O grafo possui ciclo de peso negativo.")

    return distancias