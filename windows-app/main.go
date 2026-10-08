//go:build windows

package main

import (
	_ "embed"
	"errors"
	"fmt"
	"io"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"syscall"
	"unsafe"
)

const (
	appName = "Apex Combate"
	appURL  = "https://apex-combate-demo.onrender.com/apex-combate.html?v=44&source=windows"
)

//go:embed apex.ico
var apexIcon []byte

func main() {
	if len(os.Args) > 1 && os.Args[1] == "--launch" {
		if err := launchApp(); err != nil {
			showError(err)
		}
		return
	}
	if err := install(); err != nil {
		showError(err)
		return
	}
	showMessage(
		"Instalação concluída",
		"O Apex Combate foi instalado na Área de Trabalho e no Menu Iniciar.\n\nO aplicativo será aberto agora pelo Microsoft Edge em modo de aplicativo, sem usar o Opera GX.",
		0x00000040,
	)
	if err := launchApp(); err != nil {
		showError(err)
	}
}

func install() error {
	localAppData := os.Getenv("LOCALAPPDATA")
	if localAppData == "" {
		return errors.New("o Windows não informou a pasta LOCALAPPDATA")
	}
	appDir := filepath.Join(localAppData, appName)
	if err := os.MkdirAll(appDir, 0o755); err != nil {
		return fmt.Errorf("não foi possível criar a pasta do aplicativo: %w", err)
	}

	currentExecutable, err := os.Executable()
	if err != nil {
		return fmt.Errorf("não foi possível localizar o instalador: %w", err)
	}
	installedExecutable := filepath.Join(appDir, "ApexCombate.exe")
	if !strings.EqualFold(filepath.Clean(currentExecutable), filepath.Clean(installedExecutable)) {
		if err := copyFile(currentExecutable, installedExecutable); err != nil {
			return fmt.Errorf("não foi possível instalar o executável: %w", err)
		}
	}

	iconPath := filepath.Join(appDir, "ApexCombate.ico")
	if err := os.WriteFile(iconPath, apexIcon, 0o644); err != nil {
		return fmt.Errorf("não foi possível instalar o ícone oficial: %w", err)
	}
	if err := createShortcuts(installedExecutable, iconPath); err != nil {
		return err
	}
	return nil
}

func copyFile(source, destination string) error {
	input, err := os.Open(source)
	if err != nil {
		return err
	}
	defer input.Close()

	temporary := destination + ".novo"
	output, err := os.Create(temporary)
	if err != nil {
		return err
	}
	if _, err = io.Copy(output, input); err != nil {
		output.Close()
		os.Remove(temporary)
		return err
	}
	if err = output.Close(); err != nil {
		os.Remove(temporary)
		return err
	}
	_ = os.Remove(destination)
	return os.Rename(temporary, destination)
}

func createShortcuts(executable, icon string) error {
	script := `param([string]$Target, [string]$Icon)
$ErrorActionPreference = 'Stop'
$Shell = New-Object -ComObject WScript.Shell
$Locations = @(
    [Environment]::GetFolderPath('Desktop'),
    (Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs')
)
foreach ($Location in $Locations) {
    if (-not (Test-Path $Location)) { New-Item -ItemType Directory -Path $Location -Force | Out-Null }
    $Shortcut = $Shell.CreateShortcut((Join-Path $Location 'Apex Combate.lnk'))
    $Shortcut.TargetPath = $Target
    $Shortcut.Arguments = '--launch'
    $Shortcut.WorkingDirectory = Split-Path $Target
    $Shortcut.IconLocation = $Icon + ',0'
    $Shortcut.Description = 'Apex Combate — Plataforma Universal de Artes Marciais'
    $Shortcut.Save()
}
`
	temporary, err := os.CreateTemp("", "apex-combate-instalar-*.ps1")
	if err != nil {
		return fmt.Errorf("não foi possível preparar os atalhos: %w", err)
	}
	scriptPath := temporary.Name()
	defer os.Remove(scriptPath)
	if _, err = temporary.WriteString(script); err != nil {
		temporary.Close()
		return fmt.Errorf("não foi possível escrever os atalhos: %w", err)
	}
	if err = temporary.Close(); err != nil {
		return fmt.Errorf("não foi possível concluir os atalhos: %w", err)
	}

	command := exec.Command(
		"powershell.exe",
		"-NoLogo",
		"-NoProfile",
		"-NonInteractive",
		"-ExecutionPolicy", "Bypass",
		"-File", scriptPath,
		executable,
		icon,
	)
	command.SysProcAttr = &syscall.SysProcAttr{HideWindow: true}
	if output, err := command.CombinedOutput(); err != nil {
		return fmt.Errorf("não foi possível criar os atalhos: %w (%s)", err, strings.TrimSpace(string(output)))
	}
	return nil
}

func launchApp() error {
	browser, err := findBrowser()
	if err != nil {
		return err
	}
	command := exec.Command(
		browser,
		"--app="+appURL,
		"--start-maximized",
		"--no-first-run",
	)
	if err := command.Start(); err != nil {
		return fmt.Errorf("não foi possível abrir o Apex Combate: %w", err)
	}
	return nil
}

func findBrowser() (string, error) {
	candidates := []string{
		joinIfSet(os.Getenv("PROGRAMFILES(X86)"), "Microsoft", "Edge", "Application", "msedge.exe"),
		joinIfSet(os.Getenv("PROGRAMFILES"), "Microsoft", "Edge", "Application", "msedge.exe"),
		joinIfSet(os.Getenv("LOCALAPPDATA"), "Microsoft", "Edge", "Application", "msedge.exe"),
		joinIfSet(os.Getenv("PROGRAMFILES"), "Google", "Chrome", "Application", "chrome.exe"),
		joinIfSet(os.Getenv("PROGRAMFILES(X86)"), "Google", "Chrome", "Application", "chrome.exe"),
		joinIfSet(os.Getenv("LOCALAPPDATA"), "Google", "Chrome", "Application", "chrome.exe"),
	}
	for _, candidate := range candidates {
		if candidate == "" {
			continue
		}
		if info, err := os.Stat(candidate); err == nil && !info.IsDir() {
			return candidate, nil
		}
	}
	return "", errors.New("Microsoft Edge ou Google Chrome não foi encontrado. Instale ou ative um desses navegadores para executar o aplicativo do Windows")
}

func joinIfSet(base string, elements ...string) string {
	if strings.TrimSpace(base) == "" {
		return ""
	}
	return filepath.Join(append([]string{base}, elements...)...)
}

func showError(err error) {
	showMessage(
		"Apex Combate — erro de instalação",
		"Não foi possível concluir a operação.\n\n"+err.Error(),
		0x00000010,
	)
}

func showMessage(title, message string, flags uintptr) {
	user32 := syscall.NewLazyDLL("user32.dll")
	messageBox := user32.NewProc("MessageBoxW")
	titlePointer, _ := syscall.UTF16PtrFromString(title)
	messagePointer, _ := syscall.UTF16PtrFromString(message)
	messageBox.Call(
		0,
		uintptr(unsafe.Pointer(messagePointer)),
		uintptr(unsafe.Pointer(titlePointer)),
		flags,
	)
}
