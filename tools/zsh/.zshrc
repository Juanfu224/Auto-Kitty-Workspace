# Fix the Java Problem
export _JAVA_AWT_WM_NONREPARENTING=1


# Set up the prompt
autoload -Uz promptinit
promptinit
setopt histignorealldups sharehistory

# Use emacs keybindings even if our EDITOR is set to vi
bindkey -e

# Keep 1000 lines of history within the shell and save it to ~/.zsh_history:
HISTSIZE=1000
SAVEHIST=1000
HISTFILE=~/.zsh_history

# Use modern completion system
autoload -Uz compinit
compinit

zstyle ':completion:*' auto-description 'specify: %d'
zstyle ':completion:*' completer _expand _complete _correct _approximate
zstyle ':completion:*' format 'Completing %d'
zstyle ':completion:*' group-name ''
zstyle ':completion:*' menu select=2
if command -v dircolors >/dev/null 2>&1; then
  eval "$(dircolors -b)"
fi
zstyle ':completion:*:default' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' list-colors ''
zstyle ':completion:*' list-prompt %SAt %p: Hit TAB for more, or the character to insert%s
zstyle ':completion:*' matcher-list '' 'm:{a-z}={A-Z}' 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=* l:|=*'
zstyle ':completion:*' menu select=long
zstyle ':completion:*' select-prompt %SScrolling active: current selection at %p%s
zstyle ':completion:*' use-compctl false
zstyle ':completion:*' verbose true

zstyle ':completion:*:*:kill:*:processes' list-colors '=(#b) #([0-9]#)*=0=01;31'
zstyle ':completion:*:kill:*' command 'ps -u $USER -o pid,%cpu,tty,cputime,cmd'


# Manual configuration
export PATH="$HOME/.local/bin:$PATH"

# Manual aliases
if command -v lsd >/dev/null 2>&1; then
  alias ll='lsd -lh --group-dirs=first'
  alias la='lsd -a --group-dirs=first'
  alias l='lsd --group-dirs=first'
  alias lla='lsd -lha --group-dirs=first'
  alias ls='lsd --group-dirs=first'
fi
if command -v bat >/dev/null 2>&1; then
  alias cat='bat'
elif command -v batcat >/dev/null 2>&1; then
  alias cat='batcat'
fi
alias clear-histfile='rm $HISTFILE'
alias c='clear'

if command -v dnf >/dev/null 2>&1; then
  alias update='sudo dnf upgrade -y; command -v flatpak >/dev/null 2>&1 && flatpak update -y'
  alias autoremove='sudo dnf autoremove -y'
elif command -v apt >/dev/null 2>&1; then
  alias update='sudo apt update && sudo apt full-upgrade -y; command -v flatpak >/dev/null 2>&1 && flatpak update -y'
  alias autoremove='sudo apt autoclean && sudo apt autoremove -y'
fi

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# Plugins
[[ -f /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh ]] && \
  source /usr/share/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
[[ -f /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh ]] && \
  source /usr/share/zsh-autosuggestions/zsh-autosuggestions.zsh
[[ -f /usr/share/zsh-sudo/sudo.plugin.zsh ]] && \
  source /usr/share/zsh-sudo/sudo.plugin.zsh

# Functions

# Set 'man' colors
function man() {
    env \
    LESS_TERMCAP_mb=$'\e[01;31m' \
    LESS_TERMCAP_md=$'\e[01;31m' \
    LESS_TERMCAP_me=$'\e[0m' \
    LESS_TERMCAP_se=$'\e[0m' \
    LESS_TERMCAP_so=$'\e[01;44;33m' \
    LESS_TERMCAP_ue=$'\e[0m' \
    LESS_TERMCAP_us=$'\e[01;32m' \
    man "$@"
}

# key-bindings zsh
if [ -x "$(command -v fzf)" ]; then
  if [ -f /usr/share/doc/fzf/examples/key-bindings.zsh ]; then
    source /usr/share/doc/fzf/examples/key-bindings.zsh
  elif [ -f /usr/share/fzf/shell/key-bindings.zsh ]; then
    source /usr/share/fzf/shell/key-bindings.zsh
  fi
fi


#Teclado
bindkey "^[[H" beginning-of-line
bindkey "^[[F" end-of-line
bindkey "^[[3~" delete-char
bindkey "^[[1;3C" forward-word
bindkey "^[[1;3D" backward-word
bindkey -s "^[Ok" "+"
bindkey -s "^[Om" "-"
bindkey -s "^[OM" "^M"
bindkey -s "^[Oj" "*"
bindkey -s "^[Oo" "/"

# Change cursor shape for different vi modes.
function zle-keymap-select {
  if [[ $KEYMAP == vicmd ]] || [[ $1 = 'block' ]]; then
    echo -ne '\e[1 q'
  elif [[ $KEYMAP == main ]] || [[ $KEYMAP == viins ]] || [[ $KEYMAP = '' ]] || [[ $1 = 'beam' ]]; then
    echo -ne '\e[5 q'
  fi
}
zle -N zle-keymap-select

# Start with beam shape cursor on zsh startup and after every command.
zle-line-init() { zle-keymap-select 'beam' }
zle -N zle-line-init
if command -v starship >/dev/null 2>&1; then
  eval "$(starship init zsh)"
fi
