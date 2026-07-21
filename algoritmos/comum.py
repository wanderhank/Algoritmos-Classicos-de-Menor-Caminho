from __future__ import annotations

from math import inf

Aresta = tuple[int, int, int]
MatrizDistancias = list[list[float]]


def validar_grafo(
        numero_vertices: int,
        arestas: list[Aresta],
        *,
        exigir_pesos_positivos: bool = False,
) -> None:
    if numero_vertices <= 0:
        raise ValueError("O número de vértices deve ser positivo.")

    for indice, (u, v, peso) in enumerate(arestas):
        if not 0 <= u < numero_vertices or not 0 <= v < numero_vertices:
            raise ValueError(
                f"Aresta {indice} possui vértice inválido: ({u}, {v}, {peso})."
            )
        if exigir_pesos_positivos and peso <= 0:
            raise ValueError("Este algoritmo exige pesos estritamente positivos.")


def matrizes_iguais(
        a: MatrizDistancias,
        b: MatrizDistancias,
        tolerancia: float = 1e-12,
) -> bool:
    if len(a) != len(b):
        return False

    for linha_a, linha_b in zip(a, b):
        if len(linha_a) != len(linha_b):
            return False

        for valor_a, valor_b in zip(linha_a, linha_b):
            if valor_a == inf and valor_b == inf:
                continue
            if valor_a == inf or valor_b == inf:
                return False
            if abs(valor_a - valor_b) > tolerancia:
                return False

    return True
