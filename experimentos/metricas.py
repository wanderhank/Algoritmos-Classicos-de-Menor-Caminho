from __future__ import annotations

import gc
import tracemalloc
from dataclasses import dataclass
from statistics import mean, median, stdev
from time import perf_counter
from typing import Callable

from algoritmos.comum import Aresta, MatrizDistancias

Algoritmo = Callable[[int, list[Aresta]], MatrizDistancias]


@dataclass
class EstatisticasTempo:
    media: float
    desvio_padrao: float
    mediana: float
    minimo: float
    maximo: float


def medir_tempos(
    algoritmo: Algoritmo,
    numero_vertices: int,
    arestas: list[Aresta],
    repeticoes: int = 30,
    aquecimentos: int = 3,
) -> list[float]:
    if repeticoes < 2:
        raise ValueError("Use pelo menos duas repetições.")
    if aquecimentos < 0:
        raise ValueError("O número de aquecimentos não pode ser negativo.")

    for _ in range(aquecimentos):
        algoritmo(numero_vertices, arestas)

    tempos: list[float] = []
    for _ in range(repeticoes):
        gc.collect()
        inicio = perf_counter()
        algoritmo(numero_vertices, arestas)
        tempos.append(perf_counter() - inicio)

    return tempos


def resumir_tempos(tempos: list[float]) -> EstatisticasTempo:
    if len(tempos) < 2:
        raise ValueError("São necessárias ao menos duas medições.")

    return EstatisticasTempo(
        media=mean(tempos),
        desvio_padrao=stdev(tempos),
        mediana=median(tempos),
        minimo=min(tempos),
        maximo=max(tempos),
    )


def medir_memoria_pico(
    algoritmo: Algoritmo,
    numero_vertices: int,
    arestas: list[Aresta],
) -> int:
    gc.collect()
    tracemalloc.start()
    try:
        algoritmo(numero_vertices, arestas)
        _, pico = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()

    return pico
