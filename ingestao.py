"""
ingestao.py  ->  ETAPAS 4, 5, 6 e 7: TRANSFORMAR AS APOSTILAS EM UM BANCO VETORIAL

"Ingestão" é o processo de pegar os documentos e deixá-los prontos para
a IA consultar. Este arquivo faz 4 coisas, em ordem:

    PDF  ->  (4) ler texto  ->  (5) dividir em pedaços
         ->  (6) embeddings  ->  (7) salvar no banco vetorial (FAISS)

Você só precisa rodar este arquivo UMA vez (e de novo sempre que
adicionar ou trocar PDFs na pasta data/).

Como rodar:
    python ingestao.py
"""

from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

from config import (
    PASTA_DADOS,
    PASTA_VETORES,
    TAMANHO_CHUNK,
    SOBREPOSICAO_CHUNK,
    MODELO_EMBEDDING,
)


# ===============================================================
# ETAPA 4 - LER OS PDFs
# ===============================================================
def ler_pdfs():
    """
    Lê todos os PDFs da pasta data/ e devolve uma lista de páginas.
    Cada item é um dicionário assim:
        {"texto": "conteúdo da página...", "arquivo": "apostila.pdf", "pagina": 12}
    Guardamos o nome do arquivo e o número da página para poder
    mostrar a FONTE da resposta depois (isso dá credibilidade ao projeto).
    """
    paginas = []

    # .glob("*.pdf") encontra todos os arquivos que terminam em .pdf
    arquivos_pdf = sorted(PASTA_DADOS.glob("*.pdf"))

    if not arquivos_pdf:
        print(f"Nenhum PDF encontrado em: {PASTA_DADOS}")
        print("Coloque suas apostilas lá e rode este arquivo de novo.")
        raise SystemExit(1)

    for caminho in arquivos_pdf:
        print(f"Lendo {caminho.name} ...")
        leitor = PdfReader(caminho)

        # enumerate dá o número de cada página junto com a página.
        # start=1 faz a contagem começar em 1 (como num livro).
        for numero, pagina in enumerate(leitor.pages, start=1):
            # extract_text() pode devolver None ou vazio em páginas que são
            # só imagem (PDF escaneado). O "or ''" troca None por texto vazio.
            texto = pagina.extract_text() or ""

            # Ignoramos páginas sem texto para não poluir o banco.
            if texto.strip():
                paginas.append(
                    {"texto": texto, "arquivo": caminho.name, "pagina": numero}
                )

    print(f"Total de páginas com texto: {len(paginas)}")
    return paginas


# ===============================================================
# ETAPA 5 - DIVIDIR EM PEDAÇOS (CHUNKS)
# ===============================================================
def dividir_em_chunks(paginas):
    """
    Quebra o texto de cada página em pedaços menores.

    POR QUE? A IA não manda a apostila inteira para o Gemini: ela busca só
    os pedaços relevantes para a pergunta. Pedaços menores = busca mais precisa.

    O RecursiveCharacterTextSplitter tenta cortar em lugares naturais:
    primeiro em parágrafos, depois em linhas, depois em frases, depois em palavras.
    """
    divisor = RecursiveCharacterTextSplitter(
        chunk_size=TAMANHO_CHUNK,
        chunk_overlap=SOBREPOSICAO_CHUNK,
    )

    textos = []     # os pedaços de texto
    metadados = []  # de onde cada pedaço veio (mesma ordem da lista acima)

    for pag in paginas:
        pedacos = divisor.split_text(pag["texto"])
        for pedaco in pedacos:
            textos.append(pedaco)
            metadados.append({"arquivo": pag["arquivo"], "pagina": pag["pagina"]})

    print(f"Total de pedaços (chunks): {len(textos)}")
    return textos, metadados


# ===============================================================
# ETAPA 6 - EMBEDDINGS
# ===============================================================
def criar_embeddings():
    """
    Cria o modelo de embeddings.

    EMBEDDING = transformar um texto em uma lista de números (um "vetor")
    que representa o SIGNIFICADO do texto. Textos com significado parecido
    ficam com números parecidos. Por isso "O que é NAT?" fica perto do
    trecho da apostila que explica NAT, mesmo sem as palavras serem idênticas.

    Esta função também é usada pelo rag.py, para transformar a PERGUNTA
    do usuário em números do mesmo jeito.
    """
    return HuggingFaceEmbeddings(model_name=MODELO_EMBEDDING)


# ===============================================================
# ETAPA 7 - CRIAR E SALVAR O BANCO VETORIAL
# ===============================================================
def criar_banco(textos, metadados):
    """
    Converte cada pedaço em vetor e guarda tudo no FAISS.

    FAISS é uma biblioteca (feita pelo Facebook/Meta) especializada em
    encontrar rapidamente os vetores mais parecidos com um vetor de busca.
    """
    print("Criando embeddings (pode demorar alguns minutos na primeira vez)...")
    embeddings = criar_embeddings()

    banco = FAISS.from_texts(
        textos,
        embeddings,
        metadatas=metadados,
    )

    # Salva em disco para não precisar refazer tudo a cada execução.
    banco.save_local(str(PASTA_VETORES))
    print(f"Banco vetorial salvo em: {PASTA_VETORES}")


# ===============================================================
# PROGRAMA PRINCIPAL
# ===============================================================
# O "if __name__ == '__main__'" garante que o código abaixo só roda quando
# você executa ESTE arquivo diretamente (python ingestao.py).
# Quando outro arquivo faz "from ingestao import criar_embeddings",
# essa parte NÃO roda. Isso evita reprocessar os PDFs sem querer.
if __name__ == "__main__":
    paginas = ler_pdfs()
    textos, metadados = dividir_em_chunks(paginas)
    criar_banco(textos, metadados)
    print("Pronto! Agora você já pode rodar o app: streamlit run app.py")
