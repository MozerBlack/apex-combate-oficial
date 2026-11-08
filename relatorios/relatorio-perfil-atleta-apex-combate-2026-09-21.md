# 🥋 Apex Combate — Plataforma Universal de Artes Marciais

## Relatório do Perfil do Atleta

**Responsável pelo produto:** Mozer  
**Data:** 21 de setembro de 2026  
**Assinatura:** *Uma plataforma. Todas as lutas.*  
**Situação deste relatório:** perfil completo implementado no ambiente local de revisão; conjunto ainda não publicado na versão oficial.

---

## 1. Resumo executivo

O perfil do atleta do Apex Combate reúne, em uma única conta, identidade pessoal, modalidades praticadas, graduação, categoria, clube, professor ou técnico, federação, documentos, certificados, competições, inscrições, campeonato ao vivo, carteirinha digital, preparação e jornada esportiva.

O atleta não precisa criar outra conta quando pratica uma nova arte marcial. A pessoa, o documento de acesso, o nascimento, os contatos e os documentos pessoais permanecem únicos. Cada modalidade recebe somente o seu próprio contexto esportivo.

### Regra de entrada após o login

| Modalidades disponíveis | Comportamento |
|---|---|
| Nenhuma | Abre o cadastro da primeira modalidade |
| Uma | Entra diretamente no perfil dessa modalidade |
| Duas ou mais | Exibe o seletor de modalidade |

Modalidades arquivadas não são contadas para esse direcionamento.

### Revisão “somente o necessário”

A área foi revisada para manter apenas recursos necessários e operacionais. Permaneceram **Dashboard, Carteirinha, Competições, Resultados e Perfil**. Foram retirados do atleta os atalhos de Comunidade/Desafios e botões futuros sem operação real, como carteira do dispositivo, PDF, sincronização de calendário, exportação, comprovante e filtros avançados. A troca manual entre perfis autenticados também foi desativada: a permissão é definida exclusivamente pelo login.

Para atletas menores, o responsável legal passou a ter cadastro próprio de nome, vínculo, documento, telefone e e-mail. A atualização desses dados não autoriza automaticamente a participação; a autorização depende da validação do documento pelo clube ou federação.

O percentual de completude do perfil e o gráfico de desempenho também foram retirados. A área de resultados permanece objetiva e apresenta apenas registros oficiais homologados. A opção “Perfil esportivo público” foi removida do perfil; a retirada visual isolada já está publicada no commit `d44ab59`, enquanto o restante desta revisão ampliada continua local.

---

## 2. Acesso e identidade do atleta

O atleta possui:

- acesso pelo botão público **ATLETA**;
- login com CPF, documento nacional, registro ou passaporte;
- data de nascimento em formatos flexíveis;
- autenticação com sessão individual;
- registro Apex Combate próprio;
- uma única identidade para todas as artes marciais;
- retorno seguro para a abertura pelo botão **Voltar ao início**, encerrando a sessão;
- documento mascarado nas telas do perfil;
- nome, documento e nascimento protegidos contra alteração comum;
- correção de identidade reservada a um futuro fluxo oficial de validação.

O perfil não solicita país nem WhatsApp no login do atleta, conforme decisão vigente.

---

## 3. Painel autenticado

Depois de autenticado e com uma modalidade selecionada, o atleta possui um painel com:

- saudação e identidade autenticada;
- número de registro;
- situação do registro;
- modalidade ativa;
- graduação atual;
- categoria e peso informado;
- situação da documentação;
- próximo evento ou estado vazio quando não houver inscrição;
- preparação para competição;
- inscrição, pagamento, documentos e professor/técnico;
- atividade recente;
- avisos de pendências;
- acesso rápido às competições;
- acesso rápido à carteirinha digital;
- painel lateral com clube, graduação, próximo evento e notificações;

Todos os dados esportivos do painel mudam de acordo com a modalidade selecionada, sem trocar a pessoa autenticada.

---

## 4. Múltiplas modalidades na mesma conta

Cada modalidade do atleta pode guardar separadamente:

- arte marcial;
- estilo ou vertente;
- graduação ou nível;
- categoria esportiva;
- clube, academia ou dojo;
- professor ou técnico responsável;
- federação ou organização;
- data de início na modalidade;
- situação ativa, pausada ou arquivada;
- definição de modalidade principal;
- certificados vinculados.

### Operações disponíveis

O atleta pode:

- adicionar uma nova modalidade;
- editar os dados esportivos da modalidade;
- definir outra modalidade como principal;
- pausar uma prática;
- arquivar uma modalidade;
- alternar entre modalidades pelo topo do painel;
- acessar uma modalidade diretamente pela lista do perfil.

Arquivar uma modalidade não apaga a pessoa nem cria outra conta.

---

## 5. Dados pessoais e esportivos

### Dados pessoais únicos

- nome completo;
- registro Apex Combate;
- documento de identificação;
- data de nascimento;
- e-mail;
- telefone;
- peso atual;
- contato de emergência;
- telefone de emergência.

### Dados esportivos por modalidade

- modalidade;
- estilo ou vertente;
- graduação;
- categoria atual;
- clube/academia/dojo;
- professor ou técnico;
- federação ou organização;
- situação esportiva;
- data de início.

O peso permanece ligado à pessoa. A categoria, a graduação e os vínculos esportivos pertencem ao contexto de cada modalidade.

---

## 6. Documentos pessoais

O atleta possui uma central de documentos pessoais compartilhados por sua conta:

- documento de identificação;
- atestado médico;
- termo de responsabilidade;
- autorização do responsável para menores;
- nome do arquivo;
- data de emissão;
- data de validade;
- situação de validação;
- observações da análise;
- responsável pela validação, quando disponível.

### Situações documentais

- verificado;
- pendente de análise;
- necessita revisão.

Para atletas menores, a autorização do responsável entra nos requisitos de preparação. Os metadados já são persistidos. O arquivo real deverá usar armazenamento criptografado na etapa de operação em produção.

---

## 7. Certificados por modalidade

Certificados esportivos são separados dos documentos pessoais e vinculados à modalidade correspondente.

O atleta pode cadastrar:

- certificado de graduação;
- certificado de filiação;
- curso ou formação;
- certificação de instrutor/professor;
- certificação de arbitragem.

Cada certificado possui:

- modalidade vinculada;
- título ou graduação;
- entidade emissora;
- código único;
- nome do arquivo;
- emissão;
- validade, quando houver;
- situação de análise;
- endereço de verificação preparado para validação pública.

A carteira e o perfil mostram apenas os certificados da modalidade ativa.

---

## 8. Carteirinha digital

O atleta possui uma carteirinha digital contextualizada pela modalidade selecionada, contendo:

- nome e iniciais do atleta;
- registro Apex Combate;
- situação do registro;
- modalidade;
- graduação;
- clube;
- federação;
- nascimento;
- validade;
- situação de verificação;
- filiação;
- última validação;
- QR visual e endereço de validação;
- certificados da modalidade ativa.

A carteirinha e o quadro de validação federativa exibem a validade até o encerramento do ano corrente. Documentos e certificados preservam seus próprios prazos oficialmente informados.

A emissão de PDF oficial e a integração com carteiras do dispositivo permanecem como operações futuras e não são exibidas ao atleta enquanto não estiverem funcionais.

---

## 9. Competições e inscrições

O atleta possui:

- catálogo de competições;
- busca por nome, cidade ou modalidade;
- filtros de modalidade e inscrições abertas;
- exibição apenas dos eventos compatíveis com a modalidade ativa;
- data, local, taxa, prazo e nível do evento;
- situação das inscrições;
- histórico de inscrições;
- categoria e peso do atleta;
- graduação da modalidade;
- escolha de professor ou técnico elegível;
- envio da inscrição para confirmação;
- acompanhamento de pagamento e situação.

O técnico disponível deve pertencer ao clube e estar credenciado na competição. O atleta não recebe acesso a técnicos sem vínculo autorizado.

### Central de pagamentos

Dentro de Competições, o atleta possui uma central única com:

- taxas de inscrição;
- mensalidades do clube;
- descrição da cobrança;
- tipo da cobrança;
- valor definido pelo servidor;
- vencimento;
- total em aberto;
- próximo vencimento;
- último pagamento;
- situações pendente, vencido, pago, isento, estornado, processando ou cancelado;
- escolha demonstrativa entre PIX, cartão pelo gateway e boleto;
- código de transação;
- comprovante demonstrativo;
- atualização da situação da inscrição e da delegação após confirmação.

A demonstração não movimenta dinheiro e não solicita número de cartão, CVV, senha bancária ou chave pessoal. O valor nunca é aceito do navegador: ele é recuperado da cobrança persistida para impedir alteração pelo atleta. Um atleta também não pode consultar ou pagar cobranças de outra conta. A operação real dependerá de gateway certificado e conformidade financeira.

---

## 10. Preparação para competição

O painel verifica:

- inscrição;
- pagamento;
- documentos obrigatórios;
- definição do professor ou técnico;
- percentual de prontidão;
- pendências documentais;
- pendência de pagamento;
- ausência de técnico;
- próximo evento;
- categoria e graduação usadas na competição.

### Campeonato ao vivo

Dentro de Competições, o atleta autenticado possui uma central operacional para acompanhar:

- sua próxima luta;
- adversário e lado da chave;
- categoria e divisão;
- chave completa organizada por rodada;
- número da luta;
- tatame, ringue ou área;
- horário programado e estimado;
- quantidade de lutas anteriores;
- estados programada, na sequência, chamada, em combate e finalizada;
- fila de chamadas de todas as áreas;
- resultados já publicados na chave;
- avisos oficiais de mudança de horário ou área;
- player de vídeo por tatame, ringue ou área;
- modo de filtro por texto, modalidade, área, situação ou somente a luta do atleta;
- tela cheia e controles nativos de reprodução.

A central atualiza automaticamente a cada 30 segundos e também permite atualização manual. A consulta é somente leitura e exige autenticação. O servidor confirma que o campeonato pertence às inscrições do atleta antes de responder; uma tentativa de consultar campeonato alheio recebe `404`. As informações demonstrativas são identificadas como operação de demonstração até a integração com a mesa oficial responsável pela publicação.

O vídeo permanece sem fonte enquanto não houver câmera e provedor autorizados. O sistema não simula uma luta real. A integração aceita HLS com alternativa progressiva, restringe origens externas por allowlist HTTPS e preserva a política de conteúdo do navegador. A produção ainda depende de URL assinada temporária, direitos de transmissão e consentimento de imagem, com proteção específica para menores.

---

## 11. Resultados, ranking e jornada

### Resultados e ranking

A área já possui composição para:

- pódios;
- vitórias;
- ranking estadual;
- pontos da temporada;
- medalhas;
- histórico homologado;
- súmulas.

Enquanto não há fonte oficial integrada, esses campos permanecem em estado vazio. O Apex Combate não atribui resultados, pontos ou posições inventados a um atleta.

### Referências históricas autorizadas

A área autenticada de Resultados apresenta separadamente duas referências fornecidas e autorizadas pelo proprietário do Apex Combate:

- **João Victor Mozer dos Santos** — chave 1181;
- **João Victor Mozer dos Santos** — chave 1201;
- evento: Primeira Etapa do Campeonato Paranaense de Karatê 2026 — Oeste;
- modalidade: Karatê;
- disciplina: Kumite;
- fonte nominal: `Chave_260_Final.pdf`.

Essas referências não substituem Rafael Martins como conta demonstrativa, não aparecem como resultado do usuário autenticado e não presumem adversário, vitória, colocação, pontuação ou medalha. O sistema registra apenas a participação informada e o consentimento explícito de Mozer para exibição do nome.

### Jornada da modalidade

A jornada usa dados existentes para apresentar:

- início na modalidade;
- turmas ativas;
- professor responsável;
- presenças recentes;
- treinos registrados;
- certificados e graduações;
- atividades da conta;
- marcos esportivos da modalidade selecionada.

---

## 12. Perfil, privacidade e segurança

O atleta possui:

- identificação pessoal protegida;
- contato de emergência privado;
- documentos visíveis somente em operações autorizadas;
- perfil esportivo mantido privado, sem opção de exposição pública;
- separação entre documento pessoal e certificado esportivo;
- isolamento dos dados pelo identificador do atleta;
- sessão autenticada por token temporário;
- revogação do token no servidor ao sair;
- encerramento automático após 20 minutos sem atividade, com aviso dois minutos antes;
- encerramento automático quando a API rejeita uma sessão inválida ou expirada;
- limpeza de tokens, perfis, escopos e dados locais relacionados;
- limite de tentativas por endereço de rede e por identidade;
- mensagem de acesso inválido sem revelar se a conta existe;
- política de segurança de conteúdo no navegador;
- política de referência sem vazamento de endereço;
- bloqueio de objetos e conexões não autorizadas no navegador;
- validação de arquivos PDF ou imagem e coerência das datas de emissão e validade;
- validação de que uma modalidade pertence ao atleta antes de qualquer alteração;
- bloqueio de alteração de modalidade ou certificado de outro atleta;
- trilha de auditoria para atualizações relevantes.

O atleta não possui opção de perfil esportivo público. Documentos, contatos, emergência e dados esportivos pessoais permanecem protegidos na área autenticada.

**Limite da demonstração:** documento e nascimento continuam sendo a identificação de entrada aprovada. Para dados reais em produção, o segundo fator do atleta — código pessoal, código temporário ou a combinação dos dois — ainda precisa ser escolhido por Mozer e implementado antes da operação oficial.

---

## 13. Experiência responsiva

A área do atleta mantém:

- tema escuro oficial;
- logo oficial do Apex Combate;
- composição visual da v44;
- navegação lateral em telas grandes;
- navegação inferior em celulares;
- formulários adaptados para toque;
- tipografia fluida;
- controles com tamanho adequado em dispositivos móveis;
- seletor de modalidade adaptado para celular, tablet e computador;
- cartões reorganizados conforme a largura disponível;
- suporte progressivo para dispositivos antigos sem reduzir a segurança.

---

## 14. Estrutura técnica implementada

### Dados persistentes

- `athletes`: pessoa e conta única;
- `athlete_modalities`: contextos esportivos vinculados à pessoa;
- `athlete_documents`: documentos pessoais;
- `athlete_certificates`: certificados vinculados à modalidade;
- `athlete_guardians`: responsáveis;
- inscrições, turmas e presenças já relacionadas ao atleta.

### APIs do atleta

- `POST /api/login/atleta` — autenticação e decisão do fluxo pós-login;
- `GET /api/athlete/dashboard` — painel completo com modalidade ativa;
- `POST /api/athlete/profile` — atualização de contato, peso, categoria e emergência;
- `POST /api/athlete/modalities` — criação e edição de modalidades;
- `POST /api/athlete/documents` — envio de metadados documentais;
- `POST /api/athlete/certificates` — certificado ligado à modalidade;
- `POST /api/athlete/payments/pay` — confirmação demonstrativa de cobrança pertencente ao atleta;
- `POST /api/registrations` — inscrição em competição e geração da taxa correspondente.

---

## 15. Contas demonstrativas atuais

### Rafael Martins

- três modalidades na mesma conta;
- Jiu-jítsu — modalidade principal e ativa;
- Judô — ativa;
- Karatê Shotokan — pausada;
- seletor exibido depois do login.

### Beatriz Nunes

- uma modalidade: Muay Thai;
- entrada direta no perfil, sem seletor.

### Enzo Costa

- uma modalidade: Judô;
- perfil de menor com responsável e autorização documental;
- entrada direta no perfil.

---

## 16. Situação de cada recurso

| Recurso | Situação |
|---|---|
| Identidade e login do atleta | Implementado |
| Conta única com várias modalidades | Implementado localmente |
| Fluxo pós-login 0/1/2+ | Implementado localmente |
| Dados pessoais e emergência | Implementado |
| Dados esportivos por modalidade | Implementado localmente |
| Clube, professor e organização por modalidade | Implementado localmente |
| Documentos e validação | Implementado como fluxo demonstrativo persistente |
| Certificados por modalidade | Implementado localmente |
| Carteirinha contextual | Implementada |
| Competições e inscrições | Implementadas no fluxo demonstrativo |
| Taxas de competição, mensalidades e comprovantes | Central demonstrativa implementada; gateway real pendente |
| Prontidão para competir | Implementada |
| Jornada esportiva | Implementada com dados disponíveis |
| Segurança de sessão, isolamento e navegador | Implementada na base demonstrativa |
| Segundo fator do atleta | Obrigatório para produção; método pendente de escolha |
| Resultados e ranking oficiais | Estrutura pronta; integração oficial pendente |
| PDF oficial e carteira do dispositivo | Operação oficial pendente |
| Armazenamento criptografado dos arquivos | Produção pendente |
| Publicação do novo conjunto do atleta | Pendente de revisão e autorização de Mozer |

---

## 17. Validação realizada

- verificador estático do projeto aprovado;
- JavaScript validado sem erro de sintaxe;
- Python compilado sem erro;
- 50 testes automatizados aprovados;
- autenticação com uma e várias modalidades testada;
- seleção e troca de modalidade testadas;
- criação de modalidade testada;
- cadastro de certificado testado;
- mensalidade demonstrativa confirmada sem aceitar alteração de valor do navegador;
- geração automática de taxa após nova inscrição testada;
- comprovante e atualização da inscrição testados;
- bloqueio de pagamento de outra conta testado com resposta 404;
- recarregamento do painel por modalidade testado;
- bloqueio entre contas testado com respostas 401 e 404;
- prévia responsiva local em funcionamento.

---

## 18. Conclusão

O atleta possui uma área completa de demonstração, organizada ao redor de uma identidade única e capaz de representar várias artes marciais sem duplicar contas. O perfil integra dados pessoais, modalidades, graduação, categoria, vínculos esportivos, documentação, certificados, carteirinha, competições, campeonato ao vivo, pagamentos demonstrativos, preparação e jornada.

Os recursos que dependem de autoridade externa — resultados homologados, ranking oficial, armazenamento definitivo de arquivos, PDF verificável e carteira do dispositivo — permanecem claramente identificados como integrações futuras, sem dados fictícios.

O conjunto ampliado está concluído no ambiente local de revisão e ainda não foi publicado no repositório oficial ou no Render.
