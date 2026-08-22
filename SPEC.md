# SPEC.md — Auto-Kitty-Workspace

**Versión:** 0.2 — 2026-08-22
**Estado:** Borrador

> Contrato de dominio inmutable durante una tarea activa. El código se deriva de aquí, no al revés.
> Cambios: nueva sección y/o bump de versión **entre** tareas. Criterios de una tarea = petición + sección relevante.
> Evidencia INIT: `README.md`, `main.py`, `tools/**`.

## 1. Visión y fuera de alcance

### Visión
Automatizar la instalación y configuración de un entorno de terminal themed (Kitty + Catppuccin, ZSH/Starship, Neovim/NvChad y utilidades CLI) en distros Debian-based y Fedora/RHEL-like, con un solo comando (`python3 main.py`).

### Objetivos funcionales
1. Detectar la familia de distro (`debian` vía apt / `fedora` vía dnf) y el escritorio (KDE, GNOME u otro).
2. Instalar paquetes de sistema: `zsh`, `git`, `curl`, `unzip`, `zsh-autosuggestions`, `zsh-syntax-highlighting`.
3. Instalar desde upstreams oficiales: Kitty, Starship, Neovim, bat, lsd, fzf y Hack Nerd Font.
4. Copiar assets del repo: `tools/kitty/{kitty.conf,color.ini}`, `tools/starship/starship.toml`, `tools/zsh/.zshrc` y plugin `sudo` vendored.
5. Configurar shell ZSH para el usuario actual y root; instalar CLIs compartidos en `/usr/local/bin` (salvo Kitty en `~/.local`).
6. Opcionalmente (prompt s/n) establecer Kitty como terminal por defecto (Debian `update-alternatives`, KDE `kwriteconfig*`, GNOME `gsettings`).

### Objetivos no funcionales
- Latencia p95: N/A (instalador offline-batch; no servicio en línea).
- Disponibilidad: N/A (ejecución local única).
- Accesibilidad: N/A (CLI TTY).
- Privacidad: no procesa datos personales de terceros; usa `getpass.getuser()` y paths de HOME; no telemetría propia.
- Idempotencia: re-ejecución limpia leftovers de Neovim (`wipe`); resto reescribe configs/binarios documentados en README.

### Fuera de alcance
- macOS, Windows y distros sin `apt`/`dnf`.
- Temas distintos de Catppuccin / configs no presentes en `tools/`.
- API HTTP, base de datos, autenticación de producto.
- Empaquetado deb/rpm oficial o CI de instalación end-to-end (no existe en el repo).

## 2. Arquitectura

- Estilo: script monolítico Python 3 (`main.py`) + assets estáticos en `tools/`.
- Límites de confianza: usuario local + `sudo` hacia sistema; red hacia instaladores/releases oficiales (Kitty, Starship, GitHub releases, NvChad starter).
- Diagrama (texto):

```
humano → python3 main.py → detect_distro/desktop
                        → apt|dnf (PACKAGES)
                        → download/installers (Kitty, Starship, nvim, bat, lsd, fzf, fonts)
                        → copy tools/* → ~/.config y /root
                        → [prompt] set_default_terminal
```

- Integraciones:
  | Nombre | Dirección | PII | Firma |
  |---|---|---|---|
  | Kitty installer | egress HTTPS | no | N/A (script oficial) |
  | Starship installer | egress HTTPS | no | N/A |
  | GitHub releases (neovim, bat, lsd, nerd-fonts) | egress HTTPS | no | N/A |
  | NvChad starter (git clone) | egress HTTPS/git | no | N/A |
  | apt / dnf | local + mirrors distro | no | N/A |

## 3. Modelo de datos

### Entidades
| Entidad | Invariantes | PII |
|---|---|---|
| Distro | Solo `debian` o `fedora` (detección vía `/etc/os-release`) | no |
| Desktop | `kde`, `gnome` u otro (sin auto-config de terminal genérico) | no |
| Paths instalados | Kitty bajo `~/.local`; `starship`/`lsd`/`bat`/`fzf`/`nvim` en `/usr/local/bin` | no |
| Configs | Fuentes: `tools/kitty/*`, `tools/starship/starship.toml`, `tools/zsh/.zshrc` | no |

### Enums / máquinas de estado
| Máquina | Estados | Transiciones legales | Ilegales |
|---|---|---|---|
| Distro | undetected → debian \| fedora | os-release ID_LIKE/ID | distro no soportada → die |
| Instalación | idle → steps secuenciales → done → prompt_terminal | orden fijo en `instalar()` | saltar steps no expuesto |
| Prompt terminal | ask → s (set_default_terminal) \| n (skip) | solo `s`/`n` | otras respuestas → re-preguntar |

### Persistencia
- Motor: N/A (filesystem local; sin BD).
- Transacciones obligatorias cuando: N/A.
- Claves / unicidad: N/A.

## 4. API / contratos

- Auth: N/A (CLI local; privilegio vía `sudo` interactivo del SO).
- Versionado: N/A (sin API versionada; contrato = comportamiento de `main.py` + este SPEC).
- Errores: `die(msg)` imprime en stderr coloreado y `sys.exit(code)`; comandos fallidos con `run(..., check=True)` abortan.
- Endpoints: N/A (no HTTP).

| Método | Ruta | Auth | Idempotente | Notas |
|---|---|---|---|---|
| CLI | `python3 main.py` | usuario + sudo según step | parcial (ver §1) | Reqs: Git y Python 3 instalados |

## 5. Flujos

1. **Bootstrap instalación:** pre: Linux debian/fedora, git, python3, red. Pasos: banner → `detect_distro` → `instalar()` (paquetes, Kitty, ZSH, bat, lsd, fzf, fonts, Starship, Neovim+NvChad, SELinux restorecon) → prompt terminal → mensaje final. Post: binarios y configs presentes; logout recomendado. Fallos: `die` en downloads/extract/missing binary.
2. **Terminal por defecto (opcional):** pre: Kitty instalado; respuesta `s`. Pasos: Debian alternatives y/o KDE/GNOME helpers. Post: terminal por defecto apunta a Kitty cuando el DE lo permite. Fallos: DE desconocido → mensaje manual con path del binario.
3. **Reinstall Neovim limpio:** pre: usuario re-ejecuta script o limpia paths documentados en README. Pasos: `wipe` de configs nvim user/root + `/usr/local/nvim` antes de instalar. Post: NvChad starter clonado en `~/.config/nvim` y `/root/.config/nvim`.

## 6. No funcionales detallados

- Rate limit: N/A.
- Observabilidad: logs = stdout de comandos (`$ cmd`); no loguear secretos (el script no maneja tokens).
- Backups / RPO / RTO: N/A; wipe de nvim es destructivo a propósito (documentado en README).
- Privilegio: steps con `sudo` para `/usr/local`, `/root`, paquetes, usermod shell.
- Fedora: `~/.config/environment.d/99-akw-path.conf` para PATH en GUI; `restorecon` si SELinux activo; `font_family` Kitty vía `fc-list`.

## 7. Estrategia de pruebas

Qué **debe fallar** si se rompe el contrato:

| Contrato | Test / comando |
|---|---|
| Distro soportada | Ejecutar en host sin apt/dnf → debe abortar con mensaje claro |
| Entrada CLI | `python3 main.py` es el único entrypoint documentado |
| Assets Kitty/Starship/ZSH | Tras install, existen configs bajo `~/.config/kitty`, `~/.config/starship.toml`, `~/.zshrc` derivados de `tools/` |
| CLIs compartidos | `starship`, `lsd`, `bat`, `fzf`, `nvim` resolubles para user (y root vía `/usr/local/bin`) |
| Kitty user-local | Binario bajo `~/.local/kitty.app` / symlinks en `~/.local/bin` |

Cobertura mínima de transiciones de estado: hoy **manual** (no hay suite automatizada en el repo). Gap aceptado hasta que exista test HITL/CI de smoke; no inventar harness aquí.

