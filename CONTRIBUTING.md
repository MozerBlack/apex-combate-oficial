# Contribuição — Apex Combate

O Apex Combate é um projeto proprietário. Contribuições exigem autorização de Mozer e acesso ao repositório privado.

## Fluxo

1. Abra ou selecione uma issue;
2. Crie uma branch a partir de `develop`;
3. Use `feature/descricao`, `fix/descricao` ou `docs/descricao`;
4. Faça mudanças pequenas e rastreáveis;
5. Execute `make check` e `make test`;
6. Abra um pull request para `develop`;
7. Aguarde revisão e aprovação;
8. Promova para `main` somente uma versão validada.

## Regras obrigatórias

- não criar um quarto perfil público;
- manter ATLETA, CLUBE e FEDERAÇÃO;
- técnico entra por CLUBE e atua somente na competição;
- não habilitar Apex Central sem decisão formal;
- não usar Supabase;
- não enviar segredos ou dados reais;
- manter compatibilidade responsiva, PWA e acessibilidade;
- atualizar o documento mestre e o registro de decisões quando necessário.

## Commits sugeridos

```text
feat: adiciona credenciamento por QR Code
fix: corrige isolamento entre federações
docs: registra decisão de publicação móvel
test: cobre login individual do técnico
```
