# Registro de Decisões — Apex Combate

**Responsável pelo produto:** Mozer  
**Atualizado em:** 1º de outubro de 2026

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
| DEC-038 | O desenvolvimento será versionado no GitHub com proteção de segredos, testes automatizados, GitHub Actions e construção Docker; o envio ao repositório remoto dependerá da autorização segura de Mozer. | Aprovada |

## Regras de mudança

- Somente uma instrução explícita de Mozer pode substituir uma decisão aprovada.
- Uma decisão substituída deve permanecer no histórico com indicação da nova decisão.
- Mudanças de autenticação, perfis, governança, técnico ou comércio devem atualizar a documentação mestre e os documentos específicos.
