se algoritmo?from __future__ import annotations

import heapq
from math import inf

from algoritmos.bellman_ford import _bellman_ford
from algoritmos.comum import Aresta, MatrizDistancias


def johnson(
    numero_vertices: int,
    arestas: list[Aresta],
) -> MatrizDistancias:
    super_origem = numero_vertices
    arestas_estendidas = arestas + [
        (super_origem, vertice, 0) for vertice in range(numero_vertices)
    ]

    potenciais, _ = _bellman_ford(
        numero_vertices + 1,
        arestas_estendidas,
        super_origem,
    )

    adjacencia: list[list[tuple[int, float]]] = [
        [] for _ in range(numero_vertices)
    ]

    for u, v, peso in arestas:
        peso_reponderado = peso + potenciais[u] - potenciais[v]
        if peso_reponderado < -1e-12:
            raise RuntimeError("A reponderação de Johnson produziu peso negativo.")
        adjacencia[u].append((v, peso_reponderado))

    matriz: MatrizDistancias = []

    for origem in range(numero_vertices):
        distancias_reponderadas = [inf] * numero_vertices
        distancias_reponderadas[origem] = 0
        fila: list[tuple[float, int]] = [(0, origem)]

        while fila:
            distancia_atual, u = heapq.heappop(fila)
            if distancia_atual != distancias_reponderadas[u]:
                continue

            for v, peso in adjacencia[u]:
                nova_distancia = distancia_atual + peso
                if nova_distancia < distancias_reponderadas[v]:
                    distancias_reponderadas[v] = nova_distancia
                    heapq.heappush(fila, (nova_distancia, v))

        distancias_originais = [inf] * numero_vertices
        for destino, distancia in enumerate(distancias_reponderadas):
            if distancia != inf:
                distancias_originais[destino] = (
                    distancia - potenciais[origem] + potenciais[destino]
                )

        matriz.append(distancias_originais)

    return matriz
