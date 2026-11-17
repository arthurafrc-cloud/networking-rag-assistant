# Design do RAG e engenharia de prompt

Este documento explica as decisões técnicas do pipeline e aponta o que foi medido e o que ainda não foi. Tudo o que está descrito como "implementado" pode ser conferido em `ingestao.py`, `rag.py`, `app.py` e `config.py`.

## O que é RAG neste projeto

*Retrieval-Augmented Generation*: em vez de perguntar direto ao modelo, o sistema primeiro **recupera** trechos do material e depois pede ao modelo que **gere** a resposta usando esses trechos. O conhecimento sobre o conteúdo do PDF vem da recuperação, não do treinamento do modelo.

## Decisões de projeto

### 1. Extração
`pypdf` extrai o texto de cada página. Páginas sem texto (por exemplo, escaneadas) são ignoradas. Cada página mantém o nome do arquivo e o número, que viram metadados.

### 2. Divisão em pedaços
`RecursiveCharacterTextSplitter` com `TAMANHO_CHUNK = 1000` e `SOBREPOSICAO_CHUNK = 200` (em `config.py`).

- O divisor tenta cortar em parágrafos, depois linhas, frases e palavras, para não quebrar ideias no meio.
- A sobreposição repete o fim de um pedaço no início do seguinte, para que uma frase importante não se perca no corte.
- A divisão é feita **página por página**. Vantagem: todo pedaço tem uma página de origem exata. Custo: uma explicação que atravesse duas páginas fica em pedaços separados.
- Os valores 1000 e 200 são um ponto de partida. **Não foram comparados com outros valores.**

### 3. Embeddings
Modelo `paraphrase-multilingual-MiniLM-L12-v2`, executado localmente pela biblioteca `sentence-transformers`.

- Escolhido por ser multilíngue, já que o material está em português.
- Roda sem enviar o texto do PDF a nenhum serviço externo na etapa de indexação e de busca.
- Download de cerca de 470 MB na primeira execução.
- **Não foi comparado com outros modelos de embeddings.**
- A pergunta é vetorizada pelo mesmo modelo no momento da consulta. Usar modelos diferentes na ingestão e na consulta invalidaria a busca.

### 4. Recuperação
`similarity_search` do FAISS (via LangChain) com `QTD_TRECHOS = 4`.

- Sempre devolve 4 trechos, mesmo que nenhum seja relevante. Não há limite mínimo de similaridade.
- Mais trechos dão mais contexto, mas aumentam o tamanho do prompt e a chance de incluir ruído.

### 5. Geração
`client.models.generate_content` (SDK `google-genai`) com o modelo de `MODELO_GEMINI`. Nenhum parâmetro de geração (temperatura, por exemplo) é definido, então valem os padrões da API.

### 6. Apresentação das fontes
`app.py` mostra os 4 trechos recuperados, com arquivo, página e texto, dentro de "Fontes consultadas".

**Cuidado ao interpretar:** esses são os trechos que foram *enviados* ao modelo. O sistema não verifica quais deles sustentam cada afirmação da resposta. Por isso o rótulo correto é "trechos recuperados", não "citações".

## Engenharia de prompt

O prompt é montado em `rag.montar_prompt`. Sua estrutura:

| Elemento | Texto no código (resumo) | Função |
|---|---|---|
| Papel | assistente educacional, especialista em Redes, Cisco, Python e IoT | dá o contexto e o tom |
| Restrição ao contexto | "usando SOMENTE as informações do CONTEXTO" | reduz a chance de o modelo usar conhecimento externo |
| Saída para quando não há resposta | "Não encontrei essa informação nas apostilas." | dá ao modelo uma resposta segura em vez de inventar |
| Proibição explícita | "Não invente nada" | reforça a restrição |
| Estilo | português, didático e objetivo | padroniza a resposta |
| Contexto rotulado | cada trecho precedido de `[arquivo, página N]`, trechos separados por `---` | deixa a origem de cada trecho visível ao modelo |
| Ordem | instruções, depois contexto, depois pergunta | a pergunta fica por último |

**O que isso garante e o que não garante:** o prompt *pede* ao modelo que se limite ao contexto. Não há mecanismo que *force* isso. A eficácia da instrução ainda precisa ser medida com `tests/avaliar_rag.py`.

**Observação sobre a persona:** o texto atual do prompt e o título da interface mencionam "SENAI". Isso é apenas texto do prompt e da tela e não indica vínculo oficial. Existe uma proposta de neutralizar esses textos (ver as pendências no relatório de entrega); ela não foi aplicada porque altera o comportamento do assistente e depende de aprovação.

## Parâmetros que podem ser ajustados (`config.py`)

| Parâmetro | Valor atual | Efeito de aumentar |
|---|---|---|
| `TAMANHO_CHUNK` | 1000 | pedaços maiores: mais contexto por trecho, busca menos precisa |
| `SOBREPOSICAO_CHUNK` | 200 | menos risco de cortar uma ideia, mais repetição no índice |
| `QTD_TRECHOS` | 4 | mais contexto, prompt maior, mais ruído possível |
| `MODELO_EMBEDDING` | paraphrase-multilingual-MiniLM-L12-v2 | trocar exige refazer a ingestão |
| `MODELO_GEMINI` | gemini-3.8-flash | troque se o modelo for descontinuado |

Alterar `TAMANHO_CHUNK`, `SOBREPOSICAO_CHUNK` ou `MODELO_EMBEDDING` exige rodar `python ingestao.py` de novo.

## O que ainda não foi medido

- A qualidade da recuperação (se os trechos certos aparecem entre os 4).
- A fidelidade das respostas ao contexto.
- O comportamento diante de perguntas fora do escopo, ambíguas e de tentativas de injeção de prompt.
- O efeito de mudar chunk, sobreposição, `k` ou modelo de embeddings.

## Propostas de evolução (não implementadas)

Cada item abaixo altera o comportamento do sistema e só deve ser feito com aprovação do autor.

1. Conjunto de perguntas de referência, com a página esperada, para medir a recuperação.
2. Limite mínimo de similaridade para descartar trechos irrelevantes.
3. Delimitar a pergunta do usuário no prompt e orientar o modelo a tratá-la como dado.
4. Pedir ao modelo que indique quais trechos usou e exibir só esses.
5. Memória de conversa, reescrevendo a pergunta de acompanhamento antes da busca.
6. Reordenação dos resultados (reranking) ou busca híbrida com palavras-chave.
7. Ingestão incremental e OCR para PDFs escaneados.
