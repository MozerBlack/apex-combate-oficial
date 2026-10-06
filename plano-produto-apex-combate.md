# 🥋 Apex Combate — Plataforma Universal de Artes Marciais

## Plano de Produto

> **Nome definido:** Apex Combate  
> **Proprietário:** Mozer  
> **Conceito:** plataforma universal “Tudo em um” que conecta atletas e alunos, clubes/dojôs/academias, técnicos de competição e federações de artes marciais.  
> **Status:** protótipo funcional v40 com título institucional, apresentação pública, login em etapa separada e backend local persistente. A disponibilidade jurídica da marca, do domínio e dos identificadores sociais deverá ser verificada antes do lançamento.
> **Fonte principal:** consulte `documentacao-mestre-apex-combate.md` para decisões vigentes.

**Repositório oficial:** `https://github.com/MozerBlack/apex-combate-oficial`  
**Demonstração online:** `https://apex-combate-demo.onrender.com`

### Entrega v40

A v40 oficializa e aplica o título institucional **“🥋 Apex Combate — Plataforma Universal de Artes Marciais”** na abertura pública e na documentação principal, preservando **“Uma plataforma. Todas as lutas.”** como assinatura do produto.

### Entrega v39

A v39 acrescenta uma experiência pública anterior à autenticação:

- boas-vindas e apresentação da proposta do Apex Combate;
- explicação concisa do fluxo integrado;
- visão dos grupos ATLETA, CLUBE e FEDERAÇÃO sem criar novo perfil;
- avanço para o login exclusivamente por botão, sem transição automática;
- retorno às boas-vindas após logout;
- tradução real e layout adaptado de celulares compactos a TVs.

### Entrega v38

A v38 transforma as áreas de atleta e clube em fluxos persistentes e integrados:

- perfil, peso, categoria e emergência do atleta;
- documentos e prontidão esportiva;
- responsáveis para menores;
- turmas, matrículas e presenças;
- cadastro e situação de alunos;
- delegações e pendências por competição;
- atualização cruzada entre atleta e clube;
- auditoria das operações;
- testes automatizados ponta a ponta.

---

## 1. Resumo executivo

O **Apex Combate** será um ecossistema digital para modalidades como jiu-jítsu, judô, karatê, muay thai, boxe, taekwondo, kung fu, wrestling, capoeira, kickboxing, MMA e outras.

A plataforma reunirá cinco necessidades hoje normalmente separadas:

1. **Encontrar** academias, professores, aulas e eventos;
2. **Treinar** com planos, técnicas, metas e histórico;
3. **Evoluir** acompanhando presença, graduação e desempenho;
4. **Gerenciar** academias, turmas, alunos e cobranças;
5. **Conectar** a comunidade por meio de conteúdo, desafios e competições.

### Proposta de valor

> **Toda a jornada marcial em um único aplicativo — da primeira aula à competição.**

### Diferencial central

O sistema não será limitado a uma única modalidade. Ele terá um **motor de progressão configurável**, capaz de representar:

- faixas, cordas, graus, dans, níveis ou categorias;
- regras específicas de cada modalidade, federação ou academia;
- treinos técnicos, físicos, sparring, formas/katas e competição;
- múltiplas modalidades no mesmo perfil de atleta.

---

## 2. Problema que o produto resolve

### Para atletas e alunos

- Dificuldade para encontrar uma academia adequada;
- Histórico de treino e graduação espalhado ou inexistente;
- Falta de clareza sobre evolução e objetivos;
- Informações de aulas, campeonatos e seminários dispersas;
- Pouca integração entre praticantes de modalidades diferentes.

### Para professores e academias

- Gestão manual de alunos, presença, turmas e graduações;
- Comunicação fragmentada em grupos de mensagens;
- Dificuldade para atrair e converter novos alunos;
- Cobrança e controle de mensalidades pouco organizados;
- Falta de indicadores sobre retenção e ocupação das turmas.

### Para federações

- Cadastro de clubes, academias e atletas distribuído em sistemas separados;
- Dificuldade para validar filiações, graduações, certificados e licenças;
- Organização de competições, inscrições, categorias e resultados fragmentada;
- Falta de uma visão consolidada sobre modalidades, regiões e entidades filiadas.

---

## 3. Públicos e perfis de acesso

| Grupo visível | Pessoas incluídas | Recursos prioritários |
|---|---|---|
| Atletas e alunos | Iniciantes, praticantes recreativos e competidores | Busca, agenda, check-in, metas, graduação, eventos e histórico |
| Clubes, dojôs e academias, professores e técnicos | Gestores, coordenadores, professores, técnicos e equipe autorizada | Administração do clube para gestores; assistência de competição estritamente limitada para técnicos |
| Federações | Dirigentes e equipe federativa autorizada | Filiados, registros, graduações, certificações, competições e homologações |

Uma pessoa poderá acumular funções autorizadas dentro de um grupo. No segundo grupo existem contas internas diferentes. A conta administrativa pode gerir a organização; a subconta `CLUB_TECHNICIAN` é exclusivamente destinada à assistência de atletas durante competições e permanece bloqueada para alunos gerais, turmas, financeiro e administração.

---

## 4. Pilares do produto

### 4.1 Descoberta

- Busca por modalidade, cidade, distância, nível e faixa de preço;
- Mapa de academias e eventos;
- Perfil verificado de academias e professores;
- Horários, estrutura, avaliações e aula experimental;
- Filtros de acessibilidade, faixa etária e aulas femininas ou inclusivas.

### 4.2 Treino e evolução

- Perfil marcial com múltiplas modalidades;
- Linha do tempo de graduações;
- Check-in em aulas;
- Diário de treino;
- Metas semanais e sequências de frequência;
- Biblioteca de técnicas, planos e conteúdos;
- Registro de competições, resultados e conquistas;
- Indicadores pessoais sem comparações inadequadas entre modalidades.

### 4.3 Gestão de academia

- Cadastro de unidades, professores, turmas e horários;
- Matrículas e aula experimental;
- Lista de presença e check-in por QR Code;
- Avaliação e promoção de graduação;
- Mensagens e avisos por turma;
- Planos, mensalidades e situação de pagamento;
- Painel com retenção, ocupação e novos interessados.

### 4.4 Comunidade

- Feed por interesses e modalidades;
- Perfis de atletas, professores e academias;
- Publicações com texto, foto e vídeo;
- Grupos por academia, modalidade ou evento;
- Desafios de consistência e metas;
- Denúncia, bloqueio e moderação;
- Regras rígidas contra humilhação, incentivo à violência e conteúdo perigoso.

### 4.5 Eventos e competições

- Calendário de campeonatos, seminários e graduações;
- Inscrição e pagamento;
- Categorias por idade, peso, sexo, nível e modalidade;
- Check-in, pesagem e status do participante;
- Chaves, confrontos e resultados;
- Histórico no perfil do atleta;
- Página pública e transmissão por link quando disponível.

---

## 5. Escopo recomendado para o MVP

Construir tudo ao mesmo tempo aumentaria muito o custo e atrasaria a validação. O MVP deve provar três hipóteses:

1. Atletas desejam registrar e acompanhar sua jornada marcial;
2. Academias ganham valor ao organizar aulas e alunos na plataforma;
3. A descoberta de academias gera novos contatos e aulas experimentais.

### Incluído no MVP

#### Aplicativo do aluno

- Cadastro e login;
- Perfil com foto, cidade e modalidades;
- Busca e perfil de academias;
- Solicitação de aula experimental;
- Agenda de aulas;
- Check-in por QR Code;
- Histórico de presença;
- Graduação e conquistas;
- Diário simples de treino;
- Notificações importantes.

#### Área do professor/academia

- Criação do perfil da academia;
- Cadastro de modalidades, turmas e horários;
- Convite e gestão básica de alunos;
- Confirmação de presença;
- Registro de graduação;
- Avisos para turmas;
- Painel básico de frequência e interessados.

#### Administração interna da plataforma (não é um perfil público)

- Gestão de usuários e academias;
- Verificação manual de professores e academias;
- Moderação de conteúdo e denúncias;
- Cadastro inicial de modalidades e sistemas de graduação;
- Métricas essenciais do produto.

### Fora do MVP, mas preparado para fases seguintes

- Feed social completo;
- Chat individual;
- Streaming de aulas;
- Aplicativo comercial separado conectado ao Apex Combate para lojas, catálogo, estoque, pedidos, vendas e repasses;
- Marketplace de compra exibido futuramente no Apex Combate;
- Gestão financeira e repasse avançado;
- Chaves automáticas de campeonatos;
- Rankings globais;
- Recomendações de treino por inteligência artificial;
- Integração com relógios e dispositivos de saúde.

---

## 6. Estrutura de navegação do MVP

### Aplicativo do aluno

1. **Início** — próximas aulas, progresso e avisos;
2. **Explorar** — academias, professores e modalidades;
3. **Treinos** — agenda, check-in, diário e histórico;
4. **Jornada** — graduações, metas e conquistas;
5. **Perfil** — dados, modalidades, privacidade e configurações.

### Painel administrativo do clube/dojô/academia

1. **Visão geral**;
2. **Agenda e turmas**;
3. **Alunos**;
4. **Presenças**;
5. **Graduações**;
6. **Interessados**;
7. **Delegações e credenciamento de técnicos**;
8. **Financeiro e configurações**.

### Área privada do técnico de competição

1. **Competição atribuída**;
2. **Atletas atribuídos**;
3. **Fila de lutas e linha do tempo**;
4. **Pesagem, equipamentos e checklist**;
5. **Aquecimento e corner**;
6. **Credencial QR**;
7. **Avisos, regras, ocorrências e suporte**.

O técnico não acessa os módulos administrativos do clube.

### Painel da federação

1. **Visão federativa**;
2. **Clubes e academias filiadas**;
3. **Registro de atletas**;
4. **Graduações e certificações**;
5. **Competições e calendário oficial**;
6. **Homologações**;
7. **Relatórios regionais e por modalidade**;
8. **Conformidade documental**.

---

## 7. Telas prioritárias

### Aluno

1. Boas-vindas e escolha de objetivos;
2. Seleção de modalidades;
3. Criação de perfil;
4. Tela inicial;
5. Exploração com mapa e lista;
6. Perfil da academia;
7. Solicitação de aula experimental;
8. Agenda;
9. Leitor de QR Code;
10. Diário de treino;
11. Jornada de graduação;
12. Perfil e privacidade.

### Academia/professor

1. Cadastro e verificação;
2. Painel principal;
3. Criar turma;
4. Agenda semanal;
5. Lista de alunos;
6. Chamada/check-in;
7. Perfil do aluno;
8. Registrar graduação;
9. Publicar aviso;
10. Lista de interessados.

### Federação

1. Painel de indicadores federativos;
2. Cadastro e situação dos filiados;
3. Registro esportivo de atletas;
4. Validação de graduações e certificações;
5. Homologação de eventos;
6. Relatórios e auditoria de ações.

---

## 8. Fluxos essenciais

### Fluxo A — encontrar uma academia

Cadastro → escolher modalidade → permitir localização ou informar cidade → aplicar filtros → visualizar academia → consultar horários → solicitar aula experimental → receber confirmação → comparecer e fazer check-in.

### Fluxo B — acompanhar evolução

Entrar em uma turma → realizar check-ins → registrar observações no diário → cumprir meta semanal → receber avaliação do professor → visualizar nova graduação na linha do tempo.

### Fluxo C — academia recebe um novo aluno

Criar perfil → publicar turmas → receber solicitação → confirmar aula experimental → registrar presença → convidar para matrícula → acompanhar frequência.

### Fluxo D — registrar graduação

Professor seleciona aluno → escolhe modalidade e sistema → informa nova graduação → adiciona data e observação → aluno confirma recebimento → registro aparece no histórico.

---

## 9. Regras para suportar todas as modalidades

A universalidade deve vir da arquitetura, não de uma lista fixa de faixas.

### Estrutura configurável

- **Modalidade:** jiu-jítsu, boxe, judô etc.;
- **Organização:** federação, associação ou academia;
- **Sistema de progressão:** faixa, grau, nível, corda, dan ou sem graduação;
- **Etapas:** progressão ordenada e requisitos opcionais;
- **Categorias:** idade, peso, nível e regras específicas;
- **Tipo de sessão:** técnica, físico, sparring, formas, defesa pessoal ou competição;
- **Conquistas:** graduação, participação, pódio, certificação ou meta interna.

A academia poderá usar um modelo oficial existente ou configurar sua própria progressão, sempre identificada como **“padrão da academia”** para evitar confusão com certificações oficiais.

---

## 10. Modelo de negócio

### Plano gratuito para praticantes

- Perfil marcial;
- Busca de academias;
- Agenda e check-ins;
- Histórico básico;
- Participação em eventos e desafios gratuitos.

### Plano Premium para praticantes

- Estatísticas avançadas;
- Metas e relatórios;
- Diário ilimitado;
- Conteúdo exclusivo;
- Descontos de parceiros;
- Exportação do histórico.

### Assinatura para academias

| Plano | Indicação | Recursos |
|---|---|---|
| Inicial | Academia pequena | Turmas, alunos, presença e perfil público |
| Profissional | Operação em crescimento | Automação, relatórios, cobranças e equipe |
| Rede | Múltiplas unidades | Gestão centralizada, permissões e indicadores consolidados |

### Receitas futuras

- Taxa sobre inscrição em eventos;
- Comissão por planos ou aulas vendidos;
- Comissão do marketplace conectado ao aplicativo separado dos lojistas;
- Conteúdo patrocinado claramente identificado;
- Soluções para federações e redes de academias.

**Recomendação:** não cobrar de atletas no início. A primeira receita deve vir de academias, após comprovação de ganho operacional e geração de novos alunos.

---

## 11. Tecnologia recomendada

### Estratégia de plataforma

- **Entregáveis móveis oficiais:** APK/AAB para Android e aplicativo iOS para distribuição por TestFlight/App Store;
- **Empacotamento recomendado:** base web responsiva encapsulada com Capacitor, preservando PWA, modo offline e integrações nativas;
- **Painel web responsivo:** mesma experiência adaptável para professores, técnicos, clubes, dojôs, academias, federações, computadores e TVs;
- **iPhone e iPad:** build iOS assinado, TestFlight para demonstrações e App Store para distribuição pública;
- **Regra de acesso:** o APK Android é entrega obrigatória, mas nenhum usuário será obrigado a instalá-lo; navegador e PWA continuarão disponíveis;
- **Backend:** API em TypeScript;
- **Banco:** PostgreSQL;
- **Autenticação e arquivos:** serviços próprios ou provedores gerenciados compatíveis com a arquitetura, sem Supabase;
- **Notificações:** push, e-mail e avisos internos;
- **Pagamentos no Brasil:** provedor compatível com Pix, cartão e recorrência;
- **Mapas:** provedor escolhido conforme preço, cobertura e termos de uso;
- **Mídia:** armazenamento de imagens e vídeos com processamento seguro.

### Princípios técnicos

- Um único cadastro com múltiplos papéis;
- API preparada para web e celular;
- Permissões por função e academia;
- Registro de auditoria para graduações, pagamentos e ações administrativas;
- Conteúdo e sistemas de graduação configuráveis;
- Internacionalização desde a base, começando em português do Brasil;
- Acessibilidade e funcionamento adequado em conexões móveis instáveis.

---

## 12. Modelo de dados inicial

Entidades principais:

- Usuário;
- Perfil marcial;
- Papel/permissão;
- Modalidade;
- Organização ou federação;
- Sistema e etapa de graduação;
- Academia e unidade;
- Professor;
- Turma e sessão de aula;
- Matrícula;
- Presença/check-in;
- Diário de treino;
- Meta e conquista;
- Avaliação e graduação;
- Interessado/aula experimental;
- Evento e inscrição;
- Publicação, comentário e denúncia;
- Plano, assinatura e pagamento;
- Notificação;
- Registro de auditoria.

---

## 13. Segurança, confiança e aspectos legais

### LGPD e privacidade

- Consentimento claro e específico;
- Coleta apenas dos dados necessários;
- Possibilidade de baixar e excluir dados;
- Política de retenção;
- Controle sobre visibilidade de perfil e histórico;
- Contratos adequados com fornecedores de dados.

### Menores de idade

- Conta vinculada a responsável legal;
- Perfil privado por padrão;
- Restrições de mensagens e localização;
- Consentimento para imagem e participação em eventos;
- Ferramentas de denúncia acessíveis.

### Segurança marcial

- Avisos de que técnicas devem ser praticadas com supervisão qualificada;
- Proibição de conteúdo que incentive agressão fora de contexto esportivo ou educacional;
- Sinalização de conteúdo avançado ou de risco;
- Informações de saúde tratadas como dados sensíveis;
- O aplicativo não substitui orientação médica ou profissional.

### Confiança

- Verificação de academias e professores;
- Identificação da origem de cada graduação;
- Histórico de alterações e revogações;
- Avaliações somente após interação comprovada;
- Moderação humana com apoio automatizado, nunca apenas automatizada.

---

## 14. Identidade e experiência

### Personalidade da marca

- Disciplinada, inclusiva e respeitosa;
- Moderna sem apagar as tradições;
- Competitiva sem ser agressiva;
- Universal sem misturar indevidamente regras e graduações.

### Direção visual sugerida

- Base escura ou neutra com alto contraste;
- Cor de destaque energética, como vermelho coral ou laranja;
- Tipografia forte e legível;
- Ícones próprios para treino, graduação, eventos e comunidade;
- Fotografias autênticas de diferentes modalidades, idades, corpos e gêneros.

### Ideias de slogan

- **Sua jornada marcial em um só lugar.**
- **Treine. Evolua. Conecte-se.**
- **Todas as artes, uma comunidade.**

---

## 15. Métricas de sucesso

### Aquisição

- Novos usuários por semana;
- Academias cadastradas e verificadas;
- Custo por novo usuário e nova academia;
- Solicitações de aula experimental.

### Ativação

- Percentual que conclui o perfil;
- Percentual que seleciona uma modalidade;
- Primeiro check-in em até sete dias;
- Academia que cria sua primeira turma.

### Engajamento

- Usuários ativos semanais e mensais;
- Check-ins por atleta;
- Metas concluídas;
- Aulas frequentadas;
- Retorno em 7, 30 e 90 dias.

### Valor para academias

- Novos interessados recebidos;
- Conversão de aula experimental em matrícula;
- Ocupação das turmas;
- Retenção de alunos;
- Horas administrativas economizadas.

### Receita

- Academias pagantes;
- Receita recorrente mensal;
- Conversão do teste para assinatura;
- Cancelamentos;
- Receita média por academia.

### Métrica norteadora

> **Número de treinos válidos registrados por atletas ativos por semana.**

Essa métrica conecta o produto ao comportamento mais importante: pessoas treinando com consistência.

---

## 16. Roadmap proposto

### Fase 0 — descoberta e validação (2 a 3 semanas)

- Entrevistar atletas de pelo menos cinco modalidades;
- Entrevistar professores e donos de academias de portes diferentes;
- Mapear processos atuais;
- Validar interesse, dores e disposição de pagamento;
- Definir modalidade e cidade piloto;
- Testar nome e posicionamento.

### Fase 1 — protótipo (2 a 4 semanas)

- Fluxos de aluno e academia;
- Protótipo navegável;
- Testes de usabilidade;
- Ajustes de proposta e navegação;
- Página de espera para captar interessados.

### Fase 2 — MVP técnico (10 a 14 semanas)

- Cadastro e perfis;
- Academias, turmas e agenda;
- Busca e aula experimental;
- Check-in e presença;
- Graduação e jornada;
- Painel administrativo;
- Testes, segurança e publicação piloto.

### Fase 3 — piloto controlado (6 a 8 semanas)

- Lançar em uma cidade ou região;
- Integrar de 5 a 15 academias parceiras;
- Acompanhar suporte e comportamento de uso;
- Corrigir fricções;
- Medir retenção e valor para as academias.

### Fase 4 — expansão

- Cobranças e assinaturas;
- Eventos e competições;
- Comunidade e desafios;
- Novas cidades, idiomas e países;
- Integrações com o aplicativo comercial separado e marketplace de compra no Apex Combate.

---

## 17. Estratégia de lançamento

### Cidade piloto sugerida

Começar em uma única região, com densidade suficiente de academias. Uma opção natural é **Curitiba e Região Metropolitana**, antes da expansão nacional.

### Aquisição inicial

- Academias fundadoras com benefícios vitalícios ou por prazo definido;
- Embaixadores de modalidades diferentes;
- QR Codes físicos nas academias;
- Desafio coletivo de frequência;
- Calendário regional gratuito de eventos;
- Perfil público compartilhável de academia e atleta;
- Parcerias com campeonatos e seminários locais.

### Critério para expandir

Expandir apenas quando o piloto demonstrar:

- uso recorrente de check-in;
- adesão dos professores;
- retenção de atletas;
- conversão de interessados em aulas experimentais;
- disposição real das academias para pagar.

---

## 18. Principais riscos e mitigação

| Risco | Mitigação |
|---|---|
| Escopo grande demais | MVP com três jornadas e roadmap por fases |
| Diferenças entre modalidades | Motor configurável e especialistas por modalidade |
| Professores não adotarem | Check-in rápido, implantação assistida e benefício imediato |
| Baixa densidade de usuários | Lançamento concentrado por cidade e academias parceiras |
| Graduações falsas | Fonte identificada, verificação e auditoria |
| Comunidade tóxica | Regras, denúncia, bloqueio e moderação ativa |
| Risco com menores | Conta de responsável e privacidade por padrão |
| Custo alto de vídeo | Adiar vídeo pesado e aplicar limites de armazenamento |
| Complexidade do marketplace | Manter comércio em aplicativo e backend separados, entregando primeiro o valor esportivo |

---

## 19. Decisões vigentes

1. O nome oficial é **Apex Combate** e Mozer é o proprietário;
2. O posicionamento é “Tudo em um” para todas as modalidades;
3. Existem exatamente três grupos públicos: ATLETA, CLUBE e FEDERAÇÃO;
4. Técnicos usam subconta individual pelo perfil CLUBE e atuam somente durante competições;
5. A federação é o cérebro operacional e a arquitetura suporta múltiplas federações;
6. A Apex Central proprietária de Mozer será construída posteriormente e permanece desabilitada;
7. Supabase não será utilizado;
8. O aplicativo principal é responsivo e traduzível; os entregáveis móveis finais são APK/AAB para Android e aplicativo iOS por TestFlight/App Store, sem abandonar a versão PWA universal;
9. O marketplace será ligado ao Apex Combate, mas produtos e vendas serão administrados por um segundo aplicativo para lojistas;
10. O nome oficial desse segundo produto é **Apex’s Forge**.

O histórico completo está em `registro-de-decisoes-apex-combate.md`.

---

## 20. Próximos passos recomendados

1. Validar a v38 com atletas, clubes, técnicos e uma federação piloto;
2. Migrar a fundação local para infraestrutura de produção com PostgreSQL, HTTPS, segredos e OTP real;
3. Completar notificações, documentos, auditoria e operação real de eventos;
4. Executar um piloto de competição em Curitiba;
5. Medir usabilidade da área técnica em celular e conexão instável;
6. Planejar a Central proprietária de Mozer em ambiente interno separado;
7. Definir identidade derivada, modelo de receita e regras do Apex’s Forge;
8. Construir o backend comercial separado e depois integrar catálogo e compra ao Apex Combate.

A documentação mestre em `documentacao-mestre-apex-combate.md` deve acompanhar todas as próximas alterações.
