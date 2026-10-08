# Perfis e Permissões — Apex Combate

## Perfis com acesso

A Apex Combate terá **3 grupos de acesso visíveis**:

1. **Atletas e alunos**;
2. **Clubes, dojôs e academias, professores e técnicos**;
3. **Federações**.

Dentro do segundo grupo, cada pessoa receberá permissões conforme sua função. Um professor poderá gerenciar suas turmas sem necessariamente acessar o financeiro da academia, por exemplo.

---

## 1. Atletas e alunos

### Podem

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

### Não podem

- alterar a própria graduação oficial;
- consultar informações privadas de outros atletas;
- administrar turmas ou dados financeiros;
- homologar eventos, graduações ou certificados.

---

## 2. Clubes, dojôs e academias, professores e técnicos

Este é um único grupo visível no login, com contas internas diferentes. O perfil público continua sendo **CLUBE**.

### Gestores de clubes, dojôs e academias podem

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

### Técnico de competição

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

### Restrições

- o servidor valida o vínculo entre técnico, competição e inscrição em toda operação;
- dados de saúde são excepcionais, mínimos e sujeitos à LGPD;
- a organização só acessa dados de pessoas vinculadas a ela;
- certificados oficiais dependem das regras da federação responsável;
- ações sensíveis ficam registradas em auditoria.

---

## 3. Federações

### Podem

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

### Restrições

- cada federação visualiza somente sua rede e suas competências;
- dados pessoais e sensíveis devem seguir a LGPD;
- alterações oficiais exigem histórico, responsável, data e justificativa;
- o acesso a informações de saúde deve ser excepcional e estritamente controlado.

---

## Matriz resumida

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

## Hierarquia interna do segundo grupo

Embora exista apenas um grupo visível no login, o sistema utilizará funções internas:

- proprietário ou gestor da organização;
- coordenador técnico;
- professor;
- técnico de competição;
- auxiliar;
- atendente ou financeiro.

O gestor credencia o técnico para competições e atletas específicos. A conta `CLUB_TECHNICIAN` permanece tecnicamente bloqueada fora da operação do evento, independentemente das permissões administrativas do clube.

---

## Regras de segurança

- controle de acesso baseado em papéis e permissões;
- autenticação multifator para organizações e federações;
- verificação documental de profissionais, organizações e federações;
- isolamento dos dados de cada organização;
- auditoria de graduação, filiação, pagamentos e certificados;
- gerenciamento de sessões e dispositivos;
- revisão periódica das permissões da equipe;
- consentimento e conta vinculada ao responsável legal para menores de idade;
- princípio do menor privilégio: cada usuário recebe apenas o acesso necessário.

## Administração interna

A operação técnica da Apex Combate precisará de acesso interno para suporte, segurança e moderação. Esse acesso não será apresentado como um grupo comum no aplicativo e deverá ser restrito, auditado e protegido por autenticação reforçada.
