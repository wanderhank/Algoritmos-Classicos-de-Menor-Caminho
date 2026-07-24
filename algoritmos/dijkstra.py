from __future__ import annotations

import heapq
from math import inf

from algoritmos.comum import Aresta, MatrizDistancias, validar_grafo


def construir_lista_adjacencia(
    numero_vertices: int, arestas: list
) -> list:
    
    adjacencia = [[] for _ in range(numero_vertices)]
    for u, v, peso in arestas:
        adjacencia[u].append((v, peso))
    return adjacencia


def dijkstra_origem_unica(
    origem: int,
    numero_vertices: int,
    adjacencia: list,
) -> list:

    distancias = [inf] * numero_vertices
    distancias[origem] = 0

    fila = [(0, origem)]
    visitados = [False] * numero_vertices

    while fila:
        distancia_atual, u = heapq.heappop(fila)

        if visitados[u]:
            continue
        visitados[u] = True

        for v, peso in adjacencia[u]:
            nova_distancia = distancia_atual + peso
            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                heapq.heappush(fila, (nova_distancia, v))

    return distancias


def dijkstra(numero_vertices: int, arestas: list) -> MatrizDistancias:
    validar_grafo(numero_vertices, arestas)

    adjacencia = construir_lista_adjacencia(numero_vertices, arestas)

    distancias: MatrizDistancias = [
        dijkstra_origem_unica(origem, numero_vertices, adjacencia)
        for origem in range(numero_vertices)
    ]

    return distancias
