# Aplicativo do Apex Combate para Windows

Este projeto gera o instalador `Instalar-Apex-Combate-Windows.exe` para Windows 10/11 de 64 bits.

## Funcionamento

O instalador:

- copia o iniciador para `%LOCALAPPDATA%\Apex Combate`;
- instala o ícone oficial;
- cria atalhos na Área de Trabalho e no Menu Iniciar;
- abre o Apex Combate pelo Microsoft Edge em modo de aplicativo, sem barra de endereços e sem utilizar o Opera GX;
- usa o Google Chrome como alternativa somente se o Microsoft Edge não for encontrado;
- não exige privilégios de administrador;
- mantém a demonstração sincronizada com o ambiente oficial por HTTPS.

O programa requer conexão com a internet e Microsoft Edge ou Google Chrome instalado. O executável acadêmico ainda não possui assinatura comercial de código; por isso, o Windows SmartScreen poderá exibir um aviso de editor desconhecido na primeira execução.

## Compilação

Requisitos:

- Go 1.27 ou superior;
- acesso à internet para obter `github.com/akavel/rsrc@v0.10.2`;
- `sha256sum`.

Execute na raiz do repositório:

```bash
./windows-app/build-windows.sh
```

O resultado será salvo em `releases/Instalar-Apex-Combate-Windows.exe` com seu arquivo SHA-256 correspondente.
