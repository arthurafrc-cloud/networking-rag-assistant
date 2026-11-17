# Segurança e privacidade

Resultado de uma revisão do código. Não é uma certificação nem uma auditoria externa.

## Credenciais

| Verificação | Situação |
|---|---|
| Chave escrita no código (`.py`, `requirements.txt`) | não encontrada |
| Chave lida de | variável de ambiente `GEMINI_API_KEY`, preenchida por `.env` |
| `.env` ignorado pelo Git | sim (`.gitignore`) |
| Modelo de configuração publicável | `.env.example`, sem valor real |
| Histórico do Git | não aplicável: o repositório ainda não havia sido criado quando a revisão foi feita |

**Antes de publicar:**

1. Se a chave já foi exibida em conversas, prints ou arquivos compartilhados, crie uma nova no Google AI Studio e **exclua a antiga**.
2. Se a pasta do projeto estiver em um serviço de sincronização (por exemplo, OneDrive), o `.env` também é sincronizado. Considere guardar o projeto fora dele.
3. Depois de `git init` e antes do primeiro commit, rode `git status` e confirme que `.env`, `data/*.pdf` e `vector_db/*` **não** aparecem.
4. Nunca coloque a chave em prints, logs ou issues.

## Riscos específicos de aplicações com IA

| Risco | Situação no projeto | Mitigação existente | Pendente |
|---|---|---|---|
| Injeção de prompt na pergunta | a pergunta é inserida no mesmo texto das instruções, sem delimitação e sem limite de tamanho | instrução para usar somente o contexto | delimitar a pergunta; testar com `tests/avaliar_rag.py` |
| Instruções maliciosas dentro do PDF | o texto dos trechos entra no prompt como contexto confiável | nenhuma | tratar o contexto como dado; indexar só material confiável |
| Vazamento do prompt | o prompt não contém segredos, mas pode ser pedido ao modelo | a chave não é enviada ao modelo, só usada na chamada | testar com a bateria |
| Exposição da chave | a chave não faz parte do prompt | — | rotacionar se vazou |
| Respostas sem fundamento | possível | instrução do prompt e frase de "não encontrei" | medir com perguntas de referência |
| Uso indevido de ferramentas | não se aplica: o sistema não tem ferramentas | — | — |
| Acesso não autorizado a dados | não há autenticação; o app é local | — | autenticação se for publicado |

## Índice serializado (`pickle`)

`rag.py` carrega o índice com `allow_dangerous_deserialization=True`, exigência do LangChain porque o arquivo é serializado com `pickle`. Isso é aceitável **apenas** para índices criados por você. Nunca carregue um `vector_db/` baixado de terceiros: um arquivo `pickle` malicioso pode executar código. Por isso `vector_db/` não é versionado.

## Mensagens de erro

Quando a chamada ao Gemini falha, `app.py` exibe a mensagem original da exceção. Em uso local não há problema. Em uma versão pública, troque por uma mensagem genérica e registre o detalhe apenas no servidor.

## Privacidade e dados pessoais

- O app não pede nem grava nome, e-mail, telefone, CPF ou qualquer cadastro, não mantém histórico de conversas e não cria logs de perguntas.
- A cada pergunta, o texto da pergunta e os 4 trechos recuperados do material são **enviados à API do Gemini**. Não digite dados pessoais nas perguntas e não indexe documentos com dados pessoais ou confidenciais. Consulte os termos de uso e a política de dados da API do Google para o seu tipo de conta.
- O Streamlit pode coletar estatísticas de uso anônimas por padrão. Consulte a configuração `browser.gatherUsageStats` da documentação do Streamlit se quiser desativar.
- **LGPD:** este projeto não declara conformidade com a LGPD. Por não tratar dados pessoais por projeto, o risco é baixo em uso local; se for disponibilizado a outras pessoas, será necessária uma avaliação própria.

## Capturas de tela e exemplos públicos

Antes de publicar imagens, confira que não aparecem chaves, nome de usuário do computador, caminhos pessoais, abas, favoritos ou dados de terceiros. Se a resposta exibida reproduzir trechos do material, confirme a permissão de uso.

## Como relatar um problema de segurança

Adicione aqui o canal de contato do autor antes de publicar o repositório. Não inclua chaves ou dados pessoais no relato.
