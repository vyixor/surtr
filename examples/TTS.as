
resetEnvironment
set {{ctype}} cmd
~~Text to speech
emit:info ?em-white-green "Text To Speech Automation"
emit:blue ?exec voices

get {{voiceid}} emit:prompt Type your voice 0 for voice-0, 1 for voice-1 ... >
run _show:



_show:

get {{optn}} emit:prompt Enter 0 to read text or 1 to read file >
if getValue optn ?equ 0 ?run run _asktext:
?else if getValue optn ?equ 1 ?run run _askfile: 
end:


_asktext:
get {{text}} emit:prompt your text you want to say >
say voice-{{voiceid}} 0 {{text}}
end:

_askfile:
get {{text}} emit:prompt Enter the file path (.txt only) > 
if not fileExist {{text}} ?run emit:error File not exists ++ stop

~~get file extension
splitRun ?token "." {{text}} ?run run _getfileExt:
if getValue ext ?nequ txt ?run emit:error Only .txt files are allowed ++ stop
emit:info filename {{text}}
emit:info file type {{ext}}
say voice-{{voiceid}} 0 {{text}}
end:


_getfileExt:
set {{ext}} ?var "{{item}}"
end: