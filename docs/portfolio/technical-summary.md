# Ficha técnica e identidade do repositório

## Ficha técnica

| Característica | Informação | Evidência |
|---|---|---|
| Nome | Assistente de Estudos de Redes com RAG | README |
| Objetivo | Responder perguntas sobre Redes de Computadores com base em PDFs técnicos | `rag.py`, `app.py` |
| Linguagem | Python (testado pelo autor com Python 3.12) | código; capturas do terminal |
| Interface | Streamlit | `app.py` |
| Orquestração | LangChain (divisão de texto, FAISS, embeddings) | `ingestao.py`, `rag.py` |
| Modelo de IA | Google Gemini (`gemini-3.8-flash`, definido em `config.py`) | `config.py` |
| Provedor / acesso | Google, via API e SDK `google-genai` | `rag.py`, `requirements.txt` |
| Embeddings | `paraphrase-multilingual-MiniLM-L12-v2`, executado localmente | `config.py`, `ingestao.py` |
| Banco vetorial | FAISS, salvo em `vector_db/` | `ingestao.py` |
| Banco de dados relacional | Não há | código |
| Base de conhecimento | PDFs colocados em `data/` pelo usuário; o material do desenvolvimento não é distribuído | `ingestao.py`; `docs/KNOWLEDGE_BASE.md` |
| Arquitetura | RAG com duas etapas: ingestão e consulta | `docs/ARCHITECTURE.md` |
| Recuperação | `similarity_search`, k = 4, sem limite de similaridade | `rag.py` |
| Fontes na resposta | Trechos recuperados, com arquivo e página | `app.py` |
| Memória de conversa | Não há | código |
| Ferramentas / function calling | Não há | código |
| Funcionalidades | Perguntas e respostas com contexto recuperado; exibição de fontes | código |
| Segurança | Chave em `.env`; sem registro de perguntas; riscos documentados | `docs/SECURITY.md` |
| Testes | 11 testes unitários do prompt e da configuração (passaram em ambiente de verificação com bibliotecas simuladas), teste de divisão em pedaços e bateria de comportamento pendentes de execução | `docs/TESTING.md` |
| Implantação | Local | `docs/ARCHITECTURE.md` |

## Identidade do repositório

**Nome sugerido:** `assistente-estudos-redes-rag`

O nome evita "SENAI" de propósito, para não sugerir um projeto oficial. Outras opções: `rag-estudos-redes`, `redes-rag-assistant`.

**Descrição curta (campo "About" do GitHub):**
Assistente de estudos de Redes com RAG: busca trechos em PDFs (FAISS + embeddings multilíngues), responde com o Gemini e mostra as páginas usadas. Projeto independente.

**Topics:**
`rag`, `retrieval-augmented-generation`, `gemini-api`, `langchain`, `faiss`, `sentence-transformers`, `embeddings`, `semantic-search`, `streamlit`, `python`, `nlp`, `portuguese`

**Frase de apresentação:**
Pergunte ao seu material de estudo: o assistente busca os trechos certos no PDF antes de responder e mostra de onde vieram.

**Imagem de capa:** `assets/social/cover.png` (1280 x 640 px, tamanho indicado para a imagem de pré-visualização social do GitHub). Envie em Settings > Social preview.

**Organização dos materiais:** código na raiz, documentação em `docs/`, textos e carrossel em `docs/portfolio/`, imagens em `assets/`.

**Descrição curta para o perfil do GitHub (sugestão para você adaptar):**
Estudando Redes de Computadores e IA aplicada. Projetos com Python, RAG e modelos de linguagem.

## Aviso de independência

Não use o nome ou o logotipo do SENAI no nome do repositório, na capa ou nas imagens de divulgação de forma que sugira parceria ou aprovação. Se citar o SENAI, faça apenas como contexto do seu estudo, de forma factual.
