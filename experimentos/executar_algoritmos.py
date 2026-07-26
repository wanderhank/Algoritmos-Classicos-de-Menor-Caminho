from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path

from algoritmos import ALGORITMOS
from algoritmos.comum import matrizes_iguais, validar_grafo
from algoritmos.floyd_warshall import floyd_warshall
from experimentos.gerador_grafos import configuracoes_de_carga, gerar_grafo_direcionado
from experimentos.metricas import medir_memoria_pico, medir_tempos, resumir_tempos


@dataclass
class ResultadoResumo:
    algoritmo: str
    vertices: int
    arestas: int
    densidade: str
    semente: int
    repeticoes: int
    media_segundos: float
    desvio_padrao_segundos: float
    mediana_segundos: float
    minimo_segundos: float
    maximo_segundos: float
    memoria_pico_bytes: int


def executar_uma_configuracao(
    nome: str,
    algoritmo,
    vertices: int,
    grafo,
    quantidade_arestas: int,
    densidade: str,
    semente: int,
    repeticoes: int,
    aquecimentos: int,
) -> tuple[ResultadoResumo, list[float]]:
    tempos = medir_tempos(
        algoritmo,
        vertices,
        grafo,
        repeticoes,
        aquecimentos,
    )
    estatisticas = resumir_tempos(tempos)
    memoria = medir_memoria_pico(algoritmo, vertices, grafo)

    return ResultadoResumo(
        algoritmo=nome,
        vertices=vertices,
        arestas=quantidade_arestas,
        densidade=densidade,
        semente=semente,
        repeticoes=repeticoes,
        media_segundos=estatisticas.media,
        desvio_padrao_segundos=estatisticas.desvio_padrao,
        mediana_segundos=estatisticas.mediana,
        minimo_segundos=estatisticas.minimo,
        maximo_segundos=estatisticas.maximo,
        memoria_pico_bytes=memoria,
    ), tempos


def salvar_csv(caminho: Path, campos: list[str], linhas: list[dict]) -> None:
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with caminho.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(linhas)


def executar_experimentos(
    tamanhos: list[int],
    repeticoes: int = 30,
    aquecimentos: int = 3,
    semente_base: int = 42,
    diretorio_saida: str = "resultados",
) -> None:
    resumos: list[ResultadoResumo] = []
    brutos: list[dict] = []

    configuracoes = configuracoes_de_carga(tamanhos)

    for indice, (vertices, quantidade_arestas, densidade) in enumerate(configuracoes):
        semente = semente_base + indice
        grafo = gerar_grafo_direcionado(
            vertices,
            quantidade_arestas,
            peso_minimo=1,
            peso_maximo=100,
            semente=semente,
            garantir_fortemente_conectado=True,
        )

        # A entrada é validada uma única vez e fora da região cronometrada.
        validar_grafo(vertices, grafo, exigir_pesos_positivos=True)
        referencia = floyd_warshall(vertices, grafo)

        for nome, algoritmo in ALGORITMOS.items():
            matriz = algoritmo(vertices, grafo)
            if not matrizes_iguais(matriz, referencia):
                raise AssertionError(
                    f"{nome} produziu uma matriz diferente da referência."
                )

            resumo, tempos = executar_uma_configuracao(
                nome,
                algoritmo,
                vertices,
                grafo,
                quantidade_arestas,
                densidade,
                semente,
                repeticoes,
                aquecimentos,
            )
            resumos.append(resumo)

            for repeticao, tempo in enumerate(tempos, 1):
                brutos.append(
                    {
                        "algoritmo": nome,
                        "vertices": vertices,
                        "arestas": quantidade_arestas,
                        "densidade": densidade,
                        "semente": semente,
                        "repeticao": repeticao,
                        "tempo_segundos": tempo,
                    }
                )

            print(
                f"{nome:23s} | V={vertices:4d} | E={quantidade_arestas:7d} | "
                f"{densidade:13s} | média={resumo.media_segundos:.6f}s"
            )

    pasta = Path(diretorio_saida)
    salvar_csv(
        pasta / "algoritmos_resumo.csv",
        list(ResultadoResumo.__dataclass_fields__.keys()),
        [asdict(resultado) for resultado in resumos],
    )
    salvar_csv(
        pasta / "algoritmos_tempos_brutos.csv",
        [
            "algoritmo",
            "vertices",
            "arestas",
            "densidade",
            "semente",
            "repeticao",
            "tempo_segundos",
        ],
        brutos,
    )

    print(f"\nResultados salvos em: {pasta.resolve()}")
