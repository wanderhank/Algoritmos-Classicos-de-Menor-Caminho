const CSV_URLS = [
  './resultados/bellman_ford_resumo.csv',
  './resultados/dijkstra_resumo.csv',
  './resultados/floyd_warshall_resumo.csv',
  './resultados/johnson_resumo.csv'
];
const INTERVALO_ATUALIZACAO_MS = 5000;

const elementoTempo = document.getElementById('grafico-tempo');
const elementoMemoria = document.getElementById('grafico-memoria');
const elementoStatus = document.getElementById('status');
const filtroDensidade = document.getElementById('filtro-densidade');
const botaoAtualizar = document.getElementById('botao-atualizar');

const graficoTempo = echarts.init(elementoTempo);
const graficoMemoria = echarts.init(elementoMemoria);

const COLUNAS_NUMERICAS = new Set([
  'vertices',
  'arestas',
  'semente',
  'repeticoes',
  'media_ms',
  'desvio_padrao_ms',
  'mediana_ms',
  'minimo_ms',
  'maximo_ms',
  'memoria_pico_bytes'
]);

let dadosAtuais = [];
let ultimoConteudoCsv = '';
let carregamentoEmAndamento = false;

function converterCsv(texto) {
  const linhas = texto
      .replace(/^\uFEFF/, '')
      .trim()
      .split(/\r?\n/)
      .filter((linha) => linha.trim() !== '');

  if (linhas.length < 2) {
    throw new Error('O CSV está vazio ou não possui resultados.');
  }

  const cabecalhos = linhas[0]
      .split(';')
      .map((cabecalho) => cabecalho.trim());

  return linhas
      .slice(1)
      .map((linha) => {
        const valores = linha.split(';');
        const registro = {};

        cabecalhos.forEach((cabecalho, indice) => {
          const valorOriginal = (valores[indice] ?? '').trim();

          if (COLUNAS_NUMERICAS.has(cabecalho)) {
            registro[cabecalho] = Number(valorOriginal.replace(',', '.'));
          } else {
            registro[cabecalho] = valorOriginal;
          }
        });

        return registro;
      })
      .filter((registro) =>
          registro.algoritmo &&
          registro.densidade &&
          Number.isFinite(registro.vertices) &&
          Number.isFinite(registro.arestas) &&
          Number.isFinite(registro.media_ms) &&
          Number.isFinite(registro.memoria_pico_bytes)
      );
}

function escaparHtml(valor) {
  return String(valor)
      .replaceAll('&', '&amp;')
      .replaceAll('<', '&lt;')
      .replaceAll('>', '&gt;')
      .replaceAll('"', '&quot;')
      .replaceAll("'", '&#039;');
}

function formatarNumero(valor, casas = 2) {
  return Number(valor).toLocaleString('pt-BR', {
    minimumFractionDigits: casas,
    maximumFractionDigits: casas
  });
}

function formatarInteiro(valor) {
  return Number(valor).toLocaleString('pt-BR', {
    maximumFractionDigits: 0
  });
}

function formatarBytes(bytes) {
  const valor = Number(bytes);

  if (!Number.isFinite(valor)) return '-';
  if (valor < 1024) return `${formatarInteiro(valor)} B`;
  if (valor < 1024 ** 2) return `${formatarNumero(valor / 1024)} KB`;
  return `${formatarNumero(valor / 1024 ** 2)} MB`;
}

function calcularDensidadePercentual(registro) {
  const maximoArestas = registro.vertices * (registro.vertices - 1);

  if (maximoArestas <= 0) return 0;
  return (registro.arestas / maximoArestas) * 100;
}

function ordenarDados(dados) {
  return [...dados].sort((a, b) => {
    if (a.vertices !== b.vertices) return a.vertices - b.vertices;
    return a.algoritmo.localeCompare(b.algoritmo, 'pt-BR');
  });
}

function obterDensidades(dados) {
  const ordemPreferencial = ['esparso', 'intermediario', 'denso'];
  const densidades = [...new Set(dados.map((item) => item.densidade))];

  return densidades.sort((a, b) => {
    const indiceA = ordemPreferencial.indexOf(a);
    const indiceB = ordemPreferencial.indexOf(b);

    if (indiceA === -1 && indiceB === -1) return a.localeCompare(b, 'pt-BR');
    if (indiceA === -1) return 1;
    if (indiceB === -1) return -1;
    return indiceA - indiceB;
  });
}

function rotuloDensidade(densidade) {
  const rotulos = {
    esparso: 'Esparso',
    intermediario: 'Intermediário',
    denso: 'Denso'
  };

  return rotulos[densidade] ?? densidade;
}

function atualizarOpcoesDensidade(dados) {
  const selecaoAnterior = filtroDensidade.value;
  const densidades = obterDensidades(dados);

  filtroDensidade.innerHTML = '';

  densidades.forEach((densidade) => {
    const opcao = document.createElement('option');
    opcao.value = densidade;
    opcao.textContent = rotuloDensidade(densidade);
    filtroDensidade.appendChild(opcao);
  });

  if (densidades.includes(selecaoAnterior)) {
    filtroDensidade.value = selecaoAnterior;
  } else if (densidades.includes('esparso')) {
    filtroDensidade.value = 'esparso';
  } else {
    filtroDensidade.value = densidades[0] ?? '';
  }
}

function obterDadosFiltrados() {
  const densidadeSelecionada = filtroDensidade.value;

  return ordenarDados(
      dadosAtuais.filter(
          (registro) => registro.densidade === densidadeSelecionada
      )
  );
}

function criarDatasets(dados) {
  const algoritmos = [
    ...new Set(dados.map((registro) => registro.algoritmo))
  ].sort((a, b) => a.localeCompare(b, 'pt-BR'));

  const datasets = [
    {
      id: 'dataset_bruto',
      source: dados
    }
  ];

  algoritmos.forEach((algoritmo, indice) => {
    datasets.push({
      id: `dataset_algoritmo_${indice}`,
      fromDatasetId: 'dataset_bruto',
      transform: {
        type: 'filter',
        config: {
          dimension: 'algoritmo',
          '=': algoritmo
        }
      }
    });
  });

  return { algoritmos, datasets };
}

function obterRegistroParametro(parametro) {
  return parametro?.data ?? parametro?.value ?? {};
}

function criarCabecalhoTooltip(registro) {
  return `
    <strong>${formatarInteiro(registro.vertices)} vértices</strong><br>
    Arestas: ${formatarInteiro(registro.arestas)}<br>
    Cenário: ${escaparHtml(rotuloDensidade(registro.densidade))}<br>
    Densidade calculada: ${formatarNumero(calcularDensidadePercentual(registro), 2)}%
    <hr style="margin: 7px 0">
  `;
}

function criarTooltipTempo(parametros) {
  const itens = Array.isArray(parametros) ? parametros : [parametros];
  if (!itens.length) return '';

  let html = criarCabecalhoTooltip(obterRegistroParametro(itens[0]));

  itens.forEach((item) => {
    const registro = obterRegistroParametro(item);

    html += `
      ${item.marker}<strong>${escaparHtml(item.seriesName)}</strong><br>
      <span style="margin-left:18px">Média: ${formatarNumero(registro.media_ms, 4)} ms</span><br>
      <span style="margin-left:18px">Mediana: ${formatarNumero(registro.mediana_ms, 4)} ms</span><br>
      <span style="margin-left:18px">Desvio padrão: ${formatarNumero(registro.desvio_padrao_ms, 4)} ms</span><br>
    `;
  });

  return html;
}

function criarTooltipMemoria(parametros) {
  const itens = Array.isArray(parametros) ? parametros : [parametros];
  if (!itens.length) return '';

  let html = criarCabecalhoTooltip(obterRegistroParametro(itens[0]));

  itens.forEach((item) => {
    const registro = obterRegistroParametro(item);

    html += `
      ${item.marker}<strong>${escaparHtml(item.seriesName)}</strong>:
      ${formatarBytes(registro.memoria_pico_bytes)}<br>
    `;
  });

  return html;
}

function criarSeries(algoritmos, campoY) {
  return algoritmos.map((algoritmo, indice) => ({
    name: algoritmo,
    type: 'line',
    datasetId: `dataset_algoritmo_${indice}`,
    showSymbol: true,
    symbol: 'circle',
    symbolSize: 7,
    connectNulls: false,
    emphasis: { focus: 'series' },
    encode: {
      x: 'vertices',
      y: campoY,
      itemName: 'algoritmo',
      tooltip: ['vertices', 'arestas', 'densidade', campoY]
    }
  }));
}

function criarOpcaoBase(titulo, subtitulo, dados, campoY, nomeEixoY, tooltipFormatter, formatadorEixoY) {
  const { algoritmos, datasets } = criarDatasets(dados);
  const densidade = rotuloDensidade(filtroDensidade.value);

  return {
    dataset: datasets,
    animationDuration: 500,

    title: {
      text: titulo,
      subtext: `${subtitulo} — cenário ${densidade}`,
      left: 'center'
    },

    legend: {
      type: 'scroll',
      top: 58
    },

    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      formatter: tooltipFormatter
    },

    grid: {
      top: 115,
      left: 95,
      right: 45,
      bottom: 88
    },

    xAxis: {
      type: 'value',
      name: 'Quantidade de vértices (V)',
      nameLocation: 'middle',
      nameGap: 45,
      min: 0,
      minInterval: 1,
      axisLabel: { formatter: formatarInteiro }
    },

    yAxis: {
      type: 'value',
      name: nomeEixoY,
      nameLocation: 'middle',
      nameGap: 72,
      min: 0,
      axisLabel: { formatter: formatadorEixoY }
    },

    dataZoom: [
      { type: 'inside', xAxisIndex: 0 },
      { type: 'slider', xAxisIndex: 0, bottom: 22 }
    ],

    series: criarSeries(algoritmos, campoY)
  };
}

function criarOpcaoTempo(dados) {
  return criarOpcaoBase(
      'Vértices × tempo médio',
      'Menor valor indica execução mais rápida',
      dados,
      'media_ms',
      'Tempo médio (ms)',
      criarTooltipTempo,
      (valor) => `${formatarNumero(valor, 0)} ms`
  );
}

function criarOpcaoMemoria(dados) {
  return criarOpcaoBase(
      'Vértices × memória de pico',
      'Menor valor indica menor consumo de memória',
      dados,
      'memoria_pico_bytes',
      'Memória de pico',
      criarTooltipMemoria,
      formatarBytes
  );
}

function desenharGraficos() {
  const dadosFiltrados = obterDadosFiltrados();

  if (!dadosFiltrados.length) {
    graficoTempo.clear();
    graficoMemoria.clear();
    atualizarStatus('Nenhum resultado encontrado para a densidade selecionada.', true);
    return;
  }

  graficoTempo.setOption(criarOpcaoTempo(dadosFiltrados), { notMerge: true });
  graficoMemoria.setOption(criarOpcaoMemoria(dadosFiltrados), { notMerge: true });
}

function atualizarStatus(mensagem, erro = false) {
  elementoStatus.textContent = mensagem;
  elementoStatus.classList.toggle('erro', erro);
}

async function carregarCsv(forcarAtualizacao = false) {
  if (carregamentoEmAndamento) return;

  carregamentoEmAndamento = true;

  try {
    atualizarStatus('Verificando resultados...');

    const respostas = await Promise.all(
        CSV_URLS.map(async (url) => {
          const resposta = await fetch(`${url}?timestamp=${Date.now()}`, {
            cache: 'no-store'
          });

          if (resposta.status === 404) {
            return null;
          }

          if (!resposta.ok) {
            throw new Error(`Não foi possível carregar ${url} (HTTP ${resposta.status}).`);
          }

          return {
            url,
            texto: await resposta.text()
          };
        })
    );

    const arquivosEncontrados = respostas.filter(Boolean);

    if (!arquivosEncontrados.length) {
      throw new Error(
          'Nenhum CSV separado foi encontrado. Execute ao menos um serviço de algoritmo.'
      );
    }

    const conteudoAtual = arquivosEncontrados
        .map((arquivo) => `${arquivo.url}\n${arquivo.texto}`)
        .join('\n---\n');

    if (!forcarAtualizacao && conteudoAtual === ultimoConteudoCsv) {
      atualizarStatus(`Sem alterações — verificado às ${new Date().toLocaleTimeString('pt-BR')}.`);
      return;
    }

    const novosDados = arquivosEncontrados.flatMap((arquivo) =>
        converterCsv(arquivo.texto)
    );

    if (!novosDados.length) {
      throw new Error('Nenhum registro válido foi encontrado nos arquivos CSV.');
    }

    dadosAtuais = novosDados;
    ultimoConteudoCsv = conteudoAtual;

    atualizarOpcoesDensidade(dadosAtuais);
    desenharGraficos();

    atualizarStatus(
        `Atualizado às ${new Date().toLocaleTimeString('pt-BR')} — ` +
        `${dadosAtuais.length} resultados de ${arquivosEncontrados.length} algoritmo(s).`
    );
  } catch (erro) {
    console.error(erro);
    atualizarStatus(`Erro: ${erro.message}`, true);
  } finally {
    carregamentoEmAndamento = false;
  }
}

filtroDensidade.addEventListener('change', desenharGraficos);
botaoAtualizar.addEventListener('click', () => carregarCsv(true));

window.addEventListener('resize', () => {
  graficoTempo.resize();
  graficoMemoria.resize();
});

carregarCsv(true);
setInterval(() => carregarCsv(false), INTERVALO_ATUALIZACAO_MS);
