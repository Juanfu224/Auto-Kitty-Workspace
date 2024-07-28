import os
import time
from sys import stdout


"""LOGOTIPO DE LA APLICACIÓN"""
BANNER = """
 █████╗ ██╗   ██╗████████╗ ██████╗       ██╗  ██╗██╗████████╗████████╗██╗   ██╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗      ██║ ██╔╝██║╚══██╔══╝╚══██╔══╝╚██╗ ██╔╝
███████║██║   ██║   ██║   ██║   ██║█████╗█████╔╝ ██║   ██║      ██║    ╚████╔╝ 
██╔══██║██║   ██║   ██║   ██║   ██║╚════╝██╔═██╗ ██║   ██║      ██║     ╚██╔╝  
██║  ██║╚██████╔╝   ██║   ╚██████╔╝      ██║  ██╗██║   ██║      ██║      ██║   
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝       ╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝      ╚═╝    
██╗    ██╗ ██████╗ ██████╗ ██╗  ██╗███████╗██████╗  █████╗  ██████╗███████╗    
██║    ██║██╔═══██╗██╔══██╗██║ ██╔╝██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝    
██║ █╗ ██║██║   ██║██████╔╝█████╔╝ ███████╗██████╔╝███████║██║     █████╗      
██║███╗██║██║   ██║██╔══██╗██╔═██╗ ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝      
╚███╔███╔╝╚██████╔╝██║  ██║██║  ██╗███████║██║     ██║  ██║╚██████╗███████╗    
 ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝      
                                                             (by Juanfu224)
"""


"""COLORES"""
def red():  # Rojo
    RED = "\033[1;31m"
    stdout.write(RED)

def green():  # Verde
    GREEN = "\033[0;32m"
    stdout.write(GREEN)

def blue():  # Azul
    BLUE = "\033[1;34m"
    stdout.write(BLUE)

def yellow():  # Amarillo
    YELLOW = "\033[1;33m"
    stdout.write(YELLOW)

def orange():  # Naranja
    ORANGE = "\033[1;38;5;208m"
    stdout.write(ORANGE)

def white():  # Blanco
    WHITE = "\033[1;37m"
    stdout.write(WHITE)

def purple():  # Morado
    PURPLE = "\033[1;35m"
    stdout.write(PURPLE)

def cyan():  # Cian
    CYAN = "\033[1;36m"
    stdout.write(CYAN)

def light_gray():  # Gris claro
    LIGHT_GRAY = "\033[0;37m"
    stdout.write(LIGHT_GRAY)

def dark_gray():  # Gris oscuro
    DARK_GRAY = "\033[1;30m"
    stdout.write(DARK_GRAY)

def light_blue():  # Azul claro
    LIGHT_BLUE = "\033[1;94m"
    stdout.write(LIGHT_BLUE)


"""FUNCIONES PRINCIPALES"""
def p10k():
    # Aplicar config de p10k
    os.system("git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k")
    os.system("sudo git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /root/powerlevel10k")
    os.system("cp -r ~/Auto-Kitty-Workspace/tools/zsh/.p10k.zsh ~/")
    os.system("sudo cp -r ~/Auto-Kitty-Workspace/tools/zsh/.p10k.zsh /root")


def hnf():
    # Instalar Hack Nerd Fonts
    os.system("wget https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/Hack.zip")
    os.system("unzip -o Hack.zip")
    os.system("sudo cp -r Hack*.ttf /usr/share/fonts ")
    os.system("sudo rm -r Hack*")

def kitty():
    # Configurar Kitty
    os.system("sudo apt install kitty -y")
    os.system("rm -rf ~/.config/kitty/*")  # borra config anterior
    os.system("mkdir -p ~/.config/kitty")
    os.system("cp -r ~/Auto-Kitty-Workspace/tools/terminal/kitty.conf ~/.config/kitty")
    os.system("cp -r ~/Auto-Kitty-Workspace/tools/terminal/color.ini ~/.config/kitty")


def zsh():
    # Configurar zsh por defecto
    os.system("sudo apt install zsh -y")
    os.system("sudo usermod --shell /usr/bin/zsh $USER")
    os.system("sudo usermod --shell /usr/bin/zsh root")

    # Aplicar config de zshrc
    os.system("cp -r ~/Auto-Kitty-Workspace/tools/zsh/.zshrc ~/")
    os.system("sudo cp -r ~/Auto-Kitty-Workspace/tools/zsh/.zshrc /root")

    # Instalar plugins
    os.system("sudo wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/plugins/sudo/sudo.plugin.zsh")
    os.system("sudo apt install zsh-autosuggestions zsh-syntax-highlighting lsd -y")
    os.system("sudo dpkg -i ~/Auto-Kitty-Workspace/tools/zsh/bat*")
    os.system("sudo mkdir -p /usr/share/zsh-sudo")
    os.system("sudo cp -r sudo.plugin.zsh /usr/share/zsh-sudo")
    os.system("sudo rm -r ~/Auto-Kitty-Workspace/sudo.plugin*")


def fzf():
    # Instalar FZF en el usuario y root
    os.system("sudo apt install fzf -y")
    os.system("sudo git clone --depth=1 https://github.com/junegunn/fzf.git ~/.fzf")
    os.system("sudo git clone --depth=1 https://github.com/junegunn/fzf.git /root/.fzf")
    os.system("sudo ~/.fzf/install")
    os.system("sudo /root/.fzf/install")


def nvim():
    # Borrar antigua configuración de Nvim (mejor prevenir que curar)
    os.system("sudo rm -rf ~/.config/nvim")
    os.system("sudo rm -rf ~/.local/share/nvim")
    os.system("sudo rm -rf ~/.cache/nvim")
    os.system("sudo rm -rf /root/.config/nvim")
    os.system("sudo rm -rf /root/.local/share/nvim")
    os.system("sudo rm -rf /root/.config/nvim")

    # Instalar Nvim
    os.system("curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage")
    os.system("chmod u+x nvim.appimage")
    os.system("./nvim.appimage --appimage-extract")
    os.system("sudo mv squashfs-root /")
    os.system("sudo ln -s /squashfs-root/AppRun /usr/bin/nvim")

    # Configurar Nvim en usuario y root
    os.system("git clone https://github.com/NvChad/starter ~/.config/nvim")
    os.system("sudo git clone https://github.com/NvChad/starter /root/.config/nvim")


def cambiar_terminal():
    # Cambiar terminal
    os.system("sudo update-alternatives --config x-terminal-emulator")


def instalar():
    # Instalar Kitty
    print("\n[+] Instalando la Kitty....\n")
    time.sleep(3)
    kitty()

    # Instalar zsh
    print("\n[+] Instalando ZSH....\n")
    time.sleep(3)
    zsh()

    # Instalar Hack Nerd Fonts
    print("\n[+] Instalando las Hack Nerd Fonts....\n")
    time.sleep(3)
    hnf()

    # Aplicar config de p10k
    print("\n[+] Instalando Powerlevel10k....\n")
    time.sleep(3)
    p10k()

    # Instalar FZF
    print("\n[+] Instalando FZF....\n")
    time.sleep(3)
    fzf()

    # Instalar Nvim
    print("\n[+] Instalando Nvim....\n")
    time.sleep(3)
    nvim()

"""PROGRAMA PRINCIPAL"""
if __name__ == '__main__':
    # Imprimir banner del programa
    purple()
    print(BANNER)
    
    # Funcion principal
    white()
    instalar()
 
 # Cambiar terminal por defecto
    time.sleep(2)
    blue()
    while True:
        cambiar = input("\n¿Deseas cambiar la terminal por defecto? (s/n): ").lower()
        if cambiar not in ["s", "n"]:
            print("\nSolo puedes responder 's' o 'n'\n")
            continue
        if cambiar == "s":
            cambiar_terminal()
        break

    # Mensaje final
    green()
    print("\n[+] La instalación y la configuración de la terminal se ha realizado correctamente")
    print("\n[+] Para que funcione correctamente Powerlevel10k en su terminal, es necesario tener las Hack Nerd Fonts puestas en la configuración de la tipografía. Aún así, Kitty ya viene configurada con todo lo necesario.\n")
