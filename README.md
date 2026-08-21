<h3 align="center">
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/logos/exports/1544x1544_circle.png" width="100" alt="Logo"/><br/>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
	Catppuccin for <a href="https://github.com/kovidgoyal/kitty">Kitty</a> & <a href="https://starship.rs">Starship</a>
	<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/misc/transparent.png" height="30" width="0px"/>
</h3>

![overview](https://raw.githubusercontent.com/Juanfu224/Auto-Linux-Workspace/master/tools/images/Logo.png)

# Auto-Kitty-Workspace
<p>
	Automates the installation and configuration of a fully themed workspace environment in the <b>Kitty</b> terminal using the <b>Catppuccin</b> theme.<br/>
</p>


## Features

- **ZSH** with a pastel **Starship** prompt.  
- **FZF** for an improved terminal search experience.  
- **Neovim** with the **NvChad** configuration.  
- **Custom shortcuts** for a faster workflow.  

> Compatible with **Debian-based** distributions and **Fedora** (and RHEL-like).  
> Tested on **Linux Mint 22.3 (Zena)**, **Ubuntu 24.04 (Noble Numbat)**, and aimed at **Fedora 40+**.



## Installation

> **Requirements:** Git and Python 3 must be installed. The script detects your distro and uses `apt` or `dnf` automatically.

```bash
git clone https://github.com/Juanfu224/Auto-Kitty-Workspace.git ~/Auto-Kitty-Workspace
cd ~/Auto-Kitty-Workspace
python3 main.py
```



## Script Overview

The installation script performs the following tasks:

* **Kitty installation & configuration** — Official binary installer + Catppuccin theme and shortcuts.
* **Starship + ZSH setup** — Official Starship installer and distro zsh plugins.
* **Neovim (NvChad)** — Official Neovim tarball + NvChad starter.
* **FZF / bat / lsd** — Official upstream installs (latest).
* **Plugins & utilities** — `zsh-autosuggestions`, `zsh-syntax-highlighting`, and more.



## Important Notes

* It is **recommended to restart your system** (or at least log out/in) after installation so the default shell and fonts apply.
* The script automatically removes old Neovim configurations before installing NvChad.
* **Default terminal:** on Debian/Ubuntu it uses `update-alternatives`; on Fedora (GNOME) it uses `gsettings`. Other desktops may need a manual setting.
* **Packages:** system deps (`zsh`, `git`, `curl`, `unzip`, zsh plugins) come from `apt`/`dnf`. **Kitty**, **Starship**, **Neovim**, **bat**, **lsd**, and **fzf** are installed from their official upstream sources (latest release / official installer). Hack Nerd Font uses the latest GitHub release. The zsh `sudo` plugin is vendored in the repo.

### Reinstalling Neovim (Clean Setup)

If you have an older Neovim version, remove any previous configurations before running the script:

```bash
sudo rm -rf ~/.config/nvim
sudo rm -rf ~/.local/share/nvim
sudo rm -rf ~/.cache/nvim
sudo rm -rf /root/.config/nvim
sudo rm -rf /root/.local/share/nvim
sudo rm -rf /root/.cache/nvim
```

If an error occurs during installation, rerun the script — it will automatically clean up any leftover files.



## Descriptions

| Component                   | Description                                                     |
| --------------------------- | --------------------------------------------------------------- |
| **Kitty**                   | Fast, GPU-accelerated terminal emulator for advanced users.     |
| **Starship**                | Minimal, fast, and customizable shell prompt written in Rust.   |
| **ZSH**                     | Developer-friendly shell with extensive plugin support.         |
| **FZF**                     | Command-line fuzzy finder for files, history, and more.         |
| **NvChad**                  | Neovim configuration framework focused on speed and modularity. |
| **Zsh-autosuggestions**     | Suggests commands from history as you type.                     |
| **Zsh-syntax-highlighting** | Highlights shell commands in real time.                         |
| **bat**                     | Enhanced `cat` with syntax highlighting and pagination.         |
| **lsd**                     | Modern `ls` replacement with icons and colors.                  |
| **Neovim**                  | Modern text editor based on Vim, built for extensibility.       |



## Custom Keyboard Shortcuts — Kitty Terminal

These shortcuts are configured in `kitty.conf` and help optimize navigation and workflow.


### Window Navigation

| Keys                           | Action                     | Description              |
| ------------------------------ | -------------------------- | ------------------------ |
| <kbd>Ctrl</kbd> + <kbd>←</kbd> | `neighboring_window left`  | Move to the left panel.  |
| <kbd>Ctrl</kbd> + <kbd>→</kbd> | `neighboring_window right` | Move to the right panel. |
| <kbd>Ctrl</kbd> + <kbd>↑</kbd> | `neighboring_window up`    | Move to the panel above. |
| <kbd>Ctrl</kbd> + <kbd>↓</kbd> | `neighboring_window down`  | Move to the panel below. |


### Copy & Paste Between Buffers

| Keys          | Action                | Description                     |
| ------------- | --------------------- | ------------------------------- |
| <kbd>F1</kbd> | `copy_to_buffer a`    | Copy selection to **Buffer A**. |
| <kbd>F2</kbd> | `paste_from_buffer a` | Paste from **Buffer A**.        |
| <kbd>F3</kbd> | `copy_to_buffer b`    | Copy selection to **Buffer B**. |
| <kbd>F4</kbd> | `paste_from_buffer b` | Paste from **Buffer B**.        |



### Window & Tab Management

| Keys                                                  | Action                | Description                                     |
| ----------------------------------------------------- | --------------------- | ----------------------------------------------- |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Z</kbd>     | `toggle_layout stack` | Switch to **stacked window mode**.              |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>Enter</kbd> | `new_window_with_cwd` | Open a new **window** in the current directory. |
| <kbd>Ctrl</kbd> + <kbd>Shift</kbd> + <kbd>T</kbd>     | `new_tab_with_cwd`    | Open a new **tab** in the current directory.    |



### Command History

| Keys                           | Description                          |
| ------------------------------ | ------------------------------------ |
| <kbd>Ctrl</kbd> + <kbd>R</kbd> | Search and navigate command history. |



## Credits

| Component          | Author     | Link                                    |
| ------------------ | ---------- | --------------------------------------- |
| **Script**         | Juanfu224  | [GitHub](https://github.com/Juanfu224)  |
| **Powerlevel10k**  | romkatv    | [GitHub](https://github.com/romkatv)    |
| **bat**            | sharkdp    | [GitHub](https://github.com/sharkdp)    |
| **lsd**            | Peltoche   | [GitHub](https://github.com/Peltoche)   |
| **Hack Nerd Font** | ryanoasis  | [GitHub](https://github.com/ryanoasis)  |
| **FZF**            | junegunn   | [GitHub](https://github.com/junegunn)   |
| **Neovim**         | Neovim     | [GitHub](https://github.com/neovim)     |
| **Kitty**          | kovidgoyal | [GitHub](https://github.com/kovidgoyal) |

> Inspired by **S4vitar** and **Yorkox0** ❤️


