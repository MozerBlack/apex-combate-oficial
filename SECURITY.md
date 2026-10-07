# Segurança — Apex Combate

## Reporte responsável

Falhas de segurança não devem ser abertas em issues públicas. Informe o proprietário do projeto por um canal privado autorizado, incluindo descrição, impacto, passos de reprodução e evidências sem dados pessoais reais.

## Dados que nunca entram no Git

- segredos JWT;
- arquivos `.env`;
- bancos SQLite locais;
- documentos e dados pessoais;
- certificados Android e Apple;
- tokens de serviços;
- credenciais de pagamento;
- backups de produção.

## Escopo atual

A v43 é uma demonstração funcional. Credenciais, OTP, SQLite e seeds são exclusivamente demonstrativos. Produção exige HTTPS, PostgreSQL, OTP externo, rotação de segredos, monitoramento, backups, gestão de incidentes e revisão LGPD.

## Princípios

- menor privilégio;
- isolamento por federação;
- credenciais individuais;
- auditoria de operações;
- técnico limitado à competição e a atletas designados;
- Apex Central desabilitada até implementação própria;
- segurança não reduzida para navegadores obsoletos.
