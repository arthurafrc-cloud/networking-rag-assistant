"""
rag.py  ->  ETAPAS 8, 9 e 10: BUSCAR NA APOSTILA E GERAR A RESPOSTA

RAG = Retrieval-Augmented Generation (Geração Aumentada por Recuperação).
Em português claro: antes de responder, a IA PROCURA (retrieval) os trechos
certos nas suas apostilas e usa esses trechos para GERAR (generation) a resposta.

Fluxo de cada pergunta:
    pergunta -> (8) buscar trechos parecidos no FAISS
             -> (9) montar o prompt com os trechos + a pergunta
             -> (10) enviar ao Gemini e receber a resposta

Este arquivo não é executado sozinho: ele é usado pelo app.py.
Mas você pode testá-lo direto no terminal:
    python rag.py
"""

import os

from google import genai
from langchain_community.vectorstores import FAISS

from config import PASTA_VETORES, MODELO_GEMINI, QTD_TRECHOS
from ingestao import criar_embeddings


# ===============================================================
# CARREGAR O BANCO VETORIAL (criado pelo ingestao.py)
# ===============================================================
def carregar_banco():
    """Abre o banco FAISS que foi salvo na pasta vector_db/."""
    if not (PASTA_VETORES / "index.faiss").exists():
        raise FileNotFoundError(
            "Banco vetorial não encontrado. Rode primeiro: python ingestao.py"
        )

    # IMPORTANTE: o embedding usado aqui precisa ser o MESMO usado na ingestão.
    # Senão os números não "combinam" e a busca devolve lixo.
    embeddings = criar_embeddings()

    # allow_dangerous_deserialization=True é exigido pelo LangChain porque o
    # arquivo salvo usa "pickle". É seguro AQUI porque fomos nós que criamos
    # o arquivo. Nunca ative isso para arquivos baixados de desconhecidos.
    return FAISS.load_local(
        str(PASTA_VETORES),
        embeddings,
        allow_dangerous_deserialization=True,
    )


# ===============================================================
# ETAPA 8 - BUSCAR OS TRECHOS MAIS RELEVANTES
# ===============================================================
def buscar_trechos(banco, pergunta):
    """
    Transforma a pergunta em vetor e pede ao FAISS os QTD_TRECHOS pedaços
    cujo significado é mais próximo. Devolve uma lista de "documentos";
    cada um tem .page_content (o texto) e .metadata (arquivo e página).
    """
    return banco.similarity_search(pergunta, k=QTD_TRECHOS)


# ===============================================================
# ETAPA 9 - MONTAR O PROMPT
# ===============================================================
def montar_prompt(pergunta, trechos):
    """
    Monta o texto final enviado ao Gemini.

    "Prompt" é a instrução que damos ao modelo. Um bom prompt de RAG diz:
      1) quem a IA é, 2) para usar SOMENTE o contexto, 3) o que fazer se
      a resposta não estiver lá (isso evita a IA inventar coisas).
    """
    # Junta os trechos separando-os por uma linha, indicando a fonte de cada um.
    partes = []
    for trecho in trechos:
        fonte = f"[{trecho.metadata['arquivo']}, página {trecho.metadata['pagina']}]"
        partes.append(f"{fonte}\n{trecho.page_content}")
    contexto = "\n\n---\n\n".join(partes)

    return f"""Você é um assistente educacional do SENAI, especialista em
Redes de Computadores, Cisco, Python e IoT.

Responda à pergunta do aluno usando SOMENTE as informações do CONTEXTO abaixo.
Se a resposta não estiver no contexto, diga claramente:
"Não encontrei essa informação nas apostilas."
Não invente nada. Responda em português, de forma didática e objetiva.

CONTEXTO:
{contexto}

PERGUNTA:
{pergunta}
"""


# ===============================================================
# ETAPA 10 - GERAR A RESPOSTA COM O GEMINI
# ===============================================================
def criar_cliente_gemini():
    """Cria o cliente do Gemini lendo a chave da variável de ambiente."""
    chave = os.environ.get("GEMINI_API_KEY")
    if not chave:
        raise RuntimeError(
            "Variável de ambiente GEMINI_API_KEY não configurada. "
            "Veja as instruções em testar_gemini.py."
        )
    return genai.Client(api_key=chave)


def gerar_resposta(banco, cliente, pergunta):
    """
    Função principal do RAG. Recebe a pergunta e devolve:
        (texto_da_resposta, lista_de_trechos_usados)
    """
    trechos = buscar_trechos(banco, pergunta)  # etapa 8
    prompt = montar_prompt(pergunta, trechos)  # etapa 9

    resposta = cliente.models.generate_content(  # etapa 10
        model=MODELO_GEMINI,
        contents=prompt,
    )
    return resposta.text, trechos


# ===============================================================
# TESTE NO TERMINAL (sem interface)
# ===============================================================
if __name__ == "__main__":
    banco = carregar_banco()
    cliente = criar_cliente_gemini()

    pergunta = input("Digite sua pergunta: ")
    texto, trechos = gerar_resposta(banco, cliente, pergunta)

    print("\nRESPOSTA:\n")
    print(texto)

    print("\nFONTES:")
    for t in trechos:
        print(f"- {t.metadata['arquivo']}, página {t.metadata['pagina']}")
