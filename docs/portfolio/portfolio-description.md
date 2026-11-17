# Descrição para portfólio

## Nome

Assistente de Estudos de Redes com RAG

## Objetivo

Responder perguntas sobre Redes de Computadores com base em documentos técnicos em PDF, mostrando de onde veio cada trecho usado, como exercício prático de arquitetura RAG e de integração com modelos de linguagem.

## Problema abordado

Estudar a partir de PDFs longos exige procurar a explicação certa página por página. Um chatbot genérico responde rápido, mas não sabe o que está no material do estudante e pode responder sem fundamento. Este projeto é a motivação do autor para unir os dois lados: usar um modelo de linguagem obrigando-o a se basear no documento.

## Solução

Um assistente web que, antes de gerar a resposta, recupera os trechos mais relevantes dos PDFs indexados e envia esses trechos ao Gemini com a instrução de responder somente com eles. A tela exibe a resposta e os trechos recuperados, com arquivo e página.

## Tecnologias

Python, Google Gemini API (`google-genai`), LangChain, sentence-transformers (`paraphrase-multilingual-MiniLM-L12-v2`), FAISS, pypdf e Streamlit.

## Funcionamento

1. **Ingestão:** o texto de cada página é extraído, dividido em pedaços de 1000 caracteres com 200 de sobreposição, transformado em embeddings e salvo em um índice FAISS.
2. **Consulta:** a pergunta é transformada em vetor, o FAISS devolve os 4 trechos mais próximos, o prompt é montado com as regras, os trechos rotulados e a pergunta, e o Gemini gera a resposta.
3. **Apresentação:** a interface mostra a resposta e o painel "Fontes consultadas".

## Principais recursos

- Busca semântica em português, com embeddings gerados localmente.
- Resposta limitada ao contexto recuperado, com frase definida para quando não há informação.
- Exibição de arquivo e página dos trechos recuperados.
- Configuração centralizada (tamanho dos pedaços, número de trechos, modelos).
- Documentação de arquitetura, segurança, base de conhecimento e testes.

## Aprendizados

- Como cada etapa do RAG (extração, divisão, embeddings, busca, geração) afeta o resultado.
- Escrita de prompts que restringem o modelo ao contexto e definem a resposta para o caso sem informação.
- Isolar o nome do modelo na configuração, depois de lidar com a descontinuação de modelos e a troca de SDK.
- Gestão de segredos e decisão sobre o que pode ou não ser publicado.
- Diferença entre "trecho recuperado" e "citação verificada", e por que isso importa para a confiabilidade.

## Limitações

- Sem memória de conversa.
- Responde apenas com base nos PDFs indexados (não cobre cursos, matrículas, preços ou unidades).
- Sem OCR; figuras e diagramas não são lidos.
- Sempre recupera 4 trechos, sem limite mínimo de similaridade.
- A qualidade das respostas ainda não foi medida de forma sistemática.
- Execução local, sem implantação em nuvem.

## Aviso

Projeto independente de estudo, sem vínculo, parceria ou aprovação do SENAI ou de qualquer outra instituição. O PDF usado no desenvolvimento não é distribuído.

## Link do GitHub

[INSERIR LINK DO REPOSITÓRIO]
