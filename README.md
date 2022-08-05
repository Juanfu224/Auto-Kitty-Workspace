# Auto-Linux-Mint
Automatiza la instalación y la configuración de la shell utilizada en el entorno de trabajo S4vitar, instala el tema Papirus y otras aplicaciones de escritorio en Linux Mint o cualquier distribución basada en Ubuntu 22.04.

## La utilidad consta de 9 funciones distintas:
- Instalar tema Papirus.
- Instalar Hack Nerd Fonts.
- Instalar y configurar Powerlevel10k, plugins, FZF, etc.
- Instalar NordVPN (implementado en Powerlevel10k).
- Instalar VMware y VirtualBox.
- Instalar Inkscape y Gimp.
- Instalar Discord y Telegram.
- Instalar Sublime Text.
- Instalacion ALL IN ONE.

# Instalación
**1)** Clonar el repositorio:
```
git clone https://github.com/Juanfu224/Auto-Linux-Mint.git ~/Auto-Linux-Mint
cd Auto-Linux-Mint
```

**2)** Ejecutamos el archivo 'main.py':
```
python3 main.py
```
**3)** Disfruta :)

# IMPORTANTE
- Para que funcione correctamente Powerlevel10k es necesario tener las Hack Nerd Fonts puestas en la configuración de la tipografía de la terminal.
- Hay que poner el tema Papirus el la configuración de temas del sistema.
- Es recomendable reiniciar el equipo después de hacer una instalaci 

## Inicio automático de zsh:
```
sudo usermod --shell /usr/bin/zsh [USUARIO]
sudo usermod --shell /usr/bin/zsh root
```
