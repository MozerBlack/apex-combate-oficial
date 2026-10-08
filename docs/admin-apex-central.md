# Central do Proprietário Apex Combate — planejamento

A Central do proprietário, pertencente ao Mozer, ficará acima das federações e será construída em uma etapa posterior.

## Significado do nome Apex Central

### Apex

**Apex** representa o ponto mais alto, o auge e a visão superior de todo o ecossistema. Na Central, identifica o nível máximo de governança da plataforma.

### Central

**Central** representa o núcleo de comando, inteligência, segurança e administração estratégica. É o lugar privado em que o proprietário acompanha e governa o ecossistema completo.

### Significado completo

**Apex Central** significa a central máxima de comando do ecossistema Apex: o ambiente proprietário de Mozer, posicionado acima das federações para governança global, segurança, suporte e evolução da plataforma.

### Por que o nome foi escolhido

- mantém a ligação direta com a marca Apex Combate;
- comunica autoridade, organização e visão global;
- deixa clara sua posição acima das federações;
- funciona como nome de uma central privada de comando;
- permite administrar futuramente países, federações, planos, segurança e operação geral;
- diferencia a governança proprietária da operação diária dos demais perfis;
- é simples, forte e fácil de compreender.

### Diferença para a Central da Federação

- **Apex Central:** pertence a Mozer e governa o ecossistema completo;
- **Central da Federação:** pertence à própria federação e opera somente sua rede, clubes, atletas e eventos;
- a Central da Federação não possui autoridade proprietária sobre o Apex Combate;
- as duas centrais não compartilham conta, token, rota ou permissões.

## Decisão vigente

- O botão público **FEDERAÇÃO** aceita o Presidente e a Central Administrativa da própria federação.
- `PRESIDENTE / MASTER2026 / 654321` representa o Presidente da Federação.
- `ADMIN / MASTER2026 / 654321` representa a Central da Federação Paranaense.
- A Central do proprietário não utiliza o login da Federação.
- Não existe um quarto botão na tela pública.
- A conta e as rotas da Central do proprietário estão desativadas nesta etapa.

## Arquitetura preservada para o futuro

O modelo de dados já permite uma Apex Central acima de múltiplas federações, com isolamento por `federation_id`. Quando a Central for construída, ela terá rota interna, autenticação e permissões próprias, sem se confundir com o Admin federativo.
