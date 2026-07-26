from __future__ import annotations

import unittest
from math import inf

from algoritmos import ALGORITMOS
from algoritmos.bellman_ford import bellman_ford, reconstruir_caminho
from algoritmos.comum import matrizes_iguais, validar_grafo
from algoritmos.floyd_warshall import floyd_warshall
from experimentos.gerador_grafos import configuracoes_de_carga, gerar_grafo_direcionado


class TestAlgoritmosMesmosCasos(unittest.TestCase):
    def verificar_todos(self, vertices, arestas, esperado) -> None:
        for nome, algoritmo in ALGORITMOS.items():
            with self.subTest(algoritmo=nome):
                matriz = algoritmo(vertices, arestas)
                self.assertTrue(matrizes_iguais(matriz, esperado))

    def test_grafo_positivo(self) -> None:
        arestas = [(0, 1, 4), (0, 2, 10), (1, 2, 3), (1, 3, 8), (2, 3, 2)]
        esperado = [
            [0, 4, 7, 9],
            [inf, 0, 3, 5],
            [inf, inf, 0, 2],
            [inf, inf, inf, 0],
        ]
        self.verificar_todos(4, arestas, esperado)

    def test_vertice_inalcancavel(self) -> None:
        arestas = [(0, 1, 2), (1, 2, 3)]
        esperado = [
            [0, 2, 5, inf],
            [inf, 0, 3, inf],
            [inf, inf, 0, inf],
            [inf, inf, inf, 0],
        ]
        self.verificar_todos(4, arestas, esperado)

    def test_todos_os_pares(self) -> None:
        arestas = [(0, 1, 2), (0, 2, 8), (1, 2, 3), (2, 0, 4)]
        esperado = [[0, 2, 5], [7, 0, 3], [4, 6, 0]]
        self.verificar_todos(3, arestas, esperado)

    def test_grafo_com_um_vertice(self) -> None:
        self.verificar_todos(1, [], [[0]])

    def test_grafo_sem_arestas(self) -> None:
        esperado = [
            [0, inf, inf, inf],
            [inf, 0, inf, inf],
            [inf, inf, 0, inf],
            [inf, inf, inf, 0],
        ]
        self.verificar_todos(4, [], esperado)

    def test_multiplos_caminhos_mesmo_custo(self) -> None:
        arestas = [(0, 1, 2), (0, 2, 2), (1, 3, 3), (2, 3, 3)]
        referencia = floyd_warshall(4, arestas)
        self.verificar_todos(4, arestas, referencia)

        distancias, predecessores = bellman_ford(4, arestas, 0)
        self.assertEqual(distancias[3], 5)
        self.assertIn(
            reconstruir_caminho(predecessores, 0, 3),
            ([0, 1, 3], [0, 2, 3]),
        )

    def test_grafo_direcionado(self) -> None:
        arestas = [(0, 1, 5)]
        self.verificar_todos(2, arestas, [[0, 5], [inf, 0]])

    def test_entradas_invalidas(self) -> None:
        with self.assertRaises(ValueError):
            validar_grafo(2, [(0, 3, 5)])

        with self.assertRaises(ValueError):
            validar_grafo(2, [(0, 1, 0)], exigir_pesos_positivos=True)

        with self.assertRaises(ValueError):
            gerar_grafo_direcionado(5, 10, peso_minimo=0)

    def test_gerador(self) -> None:
        grafo = gerar_grafo_direcionado(10, 30, semente=123)
        self.assertEqual(len(grafo), 30)
        self.assertTrue(all(u != v for u, v, _ in grafo))
        self.assertTrue(all(1 <= peso <= 100 for _, _, peso in grafo))
        self.assertEqual(len({(u, v) for u, v, _ in grafo}), 30)

        referencia = floyd_warshall(10, grafo)
        self.assertTrue(all(distancia != inf for linha in referencia for distancia in linha))
        self.verificar_todos(10, grafo, referencia)

    def test_reprodutibilidade_da_semente(self) -> None:
        self.assertEqual(
            gerar_grafo_direcionado(10, 30, semente=999),
            gerar_grafo_direcionado(10, 30, semente=999),
        )
        self.assertNotEqual(
            gerar_grafo_direcionado(10, 30, semente=999),
            gerar_grafo_direcionado(10, 30, semente=1000),
        )

    def test_configuracoes_de_carga_ordenadas(self) -> None:
        configuracoes = configuracoes_de_carga([10, 30])

        for i in range(0, len(configuracoes), 3):
            _, esparso, _ = configuracoes[i]
            _, intermediario, _ = configuracoes[i + 1]
            _, denso, _ = configuracoes[i + 2]
            self.assertLess(esparso, intermediario)
            self.assertLess(intermediario, denso)


if __name__ == "__main__":
    unittest.main(verbosity=2)
