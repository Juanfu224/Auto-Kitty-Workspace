import os, time
from sys import stdout

def red():
    RED = "\033[1;31m"
    stdout.write(RED)

def green():
    GREEN = "\033[0;32m"
    stdout.write(GREEN)

def blue():
    BLUE = "\033[1;34m"
    stdout.write(BLUE)

def yellow():
    YELLOW = "\033[1;33m"
    stdout.write(YELLOW)

def purple():
    PURPLE = "\033[1;35m"
    stdout.write(PURPLE)

def white():
    WHITE = "\033[1;37m"
    stdout.write(WHITE)

banner = """
 █████╗ ██╗   ██╗████████╗ ██████╗     ██╗     ██╗███╗   ██╗██╗   ██╗██╗  ██╗
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗    ██║     ██║████╗  ██║██║   ██║╚██╗██╔╝
███████║██║   ██║   ██║   ██║   ██║    ██║     ██║██╔██╗ ██║██║   ██║ ╚███╔╝
██╔══██║██║   ██║   ██║   ██║   ██║    ██║     ██║██║╚██╗██║██║   ██║ ██╔██╗
██║  ██║╚██████╔╝   ██║   ╚██████╔╝    ███████╗██║██║ ╚████║╚██████╔╝██╔╝ ██╗
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝     ╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
                                                               (by juanfu224)
███╗   ███╗██╗███╗   ██╗████████╗
████╗ ████║██║████╗  ██║╚══██╔══╝
██╔████╔██║██║██╔██╗ ██║   ██║
██║╚██╔╝██║██║██║╚██╗██║   ██║
██║ ╚═╝ ██║██║██║ ╚████║   ██║
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝   ╚═╝
"""

def menu():
    red()
    print(banner)
    blue()
    time.sleep(0.5)
    print("1 -> Instalar Tema Papirus")
    time.sleep(0.5)
    print("\n2 -> Instalar Hack Nerd Fonts")
    time.sleep(0.5)
    print("\n3 -> Instalar y configurar Powerlevel10k, plugins, FZF, etc...")
    time.sleep(0.5)
    print("\n4 -> Instalar NordVPN")
    time.sleep(0.5)
    print("\n5 -> Instalar VMware")
    time.sleep(0.5)
    print("\n6 -> Instalar Inkscape")
    time.sleep(0.5)
    print("\n7 -> Instalar Gimp")
    time.sleep(0.5)
    print("\n8 -> All In One")
    time.sleep(0.5)
    print("\n9 -> Salir")
    time.sleep(0.5)

    option = input("\n-->> ")

    if option == "1":
        papirus()
    if option == "2":
        fonts()
    if option == "3":
        p10k()
    if option == "4":
        vpn()
    if option == "5":
        vmware()
    if option == "6":
        ink()
    if option == "7":
        gimp()
    if option == "8":
        papirus()
        fonts()
        p10k()
        vpn()
        vmware()
        ink()
        gimp()
    if option == "9":
        exit()

def papirus():
    green()
    print("[+] Instalando Papirus....\n")

    # Instalando Papirus
    os.system("sudo add-apt-repository ppa:papirus/papirus")
    os.system("sudo apt-get update")
    os.system("sudo apt-get install papirus-icon-theme papirus-folders")
    os.system("papirus-folders -l --theme Papirus-Dark")
    os.system("papirus-folders -C yaru --theme Papirus-Dark")

    time.sleep(2)
    print("\n[+] Papirus ha sido instalado correctamente")
    print("\nRecuerda habilitar los iconos Papirus en la configuración de los temas del sistema\n")

def fonts():
    green()
    print("\nInstalando Hack Nerd Fonts....\n")

    # Descargar  e instalar las Hack Nerd Fonts
    os.system("wget https://github.com/ryanoasis/nerd-fonts/releases/download/v2.1.0/Hack.zip")
    os.system("unzip Hack.zip")
    os.system("sudo cp Hack*.ttf /usr/local/share/fonts")
    os.system("rm -r Hack*")
    time.sleep(2)
    print("\n[+] Hack Nerd Fonts instalados correctamente")
    print("\nRecuerda cambiar la tipografia de la terminal antes de instalar Powerlevel10k\n")

def p10k():
    green()
    print("\nInstalando y configurando Powerlevel10k, plugins, FZF, etc....\n")

    # Instalamos Powerlevel10k, bat, lsd, git, scrub, FZF, plugins....
    os.system("sudo apt install zsh git zsh-autosuggestions zsh-syntax-highlighting scrub")
    os.system("sudo dpkg -i ~/Auto-Linux-Mint/tools/bat_0.21.0_amd64.deb")
    os.system("sudo dpkg -i ~/Auto-Linux-Mint/tools/lsd_0.22.0_amd64.deb")
    os.system("sudo wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/plugins/sudo/sudo.plugin.zsh")
    os.system("sudo git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k")
    os.system("sudo git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /root/powerlevel10k")
    os.system("sudo git clone --depth=1 https://github.com/junegunn/fzf.git ~/.fzf")
    os.system("sudo git clone --depth=1 https://github.com/junegunn/fzf.git /root/.fzf")
    os.system("sudo ~/.fzf/install")
    os.system("sudo /root/.fzf/install")
    os.system("sudo mkdir /usr/share/zsh-sudo")
    os.system("sudo cp -r sudo.plugin.zsh /usr/share/zsh-sudo")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/.zshrc ~/")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/.p10k.zsh ~/")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/.zshrc /root")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/.p10k.zsh ~/")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/.p10k.zsh /root")
    os.system("sudo rm -r ~/Auto-Linux-Mint/sudo.plugin*")
    os.system("sudo usermod --shell /usr/bin/zsh root")

    time.sleep(2)
    print("\n[+] La instalación y la configuración de Powerlevel10k se ha realizado correctamente")
    print("\nPara que se inicie automáticamente zsh hay que ejecutar el siguiente comando:")
    print("\nusermod --shell /usr/bin/zsh {NOMBRE DE TU USUARIO}\n")

def vpn():
    green()
    print("\nInstalando NordVPN....\n")

# Instalamos NordVPN....
    os.system("sudo dpkg -i ~/Auto-Linux-Mint/tools/nordvpn-release_1.0.0_all.deb")
    os.system("sudo apt update")
    os.system("sudo apt install nordvpn")

    time.sleep(2)
    green()
    print("\n[+] NordVPN se ha instalado correctamente\n")

def vmware():
    green()
    print("\nInstalando Vmware....\n")

# Instalamos VMware....
    os.system("sudo wget https://download3.vmware.com/software/WKST-1624-LX/VMware-Workstation-Full-16.2.4-20089737.x86_64.bundle")
    os.system("sudo chmod 777 VMware-Workstation-Full-16.2.4-20089737.x86_64.bundle")
    os.system("sudo ./VMware-Workstation-Full-16.2.4-20089737.x86_64.bundle")

    time.sleep(2)
    print("\n[+] VMware instalado correctamente\n")

def ink():
    green()
    print("\nInstalando Inkscape....\n")

# Instalamos Inkscape....
    os.system("mkdir ~/Programas")
    os.system("sudo wget https://inkscape.org/gallery/item/34672/Inkscape-9c6d41e-x86_64.AppImage")
    os.system("sudo mv Inkscape-9c6d41e-x86_64.AppImage ~/Programas")
    os.system("sudo chmod 770 ~/Programas/Inkscape-9c6d41e-x86_64.AppImage")

    time.sleep(2)
    print("\n[+] Inkscape instalado correctamente\n")

def gimp():
    green()
    print("\nInstalando Gimp....\n")

# Instalamos Gimp....
    os.system("sudo apt update")
    os.system("sudo apt install gimp")

    time.sleep(2)
    green()
    print("\n[+] Gimp instalado correctamente\n")


if __name__ == '__main__':
    menu()
