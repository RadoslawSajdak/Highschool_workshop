---
title: "Getting started"
date: 2023-02-12T22:17:39+01:00
draft: true
---

# Mikrokontrolery w praktyce

## Wstępne wymagania
- Komputer z systemem Windows / Linux (preferowane ubuntu)
- ESP8266 oraz peryferia (dostarcza prowadzący)
## Instalacja środowiska
### Arduino IDE
Pobierz i zainstaluj arduino IDE. Poradnik oraz instalator znajdziesz na [oficjalnej stronie producenta](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started/ide-v2-downloading-and-installing)

### PlatformIO (opcjonalne)
Alternatywnym, bardziej rozbudowanym środowiskiem jest PlatformIO. Pozwala ono na tworzenie bardziej
złożonych projektów na różne platformy. Podczas warsztatu, będziemy korzystać z ArduinoIDE, jednak
przykłady da się uruchomić również przez PlatformIO. Wymaga to jednak nieco dodatkowej konfiguracji.
Instrukcja instalacji znajduje się na [stronie projektu PlatformIO](https://platformio.org/install/ide?install=vscode)

### Dodanie płytki do środowiska
Domyślnie, ArduinoIDE wspiera mikrokontrolery z rodziny AVR. ESP8266 z którego korzystamy, wymaga więc 
doinstalowania "sterowników". W tym celu, otwórz **ustawienia** (skrót **CTRL + ,**) a następnie
w oknie "menadżer dodatkowych płytek" wklej:
```link
https://arduino.esp8266.com/stable/package_esp8266com_index.json
```
![image alt](/board_manager.png){.spoiler}

Następnie, zainstaluj płytkę wybierając z lewej strony **Menedżer płytek** i wyszukując **esp8266**.
