"-------------------------------------------------------------------------------
" identity.vim --- A simple colorscheme for vim/nvim
"
" Copyright (c) 2020 Jun Kato All Rights Reserved.
" Author: Jun Kato (junk-e) <junk05301996@gmail.com>
" URL: https://github.com/junk-e
" License: This software is released under the MIT License, see LICENSE.txt.
" Modified: 2020-02-16.
"-------------------------------------------------------------------------------

let g:colors_name = expand('<sfile>:t:r')
set background=dark
highlight clear
set foldcolumn=2
hi foldcolumn guibg=#302d38
hi VertSplit guibg=#302d38 guifg=#302d38

" Color palette "{{{
"-------------------------------------------------------------------------------
let s:vmode  = "gui"

" Base color from black to white
let s:base04 = "#302d38" " Background color
let s:base03 = "#302d38" " Sub background
let s:base02 = "#66f2f2" " Comment color
let s:base01 = "#ea4c88" " Dark Base color
let s:base00 = "#f0f0f0" " Base color
let s:base11 = "#c4cacd"
let s:base12 = "#72c373"
let s:base13 = "#939595"

let s:red00  = "#ea4c88" " complement color of base00
let s:yel00  = "#f55a99" " split of base00
"}}}

let s:none = "NONE"
let s:reve = "reverse"

exe "let s:fmt_none = " . "s:vmode . '=' . s:none"
exe "let s:fmt_reve = " . "s:vmode . '=' . s:reve"
exe "let s:fg = " . "s:vmode . 'fg='"
exe "let s:bg = " . "s:vmode . 'bg='"

function Def_hi(group, fmt, fgcol, bgcol)
    return "hi! " . a:group . " " . a:fmt . " " . s:fg . a:fgcol . " " . s:bg . a:bgcol
endfunction

" Basic highlighting "{{{
"-------------------------------------------------------------------------------
"+---------+------------------------+-----------+---------+---------+
"|         | GROUP NAME             | FORMAT    | FGCOLOR | BGCOLOR |
"+---------+------------------------+-----------+---------+---------+
exe Def_hi( "Normal",                s:fmt_none, s:base13, s:base04)
exe Def_hi( "Comment",               s:fmt_none, s:base02, s:none  )
exe Def_hi( "Constant",              s:fmt_none, s:base11, s:none  )
exe Def_hi( "Identifier",            s:fmt_none, s:red00,  s:none  )
exe Def_hi( "Statement",             s:fmt_none, s:base11, s:none )
exe Def_hi( "PreProc",               s:fmt_none, s:base13, s:none  )
exe Def_hi( "Type",                  s:fmt_none, s:base13, s:none  )
exe Def_hi( "Special",               s:fmt_none, s:base13, s:none  )
exe Def_hi( "Underlined",            s:fmt_none, s:none,   s:none  )
exe Def_hi( "Ignore",                s:fmt_none, s:none,   s:none  )
exe Def_hi( "Error",                 s:fmt_none, s:none,   s:none  )
exe Def_hi( "Todo",                  s:fmt_none, s:yel00,  s:base02)
"}}}

" Extended highlighting "{{{
"-------------------------------------------------------------------------------
" Look "{{{
"----------
"|         | GROUP NAME             | FORMAT    | FGCOLOR | BGCOLOR |
exe Def_hi( "NonText",               s:fmt_none, s:base02, s:base04)
exe Def_hi( "FoldColumn",            s:fmt_none, s:base03, s:base03)
exe Def_hi( "LineNr",                s:fmt_none, s:base02, s:base03)
exe Def_hi( "CursorLineNr",          s:fmt_none, s:base02, s:base03)
exe Def_hi( "ColorColumn",           s:fmt_reve, s:base04, s:red00 )
" NOTE: The background changes according to the text color (for discomfort)
exe Def_hi( "Folded",                s:fmt_none, s:base02, s:base03)

" Popup color
exe Def_hi( "Pmenu",                 s:fmt_none, s:base03, s:base01)
exe Def_hi( "PmenuSel",              s:fmt_none, s:base01, s:base03)
exe Def_hi( "PmenuSbar",             s:fmt_none, s:none,   s:base01)
exe Def_hi( "PmenuThumb",            s:fmt_none, s:none,   s:base03)

exe Def_hi( "vimOperParen",          s:fmt_none, s:base11, s:none  )

"}}}

exe Def_hi( "StatusLine",            s:fmt_none, s:none,   s:none  )
exe Def_hi( "StatusLineNC",          s:fmt_none, s:none,   s:none  )

exe Def_hi( "SpecialKey",            s:fmt_none, s:base03, s:none  )
exe Def_hi( "Visual",                s:fmt_none, s:base04, s:base01)
exe Def_hi( "Directory",             s:fmt_none, s:none,   s:none  )
exe Def_hi( "ErrorMsg",              s:fmt_none, s:red00,  s:none  )
exe Def_hi( "Search",                s:fmt_none, s:none,   s:none  )
"}}}


" indentLine
let g:indentLine_color_gui = s:base03
"}}}
