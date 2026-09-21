set {{ctype}} cmd
get {{titlewindow}} inWindowTitle Chrome
set {{numbercount}} 1
focusWindow {{titlewindow}}

wait 2
~~read file line by line
splitRun passwordlist.txt ?run run _typer:

msg password not found
stop




_typer:
clr
emit:red trying {{numbercount}}
set {{numbercount}} ?calc "{{numbercount}} + 1"

set {{currentpassword}} ?var "{{item}}"

keyBoard type 0.25 {{item}}
keyBoard press enter
wait 6

if not seeImage successimage.png ?run run _passwordfound:

end:


_passwordfound:
msg password = {{currentpassword}}
stop