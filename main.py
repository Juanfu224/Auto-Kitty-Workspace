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


def cpu_triple() -> tuple[str, str]:
    """(nvim_arch, rust_arch) — p.ej. ('x86_64','x86_64') o ('arm64','aarch64')."""
    m = platform.machine().lower()
    if m in {"x86_64", "amd64"}:
        return "x86_64", "x86_64"
    if m in {"aarch64", "arm64"}:
        return "arm64", "aarch64"
    die(f"Arquitectura no soportada: {m}")
    raise SystemExit  # unreachable


def download(url: str, dest: Path) -> None:
    cprint(ORANGE, f"[+] {url}")
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req) as resp, dest.open("wb") as out:
        shutil.copyfileobj(resp, out)


def force_link(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() or dest.is_symlink():
        dest.unlink()
    dest.symlink_to(src)


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
        if dest.exists():
            shutil.rmtree(dest)
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
    raise SystemExit


def install_tarball_bin(url: str, binary: str) -> None:
    with tempfile.TemporaryDirectory(prefix=f"akw-{binary}-") as tmp:
        tmp_p = Path(tmp)
        archive = tmp_p / "pkg.tar.gz"
        download(url, archive)
        run(["tar", "-xzf", str(archive), "-C", str(tmp_p)])
        found = next((p for p in tmp_p.rglob(binary) if p.is_file()), None)
        if not found:
            die(f"No se encontró '{binary}' en el archivo")
        dest = LOCAL_BIN / binary
        shutil.copy2(found, dest)
        dest.chmod(0o755)


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
    raise SystemExit


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

    with tempfile.TemporaryDirectory(prefix="akw-kitty-") as tmp:
        script = Path(tmp) / "installer.sh"
        download(KITTY_INSTALLER, script)
        run(["sh", str(script), "launch=n"])

    for name in ("kitty", "kitten"):
        src = kitty_app / "bin" / name
        if not src.exists():
            die(f"Falta {src} tras instalar Kitty")
        force_link(src, LOCAL_BIN / name)

    kitty_bin = (kitty_app / "bin" / "kitty").resolve()
    icon = (
        kitty_app / "share/icons/hicolor/256x256/apps/kitty.png"
    ).resolve()
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
    _, rust_arch = cpu_triple()
    url = github_asset(repo, f"{rust_arch}-unknown-linux-musl.tar.gz")
    install_tarball_bin(url, name)


def install_fzf() -> None:
    def setup(home: Path, *, root: bool) -> None:
        dest = home / ".fzf"
        git_clone(FZF_REPO, dest, root=root)
        cmd = [str(dest / "install"), "--key-bindings", "--completion", "--no-update-rc"]
        if root:
            cmd = ["sudo", *cmd]
        run(cmd, check=False)
        if not root:
            binary = dest / "bin" / "fzf"
            if binary.exists():
                force_link(binary, LOCAL_BIN / "fzf")

    setup(HOME, root=False)
    setup(Path("/root"), root=True)


def install_fonts() -> None:
    user_fonts = HOME / ".local" / "share" / "fonts"
    user_fonts.mkdir(parents=True, exist_ok=True)
    run(["sudo", "mkdir", "-p", "/root/.local/share/fonts"])

    with tempfile.TemporaryDirectory(prefix="akw-fonts-") as tmp:
        archive = Path(tmp) / "Hack.zip"
        out = Path(tmp) / "out"
        download(HACK_NF_URL, archive)
        run(["unzip", "-o", "-q", str(archive), "-d", str(out)])
        fonts = [p for p in out.rglob("*") if p.suffix.lower() in {".ttf", ".otf"}]
        for font in fonts:
            shutil.copy2(font, user_fonts / font.name)
        if fonts:
            run(["sudo", "cp", "-f", *[str(user_fonts / f.name) for f in fonts], "/root/.local/share/fonts/"])

    run(["fc-cache", "-f"], check=False)
    run(["sudo", "fc-cache", "-f"], check=False)


def install_starship() -> None:
    with tempfile.TemporaryDirectory(prefix="akw-starship-") as tmp:
        script = Path(tmp) / "install.sh"
        download(STARSHIP_INSTALLER, script)
        run(["sh", str(script), "-y", "-b", str(LOCAL_BIN)])
    copy_user_root(REPO_ROOT / "tools" / "starship" / "starship.toml", ".config/starship.toml")


def install_nvim() -> None:
    for rel in (".config/nvim", ".local/share/nvim", ".cache/nvim"):
        path = HOME / rel
        if path.exists():
            shutil.rmtree(path)
    run(["sudo", "rm", "-rf", "/root/.config/nvim", "/root/.local/share/nvim", "/root/.cache/nvim"])

    nvim_arch, _ = cpu_triple()
    url = f"https://github.com/neovim/neovim/releases/latest/download/nvim-linux-{nvim_arch}.tar.gz"
    nvim_home = HOME / ".local" / "nvim"
    if nvim_home.exists():
        shutil.rmtree(nvim_home)

    with tempfile.TemporaryDirectory(prefix="akw-nvim-") as tmp:
        tmp_p = Path(tmp)
        archive = tmp_p / "nvim.tar.gz"
        download(url, archive)
        run(["tar", "-xzf", str(archive), "-C", str(tmp_p)])
        extracted = next(tmp_p.glob("nvim-linux-*"), None)
        if not extracted or not extracted.is_dir():
            die("No se pudo extraer Neovim")
        shutil.move(str(extracted), str(nvim_home))

    force_link(nvim_home / "bin" / "nvim", LOCAL_BIN / "nvim")
    git_clone(NVCHAD, HOME / ".config" / "nvim")
    git_clone(NVCHAD, Path("/root/.config/nvim"), root=True)


def set_default_terminal() -> None:
    kitty_bin = str(HOME / ".local" / "kitty.app" / "bin" / "kitty")
    if not Path(kitty_bin).exists():
        kitty_bin = shutil.which("kitty") or "kitty"

    if DISTRO == "debian":
        run(["sudo", "update-alternatives", "--config", "x-terminal-emulator"], check=False)
        return

    if DISTRO == "fedora" and shutil.which("gsettings"):
        schema = "org.gnome.desktop.default-applications.terminal"
        run(["gsettings", "set", schema, "exec", kitty_bin], check=False)
        run(["gsettings", "set", schema, "exec-arg", ""], check=False)
        cprint(GREEN, "\n[+] Terminal por defecto configurada (GNOME).")
        return

    cprint(
        YELLOW,
        "\n[!] Configura Kitty como terminal por defecto a mano.\n"
        f"    Binario: {kitty_bin}",
    )


def instalar() -> None:
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
    )
    for label, fn in steps:
        cprint(ORANGE, f"\n[+] {label}…\n")
        fn()


if __name__ == "__main__":
    LOCAL_BIN.mkdir(parents=True, exist_ok=True)
    os.environ["PATH"] = f"{LOCAL_BIN}:{os.environ.get('PATH', '')}"

    DISTRO = detect_distro()
    cprint(PURPLE, BANNER)
    cprint(GREEN, f"[+] Distro detectada: {DISTRO}\n")
    instalar()

    while True:
        answer = input("\n¿Deseas cambiar la terminal por defecto? (s/n): ").strip().lower()
        if answer not in {"s", "n"}:
            print("Solo puedes responder 's' o 'n'")
            continue
        if answer == "s":
            set_default_terminal()
        break

    cprint(GREEN, "\n[+] Instalación completada. Abre Kitty para comprobarlo.\nDisfruta <3")
