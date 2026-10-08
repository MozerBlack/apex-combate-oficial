# 🥋 Apex Combate — Plataforma Universal de Artes Marciais

## Índice da Documentação

**Proprietário:** Mozer  
**Versão atual:** v45

A documentação complementar fica concentrada nesta pasta para manter a raiz do repositório objetiva. Para visão geral, execução e publicação, consulte o [`README.md` principal](../README.md).

## Comece aqui

1. [`documentacao-mestre-apex-combate.md`](documentacao-mestre-apex-combate.md) — documento único oficial, reunindo toda a documentação do ecossistema;
2. [`registro-de-decisoes-apex-combate.md`](registro-de-decisoes-apex-combate.md) — decisões aprovadas e restrições;
3. [`plano-produto-apex-combate.md`](plano-produto-apex-combate.md) — visão, mercado, fases e evolução.

## Produto principal

- [`identidade-visual-apex-combate.md`](identidade-visual-apex-combate.md) — marca, logo, paleta e direção visual;
- [`perfis-e-permissoes-apex-combate.md`](perfis-e-permissoes-apex-combate.md) — três perfis e papéis internos;
- [`sistema-login-apex-combate.md`](sistema-login-apex-combate.md) — autenticação por perfil;
- [`compatibilidade-apex-combate.md`](compatibilidade-apex-combate.md) — dispositivos, responsividade e PWA;
- [`backend-apex-combate.md`](backend-apex-combate.md) — backend, dados e endpoints;
- [`admin-apex-central.md`](admin-apex-central.md) — Central proprietária futura de Mozer.

## Produto comercial conectado

- [`apexs-forge.md`](apexs-forge.md) — Apex’s Forge, aplicativo separado para lojas, produtos, estoque, pedidos e vendas.

## Implementação

- [`apex-combate.html`](../apex-combate.html) — aplicação web principal;
- [`server.py`](../server.py) — API local;
- [`apex_db.py`](../apex_db.py) — persistência e migrações;
- [`manifest.webmanifest`](../manifest.webmanifest) — instalação PWA;
- [`apex-sw.js`](../apex-sw.js) — cache e modo offline;
- [`assets/apex-combate-logo-oficial.png`](../assets/apex-combate-logo-oficial.png) — logo oficial.

## Regra de precedência

Em caso de divergência, a ordem é:

1. instrução mais recente e explícita de Mozer;
2. documentação mestre;
3. registro de decisões;
4. documento específico do módulo;
5. plano de produto histórico.
