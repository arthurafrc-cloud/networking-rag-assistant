"""
app.py  ->  ETAPA 11: A INTERFACE (O SITE DO CHAT)

Usa o Streamlit, que transforma um script Python em uma página web
sem você precisar saber HTML, CSS ou JavaScript.

Como rodar (NÃO use "python app.py"):
    streamlit run app.py

O navegador abre sozinho em http://localhost:8501
"""

import streamlit as st

from rag import carregar_banco, criar_cliente_gemini, gerar_resposta

# Configura a aba do navegador (título e ícone). Deve ser o primeiro comando st.
st.set_page_config(page_title="SENAI AI Assistant", page_icon="🤖")


# ---------------------------------------------------------------
# CARREGAR RECURSOS PESADOS UMA ÚNICA VEZ
# ---------------------------------------------------------------
# IMPORTANTE: o Streamlit reexecuta este arquivo INTEIRO a cada interação
# do usuário (cada clique, cada pergunta). Sem cache, o modelo de embeddings
# e o banco seriam recarregados toda hora e o app ficaria muito lento.
# @st.cache_resource faz a função rodar só na primeira vez e guardar o resultado.
@st.cache_resource
def iniciar():
    banco = carregar_banco()
    cliente = criar_cliente_gemini()
    return banco, cliente


# ---------------------------------------------------------------
# CABEÇALHO
# ---------------------------------------------------------------
st.title("🤖 SENAI AI Assistant")
st.caption("Tire dúvidas sobre Redes, Cisco, Python e IoT com base nas apostilas do SENAI.")

# Tentamos iniciar; se algo estiver faltando (banco ou chave), mostramos
# uma mensagem clara em vez de um erro enorme e assustador.
try:
    banco, cliente = iniciar()
except (FileNotFoundError, RuntimeError) as erro:
    st.error(str(erro))
    st.stop()  # interrompe o app aqui

# ---------------------------------------------------------------
# CAMPO DE PERGUNTA
# ---------------------------------------------------------------
pergunta = st.text_input("Digite sua dúvida", placeholder="Ex.: O que é VLAN?")

# Só executa se o usuário digitou alguma coisa (e apertou Enter).
if pergunta:
    # st.spinner mostra "Pensando..." enquanto o código dentro dele roda.
    with st.spinner("Pensando..."):
        try:
            texto, trechos = gerar_resposta(banco, cliente, pergunta)
        except Exception as erro:
            st.error(f"Ocorreu um erro ao gerar a resposta: {erro}")
            st.stop()

    # Mostra a resposta.
    st.subheader("Resposta")
    st.write(texto)

    # Mostra de onde a informação veio. Fica "fechado" até o usuário clicar.
    with st.expander("📚 Fontes consultadas"):
        for trecho in trechos:
            st.markdown(
                f"**{trecho.metadata['arquivo']}** — página {trecho.metadata['pagina']}"
            )
            st.text(trecho.page_content)
