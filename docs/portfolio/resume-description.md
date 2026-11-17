# Descrição para currículo

## Versão para a seção de projetos

**Assistente de Estudos de Redes com RAG** (projeto pessoal)
Python, Google Gemini API, LangChain, FAISS, sentence-transformers, Streamlit

- Desenvolvi um assistente que responde perguntas com base em PDFs técnicos usando RAG: extração de texto com pypdf, divisão em pedaços com LangChain, embeddings multilíngues e busca semântica com FAISS.
- Integrei a API do Google Gemini e escrevi o prompt que limita a resposta ao contexto recuperado e define o comportamento quando a informação não está no material.
- Criei a interface web com Streamlit, que exibe os trechos e as páginas usados em cada resposta.
- Documentei a arquitetura, a segurança e as limitações, e escrevi testes unitários e um roteiro de avaliação de comportamento (injeção de prompt, perguntas fora do escopo).

## Versão curta (uma linha)

Assistente de estudos com RAG em Python: busca semântica com FAISS e embeddings multilíngues, respostas geradas pelo Gemini e exibição dos trechos e páginas usados.

## Habilidades que o projeto demonstra

Só entram aqui habilidades que podem ser comprovadas no código e na documentação:

- Integração com API de modelo de linguagem (Gemini).
- Arquitetura RAG: extração, divisão de texto, embeddings, banco vetorial e recuperação.
- Engenharia de prompt: restrição ao contexto, rotulagem de fontes e resposta para "sem informação".
- Desenvolvimento de interface web simples (Streamlit).
- Python: organização em módulos, configuração centralizada, tratamento de erros básico.
- Gestão de segredos: `.env`, `.gitignore` e `.env.example`.
- Documentação técnica, testes unitários e análise de limitações e riscos (injeção de prompt, privacidade).

## O que não colocar

- "Agente de IA autônomo": o projeto é um assistente RAG com fluxo fixo.
- Qualquer métrica de acerto, usuários ou desempenho: não foram medidos.
- "Em parceria com" ou "para o SENAI": é um projeto independente.
