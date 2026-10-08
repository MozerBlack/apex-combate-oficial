# 🥋 Apex Combate — Plataforma Universal de Artes Marciais

## Documentação Completa e Unificada

**Proprietário:** Mozer  
**Produto principal:** Apex Combate  
**Produto comercial conectado:** Apex’s Forge  
**Central proprietária futura:** Apex Central  
**Versão documentada:** v44
**Data de consolidação:** 7 de outubro de 2026
**Status:** documento único oficial do ecossistema  
**Repositório oficial:** `https://github.com/MozerBlack/apex-combate-oficial`  
**Demonstração online:** `https://apex-combate-demo.onrender.com`

> Este arquivo reúne em um único lugar todas as definições de produto, identidade, autenticação, perfis, permissões, governança, arquitetura, APIs, compatibilidade, aplicativo comercial e decisões oficiais. Em caso de divergência, prevalece a instrução mais recente e explícita de Mozer.

### Entrega funcional v44

- controle **Voltar ao início** no cabeçalho autenticado compartilhado por atleta, clube, técnico e federação;
- encerramento seguro da sessão antes do retorno à abertura pública, com remoção de tokens, perfil, escopos e caches locais relacionados;
- rótulo textual em telas amplas, ícone de início acessível em telas compactas, alvo de toque ampliado e escala própria para TVs;
- escala tipográfica fluida e reutilizável com `clamp()`, `rem` e limites controlados;
- textos funcionais de 6–9 px elevados a patamares legíveis em toda a plataforma;
- formulários móveis com texto mínimo de 16 px para evitar zoom automático no iPhone;
- progressão de leitura entre celulares, tablets, notebooks, desktops, monitores grandes e TVs sem detecção de modelo;

- cabeçalho da tela de login reduzido a um tradutor flutuante e discreto, sem faixa visual;
- logo superior auxiliar, links institucionais e botão superior **Entrar** removidos do login;
- logo oficial, três acessos e autenticação do cartão central preservados;
- faixa superior da apresentação removida para iniciar diretamente no conteúdo principal;
- ações **Entrar no Apex** e **Como funciona** preservadas no hero;
- título institucional **“🥋 Apex Combate — Plataforma Universal de Artes Marciais”** aplicado na abertura e na documentação;
- assinatura **“Uma plataforma. Todas as lutas.”** preservada;
- apresentação pública de boas-vindas antes da autenticação;
- proposta “Uma plataforma. Todas as lutas.” e explicação de como o ecossistema funciona;
- avanço para o login somente por botão, sem transição automática;
- retorno à apresentação depois do logout;
- tradução efetiva e responsividade da entrada pública de 320 px a TVs;
- preservação da composição oficial com exatamente ATLETA, CLUBE e FEDERAÇÃO;
- perfil completo do atleta com peso, categoria, contatos e emergência;
- documentos esportivos com situação e prontidão calculadas;
- responsáveis vinculados para atletas menores;
- turmas do clube com professor, horário, capacidade e local;
- matrículas e presença auditável;
- alunos sincronizados com documentos e último check-in;
- delegações por competição com prontidão individual;
- APIs e banco persistente para todos esses fluxos;
- testes unitários, contratos, smoke test e fluxo integrado v38;
- implantação contínua por GitHub e Render.

---

## Índice geral

1. Visão mestre e estado atual;
2. Plano completo do produto;
3. Identidade visual;
4. Perfis e permissões;
5. Sistema de login;
6. Backend, banco e APIs;
7. Compatibilidade, responsividade e PWA;
8. Apex Central de Mozer;
9. Apex’s Forge;
10. Registro oficial de decisões.

---

## Significado oficial dos nomes do ecossistema

### Apex Combate

#### Significado de “Apex”

**Apex** é uma palavra de origem latina que significa o ponto mais alto, o topo, o auge ou o nível máximo que alguém pode alcançar. No universo marcial, representa evolução contínua, excelência técnica, disciplina e a busca pela melhor versão de si mesmo.

#### Significado de “Combate”

**Combate** identifica claramente o universo das artes marciais e dos esportes de luta. Na marca, não significa violência fora do esporte. Representa confronto regulamentado, técnica, estratégia, preparação, respeito e superação.

#### Significado completo

**Apex Combate** significa alcançar o ponto mais alto da jornada dentro do universo marcial. O nome conecta atletas, clubes, técnicos e federações à ideia de evolução até o próprio ápice.

#### Por que esse nome foi escolhido

- é forte e fácil de memorizar;
- comunica evolução, desempenho e excelência;
- deixa clara a ligação com artes marciais e esportes de combate;
- não limita o produto a uma única modalidade;
- funciona para iniciantes e competidores profissionais;
- possui potencial nacional e internacional;
- combina com o posicionamento “Tudo em um”;
- permite criar uma família de produtos conectados sob a marca Apex.

#### Assinatura

> **Uma plataforma. Todas as lutas.**

A assinatura reforça que diferentes modalidades, níveis e organizações podem conviver em um mesmo ecossistema sem perder suas regras e identidades.

### Apex’s Forge

#### Significado de “Apex’s”

**Apex’s** significa “da Apex” ou “pertencente ao ecossistema Apex”. A expressão cria uma ligação imediata com o Apex Combate e mostra que o aplicativo comercial pertence à mesma família, embora possua operação, login e finalidade próprios.

#### Significado de “Forge”

**Forge** significa **forja** em inglês. A forja é o lugar onde matérias-primas são transformadas, por trabalho, técnica, pressão e precisão, em algo forte, valioso e preparado para cumprir sua função.

No contexto comercial, representa o ambiente em que o lojista:

- constrói sua marca;
- transforma produtos em catálogo profissional;
- organiza estoque e operação;
- desenvolve vendas;
- fortalece o relacionamento com clientes;
- eleva seu negócio dentro do ecossistema marcial.

#### Significado completo

**Apex’s Forge** significa **A Forja da Apex**: a central comercial em que lojas e marcas constroem, organizam e fortalecem seus negócios conectados ao Apex Combate.

#### Por que esse nome foi escolhido

- é marcante, forte e diferente de nomes genéricos de loja;
- mantém vínculo direto com a marca Apex;
- combina com transformação, resistência e disciplina;
- representa construção e crescimento, não apenas venda;
- permite evoluir de painel de loja para ecossistema comercial completo;
- possui sonoridade premium e internacional;
- diferencia o aplicativo do lojista do aplicativo esportivo;
- funciona para lojas, marcas, fabricantes, clubes e federações.

#### Slogan de trabalho

> **Forje sua marca. Eleve seu negócio.**

“Forje sua marca” representa construção, identidade e fortalecimento. “Eleve seu negócio” conecta o crescimento comercial à ideia de Apex: chegar ao ponto mais alto.

### Apex Central

#### Significado de “Apex”

Na Central, **Apex** representa o nível mais alto de visão e governança do ecossistema. É a camada proprietária posicionada acima das operações das federações.

#### Significado de “Central”

**Central** representa o núcleo privado de comando, inteligência, segurança e administração estratégica. É o ambiente em que o proprietário acompanha e governa o ecossistema completo.

#### Significado completo

**Apex Central** significa a central máxima de comando do ecossistema Apex: o ambiente proprietário de Mozer, posicionado acima das federações para governança global, segurança, suporte e evolução da plataforma.

#### Por que esse nome foi escolhido

- mantém ligação direta com a marca Apex Combate;
- comunica autoridade, organização e visão global;
- deixa clara sua posição acima das federações;
- funciona como nome de uma central privada de comando;
- permite administrar futuramente países, federações, planos, segurança e operação geral;
- diferencia a governança proprietária da operação diária dos demais perfis;
- é simples, forte e fácil de compreender.

#### Diferença para a Central da Federação

- **Apex Central:** pertence a Mozer e governa o ecossistema completo;
- **Central da Federação:** pertence à própria federação e opera somente sua rede, clubes, atletas e eventos;
- a Central da Federação não possui autoridade proprietária sobre o Apex Combate;
- as duas centrais não compartilham conta, token, rota ou permissões;
- a Apex Central continua planejada para uma fase futura e está desabilitada na versão atual.

### Relação entre os nomes

- **Apex Combate** é o ecossistema esportivo e institucional;
- **Apex’s Forge** é o motor comercial conectado;
- **Apex Central** é a futura central proprietária de governança global;
- “Apex” une os três produtos pela ideia de alcançar e administrar o ponto mais alto;
- “Combate” identifica a jornada marcial;
- “Forge” identifica a construção e o fortalecimento dos negócios;
- “Central” identifica comando, inteligência, segurança e visão geral.

## Requisito obrigatório de compatibilidade universal

O Apex Combate deve funcionar de forma responsiva e adaptável em qualquer categoria moderna de dispositivo:

- celulares Android e iPhone;
- tablets Android e iPad;
- notebooks;
- computadores Windows, macOS e Linux;
- monitores Full HD, QHD e 4K;
- TVs e telas grandes utilizadas em competições;
- orientação retrato e paisagem;
- interação por toque, mouse, teclado e controle remoto compatível;
- instalação como PWA quando suportada;
- operação em conexões instáveis, com suporte offline nos fluxos críticos.

### Princípios de implementação

- mobile-first com expansão progressiva para telas maiores;
- componentes fluidos, sem larguras fixas que quebrem o layout;
- navegação inferior em celulares e lateral em telas maiores;
- áreas de toque adequadas;
- textos legíveis à distância em TVs;
- foco visível para teclado e controle remoto;
- suporte a áreas seguras, notch e barras do sistema;
- imagens e recursos locais para evitar dependência de CDN;
- carregamento progressivo e redução de consumo em redes móveis;
- funcionamento degradado e compreensível quando um recurso avançado não estiver disponível.

### Compatibilidade com versões móveis antigas

O projeto buscará a maior cobertura móvel possível sem reduzir a segurança dos usuários:

| Nível | Dispositivos | Experiência |
|---|---|---|
| Completo | Android e iOS/iPadOS com navegadores modernos e atualizados | Todos os módulos, PWA, offline, notificações e recursos avançados |
| Estendido | Versões antigas ainda capazes de executar HTML5, HTTPS e JavaScript compatível | Fluxos principais, com menos animações, efeitos, gráficos e processamento local |
| Legado | Sistemas muito antigos, navegadores integrados e aparelhos com pouca memória | Modo leve quando tecnicamente seguro; páginas públicas e orientação para atualização quando a autenticação segura não for possível |

#### Modo leve

- layout em uma coluna;
- ausência de animações e efeitos pesados;
- imagens compactadas;
- tabelas e gráficos simplificados;
- menor quantidade de dados por carregamento;
- carregamento sob demanda;
- formulários divididos em etapas curtas;
- funções essenciais preservadas quando houver HTTPS e criptografia adequados;
- mensagem clara quando um recurso não for compatível.

#### Estratégia técnica

- JavaScript compilado para alvos móveis antigos;
- alternativas e prefixos de CSS;
- pacote legado separado do pacote moderno;
- polyfills locais quando necessários;
- detecção de recursos, não apenas do modelo do aparelho;
- ausência de dependência obrigatória de WebGL ou hardware potente;
- testes em aparelhos reais, emuladores e serviços de compatibilidade;
- segurança nunca reduzida para acomodar navegadores obsoletos.

O aplicativo não bloqueará um dispositivo somente por ser antigo. Primeiro tentará oferecer a experiência normal e, quando necessário, ativará o modo leve. Sistemas sem suporte a HTTPS, criptografia segura ou autenticação mínima poderão acessar apenas conteúdo público compatível.

Nenhuma funcionalidade principal poderá depender exclusivamente de um tamanho de tela, sistema operacional ou método de entrada. Não é tecnicamente possível garantir suporte idêntico a todo navegador antigo já produzido; por isso, a compatibilidade será assegurada por testes, melhoria progressiva e experiência simplificada para ambientes limitados.

---

## Parte 1 — Visão mestre e estado atual

**Documento de origem:** `documentacao-mestre-apex-combate.md`

**Proprietário:** Mozer  
**Produto:** Apex Combate  
**Posicionamento:** Tudo em um para o ecossistema das artes marciais  
**Versão documentada:** v44
**Data de consolidação:** 7 de outubro de 2026
**Status:** protótipo funcional com backend local persistente

> Este é o documento principal do projeto. Em caso de divergência com notas antigas, prevalecem as decisões registradas aqui e no registro de decisões.

---

### 1. Visão do produto

O Apex Combate é uma plataforma universal para conectar e operar a jornada completa das artes marciais. O produto não pertence a uma única modalidade e deve atender jiu-jítsu, judô, karatê, muay thai, boxe, kickboxing, taekwondo, kung fu, wrestling, capoeira, MMA e demais modalidades.

A proposta central é reunir em um único ecossistema:

- perfil e jornada do atleta;
- clubes, dojôs e academias;
- professores e equipe autorizada;
- assistência técnica durante competições;
- federações e governança esportiva;
- eventos, inscrições, credenciais e resultados;
- evolução futura para serviços comerciais conectados.

**Proposta de valor:** toda a jornada marcial, da primeira aula à competição, em uma plataforma integrada.

---

### 2. Decisões permanentes do produto

1. O nome é sempre **Apex Combate**.
2. O foco é **Tudo em um**.
3. A plataforma atende todas as modalidades de artes marciais.
4. A tela pública do aplicativo principal possui exatamente três acessos:
   - **ATLETA**;
   - **CLUBE**;
   - **FEDERAÇÃO**.
5. Professor e técnico pertencem ao grupo CLUBE. Não existe quarto botão para técnico.
6. O tema visual principal é Dark Mode.
7. A imagem fornecida por Mozer é o logo oficial.
8. Não existe uma marca separada chamada “Apex Arena”. Operações offline ou de competição continuam sendo modos do Apex Combate.
9. A interface deve funcionar em celulares, tablets, notebooks, computadores, monitores grandes e TVs.
10. O seletor de idioma deve traduzir o conteúdo real da interface.
11. Supabase foi rejeitado e não deve ser utilizado.
12. A federação é o cérebro operacional do ecossistema esportivo.
13. O modelo de governança é Apex Central acima de múltiplas federações, mas a Central proprietária de Mozer está adiada e desabilitada nesta fase.
14. A Central da Federação não é a Central proprietária de Mozer.
15. O comércio será administrado pelo **Apex’s Forge**, aplicativo separado ligado ao Apex Combate, sem criar um quarto perfil público no aplicativo principal.

---

### 3. Identidade da marca

#### Nome e assinatura

- **Nome:** Apex Combate
- **Slogan principal:** Uma plataforma. Todas as lutas.
- **Mensagem:** Supere seus próprios limites.

#### Logo oficial

Arquivo: `assets/apex-combate-logo-oficial.png`

O logo não deve ser redesenhado, distorcido, recolorido ou substituído sem aprovação de Mozer.

#### Direção visual

- Dark Mode;
- preto e grafite como superfícies principais;
- vermelho Apex como cor de ação;
- branco técnico para conteúdo principal;
- alto contraste;
- linguagem forte, moderna e respeitosa;
- sem violência gráfica, sangue, caveiras ou agressividade fora do contexto esportivo;
- representação inclusiva de modalidades, idades e gêneros.

#### Paleta principal

| Cor | Código | Aplicação |
|---|---|---|
| Crimson Apex | `#EF2636` | Marca e ações principais |
| Crimson claro | `#FF5A64` | Estados ativos |
| Preto arena | `#080A0E` | Fundo principal |
| Grafite | `#0F1218` | Cartões e painéis |
| Aço | `#252B36` | Bordas |
| Branco técnico | `#F6F7F9` | Texto principal |
| Cinza tático | `#9299A6` | Texto secundário |
| Verde status | `#49D49D` | Sucesso e validação |

---

### 4. Perfis públicos e autenticação

#### 4.1 ATLETA

**Campos:**

- CPF, documento nacional ou passaporte;
- data de nascimento.

**Regras:**

- CPF com ou sem formatação;
- documentos podem conter letras e números;
- datas flexíveis são normalizadas para ISO;
- o campo país permanece removido;
- não existe validação por WhatsApp;
- o acesso é direto após documento e nascimento válidos.

**Credencial de demonstração:**

- Documento: `529.982.247-25`
- Nascimento: `10/05/1998`

#### 4.2 CLUBE

**Campos:**

- Usuário;
- Senha.

**Requisição:**

```json
{
  "usuario": "USUARIO",
  "senha": "SENHA",
  "perfil": "clube"
}
```

O mesmo formulário aceita:

- conta administrativa do clube (`CLUB_ADMIN`);
- subconta individual do técnico (`CLUB_TECHNICIAN`).

**Demonstração do clube:**

- Usuário: `RYUZOKAN`
- Senha: `2026`

**Demonstração do técnico:**

- Usuário: `TECNICO.MARCELO`
- Senha: `TECNICO2026`

#### 4.3 FEDERAÇÃO

**Campos da primeira etapa:**

- Admin;
- Senha.

**Segunda etapa:** OTP obrigatório.

O mesmo formulário aceita:

- Presidente da Federação: `PRESIDENTE` / `MASTER2026` / OTP `654321`;
- Central da Federação: `ADMIN` / `MASTER2026` / OTP `654321`.

**Papéis:**

- `PRESIDENTE_MASTER`: governança, auditoria, relatórios e decisão final;
- `ADMIN`: operação central da federação, filiados, validações, homologações e competições.

Essas credenciais são apenas demonstrativas e devem ser substituídas em produção.

---

### 5. Área do atleta

O fluxo completo do atleta foi escolhido para o produto. A área contempla ou está preparada para contemplar:

- painel pessoal;
- carteirinha digital;
- clube e federação vinculados;
- modalidades e graduação;
- agenda e check-ins;
- diário e histórico de treino;
- metas e conquistas;
- eventos e inscrições;
- seleção de técnico elegível na inscrição;
- histórico competitivo e resultados;
- documentos e privacidade.

Na inscrição, o atleta só pode selecionar um técnico:

1. ativo;
2. pertencente ao mesmo clube;
3. formalmente credenciado naquela competição.

A API rejeita tentativas de selecionar um técnico não elegível.

---

### 6. Área administrativa do clube

A conta `CLUB_ADMIN` pode administrar:

- cadastro e situação dos alunos;
- turmas, modalidades e horários;
- equipe autorizada;
- presença e indicadores;
- planos e financeiro;
- delegações;
- inscrição e prontidão de atletas;
- credenciamento de técnicos por competição;
- relatórios operacionais.

O clube é responsável por selecionar, credenciar e vincular técnicos às competições.

---

### 7. Área privada do técnico

#### 7.1 Regra central

A única função do técnico é auxiliar atletas durante competições.

Ele entra com login individual pelo botão público CLUBE e é direcionado automaticamente para sua própria área. Ele nunca recebe o dashboard administrativo do clube.

#### 7.2 Pode acessar

- competições em que foi credenciado;
- atletas explicitamente atribuídos a ele;
- delegação operacional vinculada;
- credencial individual;
- fila de lutas;
- área de chamada;
- pesagem;
- aquecimento;
- equipamentos;
- horários, áreas e número das lutas;
- corner;
- avisos da organização;
- regulamentos aplicáveis;
- ocorrências e suporte operacional.

#### 7.3 Não pode acessar

- lista geral de alunos;
- turmas e presença de aulas;
- planos e mensalidades;
- financeiro;
- administração do clube;
- cadastro ou credenciamento de outros técnicos;
- ferramentas da federação;
- ferramentas da Apex Central;
- dados de atletas não atribuídos.

#### 7.4 Recursos implementados na v38

- painel da próxima competição;
- próximo atleta e contagem regressiva;
- atualização automática a cada 30 segundos;
- fila de lutas;
- linha do tempo operacional;
- estágios de credenciamento, pesagem, equipamento, aquecimento, chamada, pronto, combate e finalizado;
- cartão operacional de cada atleta;
- checklist pré-luta;
- plano privado de corner;
- cronômetro de apoio;
- alertas do navegador;
- credencial individual com QR Code funcional;
- regras inteligentes por modalidade;
- anotação de resultado não oficial e aprendizado;
- registro de ocorrências;
- solicitações de suporte à organização;
- confirmação de leitura dos avisos;
- cache local e fila de ações offline;
- sincronização automática após reconexão.

O cronômetro do técnico é ferramenta auxiliar e não substitui o cronômetro oficial da arbitragem.

#### 7.5 Permissões técnicas

- `CLUB_TECHNICIAN`
- `COMPETITION_SUPPORT`
- `DELEGATION_READ`
- `ASSIGNED_ATHLETE_READ`
- `CALL_AREA_READ`
- `WARMUP_ACCESS`
- `CORNER_ACCESS`
- `CREDENTIAL_READ`
- `LIVE_QUEUE_READ`
- `CHECKLIST_WRITE`
- `ATHLETE_STAGE_WRITE`
- `TACTICAL_NOTES_WRITE`
- `INCIDENT_CREATE`
- `SUPPORT_REQUEST_CREATE`
- `RULES_READ`
- `OFFLINE_ACCESS`

Toda escrita valida no servidor a relação técnico → competição → inscrição → atleta.

---

### 8. Federação e governança

#### Princípio

**A federação é o cérebro de tudo.**

Cada federação controla sua própria rede:

- clubes filiados;
- atletas registrados;
- credenciais;
- modalidades e regras;
- graduações e certificações;
- eventos e homologações;
- categorias, pesagem e resultados;
- conformidade e auditoria.

O isolamento é feito por `federation_id`.

#### Presidente

Acesso de governança, relatórios, auditoria e aprovações finais.

#### Central da Federação

Administração operacional da própria federação. Não representa o proprietário do Apex Combate.

#### Apex Central de Mozer

- planejada acima de múltiplas federações;
- pertencente a Mozer;
- adiada para fase futura;
- rotas e conta proprietária desabilitadas;
- não utiliza o login público FEDERAÇÃO;
- não cria um quarto perfil na tela atual.

---

### 9. Apex’s Forge — aplicativo comercial separado

Foi decidido criar o **Apex’s Forge**, aplicativo conectado ao ecossistema para que lojas controlem seus produtos e vendas.

#### Separação proposta

**Apex Combate:**

- experiência esportiva;
- exibição do marketplace;
- busca, carrinho, compra e acompanhamento pelo cliente.

**Apex’s Forge — aplicativo comercial oficial:**

- login de lojistas;
- produtos e variações;
- estoque;
- preços e promoções;
- pedidos;
- entregas;
- financeiro e repasses;
- equipe da loja;
- relatórios.

O Apex’s Forge será um produto separado, ligado por API comercial segura. Ele não adiciona um quarto perfil ao Apex Combate e não concede acesso a dados esportivos, federativos, médicos ou administrativos que não sejam necessários para a compra.

Detalhes: `apexs-forge.md`.

---

### 10. Internacionalização

- seletor internacional de idiomas;
- tradução efetiva do conteúdo visível;
- pacotes essenciais embarcados para idiomas principais;
- tradução dinâmica por lotes para o restante da interface;
- suporte a direção RTL quando aplicável;
- idioma persistido localmente;
- restauração integral para português.

A tradução externa do protótipo depende de disponibilidade e cota do serviço utilizado. Produção deve usar serviço com SLA, cache persistente e glossário marcial próprio.

---

### 11. Responsividade e PWA

O produto foi estruturado para:

- celulares a partir de 320 px;
- tablets em retrato e paisagem;
- notebooks e desktops;
- monitores QHD/4K;
- TVs e telas grandes;
- toque, mouse, teclado e controles compatíveis.

#### PWA

- manifesto instalável;
- ícones de 192 e 512 px;
- orientação livre;
- Service Worker;
- cache de aplicação;
- navegação network-first para evitar versões antigas;
- APIs fora do cache HTTP;
- modo offline da área técnica com dados locais e fila de sincronização.

A versão atual de cache é `apex-combate-v44`.

---

### 12. Arquitetura técnica atual

#### Frontend

- aplicação principal: `apex-combate.html`;
- Dark Mode responsivo;
- HTML, CSS e JavaScript sem dependências externas obrigatórias para renderização;
- recursos visuais locais;
- recarregamento automático no ambiente de desenvolvimento.

#### Backend

- servidor: `server.py`;
- biblioteca padrão do Python;
- API HTTP JSON;
- autorização por JWT HS256;
- validade demonstrativa de uma hora;
- rate limiting básico por IP;
- respostas de API sem cache;
- auditoria de operações críticas.

#### Persistência

- camada: `apex_db.py`;
- banco atual: SQLite;
- arquivo: `data/apex-combate.sqlite3`;
- senhas: PBKDF2-SHA256 com salt individual e 260.000 iterações;
- segredo JWT local persistente.

SQLite é a fundação local do protótipo, não a recomendação final de escala. Produção deve migrar para PostgreSQL ou banco relacional equivalente.

#### Supabase

Supabase não deve ser integrado. Essa decisão foi explicitamente tomada por Mozer.

---

### 13. Modelo de dados atualmente implementado

- `federations`
- `clubs`
- `athletes`
- `technicians`
- `federation_users`
- `competitions`
- `competition_staff`
- `registrations`
- `competition_operations`
- `technician_checklists`
- `technician_notices`
- `technician_incidents`
- `technician_support_requests`
- `homologations`
- `audit_log`

#### Dados operacionais do técnico

- etapa do atleta;
- horário de chamada;
- área, tatame, ringue ou cage;
- número da luta;
- quantidade de lutas anteriores;
- tempo sugerido de aquecimento;
- situação da pesagem;
- situação dos equipamentos;
- estratégia de corner;
- resultado não oficial e observação;
- checklist;
- avisos;
- ocorrências;
- suporte.

---

### 14. Endpoints atuais

#### Plataforma

- `GET /api/health`
- `GET /api/version`
- `GET /api/session`
- `POST /api/translate`

#### Autenticação

- `POST /api/login/atleta`
- `POST /api/login`
- `POST /api/login/validar-otp`

#### Atleta

- `GET /api/athlete/dashboard`
- `GET /api/competitions`
- `POST /api/registrations`

#### Clube

- `GET /api/club/dashboard`
- `GET /api/club/technicians`
- `POST /api/club/students`
- `POST /api/club/competition-technicians`

#### Técnico

- `GET /api/technician/operations`
- `POST /api/technician/status`
- `POST /api/technician/checklist`
- `POST /api/technician/strategy`
- `POST /api/technician/result`
- `POST /api/technician/incident`
- `POST /api/technician/support`
- `POST /api/technician/notice-read`

#### Federação

- `GET /api/federation/dashboard`
- `POST /api/federation/homologations`

Rotas proprietárias da Apex Central permanecem desabilitadas.

---

### 15. Segurança e privacidade

#### Implementado na fundação local

- hash de senha com salt;
- JWT assinado;
- expiração de sessão;
- autorização por perfil e papel;
- menor privilégio para técnicos;
- validação de propriedade de recursos;
- isolamento federativo;
- 2FA demonstrativo para federação;
- rate limiting básico;
- auditoria;
- proteção de arquivos de banco e código contra acesso HTTP;
- limpeza de dados temporários de testes.

#### Obrigatório antes de produção

- HTTPS;
- PostgreSQL gerenciado;
- cofre de segredos;
- OTP real ou Passkey;
- refresh tokens revogáveis;
- gerenciamento de sessões e dispositivos;
- backups e recuperação;
- logs e observabilidade;
- armazenamento seguro de documentos;
- políticas LGPD;
- consentimento e retenção;
- controles para menores;
- testes automatizados e de invasão;
- gateway de pagamento certificado para comércio.

Dados médicos devem ser excepcionais, mínimos, autorizados e restritos. O sistema não substitui orientação médica.

---

### 16. Estado da versão v44

#### Validado

- um único controle **Voltar ao início** no cabeçalho autenticado compartilhado por atleta, clube, técnico e federação;
- encerramento de sessão com limpeza de tokens, perfil, escopos federativos, estado de clube/técnico e caches locais antes do retorno à abertura;
- apresentação responsiva do controle com texto em telas amplas, ícone nomeado em telas compactas, alvo de toque e escala para TVs;
- escala tipográfica fluida aplicada aos componentes funcionais;
- antigos tamanhos críticos de 6–9 px eliminados das declarações de fonte;
- campos móveis protegidos por mínimo de 16 px;
- cabeçalho visual do login removido, mantendo somente o tradutor discreto;
- cartão central, logo oficial e três acessos preservados;
- abertura pública sem a antiga faixa superior;
- título institucional exibido na abertura pública;
- apresentação pública exibida antes da autenticação;
- avanço para o login somente por ação explícita do visitante;
- retorno às boas-vindas depois do logout;
- três perfis públicos e nenhum quarto botão;
- login de atleta;
- login administrativo do clube;
- login individual do técnico;
- Presidente e Central da Federação com OTP;
- permissões restritas do técnico;
- isolamento entre técnicos;
- operações completas da área técnica;
- seleção de técnico elegível por competição;
- bloqueio de técnico não credenciado;
- QR Code decodificável;
- frontend v44;
- manifesto e Service Worker v44;
- sintaxe JavaScript e Python;
- integridade do HTML;
- limpeza de dados temporários de testes.

#### Limitações conhecidas

- ambiente local demonstrativo;
- SQLite não é o banco final de escala;
- OTP fixo e credenciais de demonstração não são para produção;
- tradução dinâmica depende de serviço externo;
- não há integração real de pagamento, SMS, e-mail ou push;
- não há automação de navegador instalada no ambiente atual;
- o Apex’s Forge está documentado, mas ainda não foi implementado.

---

### 17. Arquivos principais

| Arquivo | Finalidade |
|---|---|
| `apex-combate.html` | Aplicação principal v44 |
| `index.html` | Entrada da prévia |
| `server.py` | API, autenticação e autorização |
| `apex_db.py` | Banco, migrações e sementes |
| `data/apex-combate.sqlite3` | Banco local persistente |
| `manifest.webmanifest` | Manifesto PWA |
| `apex-sw.js` | Service Worker v44 |
| `assets/apex-combate-logo-oficial.png` | Logo oficial |
| `docs/backend-apex-combate.md` | Backend e APIs |
| `docs/sistema-login-apex-combate.md` | Regras de autenticação |
| `docs/perfis-e-permissoes-apex-combate.md` | Papéis e permissões |
| `docs/admin-apex-central.md` | Central proprietária futura |
| `docs/compatibilidade-apex-combate.md` | Responsividade e PWA |
| `docs/identidade-visual-apex-combate.md` | Marca e direção visual |
| `docs/apexs-forge.md` | Aplicativo comercial oficial para lojistas |
| `docs/registro-de-decisoes-apex-combate.md` | Decisões vigentes |

---

### 18. Ordem recomendada de evolução

1. Consolidar a fundação de produção do Apex Combate;
2. Migrar banco, segredos, OTP e notificações;
3. Completar operação real de eventos e federações;
4. Testar com clubes e técnicos em competição piloto;
5. Construir a Central proprietária de Mozer em rota interna própria;
6. Definir a identidade visual derivada e o modelo de negócio do Apex’s Forge;
7. Construir o serviço comercial e o painel do Apex’s Forge;
8. Integrar catálogo e compra ao Apex Combate;
9. Implantar pagamentos, split, logística, fiscal e antifraude;
10. Expandir por modalidades, federações, regiões e idiomas.

---

### 19. Regra de governança documental

Toda alteração relevante deve atualizar:

1. esta documentação mestre;
2. o documento específico do módulo;
3. o registro de decisões;
4. a versão de cache quando houver alteração no frontend/PWA;
5. os testes e a auditoria de desenvolvimento.

Nenhuma decisão futura deve reintroduzir Supabase, um quarto perfil público, acesso administrativo para o técnico ou confusão entre a Central da Federação e a Apex Central de Mozer sem autorização explícita de Mozer.

---

## Parte 2 — Plano completo do produto

**Documento de origem:** `plano-produto-apex-combate.md`

> **Nome definido:** Apex Combate  
> **Proprietário:** Mozer  
> **Conceito:** plataforma universal “Tudo em um” que conecta atletas e alunos, clubes/dojôs/academias, técnicos de competição e federações de artes marciais.  
> **Status:** protótipo funcional v44 com retorno autenticado seguro ao início, tipografia fluida por dispositivo, cabeçalho de login reduzido ao tradutor, abertura simplificada, apresentação pública, login em etapa separada e backend local persistente. A disponibilidade jurídica da marca, do domínio e dos identificadores sociais deverá ser verificada antes do lançamento.
> **Fonte principal:** consulte `documentacao-mestre-apex-combate.md` para decisões vigentes.

### Entrega v44

A v44 adiciona um único controle **Voltar ao início** ao cabeçalho compartilhado por atleta, clube, técnico e federação. A ação reutiliza o encerramento seguro de sessão: limpa tokens ativos, perfil, escopos federativos, estado de clube/técnico e caches locais relacionados antes de devolver a pessoa à abertura pública. O rótulo permanece visível em telas amplas, torna-se um botão compacto com ícone de início em áreas menores, conserva nome acessível e respeita alvos de toque e escala para TVs.

### Entrega v43

A v43 introduz uma escala tipográfica fluida e reutilizável para todo o frontend, com limites mínimos e máximos em `clamp()` e unidades relativas. Textos funcionais antes fixados entre 6 e 9 px passam a patamares legíveis, mantendo hierarquia e composição. Em telas de até 820 px, campos, seletores e áreas de texto usam no mínimo 16 px para evitar o zoom automático do iPhone. Celulares, tablets, notebooks, desktops, monitores grandes e TVs recebem crescimento progressivo sem detecção de modelo específico.

### Entrega v42

A v42 remove da tela de login o logo superior, os atalhos **Modalidades**, **Academias**, **Competições** e **Sobre**, o botão superior **Entrar** e a faixa visual do cabeçalho. O tradutor real permanece disponível em um controle flutuante e discreto, sem alterar o logo oficial, os três acessos ou a autenticação do cartão central.

---

### 1. Resumo executivo

O **Apex Combate** será um ecossistema digital para modalidades como jiu-jítsu, judô, karatê, muay thai, boxe, taekwondo, kung fu, wrestling, capoeira, kickboxing, MMA e outras.

A plataforma reunirá cinco necessidades hoje normalmente separadas:

1. **Encontrar** academias, professores, aulas e eventos;
2. **Treinar** com planos, técnicas, metas e histórico;
3. **Evoluir** acompanhando presença, graduação e desempenho;
4. **Gerenciar** academias, turmas, alunos e cobranças;
5. **Conectar** a comunidade por meio de conteúdo, desafios e competições.

#### Proposta de valor

> **Toda a jornada marcial em um único aplicativo — da primeira aula à competição.**

#### Diferencial central

O sistema não será limitado a uma única modalidade. Ele terá um **motor de progressão configurável**, capaz de representar:

- faixas, cordas, graus, dans, níveis ou categorias;
- regras específicas de cada modalidade, federação ou academia;
- treinos técnicos, físicos, sparring, formas/katas e competição;
- múltiplas modalidades no mesmo perfil de atleta.

---

### 2. Problema que o produto resolve

#### Para atletas e alunos

- Dificuldade para encontrar uma academia adequada;
- Histórico de treino e graduação espalhado ou inexistente;
- Falta de clareza sobre evolução e objetivos;
- Informações de aulas, campeonatos e seminários dispersas;
- Pouca integração entre praticantes de modalidades diferentes.

#### Para professores e academias

- Gestão manual de alunos, presença, turmas e graduações;
- Comunicação fragmentada em grupos de mensagens;
- Dificuldade para atrair e converter novos alunos;
- Cobrança e controle de mensalidades pouco organizados;
- Falta de indicadores sobre retenção e ocupação das turmas.

#### Para federações

- Cadastro de clubes, academias e atletas distribuído em sistemas separados;
- Dificuldade para validar filiações, graduações, certificados e licenças;
- Organização de competições, inscrições, categorias e resultados fragmentada;
- Falta de uma visão consolidada sobre modalidades, regiões e entidades filiadas.

---

### 3. Públicos e perfis de acesso

| Grupo visível | Pessoas incluídas | Recursos prioritários |
|---|---|---|
| Atletas e alunos | Iniciantes, praticantes recreativos e competidores | Busca, agenda, check-in, metas, graduação, eventos e histórico |
| Clubes, dojôs e academias, professores e técnicos | Gestores, coordenadores, professores, técnicos e equipe autorizada | Administração do clube para gestores; assistência de competição estritamente limitada para técnicos |
| Federações | Dirigentes e equipe federativa autorizada | Filiados, registros, graduações, certificações, competições e homologações |

Uma pessoa poderá acumular funções autorizadas dentro de um grupo. No segundo grupo existem contas internas diferentes. A conta administrativa pode gerir a organização; a subconta `CLUB_TECHNICIAN` é exclusivamente destinada à assistência de atletas durante competições e permanece bloqueada para alunos gerais, turmas, financeiro e administração.

---

### 4. Pilares do produto

#### 4.1 Descoberta

- Busca por modalidade, cidade, distância, nível e faixa de preço;
- Mapa de academias e eventos;
- Perfil verificado de academias e professores;
- Horários, estrutura, avaliações e aula experimental;
- Filtros de acessibilidade, faixa etária e aulas femininas ou inclusivas.

#### 4.2 Treino e evolução

- Perfil marcial com múltiplas modalidades;
- Linha do tempo de graduações;
- Check-in em aulas;
- Diário de treino;
- Metas semanais e sequências de frequência;
- Biblioteca de técnicas, planos e conteúdos;
- Registro de competições, resultados e conquistas;
- Indicadores pessoais sem comparações inadequadas entre modalidades.

#### 4.3 Gestão de academia

- Cadastro de unidades, professores, turmas e horários;
- Matrículas e aula experimental;
- Lista de presença e check-in por QR Code;
- Avaliação e promoção de graduação;
- Mensagens e avisos por turma;
- Planos, mensalidades e situação de pagamento;
- Painel com retenção, ocupação e novos interessados.

#### 4.4 Comunidade

- Feed por interesses e modalidades;
- Perfis de atletas, professores e academias;
- Publicações com texto, foto e vídeo;
- Grupos por academia, modalidade ou evento;
- Desafios de consistência e metas;
- Denúncia, bloqueio e moderação;
- Regras rígidas contra humilhação, incentivo à violência e conteúdo perigoso.

#### 4.5 Eventos e competições

- Calendário de campeonatos, seminários e graduações;
- Inscrição e pagamento;
- Categorias por idade, peso, sexo, nível e modalidade;
- Check-in, pesagem e status do participante;
- Chaves, confrontos e resultados;
- Histórico no perfil do atleta;
- Página pública e transmissão por link quando disponível.

---

### 5. Escopo recomendado para o MVP

Construir tudo ao mesmo tempo aumentaria muito o custo e atrasaria a validação. O MVP deve provar três hipóteses:

1. Atletas desejam registrar e acompanhar sua jornada marcial;
2. Academias ganham valor ao organizar aulas e alunos na plataforma;
3. A descoberta de academias gera novos contatos e aulas experimentais.

#### Incluído no MVP

##### Aplicativo do aluno

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

##### Área do professor/academia

- Criação do perfil da academia;
- Cadastro de modalidades, turmas e horários;
- Convite e gestão básica de alunos;
- Confirmação de presença;
- Registro de graduação;
- Avisos para turmas;
- Painel básico de frequência e interessados.

##### Administração interna da plataforma (não é um perfil público)

- Gestão de usuários e academias;
- Verificação manual de professores e academias;
- Moderação de conteúdo e denúncias;
- Cadastro inicial de modalidades e sistemas de graduação;
- Métricas essenciais do produto.

#### Fora do MVP, mas preparado para fases seguintes

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

### 6. Estrutura de navegação do MVP

#### Aplicativo do aluno

1. **Início** — próximas aulas, progresso e avisos;
2. **Explorar** — academias, professores e modalidades;
3. **Treinos** — agenda, check-in, diário e histórico;
4. **Jornada** — graduações, metas e conquistas;
5. **Perfil** — dados, modalidades, privacidade e configurações.

#### Painel administrativo do clube/dojô/academia

1. **Visão geral**;
2. **Agenda e turmas**;
3. **Alunos**;
4. **Presenças**;
5. **Graduações**;
6. **Interessados**;
7. **Delegações e credenciamento de técnicos**;
8. **Financeiro e configurações**.

#### Área privada do técnico de competição

1. **Competição atribuída**;
2. **Atletas atribuídos**;
3. **Fila de lutas e linha do tempo**;
4. **Pesagem, equipamentos e checklist**;
5. **Aquecimento e corner**;
6. **Credencial QR**;
7. **Avisos, regras, ocorrências e suporte**.

O técnico não acessa os módulos administrativos do clube.

#### Painel da federação

1. **Visão federativa**;
2. **Clubes e academias filiadas**;
3. **Registro de atletas**;
4. **Graduações e certificações**;
5. **Competições e calendário oficial**;
6. **Homologações**;
7. **Relatórios regionais e por modalidade**;
8. **Conformidade documental**.

---

### 7. Telas prioritárias

#### Aluno

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

#### Academia/professor

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

#### Federação

1. Painel de indicadores federativos;
2. Cadastro e situação dos filiados;
3. Registro esportivo de atletas;
4. Validação de graduações e certificações;
5. Homologação de eventos;
6. Relatórios e auditoria de ações.

---

### 8. Fluxos essenciais

#### Fluxo A — encontrar uma academia

Cadastro → escolher modalidade → permitir localização ou informar cidade → aplicar filtros → visualizar academia → consultar horários → solicitar aula experimental → receber confirmação → comparecer e fazer check-in.

#### Fluxo B — acompanhar evolução

Entrar em uma turma → realizar check-ins → registrar observações no diário → cumprir meta semanal → receber avaliação do professor → visualizar nova graduação na linha do tempo.

#### Fluxo C — academia recebe um novo aluno

Criar perfil → publicar turmas → receber solicitação → confirmar aula experimental → registrar presença → convidar para matrícula → acompanhar frequência.

#### Fluxo D — registrar graduação

Professor seleciona aluno → escolhe modalidade e sistema → informa nova graduação → adiciona data e observação → aluno confirma recebimento → registro aparece no histórico.

---

### 9. Regras para suportar todas as modalidades

A universalidade deve vir da arquitetura, não de uma lista fixa de faixas.

#### Estrutura configurável

- **Modalidade:** jiu-jítsu, boxe, judô etc.;
- **Organização:** federação, associação ou academia;
- **Sistema de progressão:** faixa, grau, nível, corda, dan ou sem graduação;
- **Etapas:** progressão ordenada e requisitos opcionais;
- **Categorias:** idade, peso, nível e regras específicas;
- **Tipo de sessão:** técnica, físico, sparring, formas, defesa pessoal ou competição;
- **Conquistas:** graduação, participação, pódio, certificação ou meta interna.

A academia poderá usar um modelo oficial existente ou configurar sua própria progressão, sempre identificada como **“padrão da academia”** para evitar confusão com certificações oficiais.

---

### 10. Modelo de negócio

#### Plano gratuito para praticantes

- Perfil marcial;
- Busca de academias;
- Agenda e check-ins;
- Histórico básico;
- Participação em eventos e desafios gratuitos.

#### Plano Premium para praticantes

- Estatísticas avançadas;
- Metas e relatórios;
- Diário ilimitado;
- Conteúdo exclusivo;
- Descontos de parceiros;
- Exportação do histórico.

#### Assinatura para academias

| Plano | Indicação | Recursos |
|---|---|---|
| Inicial | Academia pequena | Turmas, alunos, presença e perfil público |
| Profissional | Operação em crescimento | Automação, relatórios, cobranças e equipe |
| Rede | Múltiplas unidades | Gestão centralizada, permissões e indicadores consolidados |

#### Receitas futuras

- Taxa sobre inscrição em eventos;
- Comissão por planos ou aulas vendidos;
- Comissão do marketplace conectado ao aplicativo separado dos lojistas;
- Conteúdo patrocinado claramente identificado;
- Soluções para federações e redes de academias.

**Recomendação:** não cobrar de atletas no início. A primeira receita deve vir de academias, após comprovação de ganho operacional e geração de novos alunos.

---

### 11. Tecnologia recomendada

#### Estratégia de plataforma

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

#### Princípios técnicos

- Um único cadastro com múltiplos papéis;
- API preparada para web e celular;
- Permissões por função e academia;
- Registro de auditoria para graduações, pagamentos e ações administrativas;
- Conteúdo e sistemas de graduação configuráveis;
- Internacionalização desde a base, começando em português do Brasil;
- Acessibilidade e funcionamento adequado em conexões móveis instáveis.

---

### 12. Modelo de dados inicial

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

### 13. Segurança, confiança e aspectos legais

#### LGPD e privacidade

- Consentimento claro e específico;
- Coleta apenas dos dados necessários;
- Possibilidade de baixar e excluir dados;
- Política de retenção;
- Controle sobre visibilidade de perfil e histórico;
- Contratos adequados com fornecedores de dados.

#### Menores de idade

- Conta vinculada a responsável legal;
- Perfil privado por padrão;
- Restrições de mensagens e localização;
- Consentimento para imagem e participação em eventos;
- Ferramentas de denúncia acessíveis.

#### Segurança marcial

- Avisos de que técnicas devem ser praticadas com supervisão qualificada;
- Proibição de conteúdo que incentive agressão fora de contexto esportivo ou educacional;
- Sinalização de conteúdo avançado ou de risco;
- Informações de saúde tratadas como dados sensíveis;
- O aplicativo não substitui orientação médica ou profissional.

#### Confiança

- Verificação de academias e professores;
- Identificação da origem de cada graduação;
- Histórico de alterações e revogações;
- Avaliações somente após interação comprovada;
- Moderação humana com apoio automatizado, nunca apenas automatizada.

---

### 14. Identidade e experiência

#### Personalidade da marca

- Disciplinada, inclusiva e respeitosa;
- Moderna sem apagar as tradições;
- Competitiva sem ser agressiva;
- Universal sem misturar indevidamente regras e graduações.

#### Direção visual sugerida

- Base escura ou neutra com alto contraste;
- Cor de destaque energética, como vermelho coral ou laranja;
- Tipografia forte e legível;
- Ícones próprios para treino, graduação, eventos e comunidade;
- Fotografias autênticas de diferentes modalidades, idades, corpos e gêneros.

#### Ideias de slogan

- **Sua jornada marcial em um só lugar.**
- **Treine. Evolua. Conecte-se.**
- **Todas as artes, uma comunidade.**

---

### 15. Métricas de sucesso

#### Aquisição

- Novos usuários por semana;
- Academias cadastradas e verificadas;
- Custo por novo usuário e nova academia;
- Solicitações de aula experimental.

#### Ativação

- Percentual que conclui o perfil;
- Percentual que seleciona uma modalidade;
- Primeiro check-in em até sete dias;
- Academia que cria sua primeira turma.

#### Engajamento

- Usuários ativos semanais e mensais;
- Check-ins por atleta;
- Metas concluídas;
- Aulas frequentadas;
- Retorno em 7, 30 e 90 dias.

#### Valor para academias

- Novos interessados recebidos;
- Conversão de aula experimental em matrícula;
- Ocupação das turmas;
- Retenção de alunos;
- Horas administrativas economizadas.

#### Receita

- Academias pagantes;
- Receita recorrente mensal;
- Conversão do teste para assinatura;
- Cancelamentos;
- Receita média por academia.

#### Métrica norteadora

> **Número de treinos válidos registrados por atletas ativos por semana.**

Essa métrica conecta o produto ao comportamento mais importante: pessoas treinando com consistência.

---

### 16. Roadmap proposto

#### Fase 0 — descoberta e validação (2 a 3 semanas)

- Entrevistar atletas de pelo menos cinco modalidades;
- Entrevistar professores e donos de academias de portes diferentes;
- Mapear processos atuais;
- Validar interesse, dores e disposição de pagamento;
- Definir modalidade e cidade piloto;
- Testar nome e posicionamento.

#### Fase 1 — protótipo (2 a 4 semanas)

- Fluxos de aluno e academia;
- Protótipo navegável;
- Testes de usabilidade;
- Ajustes de proposta e navegação;
- Página de espera para captar interessados.

#### Fase 2 — MVP técnico (10 a 14 semanas)

- Cadastro e perfis;
- Academias, turmas e agenda;
- Busca e aula experimental;
- Check-in e presença;
- Graduação e jornada;
- Painel administrativo;
- Testes, segurança e publicação piloto.

#### Fase 3 — piloto controlado (6 a 8 semanas)

- Lançar em uma cidade ou região;
- Integrar de 5 a 15 academias parceiras;
- Acompanhar suporte e comportamento de uso;
- Corrigir fricções;
- Medir retenção e valor para as academias.

#### Fase 4 — expansão

- Cobranças e assinaturas;
- Eventos e competições;
- Comunidade e desafios;
- Novas cidades, idiomas e países;
- Integrações com o aplicativo comercial separado e marketplace de compra no Apex Combate.

---

### 17. Estratégia de lançamento

#### Cidade piloto sugerida

Começar em uma única região, com densidade suficiente de academias. Uma opção natural é **Curitiba e Região Metropolitana**, antes da expansão nacional.

#### Aquisição inicial

- Academias fundadoras com benefícios vitalícios ou por prazo definido;
- Embaixadores de modalidades diferentes;
- QR Codes físicos nas academias;
- Desafio coletivo de frequência;
- Calendário regional gratuito de eventos;
- Perfil público compartilhável de academia e atleta;
- Parcerias com campeonatos e seminários locais.

#### Critério para expandir

Expandir apenas quando o piloto demonstrar:

- uso recorrente de check-in;
- adesão dos professores;
- retenção de atletas;
- conversão de interessados em aulas experimentais;
- disposição real das academias para pagar.

---

### 18. Principais riscos e mitigação

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

### 19. Decisões vigentes

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

### 20. Próximos passos recomendados

1. Validar a v38 com atletas, clubes, técnicos e uma federação piloto;
2. Migrar a fundação local para infraestrutura de produção com PostgreSQL, HTTPS, segredos e OTP real;
3. Completar notificações, documentos, auditoria e operação real de eventos;
4. Executar um piloto de competição em Curitiba;
5. Medir usabilidade da área técnica em celular e conexão instável;
6. Planejar a Central proprietária de Mozer em ambiente interno separado;
7. Definir identidade derivada, modelo de receita e regras do Apex’s Forge;
8. Construir o backend comercial separado e depois integrar catálogo e compra ao Apex Combate.

A documentação mestre em `documentacao-mestre-apex-combate.md` deve acompanhar todas as próximas alterações.

---

## Parte 3 — Identidade visual

**Documento de origem:** `identidade-visual-apex-combate.md`

### Conceito

**Apex** representa o ponto mais alto de desempenho. A identidade combina:

- evolução contínua;
- disciplina;
- potência controlada;
- precisão técnica;
- união entre diferentes modalidades.

A marca oficial é a arte enviada pelo responsável do projeto e deve ser usada de forma consistente em todas as telas.

### Assinatura

**Nome:** Apex Combate  
**Slogan principal:** Uma plataforma. Todas as lutas.  
**Mensagem de campanha:** Supere seus próprios limites.

### Símbolo oficial

A assinatura contém:

- letra **A** vermelha, alta e angular;
- recorte interno que sugere energia e movimento;
- palavra **APEX** em acabamento metálico;
- palavra **COMBATE** com marcadores vermelhos laterais;
- fundo preto integrado à composição original.

Arquivo oficial: `assets/apex-combate-logo-oficial.png`

Para materiais impressos de grande formato, recomenda-se futuramente produzir uma versão vetorial oficial em SVG, PDF ou AI sem alterar o desenho.

### Paleta

| Cor | Código | Uso |
|---|---|---|
| Crimson Apex | `#EF2636` | Ações principais, destaque e marca |
| Crimson claro | `#FF5A64` | Estados ativos e pequenos destaques |
| Preto arena | `#080A0E` | Fundo principal |
| Grafite | `#0F1218` | Cartões e painéis |
| Aço | `#252B36` | Bordas e divisores |
| Branco técnico | `#F6F7F9` | Textos principais |
| Cinza tático | `#9299A6` | Textos secundários |
| Verde status | `#49D49D` | Sucesso, presença e verificação operacional |

### Tipografia recomendada

- **Títulos e campanhas:** Barlow Condensed ExtraBold Italic ou alternativa condensada equivalente;
- **Interface:** Inter ou fonte sem serifa equivalente;
- **Fallback offline do protótipo:** fontes nativas do sistema.

Títulos podem usar caixa alta, peso elevado e inclinação. Textos funcionais devem permanecer simples e legíveis.

### Direção visual

- fundos pretos e grafite;
- superfícies discretamente texturizadas;
- linhas e recortes angulares;
- vermelho usado com moderação;
- fotografias com ação real, anatomia natural e iluminação lateral;
- alto contraste e boa leitura;
- evitar fogo, caveiras, sangue ou violência gráfica;
- representar homens, mulheres, diferentes idades e várias modalidades.

### Uso do logo

- manter área livre equivalente à largura do travessão interno do símbolo;
- tamanho mínimo recomendado do símbolo digital: 32 px;
- usar preferencialmente sobre fundo preto, grafite ou branco;
- não distorcer, inclinar, contornar novamente ou alterar as cores;
- não aplicar sombras pesadas;
- não colocar sobre fotografias muito detalhadas sem uma área de proteção.

### Tom de voz

A marca deve falar de forma:

- direta;
- motivadora;
- respeitosa;
- inclusiva;
- confiante, sem arrogância;
- competitiva, sem promover agressividade fora do esporte.

#### Exemplos

- “Seu treino. Sua evolução. Seu ápice.”
- “Toda jornada começa com o primeiro treino.”
- “Encontre sua academia. Construa sua história.”
- “Disciplina transforma repetição em evolução.”

### Marca comercial associada

O futuro aplicativo separado para lojistas tem o nome oficial **Apex’s Forge**.

- **Função:** gestão de lojas, produtos, variações, estoque, pedidos, vendas e repasses;
- **Relação:** produto conectado ao Apex Combate por API comercial, sem se tornar um quarto perfil público;
- **Slogan de trabalho:** “Forje sua marca. Eleve seu negócio.”;
- **Direção:** identidade forte, premium e comercial, derivada da família Apex sem substituir a marca Apex Combate.

A identidade visual própria do Apex’s Forge será desenvolvida em fase posterior e deverá manter relação clara com a marca principal.

### Componentes do protótipo

A interface atual utiliza:

- tela de login responsiva;
- navegação institucional;
- login do atleta por documento/passaporte e nascimento;
- login do clube e técnico por Usuário e Senha;
- login da federação por Admin, Senha e OTP;
- três grupos de acesso: atletas/alunos; clubes, dojôs e academias com professores/técnicos; e federações;
- dashboard completo do atleta/aluno;
- dashboard administrativo do clube;
- área privada do técnico exclusivamente para assistência durante competições;
- dashboard federativo com filiados, registros, eventos e homologações;
- seleção automática do painel conforme o perfil de login;
- pesquisa de academias;
- check-in, agenda, evolução e conquistas;
- encerramento de sessão;
- Dark Mode como tema principal.

---

## Parte 4 — Perfis e permissões

**Documento de origem:** `perfis-e-permissoes-apex-combate.md`

### Perfis com acesso

A Apex Combate terá **3 grupos de acesso visíveis**:

1. **Atletas e alunos**;
2. **Clubes, dojôs e academias, professores e técnicos**;
3. **Federações**.

Dentro do segundo grupo, cada pessoa receberá permissões conforme sua função. Um professor poderá gerenciar suas turmas sem necessariamente acessar o financeiro da academia, por exemplo.

---

### 1. Atletas e alunos

#### Podem

- manter o próprio perfil marcial;
- participar de uma ou mais modalidades;
- vincular-se a clube, dojô ou academia;
- consultar agenda e confirmar presença;
- realizar check-in;
- registrar treinos e metas;
- acompanhar graduações e certificados;
- inscrever-se em eventos autorizados;
- visualizar histórico e resultados;
- controlar a privacidade do próprio perfil.

#### Não podem

- alterar a própria graduação oficial;
- consultar informações privadas de outros atletas;
- administrar turmas ou dados financeiros;
- homologar eventos, graduações ou certificados.

---

### 2. Clubes, dojôs e academias, professores e técnicos

Este é um único grupo visível no login, com contas internas diferentes. O perfil público continua sendo **CLUBE**.

#### Gestores de clubes, dojôs e academias podem

- administrar unidades, equipe e modalidades;
- convidar professores, técnicos, atletas e alunos;
- criar horários, turmas e planos;
- acompanhar presença, retenção e ocupação;
- gerenciar aulas experimentais e interessados;
- administrar mensalidades e pagamentos;
- manter o histórico interno de graduações;
- solicitar filiação ou renovação junto à federação;
- inscrever equipes e atletas em eventos;
- credenciar técnicos e montar delegações;
- emitir relatórios operacionais.

#### Técnico de competição

O técnico entra pelo perfil CLUBE com usuário e senha individuais e recebe uma área privada própria. Sua única função é auxiliar atletas durante competições.

Pode:

- consultar apenas competições em que foi credenciado;
- visualizar somente atletas atribuídos a ele;
- acompanhar fila de lutas, área, horário e número do combate;
- atualizar linha do tempo operacional do atleta;
- realizar checklist de documento, pesagem, uniforme e equipamentos;
- operar cronômetro de apoio para aquecimento;
- registrar plano privado de corner e anotação pós-luta;
- apresentar a credencial individual com QR Code;
- consultar regras aplicáveis às modalidades atribuídas;
- receber avisos, confirmar leitura e solicitar suporte à organização;
- registrar ocorrências relacionadas ao evento;
- trabalhar offline e sincronizar ações após a reconexão.

Não pode:

- consultar o cadastro geral de alunos;
- acessar ou administrar turmas;
- acessar planos, mensalidades ou dados financeiros;
- gerenciar o clube, a equipe técnica ou outros técnicos;
- utilizar ferramentas da federação ou da Apex Central.

#### Restrições

- o servidor valida o vínculo entre técnico, competição e inscrição em toda operação;
- dados de saúde são excepcionais, mínimos e sujeitos à LGPD;
- a organização só acessa dados de pessoas vinculadas a ela;
- certificados oficiais dependem das regras da federação responsável;
- ações sensíveis ficam registradas em auditoria.

---

### 3. Federações

#### Podem

- administrar clubes, dojôs e academias filiadas;
- registrar atletas, professores e técnicos;
- controlar filiações, licenças e renovações;
- manter regras e sistemas oficiais de graduação;
- validar graduações, certificados e credenciais;
- criar ou homologar campeonatos e seminários;
- gerenciar categorias, inscrições, pesagem, chaves e resultados;
- emitir documentos federativos;
- consultar relatórios por modalidade, região e entidade;
- auditar ações realizadas dentro de sua jurisdição.

#### Restrições

- cada federação visualiza somente sua rede e suas competências;
- dados pessoais e sensíveis devem seguir a LGPD;
- alterações oficiais exigem histórico, responsável, data e justificativa;
- o acesso a informações de saúde deve ser excepcional e estritamente controlado.

---

### Matriz resumida

| Recurso | Atletas e alunos | Organizações, professores e técnicos | Federações |
|---|:---:|:---:|:---:|
| Perfil e jornada pessoal | Próprios | Consulta vinculada | Consulta autorizada |
| Agenda e check-in | Participam | Gerenciam turmas | Relatório consolidado |
| Avaliação técnica | Visualizam | Registram e supervisionam | Auditam quando aplicável |
| Graduação | Visualizam | Propõem ou validam internamente | Homologam quando oficial |
| Mensalidades | Próprias | Gerenciam conforme permissão | Não |
| Equipe de competição | Participam | Montam e inscrevem equipes | Regulam e homologam |
| Eventos | Inscrição | Inscrevem atletas | Criam ou homologam |
| Filiação | Visualizam | Solicitam ou renovam | Aprovam e administram |
| Relatórios | Pessoais | Turmas ou organização | Rede federativa |

---

### Hierarquia interna do segundo grupo

Embora exista apenas um grupo visível no login, o sistema utilizará funções internas:

- proprietário ou gestor da organização;
- coordenador técnico;
- professor;
- técnico de competição;
- auxiliar;
- atendente ou financeiro.

O gestor credencia o técnico para competições e atletas específicos. A conta `CLUB_TECHNICIAN` permanece tecnicamente bloqueada fora da operação do evento, independentemente das permissões administrativas do clube.

---

### Regras de segurança

- controle de acesso baseado em papéis e permissões;
- autenticação multifator para organizações e federações;
- verificação documental de profissionais, organizações e federações;
- isolamento dos dados de cada organização;
- auditoria de graduação, filiação, pagamentos e certificados;
- gerenciamento de sessões e dispositivos;
- revisão periódica das permissões da equipe;
- consentimento e conta vinculada ao responsável legal para menores de idade;
- princípio do menor privilégio: cada usuário recebe apenas o acesso necessário.

### Administração interna

A operação técnica da Apex Combate precisará de acesso interno para suporte, segurança e moderação. Esse acesso não será apresentado como um grupo comum no aplicativo e deverá ser restrito, auditado e protegido por autenticação reforçada.

---

## Parte 5 — Sistema de login

**Documento de origem:** `sistema-login-apex-combate.md`

### Apresentação anterior ao login

A v39 inicia em uma tela pública de boas-vindas, distinta da autenticação. Ela usa o logo oficial, a assinatura **“Uma plataforma. Todas as lutas.”**, explica como o ecossistema funciona e apresenta somente **ATLETA**, **CLUBE** e **FEDERAÇÃO**.

O login não é aberto por temporizador nem por redirecionamento automático. O visitante precisa pressionar **Entrar no Apex** ou **Escolher perfil de acesso**. O botão **Como funciona** navega apenas pela apresentação. Ao encerrar uma sessão, a aplicação retorna às boas-vindas.

A apresentação compartilha o catálogo internacional e a tradução efetiva da interface, além de responder de 320 px a telas grandes e TVs. Depois do avanço explícito, a composição oficial do login e seus três perfis permanecem preservados.

### Perfil ATLETA

#### Objetivo

Permitir acesso rápido pelo celular durante treinos e eventos, sem senha complexa e sem confirmação por WhatsApp.

#### Identificação

1. **CPF ou documento**;
2. **Data de nascimento**;
3. Acesso direto ao dashboard após validação dos dados.

#### CPF ou documento

- O campo aceita CPF com ou sem pontos e traço;
- Quando a entrada possui somente números, a interface pode aplicar a máscara `000.000.000-00`;
- Um CPF válido é normalizado para conter somente os 11 dígitos;
- O mesmo campo aceita documento nacional ou passaporte de outros países;
- Documentos internacionais podem conter letras, números e símbolos válidos;
- Não existe seleção de país no login.

#### Data de nascimento

Formatos aceitos:

- `DD/MM/AAAA`;
- `DD-MM-AAAA`;
- `DDMMAAAA`;
- `AAAA-MM-DD`;
- `AAAAMMDD`.

Internamente, a data é normalizada para o formato ISO `AAAA-MM-DD`.

#### Fluxo

Escolher ATLETA → informar CPF ou documento → informar data de nascimento → higienizar e validar os dados → abrir o dashboard do atleta.

#### Observação de segurança

Documento e data de nascimento são dados de identificação conhecidos e oferecem proteção limitada. Para manter o acesso rápido sem WhatsApp, uma versão de produção deverá aplicar controles adicionais nos bastidores, como limite de tentativas, detecção de acessos suspeitos, bloqueio temporário e registro de auditoria. Biometria ou Passkey poderá ser oferecida futuramente como opção, sem ser obrigatória.

---

### Perfil CLUBE / ACADEMIA

#### Objetivo

Oferecer o mesmo acesso público CLUBE para a administração da organização e para subcontas individuais. A conta administrativa gerencia o clube; a conta do técnico abre exclusivamente sua área privada de assistência durante competições.

#### Campos

1. **Usuário**;
2. **Senha**.

O mesmo formulário do perfil CLUBE aceita:

- a conta administrativa do clube ou academia;
- uma subconta individual de professor ou técnico, com permissões limitadas.

O usuário é normalizado antes do envio. Professores e técnicos continuam pertencendo ao grupo CLUBE e não criam um quarto perfil público.

#### Requisição

O acesso envia uma requisição HTTP `POST` para `/api/login` com JSON:

```json
{
  "usuario": "RYUZOKAN",
  "senha": "SENHA_DO_CLUBE",
  "perfil": "clube"
}
```

#### Fluxo

Escolher CLUBE → informar usuário → informar senha → normalizar o identificador → enviar `POST /api/login` → identificar o papel interno → abrir o dashboard administrativo do clube ou a área privada do técnico de competição.

#### Demonstração

**Administração do clube**

- Usuário: `RYUZOKAN`;
- Senha: `2026`.

**Subconta do técnico**

- Usuário: `TECNICO.MARCELO`;
- Senha: `TECNICO2026`;
- Permissão: `CLUB_TECHNICIAN`;
- Direcionamento automático para a área privada individual do técnico;
- O atleta pode selecionar somente técnicos do próprio clube que estejam credenciados na competição escolhida;
- Acesso exclusivamente operacional durante competições: evento atribuído, atletas vinculados, fila de lutas, linha do tempo, chamada, pesagem, equipamentos, aquecimento, checklist, plano de corner, credencial QR, avisos, regras, ocorrências e suporte da organização;
- Sincronização automática e modo offline com envio das ações pendentes após a reconexão;
- Sem acesso ao cadastro geral de alunos, turmas, financeiro, equipe ou administração do clube.

#### Segurança de produção

- usar somente HTTPS;
- armazenar a senha como hash forte, nunca em texto simples;
- limitar tentativas e aplicar bloqueio temporário;
- não registrar a senha nos logs;
- emitir sessão segura com expiração;
- exigir troca da senha inicial;
- permitir permissões diferentes para gestor, mestre, técnico e atendente.

O servidor `server.py` autentica a conta no banco persistente local e emite um JWT com expiração. Em produção, o banco deverá ser migrado para PostgreSQL e executado atrás de HTTPS.

---

### Perfil FEDERAÇÃO / ADMINISTRAÇÃO

#### Objetivo

Manter uma única entrada pública **FEDERAÇÃO** para dois tipos de conta da mesma entidade:

- **Presidente da Federação**, que utiliza o acesso federativo normal para governança, relatórios, auditoria e decisões finais;
- **Central da Federação (Admin)**, que utiliza a credencial administrativa para executar a operação da federação, validar atletas, gerenciar filiados, homologar eventos e operar competições.

Não existe um quarto perfil ou outro botão público. A permissão vinculada à credencial define o nível de acesso depois do OTP.

#### Campos da primeira etapa

1. **Admin**;
2. **Senha**.

O mesmo formulário aceita a credencial da Federação ou a credencial Admin.

#### Passo 1 — autenticação primária

O frontend envia `POST /api/login`:

```json
{
  "usuario": "ADMIN",
  "senha": "SENHA_ADMINISTRATIVA",
  "perfil": "federacao"
}
```

O backend confirma as credenciais e exige a permissão `PRESIDENTE_MASTER` ou `ADMIN`. Uma conta autorizada recebe:

```json
{
  "status": "2FA_REQUIRED",
  "challengeId": "identificador_temporario",
  "expiresIn": 300
}
```

Nenhum token administrativo é liberado nessa etapa.

#### Passo 2 — código OTP

O frontend abre uma janela modal e envia `POST /api/login/validar-otp`:

```json
{
  "challengeId": "identificador_temporario",
  "codigo": "654321",
  "perfil": "federacao"
}
```

Após validação positiva, o servidor emite um JWT com sessão de uma hora e permissões administrativas para placar, cronômetro e súmula.

#### Demonstração

As duas contas utilizam o mesmo formulário do botão **FEDERAÇÃO**.

**Presidente da Federação — acesso normal**

- Admin: `PRESIDENTE`;
- Senha: `MASTER2026`;
- Código OTP: `654321`;
- Permissão: `PRESIDENTE_MASTER`.

**Central da Federação — Admin**

- Admin: `ADMIN`;
- Senha: `MASTER2026`;
- Código OTP: `654321`;
- Permissão: `ADMIN`.

#### Controles implementados no servidor demonstrativo

- desafio 2FA temporário com expiração de cinco minutos;
- limite de cinco tentativas de OTP;
- desafio utilizado somente uma vez;
- comparação segura das credenciais;
- JWT assinado com HMAC SHA-256;
- token com expiração de uma hora;
- permissões explícitas para placar, cronômetro e punições;
- respostas da API sem cache.

Em produção, senhas deverão usar hash forte, o segredo JWT deverá ficar em cofre seguro e os códigos OTP deverão ser gerados aleatoriamente e enviados por um provedor real.

---

## Parte 6 — Backend, banco e APIs

**Documento de origem:** `backend-apex-combate.md`

### Arquitetura atual

- Servidor HTTP/API: `server.py`, somente com biblioteca padrão do Python.
- Persistência: SQLite em `data/apex-combate.sqlite3`.
- Camada de dados e migração inicial: `apex_db.py`.
- Autenticação: JWT HS256 com segredo local persistente e validade de 1 hora.
- Senhas: PBKDF2-SHA256 com salt individual e 260.000 iterações.
- Perfis públicos: `atleta`, `clube` e `federacao`.
- Arquitetura de governança: múltiplas federações isolam suas próprias redes; o modelo preserva uma futura Apex Central proprietária acima delas, atualmente desabilitada.
- Federações controlam clubes, atletas, eventos, homologações, regras e auditoria dentro do próprio tenant.
- A Central da Federação usa a mesma entrada pública FEDERAÇÃO e representa a administração da própria federação.
- O acesso proprietário de Mozer à Apex Central está adiado e desabilitado; não existe um quarto perfil público.
- Federação: autenticação em duas etapas obrigatória.
- Auditoria: ações críticas persistidas em `audit_log`.
- Limitação básica de tentativas por IP nos endpoints de autenticação.
- Supabase não é utilizado.
- A v44 preserva esse backend e mantém a apresentação pública anterior ao login; na tela de autenticação, somente o tradutor discreto permanece no topo, com avanço explícito. Na área autenticada, o controle compartilhado “Voltar ao início” aciona o encerramento existente, remove tokens, metadados de perfil, escopos e caches locais relacionados e retorna à abertura pública.

### Endpoints principais

#### Plataforma

- `GET /api/health`
- `GET /api/version`
- `GET /api/session`
- `POST /api/translate`

#### Autenticação

- `POST /api/login/atleta`
- `POST /api/login` para clube e primeira etapa da federação
- `POST /api/login/validar-otp`

#### Atleta

- `GET /api/athlete/dashboard`
- `GET /api/competitions`
- `POST /api/registrations`

#### Clube e técnicos

- `GET /api/club/dashboard`
- `GET /api/club/technicians`
- `POST /api/club/students`
- `POST /api/club/competition-technicians`

A conta administrativa usa `CLUB_ADMIN`. O técnico entra com usuário e senha individuais pelo mesmo perfil público CLUBE, recebe `CLUB_TECHNICIAN` e é direcionado para sua própria central de competição. Não acessa alunos em geral, turmas, financeiro nem administração do clube.

#### Central operacional do técnico

- `GET /api/technician/operations`
- `POST /api/technician/status`
- `POST /api/technician/checklist`
- `POST /api/technician/strategy`
- `POST /api/technician/result`
- `POST /api/technician/incident`
- `POST /api/technician/support`
- `POST /api/technician/notice-read`

Todas essas rotas exigem `CLUB_TECHNICIAN` e validam se a competição e o atleta estão explicitamente atribuídos ao técnico autenticado. A resposta operacional inclui fila de lutas, linha do tempo, checklists, plano de corner, credencial, avisos e regras somente desse escopo. Na inscrição, o atleta só pode selecionar técnicos do próprio clube que possuam credenciamento confirmado para a competição escolhida.

#### Federação

- `GET /api/federation/dashboard`
- `POST /api/federation/homologations`

#### Apex Central

As rotas proprietárias permanecem desabilitadas nesta fase. A futura Apex Central de Mozer não utiliza as credenciais da Central da Federação.

### Dados persistidos

- Clubes e credenciais administrativas do clube;
- Atletas e vínculos com clube;
- Contas administrativas da federação;
- Competições;
- Inscrições de atletas e vínculo com o técnico escolhido;
- Operação de competição por atleta: etapa, chamada, área, luta, aquecimento, checklist, plano de corner e anotação de resultado;
- Avisos, ocorrências e solicitações de suporte do técnico;
- Processos de homologação;
- Auditoria de acessos e operações.

### Fundação de desenvolvimento no GitHub

A base v38 foi preparada para versionamento profissional:

- repositório Git local inicializado na branch `main`;
- `.gitignore` protegendo banco, segredo JWT, uploads, ambientes e certificados móveis;
- `.env.example` sem credenciais;
- `README.md`, licença proprietária, política de segurança e guia de contribuição;
- imagem Docker executada por usuário sem privilégios e com volume separado para dados;
- `docker-compose.yml` para desenvolvimento;
- testes unitários, contratos de produto e smoke test de API;
- GitHub Actions para Python 3.11, 3.12 e 3.13, autenticação ponta a ponta e construção Docker;
- templates para issues e pull requests;
- porta, host, diretório de dados e segredo JWT configuráveis por ambiente;
- bloqueio HTTP de arquivos internos, código-fonte, documentação e dados sensíveis.

O código está publicado no repositório oficial público `https://github.com/MozerBlack/apex-combate-oficial`. O GitHub Actions valida testes, contratos, autenticação e Docker antes das próximas entregas. A demonstração completa está publicada em `https://apex-combate-demo.onrender.com` por integração automática com a branch `main`.

### Fluxos integrados adicionados na v38

#### Atleta

- perfil esportivo e contato de emergência editáveis;
- peso e categoria atualizados pelo próprio atleta;
- central documental com identificação, atestado, termo, autorização e certificado;
- situação documental e prontidão calculadas no backend;
- responsáveis vinculados para menores;
- turmas matriculadas e histórico de presença;
- inscrições e técnicos elegíveis preservados.

#### Clube

- listagem real de alunos com documentos e último check-in;
- alteração auditável da situação do aluno;
- criação de turmas com modalidade, nível, horário, professor, local e capacidade;
- matrícula automática no primeiro check-in;
- presença auditável com prevenção de duplicidade diária;
- delegações por competição;
- prontidão individual por aprovação, documentos, categoria e pagamento;
- métricas integradas de turmas, presenças e delegação.

#### Novas entidades

- `athlete_documents`;
- `athlete_guardians`;
- `club_classes`;
- `class_enrollments`;
- `attendance_records`;
- `delegations`;
- `delegation_members`.

#### Novas rotas

- `POST /api/athlete/profile`;
- `POST /api/athlete/documents`;
- `POST /api/club/students/status`;
- `POST /api/club/classes`;
- `POST /api/club/attendance`;
- `POST /api/club/delegations/members`.

### Evolução para produção

1. Migrar SQLite para PostgreSQL mantendo o mesmo modelo relacional.
2. Executar a API atrás de HTTPS e proxy reverso.
3. Armazenar o segredo JWT em serviço de segredos ou variável segura.
4. Substituir OTP demonstrativo por TOTP, e-mail ou SMS real.
5. Adicionar refresh tokens revogáveis e gerenciamento de dispositivos.
6. Adicionar armazenamento S3 compatível para documentos.
7. Implementar filas assíncronas para notificações, relatórios e traduções.
8. Ampliar a suíte já iniciada com testes de integração e ponta a ponta para todos os fluxos críticos.
9. Adicionar observabilidade, backups e recuperação de desastre.
10. Aplicar políticas completas de LGPD e retenção de dados.

---

## Parte 7 — Compatibilidade, responsividade e PWA

**Documento de origem:** `compatibilidade-apex-combate.md`

### Objetivo

A Apex Combate deverá oferecer a mesma conta e os mesmos dados em qualquer tela, adaptando navegação, densidade e tamanho dos elementos ao dispositivo.

### Faixas de layout

| Contexto | Larguras de referência | Comportamento |
|---|---:|---|
| Celular compacto | 320–359 px | Conteúdo em uma coluna, textos compactos e navegação inferior |
| Celular | 360–700 px | Navegação inferior, cartões empilhados e modais em tela reduzida |
| Tablet retrato | 701–820 px | Área integral, navegação inferior e cartões mais largos |
| Tablet paisagem / notebook compacto | 821–1180 px | Barra lateral e conteúdo principal; painel auxiliar oculto |
| Notebook / desktop | 1181–1439 px | Layout completo com três áreas quando houver espaço |
| Desktop Full HD | 1440–1999 px | Mais respiro, hero ampliado e maior densidade de informações |
| Monitor 2K/4K e TV | 2000–2560+ px | Tipografia, controles e painéis ampliados para leitura à distância |

### Recursos já adicionados ao protótipo

- apresentação pública anterior ao login, responsiva de celulares compactos a TVs e sem avanço automático;
- layout responsivo de 320 px a telas 4K;
- suporte a retrato e paisagem;
- áreas seguras para notch e barra de gestos;
- botões maiores em telas sensíveis ao toque;
- navegação completa por teclado ou controle remoto que emule teclado;
- foco visual de alto contraste;
- respeito à preferência de redução de movimento;
- adaptação para modos de contraste forçado;
- imagens incorporadas sem dependência de CDN;
- manifesto PWA para instalação;
- service worker para funcionamento offline após o primeiro acesso por HTTPS;
- área do técnico com cache local do último painel sincronizado, checklists e ações enfileiradas para envio automático após a reconexão;
- ícones de 192 px e 512 px;
- orientação livre, sem bloqueio de rotação.

### Matriz mínima de testes

Antes de cada lançamento, testar pelo menos:

1. 320 × 568 — celular compacto;
2. 360 × 800 — Android comum;
3. 390 × 844 — iPhone moderno;
4. 844 × 390 — celular em paisagem;
5. 768 × 1024 — tablet em retrato;
6. 1024 × 768 — tablet em paisagem;
7. 1366 × 768 — notebook;
8. 1440 × 900 — notebook de alta resolução;
9. 1920 × 1080 — desktop e TV Full HD;
10. 2560 × 1440 — monitor QHD;
11. 3840 × 2160 — TV ou monitor 4K.

### Navegadores-alvo

- Chrome e Edge modernos;
- Safari no iPhone, iPad e macOS;
- Firefox moderno;
- Samsung Internet;
- navegadores Android baseados em Chromium;
- navegadores de Smart TV com suporte adequado a HTML5, CSS Grid e JavaScript moderno.

### Observação sobre “todas as versões”

Não é tecnicamente seguro prometer compatibilidade com todo aparelho ou navegador já produzido. Smart TVs antigas e navegadores desatualizados podem não suportar recursos modernos. A estratégia correta é:

1. manter uma versão web responsiva como base universal;
2. testar nos aparelhos e navegadores definidos na matriz;
3. oferecer uma interface simplificada quando recursos avançados não existirem;
4. empacotar versões específicas para Android, iOS ou plataformas de TV somente se distribuição em lojas for necessária;
5. acompanhar métricas reais de dispositivos para ajustar o suporte.

### Entregáveis móveis finais: Android e iOS

O Apex Combate terá aplicativos instaláveis para **Android e iPhone/iPad**, usando a mesma base responsiva. A versão web/PWA continuará disponível para notebooks, computadores, tablets, TVs e como alternativa em dispositivos móveis limitados.

A existência do APK Android é um entregável obrigatório do projeto, mas sua instalação não será obrigatória para utilizar a plataforma. O usuário poderá escolher entre abrir o Apex Combate no navegador, instalá-lo como PWA ou utilizar o aplicativo correspondente ao seu sistema.

#### Formatos Android

- **APK de demonstração:** instalação direta no aparelho para apresentação e testes;
- **APK de produção assinado:** distribuição controlada fora da loja, quando necessária;
- **AAB de produção:** publicação na Google Play Store;
- **PWA:** alternativa universal e fallback para aparelhos não compatíveis com o pacote Android.

#### Formatos iPhone e iPad

- **build de desenvolvimento:** testes em simuladores e aparelhos autorizados;
- **TestFlight:** distribuição segura da versão de demonstração para professores, avaliadores e testadores;
- **IPA assinado:** artefato técnico gerado no processo de compilação e assinatura;
- **App Store:** distribuição pública oficial após análise da Apple;
- **PWA:** alternativa imediata para aparelhos que não possam instalar a versão nativa.

#### Arquitetura compartilhada

- a interface responsiva será empacotada em contêineres Android e iOS, preferencialmente com Capacitor;
- os aplicativos conterão os recursos visuais necessários para abrir a interface e o modo demonstrativo;
- autenticação, dados sincronizados e operações oficiais utilizarão a API Apex por HTTPS;
- o servidor e o banco de produção não serão embutidos nos aplicativos;
- dados essenciais poderão ser armazenados de forma segura para operação offline e sincronizados depois;
- câmera, QR Code, notificações, compartilhamento, biometria e arquivos poderão utilizar integrações nativas;
- nenhuma chave de assinatura, segredo JWT ou credencial de produção será incluída no repositório ou exposta nos pacotes.

#### Identidade prevista

- nome público: **Apex Combate**;
- identificador Android sugerido: `br.com.apexcombate.app`;
- Bundle ID iOS sugerido: `br.com.apexcombate.app`;
- ícone: logotipo oficial;
- orientação: livre;
- aparência: Dark Mode oficial;
- atualização: controle de versão, assinatura e trilha de releases no GitHub.

#### Requisitos específicos da Apple

- projeto iOS compatível com Xcode;
- conta Apple Developer pertencente a Mozer ou à empresa responsável;
- certificados e perfis de provisionamento;
- configuração no App Store Connect;
- política de privacidade e informações de tratamento de dados;
- testes em iPhone e iPad reais;
- aprovação da Apple antes da publicação pública;
- automação em ambiente macOS, inclusive por GitHub Actions quando configurado.

#### Limites técnicos

APK/AAB são formatos exclusivos do Android. No ecossistema Apple, a distribuição ocorre por TestFlight e App Store. Versões muito antigas do iOS que não aceitem o runtime, HTTPS ou os requisitos de segurança atuais continuarão com acesso à PWA ou ao modo leve, quando tecnicamente seguro.

A geração dos aplicativos exigirá projetos Android e iOS, assinaturas digitais independentes, matrizes de testes, políticas de atualização e empacotamento automatizado.

---

## Parte 8 — Apex Central de Mozer

**Documento de origem:** `admin-apex-central.md`

A Central do proprietário, pertencente ao Mozer, ficará acima das federações e será construída em uma etapa posterior.

### Decisão vigente

- O botão público **FEDERAÇÃO** aceita o Presidente e a Central Administrativa da própria federação.
- `PRESIDENTE / MASTER2026 / 654321` representa o Presidente da Federação.
- `ADMIN / MASTER2026 / 654321` representa a Central da Federação Paranaense.
- A Central do proprietário não utiliza o login da Federação.
- Não existe um quarto botão na tela pública.
- A conta e as rotas da Central do proprietário estão desativadas nesta etapa.

### Arquitetura preservada para o futuro

O modelo de dados já permite uma Apex Central acima de múltiplas federações, com isolamento por `federation_id`. Quando a Central for construída, ela terá rota interna, autenticação e permissões próprias, sem se confundir com o Admin federativo.

---

## Parte 9 — Apex’s Forge

**Documento de origem:** `apexs-forge.md`

**Proprietário:** Mozer  
**Status:** nome oficial aprovado; implementação futura  
**Nome oficial:** Apex’s Forge  
**Vínculo:** produto separado conectado ao Apex Combate por API comercial  
**Slogan de trabalho:** Forje sua marca. Eleve seu negócio.

---

### 1. Decisão

As lojas virtuais não serão administradas dentro dos dashboards esportivos do Apex Combate. Será criado um segundo aplicativo para lojistas acompanharem e controlarem produtos, estoque, pedidos, vendas e repasses.

A separação preserva a simplicidade do aplicativo esportivo e oferece uma operação comercial profissional para vendedores.

---

### 2. Divisão de responsabilidades

#### Apex Combate

Aplicativo esportivo usado por atletas, clubes, técnicos e federações.

Na futura experiência comercial, poderá oferecer ao comprador:

- descoberta de produtos;
- busca e filtros;
- página da loja;
- página do produto;
- carrinho;
- checkout;
- pagamento;
- acompanhamento do pedido;
- avaliação e atendimento.

O Apex Combate continua com exatamente três perfis públicos: ATLETA, CLUBE e FEDERAÇÃO.

#### Aplicativo dos lojistas

Aplicativo separado usado por:

- lojas de artigos esportivos;
- marcas e fabricantes;
- clubes com produtos próprios;
- federações com produtos oficiais;
- vendedores autorizados.

Esse aplicativo terá autenticação e papéis comerciais próprios. Esses papéis não são novos perfis públicos do Apex Combate.

---

### 3. Painel da loja

O lojista deve visualizar:

- faturamento do dia e do período;
- quantidade de pedidos;
- ticket médio;
- pedidos pendentes;
- produtos mais vendidos;
- produtos com estoque baixo;
- cancelamentos e devoluções;
- valores brutos, taxas, comissão e líquido;
- repasses pendentes e concluídos;
- desempenho por modalidade e campanha.

---

### 4. Catálogo e produtos

#### Cadastro

- nome;
- descrição curta e completa;
- categoria;
- modalidade;
- marca;
- fabricante;
- SKU;
- código de barras;
- fotos;
- vídeo opcional;
- preço normal;
- preço promocional;
- custo interno opcional;
- peso e dimensões;
- dados fiscais;
- prazo de preparação;
- garantia;
- regras de troca;
- selo oficial ou homologação quando aplicável.

#### Variações

- tamanho;
- cor;
- modelo;
- material;
- lado ou versão;
- SKU e código de barras por variação;
- preço e estoque por variação.

#### Estados

- rascunho;
- em análise;
- aprovado;
- publicado;
- pausado;
- estoque baixo;
- esgotado;
- rejeitado;
- arquivado.

#### Ações

- criar;
- editar;
- duplicar;
- publicar;
- pausar;
- arquivar;
- ajustar preço;
- programar promoção;
- importar e exportar catálogo;
- acompanhar avaliações.

---

### 5. Estoque

- estoque por produto e variação;
- entrada e saída;
- reserva durante o checkout;
- liberação após falha ou expiração do pagamento;
- estoque mínimo;
- alertas de reposição;
- múltiplos depósitos ou unidades;
- inventário;
- ajuste com motivo;
- histórico imutável de movimentações;
- integração futura com ERP.

Exemplo:

| Produto | Variação | Disponível | Reservado | Situação |
|---|---|---:|---:|---|
| Kimono Apex Pro | Branco A2 | 8 | 2 | Normal |
| Kimono Apex Pro | Azul A2 | 3 | 1 | Estoque baixo |
| Kimono Apex Pro | Preto A2 | 0 | 0 | Esgotado |

---

### 6. Pedidos

#### Estados

1. criado;
2. aguardando pagamento;
3. pagamento aprovado;
4. em separação;
5. pronto para retirada;
6. enviado;
7. entregue;
8. cancelado;
9. em troca;
10. devolvido;
11. reembolsado.

#### Recursos

- detalhes do pedido;
- itens, variações e quantidades;
- identificação mínima do cliente;
- endereço quando necessário;
- etiqueta de envio;
- código de rastreamento;
- retirada na loja, clube ou competição;
- comprovação por QR Code;
- histórico de mudanças;
- mensagens operacionais;
- cancelamento, troca e devolução.

---

### 7. Financeiro e marketplace

- PIX;
- cartão;
- antifraude;
- split de pagamento;
- comissão Apex Combate;
- valor líquido da loja;
- agenda de recebíveis;
- estornos;
- reembolsos;
- repasses;
- extratos;
- conciliação;
- documentos fiscais;
- exportação contábil.

A plataforma não deve armazenar dados brutos de cartão. O processamento deve ser realizado por gateway certificado que suporte marketplace e divisão de pagamentos.

---

### 8. Entregas e retirada

- entrega residencial;
- transportadoras;
- Correios ou agregador logístico;
- retirada na loja;
- retirada no clube;
- retirada em competição;
- cálculo de frete;
- prazo estimado;
- rastreamento;
- confirmação de entrega;
- QR Code para retirada.

Retirada em competição deve ser coordenada com a organização sem misturar permissões da loja com a área operacional do técnico.

---

### 9. Marketing

- cupons;
- descontos por período;
- combos e kits;
- frete grátis;
- campanhas por modalidade;
- produtos patrocinados;
- vitrines sazonais;
- lançamento de coleção;
- segmentação respeitando consentimento;
- relatórios de conversão.

Publicidade deve ser claramente identificada.

---

### 10. Papéis da equipe da loja

| Papel | Permissões principais |
|---|---|
| Proprietário | Controle total, equipe, financeiro e contratos |
| Gerente | Produtos, estoque, pedidos e campanhas |
| Catálogo | Cadastro e manutenção de produtos |
| Estoquista | Inventário e movimentações |
| Separação | Preparação e expedição |
| Financeiro | Recebíveis, repasses e relatórios |
| Atendimento | Mensagens, trocas e devoluções |

O princípio é menor privilégio. Ações sensíveis devem ser auditadas.

---

### 11. Onboarding da loja

- tipo de vendedor;
- nome empresarial e nome da loja;
- CPF/CNPJ conforme o caso;
- responsável legal;
- endereço;
- contato;
- dados bancários enviados diretamente ao provedor autorizado;
- documentos;
- aceite de contrato;
- política de produtos;
- verificação;
- aprovação;
- criação dos usuários internos.

Deve existir revisão contra fraude, venda de itens proibidos, falsificação e uso indevido de marcas.

---

### 12. Integração com o Apex Combate

#### Serviços comerciais compartilhados

- identidade comercial;
- lojas;
- catálogo;
- mídia de produtos;
- estoque;
- preços;
- carrinho;
- pedidos;
- pagamentos;
- logística;
- cupons;
- avaliações;
- repasses;
- auditoria comercial.

#### Comunicação

- APIs versionadas;
- webhooks assinados;
- eventos assíncronos;
- idempotência;
- sincronização de estoque;
- notificações em tempo real;
- trilha de auditoria.

#### Identificadores

O serviço comercial pode guardar referências mínimas, como `apex_user_id`, `club_id` ou `federation_id`, sem copiar o cadastro esportivo completo.

---

### 13. Isolamento de dados

A loja não pode acessar:

- documentos esportivos;
- data de nascimento além do estritamente necessário e permitido;
- graduações;
- dados médicos;
- histórico de treino;
- administração de clubes;
- ferramentas de federações;
- área dos técnicos;
- operação da Apex Central.

O comércio recebe apenas dados necessários para compra, entrega, fiscal, suporte e prevenção de fraude.

---

### 14. Segurança e conformidade

- HTTPS;
- autenticação forte;
- 2FA para proprietários e financeiro;
- sessões revogáveis;
- RBAC;
- auditoria;
- criptografia;
- segregação por `store_id`;
- LGPD;
- política de retenção;
- consentimento de marketing;
- prevenção contra fraude;
- moderação de catálogo;
- PCI por meio do gateway;
- regras fiscais e consumeristas;
- processo de incidente e suporte.

---

### 15. Modelo de dados proposto

- `stores`
- `store_users`
- `store_roles`
- `seller_verifications`
- `products`
- `product_media`
- `product_variants`
- `categories`
- `modalities`
- `inventory_locations`
- `inventory_balances`
- `inventory_movements`
- `prices`
- `promotions`
- `coupons`
- `carts`
- `cart_items`
- `orders`
- `order_items`
- `payments`
- `payment_splits`
- `payouts`
- `shipments`
- `returns`
- `refunds`
- `reviews`
- `seller_notifications`
- `commerce_audit_log`

---

### 16. Modelo de receita

- comissão por venda;
- assinatura de loja;
- plano premium;
- produto patrocinado;
- posição de destaque;
- campanhas de marca;
- serviços logísticos;
- ferramentas avançadas de análise;
- vendas de produtos oficiais Apex Combate.

As taxas devem ser claras antes da publicação da loja e em cada pedido.

---

### 17. Fases recomendadas

#### Fase 1 — fundação

- identidade final;
- onboarding;
- autenticação;
- cadastro de loja;
- catálogo;
- variações;
- estoque;
- painel básico.

#### Fase 2 — pedidos

- carrinho no Apex Combate;
- checkout;
- pedidos;
- atualização de status;
- retirada e entrega.

#### Fase 3 — pagamentos

- PIX e cartão;
- antifraude;
- split;
- comissão;
- repasses;
- estorno.

#### Fase 4 — escala

- logística integrada;
- fiscal;
- promoções;
- anúncios;
- ERP;
- análises avançadas;
- internacionalização.

---

### 18. Decisões ainda pendentes

- identidade visual derivada;
- domínio e publicação nas lojas de aplicativos;
- quem pode vender no lançamento;
- comissão e planos;
- gateway de pagamento;
- operador logístico;
- política de aprovação de produtos;
- responsabilidade fiscal;
- cidade e grupo piloto.

Nenhuma dessas pendências altera a decisão principal: o Apex’s Forge será o aplicativo separado, conectado ao Apex Combate, para o lojista controlar os próprios produtos e vendas.

---

## Parte 10 — Registro oficial de decisões

**Documento de origem:** `registro-de-decisoes-apex-combate.md`

**Responsável pelo produto:** Mozer  
**Atualizado em:** 7 de outubro de 2026

Este arquivo registra decisões vigentes para impedir regressões de escopo ou interpretações conflitantes.

| ID | Decisão vigente | Estado |
|---|---|---|
| DEC-001 | O nome do produto é Apex Combate. | Aprovada |
| DEC-002 | O posicionamento é “Tudo em um”. | Aprovada |
| DEC-003 | A plataforma atende todas as modalidades. | Aprovada |
| DEC-004 | Existem exatamente três acessos públicos: ATLETA, CLUBE e FEDERAÇÃO. | Aprovada |
| DEC-005 | Professor e técnico pertencem ao perfil CLUBE; não existe quarto botão. | Aprovada |
| DEC-006 | Tema principal em Dark Mode e uso do logo oficial fornecido. | Aprovada |
| DEC-007 | Não criar a marca “Apex Arena”; competição offline é modo do Apex Combate. | Aprovada |
| DEC-008 | Atleta entra com documento/passaporte e nascimento, sem país e sem WhatsApp. | Aprovada |
| DEC-009 | Clube entra com Usuário e Senha. | Aprovada |
| DEC-010 | Federação entra com Admin e Senha, seguida de OTP. | Aprovada |
| DEC-011 | Presidente e Central Admin da Federação usam o mesmo perfil público FEDERAÇÃO. | Aprovada |
| DEC-012 | A Central da Federação não é a Central proprietária de Mozer. | Aprovada |
| DEC-013 | Apex Central de Mozer será construída depois e permanece desabilitada. | Adiada |
| DEC-014 | A federação é o cérebro operacional do ecossistema. | Aprovada |
| DEC-015 | Arquitetura de governança: Apex Central + múltiplas federações. | Aprovada |
| DEC-016 | Supabase não será utilizado. | Rejeição definitiva |
| DEC-017 | Técnico entra com login individual pelo perfil CLUBE e possui área privada própria. | Aprovada |
| DEC-018 | A única função do técnico é auxiliar atletas durante competições. | Aprovada |
| DEC-019 | Técnico só acessa competições e atletas atribuídos, chamada, pesagem, aquecimento, equipamento, credencial, avisos, regras e corner. | Aprovada |
| DEC-020 | Técnico não acessa alunos gerais, turmas, financeiro, clube, federação ou Apex Central. | Aprovada |
| DEC-021 | O atleta só pode selecionar técnico do clube credenciado na competição escolhida. | Aprovada |
| DEC-022 | A área técnica terá operação ao vivo, checklist, plano de corner, cronômetro, ocorrências, suporte e modo offline. | Implementada v36/v37 |
| DEC-023 | A aplicação deve responder de celulares compactos a TVs e 4K. | Aprovada |
| DEC-024 | O seletor de idioma traduz a interface real. | Aprovada |
| DEC-025 | Alterações de desenvolvimento recarregam automaticamente na prévia. | Implementada |
| DEC-026 | O fluxo completo da área do atleta foi escolhido. | Aprovada |
| DEC-027 | O marketplace será ligado ao Apex Combate, mas o controle das lojas ficará em segundo aplicativo. | Aprovada |
| DEC-028 | O aplicativo comercial separado e conectado por API tem o nome oficial **Apex’s Forge**. | Aprovada |
| DEC-029 | O aplicativo das lojas não cria quarto perfil público no Apex Combate. | Aprovada |
| DEC-030 | Lojas controlam produtos, variações, estoque, pedidos, vendas, equipe e repasses no Apex’s Forge. | Aprovada |
| DEC-031 | Apex Combate representa o ápice da jornada marcial; Apex’s Forge representa a forja comercial em que lojas constroem e fortalecem seus negócios. | Aprovada |
| DEC-032 | Apex Central é o nome da futura central proprietária de Mozer, núcleo máximo de comando e governança global, distinto da Central da Federação. | Aprovada e adiada para implementação futura |
| DEC-033 | O Apex Combate deve funcionar de forma responsiva e adaptável em celulares, tablets, notebooks, computadores, monitores grandes e TVs, com suporte a toque, mouse, teclado, orientação livre e PWA. | Requisito obrigatório |
| DEC-034 | Versões móveis antigas devem receber compatibilidade progressiva e modo leve sempre que suportarem os requisitos mínimos de HTTPS e autenticação segura; a segurança não poderá ser reduzida para acomodar navegadores obsoletos. | Requisito obrigatório |
| DEC-035 | O entregável Android final do Apex Combate será um APK, acompanhado por AAB para a Google Play e pela versão web/PWA universal. | Aprovada |
| DEC-036 | O Apex Combate também terá aplicativo instalável para iPhone e iPad, distribuído por TestFlight em demonstrações e pela App Store na publicação oficial, mantendo a PWA como alternativa. | Aprovada |
| DEC-037 | O APK Android é um entregável obrigatório do projeto, mas sua instalação não é obrigatória para utilizar o Apex Combate; navegador e PWA permanecem como acessos completos. | Aprovada |
| DEC-038 | O desenvolvimento será versionado no GitHub com proteção de segredos, testes automatizados, GitHub Actions e construção Docker; o envio ao repositório remoto dependerá da autorização segura de Mozer. | Aprovada e implementada |
| DEC-039 | O repositório oficial público da versão atual é `MozerBlack/apex-combate-oficial`; o repositório acadêmico anterior permanece separado e inalterado. | Aprovada e implementada |
| DEC-040 | A demonstração completa será publicada pelo Render em `https://apex-combate-demo.onrender.com`, integrada à branch `main`. | Aprovada e implementada |
| DEC-041 | A v38 prioriza as áreas completas de atleta e clube com perfil, documentos, responsáveis, turmas, presença, alunos e delegações persistentes. | Aprovada e implementada |
| DEC-042 | A v39 inicia em uma apresentação responsiva de boas-vindas e “Como funciona”; o login oficial só aparece após ação explícita em um botão, sem avanço automático, e o logout retorna à apresentação. | Aprovada e implementada |
| DEC-043 | O título institucional é “🥋 Apex Combate — Plataforma Universal de Artes Marciais”, aplicado na abertura pública e na documentação; “Uma plataforma. Todas as lutas.” permanece como assinatura. | Aprovada e implementada na v40 |
| DEC-044 | A faixa superior da apresentação pública é removida; a abertura começa diretamente no hero, mantendo “Entrar no Apex” e “Como funciona” no conteúdo principal. | Aprovada e implementada na v41 |
| DEC-045 | Na tela de login, o cabeçalho superior é reduzido ao tradutor discreto: removem-se logo auxiliar, links institucionais, botão superior “Entrar” e faixa visual; preservam-se a tradução real e o cartão central oficial. | Aprovada e implementada na v42 |
| DEC-046 | A tipografia da plataforma cresce de forma fluida conforme a área de exibição, com `clamp()`, unidades relativas, limites controlados, eliminação de textos funcionais de 6–9 px e mínimo de 16 px nos controles de formulário móveis. | Aprovada e implementada na v43 |
| DEC-047 | A área autenticada compartilha um único controle “Voltar ao início” para atleta, clube, técnico e federação; sua ativação encerra a sessão com limpeza de tokens, perfil, escopos e caches locais relacionados antes de retornar à abertura pública, com apresentação responsiva e acessível. | Aprovada e implementada na v44 |

### Regras de mudança

- Somente uma instrução explícita de Mozer pode substituir uma decisão aprovada.
- Uma decisão substituída deve permanecer no histórico com indicação da nova decisão.
- Mudanças de autenticação, perfis, governança, técnico ou comércio devem atualizar a documentação mestre e os documentos específicos.

---


## Encerramento

Esta documentação única deve ser atualizada sempre que Mozer aprovar uma alteração relevante no Apex Combate ou no Apex’s Forge. Os documentos modulares permanecem como fontes de manutenção, mas este arquivo é a referência consolidada para leitura, apresentação e planejamento do ecossistema.
