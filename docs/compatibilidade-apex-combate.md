# Compatibilidade Universal — Apex Combate

## Objetivo

A compatibilidade universal é um requisito obrigatório do Apex Combate. A plataforma deverá oferecer a mesma conta e os mesmos dados em qualquer tela, adaptando navegação, densidade e tamanho dos elementos ao dispositivo.

O produto deve atender:

- celulares Android e iPhone;
- tablets Android e iPad;
- notebooks;
- computadores Windows, macOS e Linux;
- monitores Full HD, QHD e 4K;
- TVs e telas de competição;
- orientação retrato e paisagem;
- toque, mouse, teclado e controle remoto compatível;
- instalação como PWA quando o sistema permitir;
- conexões instáveis, com recursos offline nos fluxos críticos.

Nenhuma funcionalidade principal poderá depender exclusivamente de um tamanho de tela, sistema operacional ou método de entrada.

## Política para versões de dispositivos móveis

O projeto deve buscar a maior cobertura possível sem comprometer a segurança dos dados. O suporte será dividido em três níveis:

| Nível | Dispositivos | Experiência |
|---|---|---|
| Completo | Android e iOS/iPadOS com navegadores modernos e atualizados | Todos os módulos, PWA, offline, notificações e recursos avançados |
| Estendido | Versões antigas ainda capazes de executar HTML5, HTTPS e JavaScript compatível | Fluxos principais, com menos animações, efeitos, gráficos e processamento local |
| Legado | Sistemas muito antigos, navegadores integrados e aparelhos com pouca memória | Modo leve quando tecnicamente seguro; páginas públicas e orientação para atualização quando autenticação segura não for possível |

### Modo leve para aparelhos antigos

- layout em uma coluna;
- ausência de animações e efeitos pesados;
- imagens compactadas;
- tabelas e gráficos simplificados;
- menor quantidade de dados por carregamento;
- carregamento sob demanda;
- formulários divididos em etapas curtas;
- preservação das funções essenciais de login, inscrição e consulta sempre que o navegador suportar HTTPS e criptografia adequados;
- mensagem clara quando um recurso não for tecnicamente compatível.

### Estratégia técnica

- compilação de JavaScript para alvos móveis antigos;
- prefixos e alternativas de CSS;
- pacote legado separado do pacote moderno;
- polyfills locais somente quando necessários;
- detecção de recursos, e não apenas do modelo do aparelho;
- ausência de dependência obrigatória de WebGL ou hardware potente;
- testes em aparelhos reais, emuladores e serviços de compatibilidade;
- proibição de reduzir requisitos de segurança apenas para manter um navegador obsoleto.

O aplicativo não bloqueará um aparelho apenas por ser antigo. Primeiro tentará carregar a experiência normal e, quando necessário, oferecerá o modo leve. Sistemas que não suportem HTTPS, criptografia segura ou recursos mínimos de autenticação poderão acessar somente conteúdo público compatível.

## Faixas de layout

| Contexto | Larguras de referência | Comportamento |
|---|---:|---|
| Celular compacto | 320–359 px | Conteúdo em uma coluna, textos compactos e navegação inferior |
| Celular | 360–700 px | Navegação inferior, cartões empilhados e modais em tela reduzida |
| Tablet retrato | 701–820 px | Área integral, navegação inferior e cartões mais largos |
| Tablet paisagem / notebook compacto | 821–1180 px | Barra lateral e conteúdo principal; painel auxiliar oculto |
| Notebook / desktop | 1181–1439 px | Layout completo com três áreas quando houver espaço |
| Desktop Full HD | 1440–1999 px | Mais respiro, hero ampliado e maior densidade de informações |
| Monitor 2K/4K e TV | 2000–2560+ px | Tipografia, controles e painéis ampliados para leitura à distância |

## Recursos já adicionados ao protótipo

- apresentação pública anterior ao login, responsiva de celulares compactos a TVs e sem avanço automático;
- layout responsivo de 320 px a telas 4K;
- suporte a retrato e paisagem;
- áreas seguras para notch e barra de gestos;
- botões maiores em telas sensíveis ao toque;
- navegação completa por teclado ou controle remoto que emule teclado;
- foco visual de alto contraste;
- respeito à preferência de redução de movimento;
- adaptação para modos de contraste forçado;
- imagens incorporadas sem dependência de CDN;
- manifesto PWA para instalação;
- service worker para funcionamento offline após o primeiro acesso por HTTPS;
- área do técnico com cache local do último painel sincronizado, checklists e ações enfileiradas para envio automático após a reconexão;
- ícones de 192 px e 512 px;
- orientação livre, sem bloqueio de rotação.

## Matriz mínima de testes

Antes de cada lançamento, testar pelo menos:

1. 320 × 568 — celular compacto;
2. 360 × 800 — Android comum;
3. 390 × 844 — iPhone moderno;
4. 844 × 390 — celular em paisagem;
5. 768 × 1024 — tablet em retrato;
6. 1024 × 768 — tablet em paisagem;
7. 1366 × 768 — notebook;
8. 1440 × 900 — notebook de alta resolução;
9. 1920 × 1080 — desktop e TV Full HD;
10. 2560 × 1440 — monitor QHD;
11. 3840 × 2160 — TV ou monitor 4K.

## Navegadores-alvo

- Chrome e Edge modernos;
- Safari no iPhone, iPad e macOS;
- Firefox moderno;
- Samsung Internet;
- navegadores Android baseados em Chromium;
- navegadores de Smart TV com suporte adequado a HTML5, CSS Grid e JavaScript moderno.

## Observação sobre “todas as versões”

Não é tecnicamente seguro prometer compatibilidade com todo aparelho ou navegador já produzido. Smart TVs antigas e navegadores desatualizados podem não suportar recursos modernos. A estratégia correta é:

1. manter uma versão web responsiva como base universal;
2. testar nos aparelhos e navegadores definidos na matriz;
3. oferecer uma interface simplificada quando recursos avançados não existirem;
4. empacotar versões específicas para Android, iOS ou plataformas de TV somente se distribuição em lojas for necessária;
5. acompanhar métricas reais de dispositivos para ajustar o suporte.

## Entregáveis móveis finais: Android e iOS

O Apex Combate terá aplicativos instaláveis para **Android e iPhone/iPad**, usando a mesma base responsiva. A versão web/PWA continuará disponível para notebooks, computadores, tablets, TVs e como alternativa em dispositivos móveis limitados.

A existência do APK Android é um entregável obrigatório do projeto, mas sua instalação não será obrigatória para utilizar a plataforma. O usuário poderá escolher entre abrir o Apex Combate no navegador, instalá-lo como PWA ou utilizar o aplicativo correspondente ao seu sistema.

### Formatos Android

- **APK de demonstração:** instalação direta no aparelho para apresentação e testes;
- **APK de produção assinado:** distribuição controlada fora da loja, quando necessária;
- **AAB de produção:** publicação na Google Play Store;
- **PWA:** alternativa universal e fallback para aparelhos não compatíveis com o pacote Android.

### APK demonstrativo disponível

- artefato: `releases/Apex-Combate-Demo-v44.apk`;
- projeto-fonte: `android-apk/`;
- identificador: `br.com.apexcombate.app`;
- versão: `44.0-demo` (`versionCode` 44);
- compatibilidade mínima: Android 6.0 / API 23;
- funcionamento: contêiner Android nativo com `WebView` seguro apontando para a demonstração oficial por HTTPS;
- proteções: tráfego HTTP e conteúdo misto bloqueados, depuração do `WebView` desativada, Safe Browsing quando suportado e assinatura RSA exclusiva de demonstração;
- limitações: exige internet, depende do Android System WebView e ainda não é o pacote de produção da Google Play;
- assinatura: chave local preservada fora do Git para permitir futuras atualizações com a mesma identidade.

### Formatos iPhone e iPad

- **build de desenvolvimento:** testes em simuladores e aparelhos autorizados;
- **TestFlight:** distribuição segura da versão de demonstração para professores, avaliadores e testadores;
- **IPA assinado:** artefato técnico gerado no processo de compilação e assinatura;
- **App Store:** distribuição pública oficial após análise da Apple;
- **PWA:** alternativa imediata para aparelhos que não possam instalar a versão nativa.

### Arquitetura compartilhada

- a interface responsiva será empacotada em contêineres Android e iOS, preferencialmente com Capacitor;
- os aplicativos conterão os recursos visuais necessários para abrir a interface e o modo demonstrativo;
- autenticação, dados sincronizados e operações oficiais utilizarão a API Apex por HTTPS;
- o servidor e o banco de produção não serão embutidos nos aplicativos;
- dados essenciais poderão ser armazenados de forma segura para operação offline e sincronizados depois;
- câmera, QR Code, notificações, compartilhamento, biometria e arquivos poderão utilizar integrações nativas;
- nenhuma chave de assinatura, segredo JWT ou credencial de produção será incluída no repositório ou exposta nos pacotes.

### Identidade prevista

- nome público: **Apex Combate**;
- identificador Android oficial: `br.com.apexcombate.app`;
- Bundle ID iOS sugerido: `br.com.apexcombate.app`;
- ícone: logotipo oficial;
- orientação: livre;
- aparência: Dark Mode oficial;
- atualização: controle de versão, assinatura e trilha de releases no GitHub.

### Requisitos específicos da Apple

- projeto iOS compatível com Xcode;
- conta Apple Developer pertencente a Mozer ou à empresa responsável;
- certificados e perfis de provisionamento;
- configuração no App Store Connect;
- política de privacidade e informações de tratamento de dados;
- testes em iPhone e iPad reais;
- aprovação da Apple antes da publicação pública;
- automação em ambiente macOS, inclusive por GitHub Actions quando configurado.

### Limites técnicos

APK/AAB são formatos exclusivos do Android. No ecossistema Apple, a distribuição ocorre por TestFlight e App Store. Versões muito antigas do iOS que não aceitem o runtime, HTTPS ou os requisitos de segurança atuais continuarão com acesso à PWA ou ao modo leve, quando tecnicamente seguro.

A geração dos aplicativos exigirá projetos Android e iOS, assinaturas digitais independentes, matrizes de testes, políticas de atualização e empacotamento automatizado.
