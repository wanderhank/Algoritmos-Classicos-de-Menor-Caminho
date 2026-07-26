from __future__ import annotations

from math import inf
from typing import Optional

from algoritmos.comum import Aresta, MatrizDistancias


def _bellman_ford(
    numero_vertices: int,
    arestas: list[Aresta],
    origem: int,
) -> tuple[list[float], list[Optional[int]]]:
    """Implementação central do Bellman-Ford para uma origem."""
    distancias = [inf] * numero_vertices
    predecessores: list[Optional[int]] = [None] * numero_vertices
    distancias[origem] = 0

    for _ in range(numero_vertices - 1):
        houve_atualizacao = False

        for u, v, peso in arestas:
            if distancias[u] == inf:
                continue

            nova_distancia = distancias[u] + peso
            if nova_distancia < distancias[v]:
                distancias[v] = nova_distancia
                predecessores[v] = u
                houve_atualizacao = True

        if not houve_atualizacao:
            break

    for u, v, peso in arestas:
        if distancias[u] != inf and distancias[u] + peso < distancias[v]:
            raise ValueError("O grafo possui ciclo de peso negativo.")

    return distancias, predecessores


def bellman_ford(
    numero_vertices: int,
    arestas: list[Aresta],
    origem: int,
) -> tuple[list[float], list[Optional[int]]]:
    """Calcula as menores distâncias a partir de uma origem."""
    if not 0 <= origem < numero_vertices:
        raise ValueError("A origem informada é inválida.")

    return _bellman_ford(numero_vertices, arestas, origem)


def reconstruir_caminho(
    predecessores: list[Optional[int]],
    origem: int,
    destino: int,
) -> list[int]:
    if not 0 <= origem < len(predecessores) or not 0 <= destino < len(predecessores):
        raise ValueError("Origem ou destino inválido para reconstrução.")

    caminho: list[int] = []
    atual: Optional[int] = destino

    while atual is not None:
        caminho.append(atual)
        if atual == origem:
            caminho.reverse()
            return caminho
        atual = predecessores[atual]

    return []


def bellman_ford_todos_os_pares(
    numero_vertices: int,
    arestas: list[Aresta],
) -> MatrizDistancias:
    """Executa Bellman-Ford uma vez para cada vértice de origem."""
    matriz: MatrizDistancias = []

    for origem in range(numero_vertices):
        distancias, _ = _bellman_ford(numero_vertices, arestas, origem)
        matriz.append(distancias)

    return matriz

