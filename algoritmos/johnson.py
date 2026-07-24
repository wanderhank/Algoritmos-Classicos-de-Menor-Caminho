from __future__ import annotations

from math import inf

from algoritmos.comum import Aresta, MatrizDistancias, validar_grafo
from algoritmos.dijkstra import construir_lista_adjacencia, dijkstra_origem_unica


def _bellman_ford_origem_unica(
    origem: int,
    numero_vertices: int,
    arestas: list,
) -> list:
    distancias = [inf] * numero_vertices
    distancias[origem] = 0

    for _ in range(numero_vertices - 1):
        houve_atualizacao = False
        for u, v, peso in arestas:
            if distancias[u] == inf:
                continue
            nova_distancia = distancias[u] + peso
            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                houve_atualizacao = True
        if not houve_atualizacao:
            break

    for u, v, peso in arestas:
        if distancias[u] != inf and distancias[u] + peso < distancias[v]:
            raise ValueError("O grafo possui ciclo de peso negativo.")

    return distancias


def johnson(numero_vertices: int, arestas: list) -> MatrizDistancias:
    validar_grafo(numero_vertices, arestas)

    # 1. vertice virtual, conectado a todos com peso 0
    vertice_virtual = numero_vertices
    arestas_aumentadas = list(arestas) + [
        (vertice_virtual, v, 0) for v in range(numero_vertices)
    ]

    # 2. Bellman-Ford a partir do vertice virtual
    h = _bellman_ford_origem_unica(
        vertice_virtual, numero_vertices + 1, arestas_aumentadas
    )

    # 3. reponderacao das arestas originais
    arestas_repesadas = [
        (u, v, peso + h[u] - h[v]) for u, v, peso in arestas
    ]

    # 4. Dijkstra a partir de cada vertice, no grafo reponderado
    adjacencia = construir_lista_adjacencia(numero_vertices, arestas_repesadas)

    distancias: MatrizDistancias = []
    for origem in range(numero_vertices):
        distancias_reponderadas = dijkstra_origem_unica(origem, numero_vertices, adjacencia)

        # 5. desfaz a reponderacao
        distancias_origem = [
            (distancias_reponderadas[destino] - h[origem] + h[destino])
            if distancias_reponderadas[destino] != inf else inf
            for destino in range(numero_vertices)
        ]
        distancias.append(distancias_origem)

    return distancias
