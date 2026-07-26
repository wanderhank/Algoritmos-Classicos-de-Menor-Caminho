from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from algoritmos import ALGORITMOS
from algoritmos.comum import matrizes_iguais, validar_grafo
from algoritmos.floyd_warshall import floyd_warshall
from experimentos.gerador_grafos import (
    configuracoes_de_carga,
    gerar_grafo_direcionado,
)
from experimentos.metricas import (
    medir_memoria_pico,
    medir_tempos,
    resumir_tempos,
)


@dataclass
class ResultadoResumo:
    algoritmo: str
    vertices: int
    arestas: int
    densidade: str
    semente: int
    repeticoes: int
    media_ms: float
    desvio_padrao_ms: float
    mediana_ms: float
    minimo_ms: float
    maximo_ms: float
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
    """
    Executa um algoritmo para uma configuração específica.

    Os tempos são medidos internamente em segundos e convertidos
    para milissegundos antes do cálculo das estatísticas.
    """

    tempos_segundos = medir_tempos(
        algoritmo,
        vertices,
        grafo,
        repeticoes,
        aquecimentos,
    )

    tempos_ms = [
        tempo * 1000
        for tempo in tempos_segundos
    ]

    estatisticas = resumir_tempos(tempos_ms)

    # A memória é medida separadamente para evitar interferência
    # do tracemalloc nas medições de tempo.
    memoria = medir_memoria_pico(
        algoritmo,
        vertices,
        grafo,
    )

    resumo = ResultadoResumo(
        algoritmo=nome,
        vertices=vertices,
        arestas=quantidade_arestas,
        densidade=densidade,
        semente=semente,
        repeticoes=repeticoes,
        media_ms=estatisticas.media,
        desvio_padrao_ms=estatisticas.desvio_padrao,
        mediana_ms=estatisticas.mediana,
        minimo_ms=estatisticas.minimo,
        maximo_ms=estatisticas.maximo,
        memoria_pico_bytes=memoria,
    )

    return resumo, tempos_ms


def formatar_valor_csv(valor: Any) -> Any:
    """
    Formata valores de ponto flutuante com vírgula decimal.

    Exemplo:
        0.058472 -> 0,058472
    """

    if isinstance(valor, float):
        return f"{valor:.6f}".replace(".", ",")

    return valor


def formatar_linha_csv(
        linha: dict[str, Any],
) -> dict[str, Any]:
    """
    Aplica a formatação pt-BR aos valores da linha.
    """

    return {
        campo: formatar_valor_csv(valor)
        for campo, valor in linha.items()
    }


def salvar_csv(
        caminho: Path,
        campos: list[str],
        linhas: list[dict[str, Any]],
) -> None:
    """
    Salva o CSV usando:

    - ponto e vírgula como delimitador;
    - vírgula como separador decimal;
    - UTF-8 com BOM, para melhorar a compatibilidade com Excel.
    """

    caminho.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with caminho.open(
            "w",
            newline="",
            encoding="utf-8-sig",
    ) as arquivo:
        escritor = csv.DictWriter(
            arquivo,
            fieldnames=campos,
            delimiter=";",
        )

        escritor.writeheader()

        escritor.writerows(
            formatar_linha_csv(linha)
            for linha in linhas
        )


def executar_experimentos(
        tamanhos: list[int],
        repeticoes: int = 30,
        aquecimentos: int = 3,
        semente_base: int = 42,
        diretorio_saida: str = "resultados",
) -> None:
    """
    Executa o experimento comparativo dos algoritmos.

    Para cada combinação de tamanho e densidade:

    1. gera o grafo;
    2. valida a entrada uma única vez;
    3. calcula a matriz de referência;
    4. verifica a correção de cada algoritmo;
    5. mede tempo e memória;
    6. salva resultados resumidos e brutos em CSV.
    """

    resumos: list[ResultadoResumo] = []
    brutos: list[dict[str, Any]] = []

    configuracoes = configuracoes_de_carga(tamanhos)

    for indice, (
            vertices,
            quantidade_arestas,
            densidade,
    ) in enumerate(configuracoes):
        semente = semente_base + indice

        # O grafo é gerado fora da região cronometrada.
        grafo = gerar_grafo_direcionado(
            vertices,
            quantidade_arestas,
            peso_minimo=1,
            peso_maximo=100,
            semente=semente,
            garantir_fortemente_conectado=True,
        )

        # A entrada é validada uma única vez e fora da medição.
        validar_grafo(
            vertices,
            grafo,
            exigir_pesos_positivos=True,
        )

        # Floyd-Warshall é usado como referência de correção.
        referencia = floyd_warshall(
            vertices,
            grafo,
        )

        for nome, algoritmo in ALGORITMOS.items():
            # Verifica se o algoritmo produz a matriz correta.
            matriz = algoritmo(
                vertices,
                grafo,
            )

            if not matrizes_iguais(
                    matriz,
                    referencia,
            ):
                raise AssertionError(
                    f"{nome} produziu uma matriz diferente da referência."
                )

            resumo, tempos_ms = executar_uma_configuracao(
                nome=nome,
                algoritmo=algoritmo,
                vertices=vertices,
                grafo=grafo,
                quantidade_arestas=quantidade_arestas,
                densidade=densidade,
                semente=semente,
                repeticoes=repeticoes,
                aquecimentos=aquecimentos,
            )

            resumos.append(resumo)

            for repeticao, tempo_ms in enumerate(
                    tempos_ms,
                    start=1,
            ):
                brutos.append(
                    {
                        "algoritmo": nome,
                        "vertices": vertices,
                        "arestas": quantidade_arestas,
                        "densidade": densidade,
                        "semente": semente,
                        "repeticao": repeticao,
                        "tempo_ms": tempo_ms,
                    }
                )

            print(
                f"{nome:23s} | "
                f"V={vertices:4d} | "
                f"E={quantidade_arestas:7d} | "
                f"{densidade:13s} | "
                f"média={resumo.media_ms:.6f} ms"
            )

    pasta = Path(diretorio_saida)

    salvar_csv(
        caminho=pasta / "algoritmos_resumo.csv",
        campos=list(
            ResultadoResumo.__dataclass_fields__.keys()
        ),
        linhas=[
            asdict(resultado)
            for resultado in resumos
        ],
    )

    salvar_csv(
        caminho=pasta / "algoritmos_tempos_brutos.csv",
        campos=[
            "algoritmo",
            "vertices",
            "arestas",
            "densidade",
            "semente",
            "repeticao",
            "tempo_ms",
        ],
        linhas=brutos,
    )

    print(
        f"\nResultados salvos em: "
        f"{pasta.resolve()}"
    )
