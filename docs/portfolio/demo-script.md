# Roteiro de demonstração em vídeo (45 a 60 segundos)

**Não grave nem publique antes de rodar a bateria de testes** (`python tests/avaliar_rag.py`). O roteiro mostra uma pergunta fora do escopo, e esse comportamento ainda não foi validado. Use na gravação apenas o que você viu funcionar.

**Preparação**

- Navegador com a **tradução automática desligada** (nos prints anteriores a página aparecia traduzida).
- Janela só com o app: sem favoritos, abas pessoais ou notificações.
- Terminal fora de cena, ou com a pasta do projeto e sem o nome de usuário do Windows visível.
- Pergunte apenas coisas que você já testou e sabe a resposta.
- Narração em tom natural. Não leia o texto como um comercial.

## Cenas

| Tempo | Na tela | Narração |
|---|---|---|
| 0 a 8 s | Tela inicial do app | "Este é um assistente de estudos que montei para Redes de Computadores. Ele responde com base nos PDFs que eu indexo." |
| 8 a 22 s | Digitar "O que é PA?" e mostrar a resposta | "Faço uma pergunta sobre o meu material. A resposta é gerada pelo Gemini, mas só depois de o sistema buscar os trechos mais relevantes do PDF." |
| 22 a 34 s | Abrir "Fontes consultadas" e rolar os trechos | "Aqui estão os trechos que foram enviados ao modelo, com o arquivo e a página. Dá para conferir no original." |
| 34 a 48 s | Digitar uma pergunta que o material não cobre (por exemplo, "Quem ganhou a Copa do Mundo de 2022?") | "Se a pergunta não tem a ver com o material, o prompt pede para ele dizer que não encontrou, em vez de inventar. Ainda estou testando o quanto isso funciona." (**só grave isto se o teste confirmou o comportamento**) |
| 48 a 58 s | Mostrar o diagrama de arquitetura ou o README no GitHub | "Por trás, o texto do PDF é dividido em pedaços, transformado em embeddings e guardado no FAISS. Usei Python, LangChain, Gemini e Streamlit. O código e a documentação estão no meu GitHub." |

## Texto corrido da narração (para ensaio)

Este é um assistente de estudos que montei para Redes de Computadores. Ele responde com base nos PDFs que eu indexo. Faço uma pergunta sobre o meu material, e a resposta é gerada pelo Gemini, mas só depois de o sistema buscar os trechos mais relevantes do PDF. Aqui estão os trechos que foram enviados ao modelo, com arquivo e página, então dá para conferir no original. Quando a pergunta não tem a ver com o material, o prompt pede para ele dizer que não encontrou, em vez de inventar. Ainda estou testando o quanto isso funciona. Por trás, o texto é dividido em pedaços, transformado em embeddings e guardado no FAISS. Usei Python, LangChain, Gemini e Streamlit. O código e a documentação estão no meu GitHub.

## Cuidados

- Não mostre a chave, o arquivo `.env` nem o terminal com o caminho da sua pasta pessoal.
- Se a resposta mostrar trechos do PDF, confirme que você pode exibi-los.
- Não afirme que o assistente "sempre acerta" ou que responde sobre cursos e matrículas.
- Se a pergunta fora do escopo não der o resultado esperado, grave só as três primeiras cenas e a final, e registre o caso em `docs/TESTING.md`.
