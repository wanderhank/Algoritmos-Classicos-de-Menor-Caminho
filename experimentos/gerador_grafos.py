from __future__ import annotations

import random

from algoritmos.comum import Aresta


def gerar_grafo_direcionado(
        numero_vertices: int,
        numero_arestas: int,
        peso_minimo: int = 1,
        peso_maximo: int = 100,
        semente: int = 42,
        garantir_fortemente_conectado: bool = True,
) -> list[Aresta]:
    if numero_vertices <= 0:
        raise ValueError("O número de vértices deve ser positivo.")
    if peso_minimo <= 0 or peso_maximo < peso_minimo:
        raise ValueError("Os pesos devem ser positivos e formar um intervalo válido.")

    maximo = numero_vertices * (numero_vertices - 1)
    minimo = numero_vertices if numero_vertices > 1 and garantir_fortemente_conectado else 0
    if not minimo <= numero_arestas <= maximo:
        raise ValueError(f"A quantidade de arestas deve estar entre {minimo} e {maximo}.")

    rng = random.Random(semente)
    pares: set[tuple[int, int]] = set()
    arestas: list[Aresta] = []

    if garantir_fortemente_conectado and numero_vertices > 1:
        # Ciclo dirigido garante caminho entre todos os pares.
        ordem = list(range(numero_vertices))
        rng.shuffle(ordem)
        for i, u in enumerate(ordem):
            v = ordem[(i + 1) % numero_vertices]
            pares.add((u, v))
            arestas.append((u, v, rng.randint(peso_minimo, peso_maximo)))

    while len(arestas) < numero_arestas:
        u = rng.randrange(numero_vertices)
        v = rng.randrange(numero_vertices)
        if u == v or (u, v) in pares:
            continue
        pares.add((u, v))
        arestas.append((u, v, rng.randint(peso_minimo, peso_maximo)))

    return arestas


def configuracoes_de_carga(tamanhos: list[int]) -> list[tuple[int, int, str]]:
    configuracoes: list[tuple[int, int, str]] = []
    for vertices in tamanhos:
        if vertices < 2:
            raise ValueError("As cargas experimentais exigem pelo menos 2 vértices.")
        maximo = vertices * (vertices - 1)
        esparso = min(maximo, max(vertices, 2 * vertices))
        intermediario = min(maximo, max(esparso + 1, round(maximo * 0.20)))
        denso = min(maximo, max(intermediario + 1, round(maximo * 0.50)))
        configuracoes.extend(
            [
                (vertices, esparso, "esparso"),
                (vertices, intermediario, "intermediario"),
                (vertices, denso, "denso"),
            ]
        )
    return configuracoes