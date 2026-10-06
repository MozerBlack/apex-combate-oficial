# Sistema de Login — Apex Combate

## Apresentação anterior ao login

A aplicação inicia em uma tela pública de boas-vindas, distinta da autenticação. Essa apresentação usa o logo oficial, a assinatura **“Uma plataforma. Todas as lutas.”**, explica como o ecossistema funciona e apresenta somente os grupos **ATLETA**, **CLUBE** e **FEDERAÇÃO**.

A tela de login não aparece por temporizador nem por redirecionamento automático. O visitante precisa pressionar **Entrar**, **Entrar no Apex** ou **Escolher perfil de acesso**. Depois disso, a composição oficial de login permanece inalterada e oferece exatamente os três perfis públicos. O botão **Como funciona** apenas navega pela própria apresentação. Ao encerrar uma sessão, a pessoa retorna às boas-vindas.

O seletor de idioma da apresentação usa o mesmo catálogo internacional e a mesma tradução efetiva da interface. O layout é adaptável de 320 px a telas grandes e TVs.

## Perfil ATLETA

### Objetivo

Permitir acesso rápido pelo celular durante treinos e eventos, sem senha complexa e sem confirmação por WhatsApp.

### Identificação

1. **CPF ou documento**;
2. **Data de nascimento**;
3. Acesso direto ao dashboard após validação dos dados.

### CPF ou documento

- O campo aceita CPF com ou sem pontos e traço;
- Quando a entrada possui somente números, a interface pode aplicar a máscara `000.000.000-00`;
- Um CPF válido é normalizado para conter somente os 11 dígitos;
- O mesmo campo aceita documento nacional ou passaporte de outros países;
- Documentos internacionais podem conter letras, números e símbolos válidos;
- Não existe seleção de país no login.

### Data de nascimento

Formatos aceitos:

- `DD/MM/AAAA`;
- `DD-MM-AAAA`;
- `DDMMAAAA`;
- `AAAA-MM-DD`;
- `AAAAMMDD`.

Internamente, a data é normalizada para o formato ISO `AAAA-MM-DD`.

### Fluxo

Escolher ATLETA → informar CPF ou documento → informar data de nascimento → higienizar e validar os dados → abrir o dashboard do atleta.

### Observação de segurança

Documento e data de nascimento são dados de identificação conhecidos e oferecem proteção limitada. Para manter o acesso rápido sem WhatsApp, uma versão de produção deverá aplicar controles adicionais nos bastidores, como limite de tentativas, detecção de acessos suspeitos, bloqueio temporário e registro de auditoria. Biometria ou Passkey poderá ser oferecida futuramente como opção, sem ser obrigatória.

---

## Perfil CLUBE / ACADEMIA

### Objetivo

Oferecer o mesmo acesso público CLUBE para a administração da organização e para subcontas individuais. A conta administrativa gerencia o clube; a conta do técnico abre exclusivamente sua área privada de assistência durante competições.

### Campos

1. **Usuário**;
2. **Senha**.

O mesmo formulário do perfil CLUBE aceita:

- a conta administrativa do clube ou academia;
- uma subconta individual de professor ou técnico, com permissões limitadas.

O usuário é normalizado antes do envio. Professores e técnicos continuam pertencendo ao grupo CLUBE e não criam um quarto perfil público.

### Requisição

O acesso envia uma requisição HTTP `POST` para `/api/login` com JSON:

```json
{
  "usuario": "RYUZOKAN",
  "senha": "SENHA_DO_CLUBE",
  "perfil": "clube"
}
```

### Fluxo

Escolher CLUBE → informar usuário → informar senha → normalizar o identificador → enviar `POST /api/login` → identificar o papel interno → abrir o dashboard administrativo do clube ou a área privada do técnico de competição.

### Demonstração

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

### Segurança de produção

- usar somente HTTPS;
- armazenar a senha como hash forte, nunca em texto simples;
- limitar tentativas e aplicar bloqueio temporário;
- não registrar a senha nos logs;
- emitir sessão segura com expiração;
- exigir troca da senha inicial;
- permitir permissões diferentes para gestor, mestre, técnico e atendente.

O servidor `server.py` autentica a conta no banco persistente local e emite um JWT com expiração. Em produção, o banco deverá ser migrado para PostgreSQL e executado atrás de HTTPS.

---

## Perfil FEDERAÇÃO / ADMINISTRAÇÃO

### Objetivo

Manter uma única entrada pública **FEDERAÇÃO** para dois tipos de conta da mesma entidade:

- **Presidente da Federação**, que utiliza o acesso federativo normal para governança, relatórios, auditoria e decisões finais;
- **Central da Federação (Admin)**, que utiliza a credencial administrativa para executar a operação da federação, validar atletas, gerenciar filiados, homologar eventos e operar competições.

Não existe um quarto perfil ou outro botão público. A permissão vinculada à credencial define o nível de acesso depois do OTP.

### Campos da primeira etapa

1. **Admin**;
2. **Senha**.

O mesmo formulário aceita a credencial da Federação ou a credencial Admin.

### Passo 1 — autenticação primária

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

### Passo 2 — código OTP

O frontend abre uma janela modal e envia `POST /api/login/validar-otp`:

```json
{
  "challengeId": "identificador_temporario",
  "codigo": "654321",
  "perfil": "federacao"
}
```

Após validação positiva, o servidor emite um JWT com sessão de uma hora e permissões administrativas para placar, cronômetro e súmula.

### Demonstração

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

### Controles implementados no servidor demonstrativo

- desafio 2FA temporário com expiração de cinco minutos;
- limite de cinco tentativas de OTP;
- desafio utilizado somente uma vez;
- comparação segura das credenciais;
- JWT assinado com HMAC SHA-256;
- token com expiração de uma hora;
- permissões explícitas para placar, cronômetro e punições;
- respostas da API sem cache.

Em produção, senhas deverão usar hash forte, o segredo JWT deverá ficar em cofre seguro e os códigos OTP deverão ser gerados aleatoriamente e enviados por um provedor real.
