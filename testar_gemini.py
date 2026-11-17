"""
testar_gemini.py  ->  ETAPA 3: TESTAR SE A CHAVE DA API FUNCIONA

Rode este arquivo ANTES de qualquer outro.
Ele só faz uma pergunta simples ao Gemini. Se aparecer uma resposta,
sua chave está configurada certo e você pode seguir para a próxima etapa.

Como rodar:
    python testar_gemini.py
"""

import os

from google import genai

from config import MODELO_GEMINI

# os.environ guarda as "variáveis de ambiente" do seu computador.
# .get() devolve o valor, ou None se a variável não existir.
chave = os.environ.get("GEMINI_API_KEY")

if not chave:
    # Se a chave não foi configurada, explicamos o que fazer e paramos.
    print("ERRO: a chave GEMINI_API_KEY não foi encontrada.")
    print()
    print("Opção A (recomendada): crie um arquivo chamado .env nesta pasta com a linha:")
    print("   GEMINI_API_KEY=cole_sua_chave_aqui")
    print()
    print("Opção B: configure a variável no terminal.")
    print("1) Crie sua chave em https://aistudio.google.com")
    print("2) Configure a variável no terminal:")
    print('   Windows (PowerShell): $env:GEMINI_API_KEY="cole_sua_chave_aqui"')
    print('   Windows (CMD):        set GEMINI_API_KEY=cole_sua_chave_aqui')
    print('   Linux / Mac:          export GEMINI_API_KEY="cole_sua_chave_aqui"')
    print("3) Rode este arquivo de novo NO MESMO terminal.")
    raise SystemExit(1)  # encerra o programa

# Cria o "cliente": o objeto que conversa com os servidores do Google.
client = genai.Client(api_key=chave)

# Envia uma pergunta e guarda a resposta.
resposta = client.models.generate_content(
    model=MODELO_GEMINI,
    contents="Explique em duas frases o que é NAT em redes de computadores.",
)

# resposta.text contém o texto gerado pelo Gemini.
print("Resposta do Gemini:")
print(resposta.text)
