# Publicações para o LinkedIn

Três versões do mesmo projeto. Escolha uma, ajuste ao seu jeito de escrever e publique você mesmo.

**Antes de publicar:**

- Troque `[INSERIR LINK DO REPOSITÓRIO]` pelo endereço real, depois de decidir tornar o repositório público.
- Anexe o carrossel `docs/portfolio/linkedin-carousel.pdf` como documento.
- Confira o checklist de publicação no relatório de entrega (chave nova, PDF fora do repositório, prints sem dados pessoais).
- Todas as afirmações abaixo vêm do código. Se você mudar o projeto, revise os textos.

---

## Versão A: curta e objetiva

Terminei a primeira versão de um projeto de estudo: um assistente que responde perguntas sobre Redes de Computadores com base em PDFs técnicos.

Em vez de perguntar direto a um modelo, ele primeiro busca no material os trechos mais relevantes (a técnica se chama RAG) e só depois pede ao Gemini que responda usando esse contexto. A tela mostra também de quais páginas vieram os trechos.

Feito com Python, API do Gemini, LangChain, FAISS e Streamlit. Ainda tem limitações, como a falta de memória de conversa, e está tudo documentado no repositório:
[INSERIR LINK DO REPOSITÓRIO]

#InteligenciaArtificial #Python #RAG

---

## Versão B: detalhada

Estudar a partir de PDFs longos significa procurar a explicação certa página por página. Um chatbot genérico responde rápido, mas não sabe o que está no *meu* material. Foi dessa diferença que nasceu um projeto que eu queria fazer: um assistente de estudos para Redes de Computadores que responde com base nos documentos que eu indexo.

**Como funciona**
Primeiro, o texto do PDF é extraído página por página, dividido em pedaços e transformado em vetores numéricos (embeddings). Esses vetores ficam em um índice FAISS. Quando faço uma pergunta, o sistema busca os 4 trechos mais parecidos com ela e envia ao Gemini, junto com a pergunta e uma instrução: responder somente com o contexto recebido e dizer que não encontrou quando a resposta não estiver lá.

**O que aparece na tela**
A resposta e os trechos recuperados, com o nome do arquivo e a página. Importante: são os trechos que o modelo recebeu, não uma citação verificada de cada afirmação.

**O que usei**
Python, API do Google Gemini, LangChain, embeddings multilíngues (sentence-transformers), FAISS e Streamlit.

**O que aprendi**
- Como cada etapa do RAG influencia o resultado: extração, divisão do texto, embeddings, busca e geração.
- Escrever um prompt que limita o modelo ao contexto e define o que fazer quando não há resposta.
- Que modelos e SDKs de IA mudam rápido: precisei trocar o SDK e o modelo no meio do caminho e passei o nome do modelo para um arquivo de configuração.
- Cuidar de chaves de API e do que pode ou não ir para o GitHub.

**O que ainda falta**
Não há memória de conversa, ainda não medi a qualidade das respostas de forma sistemática e a instrução de "não encontrei" precisa de mais testes. Está tudo listado nas limitações do README.

É um projeto independente, sem vínculo com nenhuma instituição, e o PDF que usei não está no repositório.

Código e documentação:
[INSERIR LINK DO REPOSITÓRIO]

#InteligenciaArtificial #IAGenerativa #Python #RAG

---

## Versão C: técnica

Mini projeto de RAG em português: perguntas sobre Redes de Computadores respondidas a partir de PDFs, com Gemini e FAISS.

Pipeline, como está no código:

**Ingestão**
- `pypdf` extrai o texto por página e guarda arquivo e página como metadados.
- `RecursiveCharacterTextSplitter`: 1000 caracteres, sobreposição de 200, aplicado por página.
- Embeddings com `paraphrase-multilingual-MiniLM-L12-v2`, executados localmente.
- Índice FAISS salvo em disco.

**Consulta**
- A pergunta é vetorizada pelo mesmo modelo e o `similarity_search` devolve k = 4 trechos.
- O prompt tem papel, restrição ao contexto, frase de saída para "sem resposta" e cada trecho rotulado com `[arquivo, página]`.
- A geração usa o SDK `google-genai`, e o nome do modelo fica em `config.py`.
- O Streamlit exibe a resposta e os trechos recuperados.

**Limites que documentei**
- Sempre recupera 4 trechos, sem limite mínimo de similaridade.
- Os trechos exibidos são os recuperados, não citações verificadas.
- O prompt concatena a pergunta sem delimitação, então não está protegido contra injeção de prompt. Ainda não testei isso de forma sistemática.
- Sem memória de conversa, sem OCR e sem avaliação quantitativa da recuperação.

Os próximos passos que quero fazer são um conjunto de perguntas de referência para medir a recuperação, um limite mínimo de similaridade e delimitar a entrada do usuário no prompt.

Se você trabalha com RAG, vou gostar de ouvir como avalia a qualidade da recuperação em projetos pequenos.

Repositório com arquitetura, decisões e testes:
[INSERIR LINK DO REPOSITÓRIO]

#RAG #LangChain #Python #IAGenerativa #FAISS

---

## Sugestões de chamada para ação

- "Se quiser ver o código e a documentação, o link está no primeiro comentário."
- "Feedback é bem-vindo, principalmente sobre como avaliar a recuperação."
- "Se você já montou um RAG, o que teria feito diferente na divisão do texto?"

## Hashtags

Use de três a cinco por publicação. As escolhidas têm relação direta com o conteúdo: `#InteligenciaArtificial`, `#IAGenerativa`, `#Python`, `#RAG`, `#LangChain`, `#FAISS`. Evitei `#SENAI` porque o projeto é independente.

## Pontos que não devem aparecer nos textos

- Que o projeto é oficial, institucional ou feito em parceria com o SENAI.
- Que responde dúvidas sobre cursos, matrículas, preços ou unidades.
- Que é um "agente autônomo": o fluxo é fixo, sem escolha de ferramentas.
- Números de acerto ou estatísticas: nenhuma medição de qualidade foi feita ainda.
