# Auto-Kitty-Workspace
Automatiza la instalación y la configuración de un entorno de trabajo en la famosa terminal Kitty, con el ZSH, Powerlevel10k, Nvchad, FZF, compativilidad con NordVPN y algunas funciones mas.

Es compatible con cualquier distribución basada en Ubuntu. Probado en Linux Mint 22 (Wilma) y Ubuntu 22.04 LTS.

# Vista general
![vista general](https://raw.githubusercontent.com/Juanfu224/Auto-Linux-Workspace/master/tools/Vista.png)

# Instalación
```
sudo apt install git
git clone https://github.com/Juanfu224/Auto-Kitty-Workspace.git ~/Auto-Kitty-Workspace
cd ~/Auto-Kitty-Workspace
python3 main.py
```

## Funciones del Script
El script consta de varias funciones distintas:
- **Instalar y configurar Kitty**: Emulador de terminal para usuarios avanzados.

- **Instalar y configurar Powerlevel10k en la ZSH**: Tema de la zsh que proporciona un prompt rápido y altamente personalizable.

- **Configurar Neovim con NvChad**: Configuración de Neovim para desarrolladores, proporcionando una experiencia de edición de texto moderna y modular.

- **Instalar FZF**: Buscador difuso de línea de comandos de propósito general, útil para buscar archivos, comandos y más.

- **Proporcionar plugins**: Incluye Zsh-autosuggestions, Zsh-syntax-highlighting, bat, lsd, entre otros.

# Importante
- Para que funcione correctamente Powerlevel10k en su terminal, es necesario tener las Hack Nerd Fonts puestas en la configuración de la tipografía. Aún asi, la Kitty ya viene configurada con todo lo necesario.

- Es recomendable reiniciar el equipo después de hacer una instalación completa.

## Reinstalar Nvim:
En caso de tener una versión antigua de Neovim ya instalada, es muy recomendable desinstalarlo y borrar los archivos residuales que hayan quedado en el sistema con los siguientes comandos:
```
sudo rm -rf ~/.config/nvim
sudo rm -rf ~/.local/share/nvim
sudo rm -rf ~/.cache/nvim
sudo rm -rf /root/.config/nvim
sudo rm -rf /root/.local/share/nvim
sudo rm -rf /root/.config/nvim
```
A veces suelen ocurrir fallos a la hora de instalar Nvim, por lo que hay que volver a ejecutar el script. Este script ya borra toda la configuración anterior de nvim de forma automática.

# Utilidades:
- **Kitty**: Emulador de terminal para usuarios avanzados.

- **Powerlevel10k**: Tema de la zsh que proporciona un prompt rápido y altamente personalizable.

- **zsh**: Shell poderoso y amigable con los desarrolladores, conocido por su robusta capacidad de configuración y plugins.

- **FZF**: Buscador difuso de línea de comandos de propósito general, útil para buscar archivos, comandos y más.

- **Hack Nerd Font**: Fuente principal utilizada, diseñada para mejorar la legibilidad y compatibilidad con iconos en terminales y editores de código.

- **NordVPN**: Red privada virtual de Nord, utilizada para mantener la privacidad y seguridad en línea.

- **NvChad**: Configuración de Neovim para desarrolladores, proporcionando una experiencia de edición de texto moderna y modular.

- **Zsh-autosuggestions**: Plugin de Zsh que sugiere comandos mientras escribes basándose en tu historial.

- **Zsh-syntax-highlighting**: Plugin de Zsh que resalta la sintaxis del comando actual.

- **bat**: Clon de `cat` con resaltado de sintaxis y paginación integrada, útil para visualizar archivos en la terminal.

- **lsd**: Mejorado y moderno `ls` que ofrece colores, iconos y una mejor experiencia visual al listar archivos y directorios en la terminal.

- **Neovim**: Editor de texto modernizado basado en Vim, enfocado en extensibilidad y usabilidad.

## Shortcuts (atajos de teclado) 
<kbd>Ctrl</kbd> + <kbd>←</kbd> : Cambiar a la ventana vecina a la izquierda.

<kbd>Ctrl</kbd> + <kbd>→</kbd> : Cambiar a la ventana vecina a la derecha.

<kbd>Ctrl</kbd> + <kbd>↑</kbd> : Cambiar a la ventana vecina arriba.

<kbd>Ctrl</kbd> + <kbd>↓</kbd> : Cambiar a la ventana vecina abajo.

<kbd>F1</kbd> : Copiar al buffer a.

<kbd>F2</kbd> : Pegar desde el buffer a.

<kbd>F3</kbd> : Copiar al buffer b.

<kbd>F4</kbd> : Pegar desde el buffer b.

<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Z</kbd> : Cambiar al diseño de ventanas en pila.

<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Enter</kbd> : Abrir una nueva ventana con el directorio actual.

<kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd> : Abrir una nueva pestaña con el directorio actual.

## Créditos
- Autor del script: Juanfu224 --> https://github.com/Juanfu224
- Autor de Powerlevel10k: romkatv --> https://github.com/romkatv
- Autor de bat: sharkdp --> https://github.com/sharkdp
- Autor de lsd: Peltoche --> https://github.com/Peltoche
- Autor de HNF: ryanoasis --> https://github.com/ryanoasis
- Autor de FZF: junegunn --> https://github.com/junegunn
- Autor de Nvim: Neovim --> https://github.com/neovim
- Autor de Kitty: kovidgoyal --> https://github.com/kovidgoyal
- Inspirado en S4vitar y Yorkox0 ❤️
