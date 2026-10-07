# Backend Apex Combate — Fundação local v41

## Arquitetura atual

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
- A v41 preserva esse backend e acrescenta no frontend uma apresentação pública anterior ao login, com avanço explícito e retorno após logout.

## Endpoints principais

### Plataforma

- `GET /api/health`
- `GET /api/version`
- `GET /api/session`
- `POST /api/translate`

### Autenticação

- `POST /api/login/atleta`
- `POST /api/login` para clube e primeira etapa da federação
- `POST /api/login/validar-otp`

### Atleta

- `GET /api/athlete/dashboard`
- `GET /api/competitions`
- `POST /api/registrations`

### Clube e técnicos

- `GET /api/club/dashboard`
- `GET /api/club/technicians`
- `POST /api/club/students`
- `POST /api/club/competition-technicians`

A conta administrativa usa `CLUB_ADMIN`. O técnico entra com usuário e senha individuais pelo mesmo perfil público CLUBE, recebe `CLUB_TECHNICIAN` e é direcionado para sua própria central de competição. Não acessa alunos em geral, turmas, financeiro nem administração do clube.

### Central operacional do técnico

- `GET /api/technician/operations`
- `POST /api/technician/status`
- `POST /api/technician/checklist`
- `POST /api/technician/strategy`
- `POST /api/technician/result`
- `POST /api/technician/incident`
- `POST /api/technician/support`
- `POST /api/technician/notice-read`

Todas essas rotas exigem `CLUB_TECHNICIAN` e validam se a competição e o atleta estão explicitamente atribuídos ao técnico autenticado. A resposta operacional inclui fila de lutas, linha do tempo, checklists, plano de corner, credencial, avisos e regras somente desse escopo. Na inscrição, o atleta só pode selecionar técnicos do próprio clube que possuam credenciamento confirmado para a competição escolhida.

### Federação

- `GET /api/federation/dashboard`
- `POST /api/federation/homologations`

### Apex Central

As rotas proprietárias permanecem desabilitadas nesta fase. A futura Apex Central de Mozer não utiliza as credenciais da Central da Federação.

## Dados persistidos

- Clubes e credenciais administrativas do clube;
- Atletas e vínculos com clube;
- Contas administrativas da federação;
- Competições;
- Inscrições de atletas e vínculo com o técnico escolhido;
- Operação de competição por atleta: etapa, chamada, área, luta, aquecimento, checklist, plano de corner e anotação de resultado;
- Avisos, ocorrências e solicitações de suporte do técnico;
- Processos de homologação;
- Auditoria de acessos e operações.

## Fundação de desenvolvimento no GitHub

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

## Fluxos integrados adicionados na v38

### Atleta

- perfil esportivo e contato de emergência editáveis;
- peso e categoria atualizados pelo próprio atleta;
- central documental com identificação, atestado, termo, autorização e certificado;
- situação documental e prontidão calculadas no backend;
- responsáveis vinculados para menores;
- turmas matriculadas e histórico de presença;
- inscrições e técnicos elegíveis preservados.

### Clube

- listagem real de alunos com documentos e último check-in;
- alteração auditável da situação do aluno;
- criação de turmas com modalidade, nível, horário, professor, local e capacidade;
- matrícula automática no primeiro check-in;
- presença auditável com prevenção de duplicidade diária;
- delegações por competição;
- prontidão individual por aprovação, documentos, categoria e pagamento;
- métricas integradas de turmas, presenças e delegação.

### Novas entidades

- `athlete_documents`;
- `athlete_guardians`;
- `club_classes`;
- `class_enrollments`;
- `attendance_records`;
- `delegations`;
- `delegation_members`.

### Novas rotas

- `POST /api/athlete/profile`;
- `POST /api/athlete/documents`;
- `POST /api/club/students/status`;
- `POST /api/club/classes`;
- `POST /api/club/attendance`;
- `POST /api/club/delegations/members`.

## Evolução para produção

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
