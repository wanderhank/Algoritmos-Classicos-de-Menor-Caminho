from __future__ import annotations

import argparse
import unittest

from algoritmos import ALGORITMOS
from experimentos.executar_algoritmos import executar_experimentos


def executar_testes() -> bool:
    suite = unittest.defaultTestLoader.discover("testes")
    resultado = unittest.TextTestRunner(verbosity=2).run(suite)
    return resultado.wasSuccessful()


def criar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Testes e experimento de algoritmos de menor caminho."
    )
    parser.add_argument("--somente-testes", action="store_true")
    parser.add_argument("--pular-testes", action="store_true")
    parser.add_argument(
        "--algoritmo",
        choices=["todos", *ALGORITMOS.keys()],
        default="todos",
        help="Algoritmo que será executado no experimento.",
    )
    parser.add_argument("--tamanhos", nargs="+", type=int, default=[30, 60, 100, 150])
    parser.add_argument("--repeticoes", type=int, default=30)
    parser.add_argument("--aquecimentos", type=int, default=3)
    parser.add_argument("--saida", default="resultados")
    return parser


def main() -> None:
    args = criar_parser().parse_args()

    if not args.pular_testes and not executar_testes():
        raise SystemExit(1)

    if not args.somente_testes:
        executar_experimentos(
            tamanhos=args.tamanhos,
            repeticoes=args.repeticoes,
            aquecimentos=args.aquecimentos,
            diretorio_saida=args.saida,
            algoritmo_selecionado=args.algoritmo,
        )


if __name__ == "__main__":
    main()
