# Auto-Linux-Workspace
Es compatible con Linux Mint o cualquier distribución basada en Ubuntu y Debian.

Testeado en Ubuntu, Linux Mint, Kali Linux y Parrot OS.

## El script consta de 10 funciones distintas:
- Instalar y configurar Kitty, P10k, FZF, Nvim, plugins etc...
- Instalar y configurar Bspwm, Polybar, Picom y Rofi
- Instalar NordVPN (implementado con Powerlevel10k).
- Instalar VirtualBox.
- Instalar LibreOffice.
- Instalar Sublime Text.
- ALL IN ONE.

# Instalación
```
git clone https://github.com/Juanfu224/Auto-Linux-Mint.git ~/Auto-Linux-Workspace
cd ~/Auto-Linux-Workspace
python3 main.py
```

# Vista general
![vista general](https://raw.githubusercontent.com/Juanfu224/Auto-Linux-Workspace/master/tools/Vista.png)

# Importante
- Para que funcione correctamente Powerlevel10k es necesario tener las Hack Nerd Fonts puestas en la configuración de la tipografía de la terminal, aún asi, la Kitty ya viene configurada con todo lo necesario.
- Hay que poner el tema Papirus en la configuración de temas del sistema.
- Es recomendable reiniciar el equipo después de hacer una instalación completa.

## Reinstalar Nvim:
En caso de tener una versión antigua de Neovim ya instalada, es muy recomendable desinstalarlo y borrar los archivos residuales que hayan quedado en el sistema con los siguientes comandos:
```
sudo apt purge neovim
sudo apt autoremove
```
A veces suelen ocurrir fallos a la hora de instalar Nvim, por lo que hay que volver a ejecutar la 2º opción del script. 

## Configurar IP en la Polybar:
En el caso de que de error al mostrarse la IP en la polybar o no sea correcta, hay que cambiar "wlp1s0" por el nombre de tu tarjeta de red en el siguiente archivo:
```
~/.config/bin/ethernet_status.sh 
```

# Utilidades:
- **Papirus**: Temas para los ficheros y aplicaciones.
- **Kitty**: Emulador de terminal para usuarios avanzados.
- **Powerlevel10k**: Tema de la zsh.
- **ZSH**: Shell.
- **FZF**: Buscador difuso de línea de comandos de propósito general.
- **Hack Nerd Font**: Fuente.
- **Bspwm**: Tiling Window Manager.
- **Rofi**: Selector de ventana y lanzador de aplicaciones.
- **Polybar**: Herramienta rápida y fácil de usar para crear barras de estado.
- **NordVPN**: Red privada virtual de Nord.

## Shortcuts (atajos de teclado)
<kbd>Windows</kbd> + <kbd>Enter</kbd> : Abrir la consola (gnome-terminal).  
<kbd>Windows</kbd> + <kbd>W</kbd> : Cerrar la ventana actual.  
<kbd>Windows</kbd> + <kbd>Alt</kbd> + <kbd>R</kbd> : Reiniciar la configuración del bspwm.  
<kbd>Windows</kbd> + <kbd>Alt</kbd> + <kbd>Q</kbd> : Cerrar sesión.  
<kbd>Windows</kbd> + <kbd>(⬆⬅⬇➡)</kbd> : Moverse por las ventanas en la workspace actual.  
<kbd>Windows</kbd> + <kbd>D</kbd> : Abrir el Rofi. <kbd>Esc</kbd> para salir.  
<kbd>Windows</kbd> + <kbd>(1,2,3,4,5,6,7,8,9,0)</kbd> : Cambiar el workspace.  
<kbd>Windows</kbd> + <kbd>T</kbd> : Cambiar la ventana actual a modo "terminal" (normal). Nos sirve cuando la ventana está en modo pantalla completa o flotante.  
<kbd>Windows</kbd> + <kbd>M</kbd> : Cambiar la ventana actual a modo "completo" (no ocupa la polybar). Presione la mismas teclas para volver a modo "terminal" (normal).  
<kbd>Windows</kbd> + <kbd>F</kbd> : Cambiar la ventana actual a modo pantalla completa (ocupa todo incluyendo la polybar).  
<kbd>Windows</kbd> + <kbd>S</kbd> : Cambiar la ventana actual a modo "flotante".  
<kbd>Windows</kbd> + <kbd>Alt</kbd> + <kbd>(1,2,3,4,5,6,7,8,9,0)</kbd> : Mover la ventana actual a otro workspace.  
<kbd>Windows</kbd> + <kbd>Alt</kbd> + <kbd>(⬆⬅⬇➡)</kbd> : Cambiar el tamaño de la ventana actual (solo funciona si está en modo terminal o flotante).  
<kbd>Windows</kbd> + <kbd>Ctrl</kbd> + <kbd>(⬆⬅⬇➡)</kbd> : Cambiar la posición de la ventana actual (solo funciona en modo flotante).  
<kbd>Windows</kbd> + <kbd>Shift</kbd> + <kbd>G</kbd> : Abrir Google Chrome (es necesario instalarlo primero).  
<kbd>Windows</kbd> + <kbd>Ctrl</kbd> + <kbd>Alt</kbd> + <kbd>(⬆⬅⬇➡)</kbd> : Mostrar una preselección para luego abrir una ventana (una terminal, Google Chrome, un archivo, etc.). <kbd>Windows</kbd> + <kbd>Ctrl</kbd> + <kbd>Space</kbd> para deshacer la preselección.

## Créditos
- Autor del script: Juanfu224 --> https://github.com/Juanfu224
- Autor de Papirus: Papirus Development Team --> https://github.com/PapirusDevelopmentTeam
- Autor de Powerlevel10k: romkatv --> https://github.com/romkatv
- Autor de bat: sharkdp --> https://github.com/sharkdp
- Autor de lsd: Peltoche --> https://github.com/Peltoche
- Inspirado en S4vitar y Yorkox0 ❤️
