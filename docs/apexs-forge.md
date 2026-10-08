# Apex’s Forge — Aplicativo Comercial Conectado

**Proprietário:** Mozer  
**Status:** nome oficial aprovado; implementação futura  
**Nome oficial:** Apex’s Forge  
**Vínculo:** produto separado conectado ao Apex Combate por API comercial  
**Slogan de trabalho:** Forje sua marca. Eleve seu negócio.

---

## 1. Decisão

As lojas virtuais não serão administradas dentro dos dashboards esportivos do Apex Combate. Será criado um segundo aplicativo para lojistas acompanharem e controlarem produtos, estoque, pedidos, vendas e repasses.

A separação preserva a simplicidade do aplicativo esportivo e oferece uma operação comercial profissional para vendedores.

---

## 2. Significado do nome Apex’s Forge

### Apex’s

**Apex’s** significa “da Apex” ou “pertencente ao ecossistema Apex”. A palavra mantém a ligação imediata com o Apex Combate e mostra que o aplicativo comercial faz parte da mesma família, apesar de possuir operação, login e finalidade próprios.

### Forge

**Forge** significa **forja** em inglês. A forja é o lugar onde matérias-primas são transformadas, por trabalho, técnica, pressão e precisão, em algo forte, valioso e preparado para cumprir sua função.

No aplicativo, a forja é uma metáfora para o ambiente em que o lojista:

- constrói sua marca;
- transforma produtos em catálogo profissional;
- organiza estoque e operação;
- desenvolve vendas;
- fortalece o relacionamento com clientes;
- eleva seu negócio dentro do ecossistema marcial.

### Significado completo

**Apex’s Forge** significa **A Forja da Apex**: a central comercial em que lojas e marcas constroem, organizam e fortalecem seus negócios conectados ao Apex Combate.

### Por que o nome foi escolhido

- é marcante, forte e diferente de nomes genéricos de loja;
- mantém vínculo direto com a marca Apex;
- combina com disciplina, transformação e resistência das artes marciais;
- representa criação e crescimento, não apenas venda;
- permite que o produto evolua de painel de loja para ecossistema comercial completo;
- possui sonoridade premium e internacional;
- diferencia claramente o aplicativo do lojista do aplicativo esportivo;
- funciona para lojas, marcas, fabricantes, clubes e federações.

### Slogan de trabalho

> **Forje sua marca. Eleve seu negócio.**

“Forje sua marca” representa construção, identidade e fortalecimento. “Eleve seu negócio” conecta o crescimento comercial à ideia de Apex: chegar ao ponto mais alto.

---

## 3. Divisão de responsabilidades

### Apex Combate

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

### Aplicativo dos lojistas

Aplicativo separado usado por:

- lojas de artigos esportivos;
- marcas e fabricantes;
- clubes com produtos próprios;
- federações com produtos oficiais;
- vendedores autorizados.

Esse aplicativo terá autenticação e papéis comerciais próprios. Esses papéis não são novos perfis públicos do Apex Combate.

---

## 4. Painel da loja

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

## 5. Catálogo e produtos

### Cadastro

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

### Variações

- tamanho;
- cor;
- modelo;
- material;
- lado ou versão;
- SKU e código de barras por variação;
- preço e estoque por variação.

### Estados

- rascunho;
- em análise;
- aprovado;
- publicado;
- pausado;
- estoque baixo;
- esgotado;
- rejeitado;
- arquivado.

### Ações

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

## 6. Estoque

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

## 7. Pedidos

### Estados

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

### Recursos

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

## 8. Financeiro e marketplace

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

## 9. Entregas e retirada

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

## 10. Marketing

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

## 11. Papéis da equipe da loja

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

## 12. Onboarding da loja

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

## 13. Integração com o Apex Combate

### Serviços comerciais compartilhados

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

### Comunicação

- APIs versionadas;
- webhooks assinados;
- eventos assíncronos;
- idempotência;
- sincronização de estoque;
- notificações em tempo real;
- trilha de auditoria.

### Identificadores

O serviço comercial pode guardar referências mínimas, como `apex_user_id`, `club_id` ou `federation_id`, sem copiar o cadastro esportivo completo.

---

## 14. Isolamento de dados

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

## 15. Segurança e conformidade

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

## 16. Modelo de dados proposto

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

## 17. Modelo de receita

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

## 18. Fases recomendadas

### Fase 1 — fundação

- identidade final;
- onboarding;
- autenticação;
- cadastro de loja;
- catálogo;
- variações;
- estoque;
- painel básico.

### Fase 2 — pedidos

- carrinho no Apex Combate;
- checkout;
- pedidos;
- atualização de status;
- retirada e entrega.

### Fase 3 — pagamentos

- PIX e cartão;
- antifraude;
- split;
- comissão;
- repasses;
- estorno.

### Fase 4 — escala

- logística integrada;
- fiscal;
- promoções;
- anúncios;
- ERP;
- análises avançadas;
- internacionalização.

---

## 19. Decisões ainda pendentes

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
