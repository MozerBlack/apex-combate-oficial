# APK demonstrativo — Apex Combate

Este projeto gera o APK Android demonstrativo do Apex Combate sem dependências de bibliotecas externas. O aplicativo usa um `WebView` Android seguro para abrir a versão oficial publicada em:

`https://apex-combate-demo.onrender.com/apex-combate.html?v=44&source=apk`

## Identificação

- Pacote: `br.com.apexcombate.app`
- Nome: `Apex Combate`
- Versão Android: `44.0-demo`
- Version code: `44`
- Android mínimo: 6.0 / API 23
- Android alvo: API 33

## Recursos do invólucro Android

- tela de carregamento com a identidade oficial;
- navegação interna mantida no aplicativo;
- links externos encaminhados ao navegador do aparelho;
- seleção de arquivos compatível com formulários web;
- bloqueio de tráfego HTTP sem criptografia e de conteúdo misto;
- Safe Browsing quando suportado pelo Android WebView;
- tela de reconexão quando o carregamento principal falha;
- botão Voltar do Android integrado ao histórico da plataforma;
- rotação e diferentes tamanhos de tela preservados.

## Compilação

É necessário um Android SDK com:

- `platforms;android-33`;
- `build-tools;33.0.2`;
- Java 11 ou superior;
- `zip`, OpenSSL e utilitários POSIX (`awk`, `sha256sum`).

Com o SDK em `/tmp/android-sdk`:

```bash
./android-apk/build-apk.sh
```

Ou informe outro SDK:

```bash
ANDROID_SDK_ROOT=/caminho/do/android-sdk ./android-apk/build-apk.sh
```

O APK é gerado em `releases/Apex-Combate-Demo-v44.apk`.

## Assinatura

Na primeira compilação, o script cria uma chave RSA e um certificado de demonstração persistentes em `deploy-keys/`. Esses arquivos são ignorados pelo Git e devem ser preservados para que futuras atualizações possam manter a mesma assinatura. A chave demonstrativa não deve ser usada para publicação na Play Store.

## Observação

O APK é destinado à apresentação acadêmica e requer internet para acessar o backend oficial da demonstração no Render. Uma versão de produção deverá usar assinatura de lançamento protegida, política de atualização, revisão da Play Store e infraestrutura de produção.
