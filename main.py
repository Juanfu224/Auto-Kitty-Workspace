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
    print("\n3 -> Instalar y configurar Powerlevel10k, plugins, Nvim, FZF, etc...")
    time.sleep(0.5)
    print("\n4 -> Instalar y configurar Bspwm, Polybar, Picom y Rofi")
    time.sleep(0.5)
    print("\n5 -> Instalar NordVPN")
    time.sleep(0.5)
    print("\n6 -> Instalar VMware y VirtualBox")
    time.sleep(0.5)
    print("\n7 -> Instalar Inkscape y Gimp")
    time.sleep(0.5)
    print("\n8 -> Instalar Discord y Telegram")
    time.sleep(0.5)
    print("\n9 -> Instalar Sublime Text")
    time.sleep(0.5)
    print("\n10 -> ALL IN ONE")
    time.sleep(0.5)
    print("\n11 -> Salir")
    time.sleep(0.5)

    option = input("\n-->> ")

    if option == "1":
        papirus()
    if option == "2":
        fonts()
    if option == "3":
        p10k()
    if option == "4":
        bspwm()
    if option == "5":
        vpn()
    if option == "6":
        vbox()
    if option == "7":
        ink()
    if option == "8":
        discord()
    if option == "9":
        sublime()
    if option == "10":
        papirus()
        fonts()
        p10k()
        bspwm()
        vpn()
        vbox()
        ink()
        discord()
        sublime()
    if option == "11":
        exit()

def papirus():
    green()
    print("\n[+] Instalando Papirus....\n")

    # Instalando Papirus
    os.system("sudo add-apt-repository ppa:papirus/papirus")
    os.system("sudo apt-get update")
    os.system("sudo apt-get install papirus-icon-theme papirus-folders")
    os.system("papirus-folders -l --theme Papirus-Dark")
    os.system("papirus-folders -C yaru --theme Papirus-Dark")
    os.system("sudo add-apt-repository --remove ppa:papirus/papirus")

    time.sleep(2)
    green()
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
    green()
    print("\n[+] Hack Nerd Fonts instalados correctamente")

def p10k():
    green()
    print("\nInstalando y configurando Powerlevel10k, plugins, FZF, Nvim, etc....\n")

    # Instalamos Powerlevel10k, bat, lsd, git, scrub, FZF, plugins....
    os.system("sudo apt install zsh git zsh-autosuggestions zsh-syntax-highlighting scrub neovim")
    os.system("sudo dpkg -i ~/Auto-Linux-Mint/tools/zsh/bat_0.21.0_amd64.deb")
    os.system("sudo dpkg -i ~/Auto-Linux-Mint/tools/zsh/lsd_0.22.0_amd64.deb")
    os.system("sudo wget https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/plugins/sudo/sudo.plugin.zsh")
    os.system("sudo git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k")
    os.system("sudo git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /root/powerlevel10k")
    os.system("sudo git clone --depth=1 https://github.com/junegunn/fzf.git ~/.fzf")
    os.system("sudo git clone --depth=1 https://github.com/junegunn/fzf.git /root/.fzf")
    os.system("sudo ~/.fzf/install")
    os.system("sudo /root/.fzf/install")
    os.system("sudo mkdir /usr/share/zsh-sudo")
    os.system("sudo cp -r sudo.plugin.zsh /usr/share/zsh-sudo")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/zsh/.zshrc ~/")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/zsh/.p10k.zsh ~/")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/zsh/.zshrc /root")
    os.system("sudo cp -r ~/Auto-Linux-Mint/tools/zsh/.p10k.zsh /root")
    os.system("sudo rm -r ~/Auto-Linux-Mint/sudo.plugin*")
    os.system("sudo mkdir -p ~/.config/nvim")
    os.system("sudo mkdir -p /root/.config/nvim")
    os.system("sudo cp ~/Auto-Linux-Mint/tools/nvim/* ~/.config/nvim")
    os.system("sudo cp ~/Auto-Linux-Mint/tools/nvim/* /root/.config/nvim")

    time.sleep(2)
    green()
    print("\n[+] La instalación y la configuración de Powerlevel10k se ha realizado correctamente")
    print("\nRecuerda cambiar la tipografia de la terminal a Hack Nerd Font para que funcione Powerlevel10k\n")

def bspwm():
    green()
    print("[+] Instalando requerimientos necesarios...\n")

    # Instalando Requerimientos
    os.system("sudo apt-get update -y")
    os.system("sudo apt install net-tools libuv1-dev build-essential git vim xcb libxcb-util0-dev libxcb-ewmh-dev libxcb-randr0-dev libxcb-icccm4-dev libxcb-keysyms1-dev libxcb-xinerama0-dev libasound2-dev libxcb-xtest0-dev libxcb-shape0-dev -y")
    os.system("sudo apt install cmake cmake-data pkg-config python3-sphinx libcairo2-dev libxcb1-dev libxcb-util0-dev libxcb-randr0-dev libxcb-composite0-dev python3-xcbgen xcb-proto libxcb-image0-dev libxcb-ewmh-dev libxcb-icccm4-dev libxcb-xkb-dev libxcb-xrm-dev libxcb-cursor-dev libasound2-dev libpulse-dev libjsoncpp-dev libmpdclient-dev libcurl4-openssl-dev libnl-genl-3-dev -y")
    os.system("sudo apt install meson libxext-dev libxcb1-dev libxcb-damage0-dev libxcb-xfixes0-dev libxcb-shape0-dev libxcb-render-util0-dev libxcb-render0-dev libxcb-randr0-dev libxcb-composite0-dev libxcb-image0-dev libxcb-present-dev libxcb-xinerama0-dev libpixman-1-dev libdbus-1-dev libconfig-dev libgl1-mesa-dev libpcre2-dev libevdev-dev uthash-dev libev-dev libx11-xcb-dev libxcb-glx0-dev -y")
    os.system("sudo apt install bspwm rofi caja feh gnome-terminal scrot neovim xclip tmux acpi scrub bat wmname -y")
    os.system("sudo apt-get -f -y install")
    os.system("sudo apt autoclean")
   
    time.sleep(2)
    green()
    print("\n[+] Requetimientos instalados correctamente\n")

    # Clona la repo de bspwm
    os.system("git clone https://github.com/baskerville/bspwm.git")
    os.system("mv bspwm/* .")
    os.system("sudo rm -r bspwm/")
    os.system("make")

    # Acava del build
    os.system("sudo make install")

    # Elimina los archivos de bspwm
    os.system("sudo rm -r artworks/ contrib/ doc/ src/ tests/ bspc bspc.o bspwm bspwm.o desktop.o events.o ewmh.o geometry.o helpers.o history.o jsmn.o LICENSE Makefile messages.o monitor.o parse.o pointer.o query.o README.md restore.o rule.o settings.o Sourcedeps stack.o subscribe.o tree.o VERSION window.o")

    # Clona la repo de sxhkd
    os.system("git clone https://github.com/baskerville/sxhkd.git")
    os.system("mv sxhkd/* .")
    os.system("sudo rm -r sxhkd/")
    os.system("cd ../sxhkd")
    os.system("make")

    # Acaba el build
    os.system("sudo make install")

    # Crea las carpetas de bspwm y sxhkd en ~/.config
    os.system("mkdir ~/.config/bspwm")
    os.system("mkdir ~/.config/sxhkd")
    os.system("cp examples/bspwmrc ~/.config/bspwm/")

    # Les da permisos de ejecucion a bspwmrc
    os.system("chmod +x ~/.config/bspwm/bspwmrc")
    os.system("cp examples/sxhkdrc ~/.config/sxhkd/")

    # Elimina los archivos de sxhkd
    os.system("sudo rm -r contrib/ doc/ examples/ src/ grab.o helpers.o LICENSE Makefile parse.o README.md Sourcedeps sxhkd sxhkd.o types.o VERSION")
    os.system("cp ~/Auto-Linux-Mint/tools/bspwm/sxhkdrc ~/.config/sxhkd")
    
    time.sleep(2)
    green()
    print("\n[+] Bspwm instalado correctamente!")

    # Clona el repo de polybar
    os.system("git clone --recursive https://github.com/polybar/polybar")
    os.system("mv polybar/* .")
    os.system("sudo rm -r polybar/")
    os.system("cmake .")
    os.system("make -j$(nproc)")

    # Acaba el build
    os.system("sudo make install")

    # Elimina los archivos de polybar
    os.system("sudo rm -r bin/ cmake/ CMakeFiles/ common/ config/ contrib/ doc/ generated-sources/ include/ lib/ libs/ polybar/ src/ tests/ banner.png build.sh CHANGELOG.md CMajeCache.txt cmake_install.cmake CMakeLists.txt compile_commands.json CONTRIBUTING.md install_manifest LICENSE Makefile README.md SUPPORT.md version.txt")

    # Clona el repo de picom
    os.system("git clone https://github.com/ibhagwan/picom.git")
    os.system("mv picom/* .")
    os.system("sudo rm -r picom/")
    os.system("git submodule update --init --recursive")
    os.system("meson --buildtype=release . build")
    os.system("ninja -C build")

    # Hace el build de picom
    os.system("sudo ninja -C build install")

    # Elimina los archivos de picom
    os.system("sudo rm -r *.md *.conf *.desktop *.txt *.build *.spdx *.glsl COPYING Doxyfile CONTRIBUTORS bin/ build/ dbus-examples/ LICENSES/ man/ media/ meson/ src/ subprojects/ tests/")

    # Añade el wallpaper
    os.system("mkdir ~/.wallpapers")
    os.system("cp ~/Auto-Linux-Mint/tools/bspwm/wallpaper.jpg ~/.wallpapers")
    os.system("echo 'feh --bg-fill ~/.wallpapers/wallpaper.jpg' >> ~/.config/bspwm/bspwmrc")
    os.system("echo 'xsetroot -cursor_name left_ptr &' >> ~/.config/bspwm/bspwmrc")
    os.system("echo 'wmname LG3D &' >> ~/.config/bspwm/bspwmrc")

    # Clona el tema de blue-sky
    os.system("git clone https://github.com/VaughnValle/blue-sky.git")
    os.system("mkdir ~/.config/polybar")

    # Copia el tema de blue-sky a la config de polybar                                 |
    #os.system("cp -r blue-sky/polybar/* ~/.config/polybar")                           |
    #os.system("echo '~/.config/polybar/./launch.sh' >> ~/.config/bspwm/bspwmrc")      | #OLD SETTINGS
    #os.system("sudo cp blue-sky/polybar/fonts/* /usr/share/fonts/truetype")           |
    #os.system("fc-cache -v")                                                          |

    # Copia el tema de polybar a ~/.config
    os.system("cp ~/Auto-Linux-Mint/tools/bspwm/polybar-backup.zip .")
    os.system("unzip polybar-backup.zip")
    os.system("sudo mv polybar-backup/ ~/.config/")
    os.system("sudo rm -r ~/.config/polybar/ 2>/dev/null")
    os.system("sudo mv ~/.config/polybar-backup/ ~/.config/polybar/")
    os.system("echo '~/.config/polybar/./launch.sh' >> ~/.config/bspwm/bspwmrc")

    # Copia la config de picom
    os.system("mkdir ~/.config/picom")
    os.system("echo 'bspc config focus_follows_pointer true' >> ~/.config/bspwm/bspwmrc")
    
    expback = input("\nDesea usear los experimental-backends en picom? Si no se activa se puede detectar lentitud en el equipo al no disponer de una buena GPU. si/no -> ")

    if expback == "si":
        os.system("cp ~/Auto-Linux-Mint/tools/bspwm/picom.conf ~/.config/picom")

    if expback == "no":
        os.system("cp ~/Auto-Linux-Mint/tools/bspwm/picom-blur.conf ~/.config/picom/picom.conf")

    os.system("echo 'bspc config border_width 0' >> ~/.config/bspwm/bspwmrc")
    os.system("mkdir ~/.config/bin")
    os.system("echo 'picom --experimental-backends &' >> ~/.config/bspwm/bspwmrc")

    # Instalacion de Fuentes para Polybar
    os.system("sudo cp ~/.config/polybar/fonts/* /usr/share/fonts")

    # Mete el ethernet_status.sh, hackthebox_status.sh, target_to_hack.sh y target en ~/.config/bin
    os.system("chmod +x ~/Auto-Linux-Mint/tools/bspwm/ethernet_status.sh 2>/dev/null")
    os.system("mv ~/Auto-Linux-Mint/tools/bspwm/ethernet_status.sh ~/.config/bin")
    os.system("chmod +x ~/Auto-Linux-Mint/tools/bspwm/hackthebox.sh")
    os.system("mv ~/Auto-Linux-Mint/tools/bspwm/hackthebox.sh ~/.config/bin")
    os.system("cp ~/Auto-Linux-Mint/tools/bspwm/target_to_hack.sh .")
    os.system("chmod +x ~/Auto-Linux-Mint/tools/bspwm/target_to_hack.sh")
    os.system("mv ~/Auto-Linux-Mint/tools/bspwm/target_to_hack.sh ~/.config/bin")
    os.system("echo '' > ~/.config/bin/target")
    os.system("chmod +x ~/Auto-Linux-Mint/tools/bspwm/battery.sh")
    os.system("mv ~/Auto-Linux-Mint/tools/bspwm/battery.sh ~/.config/bin/")
    os.system("echo '' > ~/.config/bin/target")

    # Copia la config de polybar personalizada
    #os.system("cp ~/Auto-Linux-Mint/tools/bspwm/launch.sh ~/.config/polybar")
    #os.system("cp ~/Auto-Linux-Mint/tools/bspwm/current.ini ~/.config/polybar")

    # Copia la config de rofi personalizada
    os.system("mkdir ~/.config/rofi")
    os.system("mkdir ~/.config/rofi/themes")
    os.system("cp ~/Auto-Linux-Mint/tools/bspwm/nord.rasi ~/.config/rofi/themes")

    # Mueve los comandos settarget y cleartarget a /bin
    os.system("sudo cp ~/Auto-Linux-Mint/tools/bspwm/settarget /bin")
    os.system("sudo cp ~/Auto-Linux-Mint/tools/bspwm/cleartarget /bin")
    os.system("sudo chmod +x /bin/settarget")
    os.system("sudo chmod +x /bin/cleartarget")
    
    # Instalando Oh My Tmux
    os.system("git clone https://github.com/gpakosz/.tmux.git /home/$USER/.tmux")
    os.system("ln -s -f .tmux/.tmux.conf /home/$USER")
    os.system("cp /home/$USER/.tmux/.tmux.conf.local /home/$USER")
    
    # Instalando Oh My Tmux para root
    os.system("sudo git clone https://github.com/gpakosz/.tmux.git /root/.tmux")
    os.system("sudo ln -s -f .tmux/.tmux.conf /root")
    os.system("sudo cp /root/.tmux/.tmux.conf.local /root")

    # Instalando fastTCPscan.go
    os.system("chmod +x ~/Auto-Linux-Mint/tools/bspwm/fastTCPscan.go")
    os.system("sudo cp ~/Auto-Linux-Mint/tools/bspwm/fastTCPscan.go /bin")

    # Instalando wichSystem.py
    os.system("chmod +x ~/Auto-Linux-Mint/tools/bspwm/wichSystem.py")
    os.system("sudo mv ~/Auto-Linux-Mint/tools/bspwm/wichSystem.py /bin/")

def vpn():
    green()
    print("\nInstalando NordVPN....\n")

# Instalamos NordVPN....
    os.system("sudo dpkg -i ~/Auto-Linux-Mint/tools/zsh/nordvpn-release_1.0.0_all.deb")
    os.system("sudo apt update")
    os.system("sudo apt install nordvpn")

    time.sleep(2)
    green()
    print("\n[+] NordVPN se ha instalado correctamente\n")

def vbox():
    green()
    print("\nInstalando Vmware....\n")

# Instalamos VMware....
    os.system("sudo wget https://download3.vmware.com/software/WKST-1624-LX/VMware-Workstation-Full-16.2.4-20089737.x86_64.bundle")
    os.system("sudo chmod 777 VMware-Workstation-Full-16.2.4-20089737.x86_64.bundle")
    os.system("sudo ./VMware-Workstation-Full-16.2.4-20089737.x86_64.bundle")
    os.system("sudo apt-get -f install")
    os.system("sudo rm -r VMware-Workstation*")

    time.sleep(2)
    green()
    print("\n[+] VMware instalado correctamente\n")
    print("\nInstalando VirtualBox....\n")

# Instalamos VirtualBox....
    os.system("sudo wget https://download.virtualbox.org/virtualbox/6.1.36/virtualbox-6.1_6.1.36-152435~Ubuntu~jammy_amd64.deb")
    os.system("sudo dpkg -i virtualbox-6.1_6.1.36-152435\~Ubuntu\~jammy_amd64.deb")
    os.system("sudo apt-get -f install")
    os.system("sudo rm -r virtualbox*")

    time.sleep(2)
    green()
    print("\n[+] VirtualBox instalado correctamente\n")

def ink():
    green()
    print("\nInstalando Inkscape....\n")

# Instalamos Inkscape....
    os.system("sudo wget https://inkscape.org/gallery/item/34672/Inkscape-9c6d41e-x86_64.AppImage")
    os.system("sudo mv Inkscape-9c6d41e-x86_64.AppImage /opt")
    os.system("sudo chmod 777 /opt/Inkscape-9c6d41e-x86_64.AppImage")

    time.sleep(2)
    green()
    print("\n[+] Inkscape instalado correctamente en /opt\n")
    print("\nInstalando Gimp....\n")

# Instalamos Gimp....
    os.system("sudo apt update")
    os.system("sudo apt install gimp")

    time.sleep(2)
    green()
    print("\n[+] Gimp instalado correctamente\n")

def discord():
    green()
    print("\nInstalando Discord....\n")

# Instalamos Discord
    os.system("sudo wget https://dl.discordapp.net/apps/linux/0.0.18/discord-0.0.18.deb")
    os.system("sudo dpkg -i discord-0.0.18.deb")
    os.system("sudo apt-get -f install")
    os.system("sudo rm -r discord*")

    time.sleep(2)
    green()
    print("\n[+] Discord instalado correctamente\n")
    print("\nInstalando Telegram....\n")

# Instalamos Telegram....
    os.system("sudo apt update")
    os.system("sudo apt install telegram-desktop")

    time.sleep(2)
    green()
    print("\n[+] Telegram instalado correctamente\n")

def sublime():
    green()
    print("\nInstalando Sublime Text....\n")

# Instalamos sublime-text
    os.system("sudo wget https://download.sublimetext.com/sublime-text_build-4126_amd64.deb")
    os.system("sudo dpkg -i sublime-text_build-4126_amd64.deb")
    os.system("sudo rm -r sublime-text*")

    time.sleep(2)
    green()
    print("\n[+] Sublime Text instalado correctamente\n")


if __name__ == '__main__':
    menu()
