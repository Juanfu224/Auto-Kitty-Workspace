#!/usr/bin/env python3
"""Auto-Kitty-Workspace — instalador multi-distro (Debian/Ubuntu y Fedora)."""

from __future__ import annotations

import getpass
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
HOME = Path.home()
LOCAL_BIN = HOME / ".local" / "bin"
USR_LOCAL_BIN = Path("/usr/local/bin")
USR_LOCAL_NVIM = Path("/usr/local/nvim")
DISTRO: str | None = None

PACKAGES = (
    "zsh",
    "git",
    "curl",
    "unzip",
    "zsh-autosuggestions",
    "zsh-syntax-highlighting",
)

UA = {"User-Agent": "Auto-Kitty-Workspace"}
HACK_NF_URL = "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Hack.zip"
KITTY_INSTALLER = "https://sw.kovidgoyal.net/kitty/installer.sh"
STARSHIP_INSTALLER = "https://starship.rs/install.sh"
NVCHAD = "https://github.com/NvChad/starter"
FZF_REPO = "https://github.com/junegunn/fzf.git"

BANNER = r"""
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

RED, GREEN, YELLOW, ORANGE, PURPLE, RESET = (
    "\033[1;31m",
    "\033[0;32m",
    "\033[1;33m",
    "\033[1;38;5;208m",
    "\033[1;35m",
    "\033[0m",
)


def cprint(color: str, msg: str) -> None:
    print(f"{color}{msg}{RESET}")


def die(msg: str, code: int = 1) -> None:
    cprint(RED, f"[!] {msg}")
    sys.exit(code)


def run(cmd: list[str], *, check: bool = True) -> None:
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, check=False, text=True)
    if check and result.returncode != 0:
        die(f"Error ejecutando: {' '.join(cmd)}", result.returncode)


def resolve_arch() -> tuple[str, str]:
    """Devuelve (nvim_arch, rust_arch)."""
    m = platform.machine().lower()
    if m in {"x86_64", "amd64"}:
        return "x86_64", "x86_64"
    if m in {"aarch64", "arm64"}:
        return "arm64", "aarch64"
    die(f"Arquitectura no soportada: {m}")


NVIM_ARCH, RUST_ARCH = resolve_arch()


def download(url: str, dest: Path) -> None:
    cprint(ORANGE, f"[+] {url}")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req) as resp, dest.open("wb") as out:
        shutil.copyfileobj(resp, out)


def run_installer(url: str, *args: str) -> None:
    with tempfile.TemporaryDirectory(prefix="akw-installer-") as tmp:
        script = Path(tmp) / "install.sh"
        download(url, script)
        run(["sh", str(script), *args])


def force_link(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    dest.symlink_to(src)


def install_system_bin(src: Path, name: str) -> None:
    """Instala un binario en /usr/local/bin (root-owned, 0755) para user y root."""
    run(["sudo", "install", "-m", "755", str(src), str(USR_LOCAL_BIN / name)])


def wipe(*paths: Path) -> None:
    for path in paths:
        p = str(path)
        if p.startswith(("/root", "/usr/local")):
            run(["sudo", "rm", "-rf", p])
        elif path.exists():
            shutil.rmtree(path)


def copy_user_root(src: Path, rel: str) -> None:
    user = HOME / rel
    user.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, user)
    root = Path("/root") / rel
    run(["sudo", "mkdir", "-p", str(root.parent)])
    run(["sudo", "cp", "-f", str(src), str(root)])


def git_clone(url: str, dest: Path, *, root: bool = False) -> None:
    if root:
        run(["sudo", "rm", "-rf", str(dest)])
        run(["sudo", "git", "clone", "--depth=1", url, str(dest)])
    else:
        wipe(dest)
        run(["git", "clone", "--depth=1", url, str(dest)])


def github_asset(repo: str, needle: str) -> str:
    api = f"https://api.github.com/repos/{repo}/releases/latest"
    req = urllib.request.Request(
        api, headers={**UA, "Accept": "application/vnd.github+json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)
    for asset in data.get("assets", []):
        name = asset.get("name", "")
        if needle in name and name.endswith(".tar.gz") and "sha" not in name.lower():
            return asset["browser_download_url"]
    die(f"Sin asset '{needle}' en {repo}")


def install_tarball_bin(url: str, binary: str) -> None:
    with tempfile.TemporaryDirectory(prefix=f"akw-{binary}-") as tmp:
        tmp_p = Path(tmp)
        archive = tmp_p / "pkg.tar.gz"
        download(url, archive)
        run(["tar", "-xzf", str(archive), "-C", str(tmp_p)])
        found = next((p for p in tmp_p.rglob(binary) if p.is_file()), None)
        if not found:
            die(f"No se encontró '{binary}' en el archivo")
        install_system_bin(found, binary)


def detect_desktop() -> str:
    blob = " ".join(
        [
            os.environ.get("XDG_CURRENT_DESKTOP", ""),
            os.environ.get("DESKTOP_SESSION", ""),
            os.environ.get("XDG_SESSION_DESKTOP", ""),
        ]
    ).lower()
    if "kde" in blob or "plasma" in blob:
        return "kde"
    if "gnome" in blob:
        return "gnome"
    return "other"


def detect_distro() -> str:
    path = Path("/etc/os-release")
    if not path.exists():
        die("No se encontró /etc/os-release")
    data = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            data[k] = v.strip().strip('"')
    identity = f"{data.get('ID', '')} {data.get('ID_LIKE', '')}".lower()
    if any(t in identity for t in ("debian", "ubuntu", "linuxmint", "pop")):
        return "debian"
    if any(t in identity for t in ("fedora", "rhel", "centos", "rocky", "alma")):
        return "fedora"
    die(
        f"Distro no soportada ({data.get('PRETTY_NAME', '?')}). "
        "Usa Debian/Ubuntu o Fedora."
    )


def ensure_user_path() -> None:
    LOCAL_BIN.mkdir(parents=True, exist_ok=True)
    env_dir = HOME / ".config" / "environment.d"
    env_dir.mkdir(parents=True, exist_ok=True)
    (env_dir / "99-akw-path.conf").write_text(
        f'PATH="{LOCAL_BIN}:${{PATH}}"\n', encoding="utf-8"
    )
    os.environ["PATH"] = f"{LOCAL_BIN}:{os.environ.get('PATH', '')}"


def selinux_restore() -> None:
    if not shutil.which("restorecon") or not shutil.which("getenforce"):
        return
    status = subprocess.run(
        ["getenforce"], capture_output=True, text=True, check=False
    )
    if status.returncode != 0 or status.stdout.strip() == "Disabled":
        return
    local = HOME / ".local"
    if local.exists():
        run(["restorecon", "-Rv", str(local)], check=False)


def apply_kitty_font() -> None:
    cfg = HOME / ".config" / "kitty" / "kitty.conf"
    if not cfg.exists():
        return
    result = subprocess.run(
        ["fc-list", ":family"], capture_output=True, text=True, check=False
    )
    families: set[str] = set()
    for line in result.stdout.splitlines():
        for part in line.split(","):
            name = part.strip()
            if "hack" in name.lower() and "nerd" in name.lower():
                families.add(name)
    family = "Hack Nerd Font"
    for preferred in ("Hack Nerd Font", "HackNerdFont", "Hack Nerd Font Mono"):
        if preferred in families:
            family = preferred
            break
    else:
        if families:
            family = sorted(families)[0]

    lines = []
    for line in cfg.read_text(encoding="utf-8").splitlines():
        if line.strip().startswith("font_family"):
            lines.append(f"font_family      {family}")
        else:
            lines.append(line)
    cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
    cprint(GREEN, f"[+] Fuente Kitty: {family}")


def kwrite(key: str, value: str) -> bool:
    tool = shutil.which("kwriteconfig6") or shutil.which("kwriteconfig5")
    if not tool:
        return False
    run(
        [tool, "--file", "kdeglobals", "--group", "General", "--key", key, value],
        check=False,
    )
    return True


def set_kde_terminal(kitty_bin: str) -> bool:
    if not kwrite("TerminalApplication", kitty_bin):
        return False
    kwrite("TerminalService", "kitty.desktop")
    cprint(GREEN, "\n[+] Terminal por defecto configurada (KDE Plasma).")
    cprint(YELLOW, "    Puede hacer falta cerrar sesión o reiniciar Dolphin.")
    return True


def set_gnome_terminal(kitty_bin: str) -> bool:
    if not shutil.which("gsettings"):
        return False
    schema = "org.gnome.desktop.default-applications.terminal"
    run(["gsettings", "set", schema, "exec", kitty_bin], check=False)
    run(["gsettings", "set", schema, "exec-arg", ""], check=False)
    cprint(GREEN, "\n[+] Terminal por defecto configurada (GNOME).")
    return True


def pkg_install() -> None:
    if DISTRO == "debian":
        run(["sudo", "apt", "update"])
        run(["sudo", "apt", "install", "-y", *PACKAGES])
    else:
        run(["sudo", "dnf", "install", "-y", *PACKAGES])


def install_kitty() -> None:
    kitty_app = HOME / ".local" / "kitty.app"
    apps = HOME / ".local" / "share" / "applications"
    apps.mkdir(parents=True, exist_ok=True)

    run_installer(KITTY_INSTALLER, "launch=n")

    for name in ("kitty", "kitten"):
        src = kitty_app / "bin" / name
        if not src.exists():
            die(f"Falta {src} tras instalar Kitty")
        force_link(src, LOCAL_BIN / name)

    kitty_bin = (kitty_app / "bin" / "kitty").resolve()
    icon = (kitty_app / "share/icons/hicolor/256x256/apps/kitty.png").resolve()
    for name in ("kitty.desktop", "kitty-open.desktop"):
        src = kitty_app / "share" / "applications" / name
        if not src.exists():
            continue
        text = src.read_text(encoding="utf-8")
        text = text.replace("Icon=kitty", f"Icon={icon}")
        text = text.replace("Exec=kitty", f"Exec={kitty_bin}")
        (apps / name).write_text(text, encoding="utf-8")

    xdg = HOME / ".config" / "xdg-terminals.list"
    xdg.parent.mkdir(parents=True, exist_ok=True)
    xdg.write_text("kitty.desktop\n", encoding="utf-8")

    cfg = HOME / ".config" / "kitty"
    cfg.mkdir(parents=True, exist_ok=True)
    for name in ("kitty.conf", "color.ini"):
        shutil.copy2(REPO_ROOT / "tools" / "kitty" / name, cfg / name)


def install_zsh() -> None:
    user = getpass.getuser()
    run(["sudo", "usermod", "--shell", "/usr/bin/zsh", user])
    run(["sudo", "usermod", "--shell", "/usr/bin/zsh", "root"])
    zshrc = REPO_ROOT / "tools" / "zsh" / ".zshrc"
    shutil.copy2(zshrc, HOME / ".zshrc")
    run(["sudo", "cp", "-f", str(zshrc), "/root/.zshrc"])
    plugin = REPO_ROOT / "tools" / "zsh" / "plugins" / "sudo.plugin.zsh"
    run(["sudo", "mkdir", "-p", "/usr/share/zsh-sudo"])
    run(["sudo", "cp", "-f", str(plugin), "/usr/share/zsh-sudo/sudo.plugin.zsh"])


def install_rust_tool(name: str, repo: str) -> None:
    url = github_asset(repo, f"{RUST_ARCH}-unknown-linux-musl.tar.gz")
    install_tarball_bin(url, name)


def install_fzf() -> None:
    def setup(home: Path, *, root: bool) -> None:
        dest = home / ".fzf"
        git_clone(FZF_REPO, dest, root=root)
        cmd = [str(dest / "install"), "--key-bindings", "--completion", "--no-update-rc"]
        if root:
            cmd = ["sudo", *cmd]
        run(cmd, check=False)

    setup(HOME, root=False)
    setup(Path("/root"), root=True)
    fzf_bin = HOME / ".fzf" / "bin" / "fzf"
    if not fzf_bin.is_file():
        die("No se encontró fzf tras la instalación")
    install_system_bin(fzf_bin, "fzf")


def install_fonts() -> None:
    user_fonts = HOME / ".local" / "share" / "fonts"
    root_fonts = Path("/root/.local/share/fonts")
    user_fonts.mkdir(parents=True, exist_ok=True)
    run(["sudo", "mkdir", "-p", str(root_fonts)])

    with tempfile.TemporaryDirectory(prefix="akw-fonts-") as tmp:
        archive = Path(tmp) / "Hack.zip"
        out = Path(tmp) / "out"
        staged = Path(tmp) / "staged"
        staged.mkdir()
        download(HACK_NF_URL, archive)
        run(["unzip", "-o", "-q", str(archive), "-d", str(out)])
        for font in out.rglob("*"):
            if font.suffix.lower() in {".ttf", ".otf"}:
                shutil.copy2(font, staged / font.name)
                shutil.copy2(font, user_fonts / font.name)
        if any(staged.iterdir()):
            run(["sudo", "cp", "-t", str(root_fonts), "--", *map(str, staged.iterdir())])

    run(["fc-cache", "-f"], check=False)
    run(["sudo", "fc-cache", "-f"], check=False)
    apply_kitty_font()


def install_starship() -> None:
    with tempfile.TemporaryDirectory(prefix="akw-starship-") as tmp:
        bindir = Path(tmp) / "bin"
        bindir.mkdir()
        run_installer(STARSHIP_INSTALLER, "-y", "-b", str(bindir))
        binary = bindir / "starship"
        if not binary.is_file():
            die("No se encontró starship tras el instalador")
        install_system_bin(binary, "starship")
    copy_user_root(
        REPO_ROOT / "tools" / "starship" / "starship.toml",
        ".config/starship.toml",
    )


def install_nvim() -> None:
    wipe(
        HOME / ".config" / "nvim",
        HOME / ".local" / "share" / "nvim",
        HOME / ".cache" / "nvim",
        HOME / ".local" / "nvim",
        Path("/root/.config/nvim"),
        Path("/root/.local/share/nvim"),
        Path("/root/.cache/nvim"),
        USR_LOCAL_NVIM,
    )

    url = (
        "https://github.com/neovim/neovim/releases/latest/download/"
        f"nvim-linux-{NVIM_ARCH}.tar.gz"
    )

    with tempfile.TemporaryDirectory(prefix="akw-nvim-") as tmp:
        tmp_p = Path(tmp)
        archive = tmp_p / "nvim.tar.gz"
        download(url, archive)
        run(["tar", "-xzf", str(archive), "-C", str(tmp_p)])
        extracted = next(tmp_p.glob("nvim-linux-*"), None)
        if not extracted or not extracted.is_dir():
            die("No se pudo extraer Neovim")
        run(["sudo", "mv", str(extracted), str(USR_LOCAL_NVIM)])

    nvim_bin = USR_LOCAL_NVIM / "bin" / "nvim"
    if not nvim_bin.is_file():
        die(f"Falta {nvim_bin} tras instalar Neovim")
    run(["sudo", "ln", "-sfn", str(nvim_bin), str(USR_LOCAL_BIN / "nvim")])
    git_clone(NVCHAD, HOME / ".config" / "nvim")
    git_clone(NVCHAD, Path("/root/.config/nvim"), root=True)


def set_default_terminal() -> None:
    kitty_bin = str((HOME / ".local" / "kitty.app" / "bin" / "kitty").resolve())
    if not Path(kitty_bin).exists():
        kitty_bin = shutil.which("kitty") or "kitty"

    if DISTRO == "debian":
        run(
            ["sudo", "update-alternatives", "--config", "x-terminal-emulator"],
            check=False,
        )

    desktop = detect_desktop()
    if desktop == "kde" and set_kde_terminal(kitty_bin):
        return
    if desktop == "gnome" and set_gnome_terminal(kitty_bin):
        return

    cprint(
        YELLOW,
        "\n[!] Configura Kitty como terminal por defecto a mano.\n"
        f"    Binario: {kitty_bin}",
    )


def instalar() -> None:
    ensure_user_path()
    steps = (
        ("Paquetes del sistema", pkg_install),
        ("Kitty (oficial)", install_kitty),
        ("ZSH", install_zsh),
        ("bat (oficial)", lambda: install_rust_tool("bat", "sharkdp/bat")),
        ("lsd (oficial)", lambda: install_rust_tool("lsd", "lsd-rs/lsd")),
        ("fzf (oficial)", install_fzf),
        ("Hack Nerd Fonts", install_fonts),
        ("Starship (oficial)", install_starship),
        ("Neovim + NvChad (oficial)", install_nvim),
        ("SELinux (restorecon)", selinux_restore),
    )
    for label, fn in steps:
        cprint(ORANGE, f"\n[+] {label}…\n")
        fn()


if __name__ == "__main__":
    DISTRO = detect_distro()
    cprint(PURPLE, BANNER)
    cprint(GREEN, f"[+] Distro detectada: {DISTRO} | Escritorio: {detect_desktop()}\n")
    instalar()

    while True:
        answer = input("\n¿Deseas cambiar la terminal por defecto? (s/n): ").strip().lower()
        if answer not in {"s", "n"}:
            print("Solo puedes responder 's' o 'n'")
            continue
        if answer == "s":
            set_default_terminal()
        break

    cprint(
        GREEN,
        "\n[+] Instalación completada. Abre Kitty para comprobarlo.\n"
        "    Si acabas de instalar, cierra sesión para aplicar PATH y terminal por defecto.\n"
        "Disfruta <3",
    )
