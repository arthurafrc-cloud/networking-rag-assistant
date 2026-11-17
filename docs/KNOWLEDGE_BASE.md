# Base de conhecimento

## O que é

A base de conhecimento do assistente é o conjunto de **PDFs que você colocar em `data/`** e indexar com `python ingestao.py`. Não há outra fonte: nada de páginas da web, bancos de dados, APIs ou informações escritas diretamente no código.

## Escopo

- Conteúdo: o que estiver no texto dos PDFs indexados. No desenvolvimento, foi usado um material técnico sobre Redes de Computadores.
- O assistente **não** tem informações sobre cursos, matrículas, inscrições, preços, prazos, documentos exigidos, unidades ou horários de nenhuma instituição. Essas funcionalidades não foram implementadas.
- Não há distinção regional, porque não há conteúdo institucional.

## Origem e permissão de uso do material

| Item | Situação |
|---|---|
| PDF usado no desenvolvimento | não é distribuído neste repositório |
| Origem do material | a confirmar pelo autor |
| Permissão de redistribuição | não confirmada |
| Índice FAISS gerado a partir dele | não é distribuído (contém trechos do texto) |

Enquanto a origem e a permissão não forem confirmadas, `data/` e `vector_db/` ficam fora do Git (ver `.gitignore`). Se você publicar uma versão com material de terceiros, obtenha autorização ou aponte links para as fontes oficiais em vez de copiar o conteúdo.

## Como as informações são organizadas

1. Cada PDF é lido página por página.
2. O texto de cada página é dividido em pedaços de até 1000 caracteres, com 200 de sobreposição.
3. Cada pedaço guarda dois metadados: `arquivo` (nome do PDF) e `pagina` (número da página).
4. Cada pedaço vira um vetor e é salvo no índice FAISS em `vector_db/`.

## Como atualizar ou adicionar fontes

1. Coloque o novo PDF em `data/` (ou troque o antigo).
2. Rode `python ingestao.py`. **O índice é recriado do zero** com todos os PDFs da pasta.
3. Reinicie o app, porque o índice é carregado uma vez e mantido em cache.

## Limitações de cobertura

- Só o texto é extraído. Imagens, diagramas, capturas de tela e o texto dentro delas não são lidos.
- PDFs escaneados sem camada de texto são ignorados (não há OCR).
- A formatação de tabelas e colunas pode se perder na extração do `pypdf`.
- Uma ideia que atravesse duas páginas é recuperada em pedaços separados.

## Informações desatualizadas ou conflitantes

O sistema **não** guarda data de publicação nem versão dos documentos e **não** detecta conflitos entre eles. Boas práticas:

- Mantenha uma única versão de cada documento em `data/`.
- Inclua versão ou data no nome do arquivo (por exemplo, `guia-redes-2026-03.pdf`), já que o nome aparece nas fontes exibidas.
- Se dois PDFs tratarem do mesmo assunto de forma diferente, o assistente pode misturar os trechos. Prefira indexar apenas o mais atual.
- Para assuntos que mudam com frequência (cursos, preços, prazos), este tipo de base estática não é adequada sem um processo de atualização.
