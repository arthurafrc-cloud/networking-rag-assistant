"""
config.py  ->  CONFIGURAÇÕES DO PROJETO

Aqui ficam todos os "números e nomes" que você pode querer mudar.
Em vez de espalhar esses valores pelo código, deixamos tudo num lugar só.
Os outros arquivos (ingestao.py, rag.py, app.py) fazem "from config import ..."
para usar esses valores.
"""

import os
from pathlib import Path

# ---------------------------------------------------------------
# PASTAS
# ---------------------------------------------------------------
# __file__ é o caminho deste arquivo (config.py).
# .parent é a pasta onde ele está (senai-ai-assistant/).
# Assim o projeto funciona não importa de onde você rode o comando.
PASTA_BASE = Path(__file__).parent

# ---------------------------------------------------------------
# CHAVE DA API (lida do arquivo .env)
# ---------------------------------------------------------------
# O arquivo .env fica na mesma pasta e tem uma linha assim:
#     GEMINI_API_KEY=sua_chave_aqui
# Este pequeno bloco lê o arquivo e coloca cada linha como variável de
# ambiente, que é de onde o rag.py e o testar_gemini.py leem a chave.
# Assim a chave fica FORA do código: o .env está no .gitignore e nunca
# vai para o GitHub.
def carregar_env():
    arquivo_env = PASTA_BASE / ".env"
    if not arquivo_env.exists():
        return
    for linha in arquivo_env.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        # Ignora linhas vazias, comentários (#) e linhas sem "="
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        nome, valor = linha.split("=", 1)
        # setdefault: se você já configurou a variável no terminal,
        # o valor do terminal tem prioridade e o .env não a sobrescreve.
        os.environ.setdefault(nome.strip(), valor.strip().strip('"').strip("'"))


carregar_env()

# Pasta onde você coloca os PDFs das apostilas
PASTA_DADOS = PASTA_BASE / "data"

# Pasta onde o banco vetorial (FAISS) será salvo
PASTA_VETORES = PASTA_BASE / "vector_db"

# ---------------------------------------------------------------
# DIVISÃO DO TEXTO EM PEDAÇOS (chunks)
# ---------------------------------------------------------------
# Tamanho máximo de cada pedaço, em caracteres.
# Pedaços muito grandes misturam assuntos; muito pequenos perdem contexto.
# 1000 é um bom ponto de partida.
TAMANHO_CHUNK = 1000

# Quantos caracteres se repetem entre um pedaço e o próximo.
# Serve para uma frase importante não ser cortada ao meio e se perder.
SOBREPOSICAO_CHUNK = 200

# ---------------------------------------------------------------
# EMBEDDINGS
# ---------------------------------------------------------------
# Modelo que transforma texto em números.
# O modelo do tutorial original (all-MiniLM-L6-v2) foi treinado em inglês.
# Como as apostilas do SENAI estão em português, usamos um modelo MULTILÍNGUE,
# que entende português muito melhor.
# Na primeira execução ele é baixado da internet (cerca de 500 MB).
MODELO_EMBEDDING = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# ---------------------------------------------------------------
# BUSCA
# ---------------------------------------------------------------
# Quantos trechos da apostila são enviados ao Gemini como contexto.
# Mais trechos = mais informação, mas também mais lento e mais chance de ruído.
QTD_TRECHOS = 4

# ---------------------------------------------------------------
# GEMINI
# ---------------------------------------------------------------
# Nome do modelo do Gemini. Se um dia der erro de "modelo não encontrado",
# veja os nomes atuais em https://ai.google.dev/gemini-api/docs/models
# e troque aqui. Só precisa mudar neste lugar.
MODELO_GEMINI = "gemini-3.8-flash"

# A chave da API NÃO fica escrita aqui: ela vem do arquivo .env (veja
# carregar_env() acima). Nunca escreva a chave direto no código: se você
# subir o projeto no GitHub, qualquer pessoa pode usá-la.
