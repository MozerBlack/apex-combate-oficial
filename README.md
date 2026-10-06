🥋 Apex Combate — Plataforma Universal de Artes Marciais

Apex Combate é uma plataforma universal “Tudo em um” para atletas, clubes, dojôs, academias e federações de artes marciais. O produto cobre a jornada esportiva, a operação de competições e a governança multi-federação sem criar perfis públicos além de **ATLETA**, **CLUBE** e **FEDERAÇÃO**.

> Estado atual: v40 demonstrativa, com apresentação pública antes do login, frontend responsivo, PWA, API Python, banco SQLite local e fluxos integrados de atleta e clube. Antes de produção serão necessários PostgreSQL, HTTPS, OTP real, armazenamento seguro, monitoramento e infraestrutura gerenciada.

- **Demonstração online:** https://apex-combate-demo.onrender.com
- **Repositório oficial:** https://github.com/MozerBlack/apex-combate-oficial
- **Pipeline:** GitHub Actions com testes de contrato, autenticação, fluxos v38 e Docker.

## Propriedade

Produto de **Mozer**, proprietário do Apex Combate. Código e documentação são proprietários e permanecem reservados.

## Produtos do ecossistema

- **Apex Combate:** aplicativo esportivo e institucional;
- **Apex’s Forge:** aplicativo comercial separado para lojistas;
- **Apex Central:** futura central privada de governança de Mozer.

## Perfis públicos

1. **ATLETA** — cadastro, documentos, inscrições, histórico e jornada esportiva;
2. **CLUBE** — clubes, academias, professores e técnicos;
3. **FEDERAÇÃO** — governança, homologações, eventos e operação federativa.

Técnicos entram pelo perfil **CLUBE** com credenciais individuais e possuem acesso restrito à assistência de atletas designados durante competições.

## Entrada da plataforma

A v39 inicia em uma apresentação pública responsiva com boas-vindas, proposta “Uma plataforma. Todas as lutas.”, explicação do funcionamento e visão dos três grupos. O login oficial só é exibido quando a pessoa pressiona um botão **Entrar**; não existe avanço automático. Ao sair de uma conta, a aplicação retorna à apresentação. O seletor de idioma também traduz essa tela pela API existente.

## Início rápido

### Requisitos

- Python 3.11 ou superior;
- navegador moderno;
- nenhuma dependência Python externa para a versão demonstrativa.

### Execução local

```bash
python3 server.py
```

Abra:

```text
http://localhost:8080
```

A primeira execução cria o banco demonstrativo e um segredo JWT em `data/`. Esses arquivos são ignorados pelo Git.

### Configuração opcional

```bash
cp .env.example .env
set -a
. ./.env
set +a
python3 server.py
```

Variáveis aceitas:

| Variável | Finalidade | Padrão |
|---|---|---|
| `HOST` | Endereço de escuta | `0.0.0.0` |
| `PORT` | Porta HTTP | `8080` |
| `APEX_DATA_DIR` | Diretório de dados locais | `./data` |
| `APEX_DB_PATH` | Caminho opcional do SQLite | `<APEX_DATA_DIR>/apex-combate.sqlite3` |
| `APEX_JWT_SECRET` | Segredo JWT injetado pelo ambiente | arquivo local gerado automaticamente |
| `APEX_JWT_SECRET_FILE` | Arquivo alternativo do segredo | `<APEX_DATA_DIR>/.jwt-secret` |

## Docker

```bash
docker compose up --build
```

O serviço abre na porta 8080 e usa um volume nomeado para o banco demonstrativo.

## Qualidade

```bash
make check
make test
```

Ou diretamente:

```bash
python3 scripts/check_project.py
python3 -m unittest discover -s tests -v
```

Para o teste completo com API, inicie o servidor e execute:

```bash
python3 scripts/smoke_test.py http://127.0.0.1:8080
```

## GitHub Actions

O workflow `.github/workflows/ci.yml` verifica automaticamente:

- Python 3.11, 3.12 e 3.13;
- contratos dos três perfis públicos;
- PWA e estrutura documental;
- autenticação e dashboard do atleta;
- bloqueio de arquivos sensíveis;
- construção da imagem Docker.

## Compatibilidade

- Android, iPhone e iPad;
- tablets;
- notebooks e computadores;
- TVs e monitores grandes;
- toque, mouse, teclado e orientação livre;
- PWA e fluxos críticos offline;
- modo leve planejado para versões móveis antigas.

Entregas planejadas:

- APK/AAB para Android;
- TestFlight/App Store para iPhone e iPad;
- web/PWA para acesso universal.

A instalação do APK não é obrigatória para utilizar a plataforma.

## Arquitetura atual

```text
Navegador / PWA
       │
       ▼
server.py — HTTP, API, autenticação e autorização
       │
       ▼
apex_db.py — persistência, seeds e auditoria
       │
       ▼
SQLite local — demonstração
```

A arquitetura de produção migrará a persistência para PostgreSQL e serviços gerenciados, mantendo isolamento por federação e sem Supabase.

## Segurança

Nunca envie ao repositório:

- `.env`;
- `data/.jwt-secret`;
- bancos SQLite;
- documentos de usuários;
- chaves Android ou Apple;
- tokens e credenciais de produção.

Consulte [SECURITY.md](SECURITY.md) para reporte responsável.

## Documentação

- [Documento mestre](documentacao-mestre-apex-combate.md)
- [Índice documental](README-APEX-COMBATE.md)
- [Registro de decisões](registro-de-decisoes-apex-combate.md)
- [Compatibilidade](compatibilidade-apex-combate.md)
- [Apex’s Forge](apexs-forge.md)

## Licença

Software proprietário. Todos os direitos reservados a Mozer. Consulte [LICENSE](LICENSE).
