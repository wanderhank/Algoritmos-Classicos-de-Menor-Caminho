from __future__ import annotations

import heapq
from math import inf

from algoritmos.comum import Aresta, MatrizDistancias


def criar_lista_adjacencia(
    numero_vertices: int,
    arestas: list[Aresta],
) -> list[list[tuple[int, int]]]:
    adjacencia: list[list[tuple[int, int]]] = [[] for _ in range(numero_vertices)]

    for u, v, peso in arestas:
        adjacencia[u].append((v, peso))

    return adjacencia


def dijkstra(
    numero_vertices: int,
    adjacencia: list[list[tuple[int, int]]],
    origem: int,
) -> list[float]:
    if not 0 <= origem < numero_vertices:
        raise ValueError("A origem informada é inválida.")

    distancias = [inf] * numero_vertices
    distancias[origem] = 0
    fila: list[tuple[float, int]] = [(0, origem)]

    while fila:
        distancia_atual, u = heapq.heappop(fila)
        if distancia_atual != distancias[u]:
            continue

        for v, peso in adjacencia[u]:
            nova_distancia = distancia_atual + peso
            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                heapq.heappush(fila, (nova_distancia, v))

    return distancias


def dijkstra_todos_os_pares(
    numero_vertices: int,
    arestas: list[Aresta],
) -> MatrizDistancias:
    adjacencia = criar_lista_adjacencia(numero_vertices, arestas)
    return [
        dijkstra(numero_vertices, adjacencia, origem)
        for origem in range(numero_vertices)
    ]
