
~~SURTR FILE WATCHER
resetEnvironment
set {{ctype}} cmd
set {{onerror}} nostop
get {{file}} userInput Type the file location and filename

set {{errornumber}} 0
watchFile {{file}}




if getValue errornumber ?grtn 0 ?run run _error: 

msg Watching {{file}} we will alert you^
if we detect any changes

~~get the file state

get {{change}} changeDetected {{file}}
clr


watcher:
clr
emit Watching ?em-yellow {{file}}
get {{changedetector}} changeDetected {{file}}
emit Latest Changes ?em-red {{changedetector}}
emit Old changes ?em-green {{change}}


if getValue changedetector ?nequ {{change}} ?run run fileoptions:
emit:blue  Still watching...
run watcher:
end:


fileoptions:
get {{options}} userInput change has been detected type restore to restore file to^

its previous state or type stop to stop^

monitoring file or type skip to^

ignore changes and continue

if getValue options ?cntn restore ?run^
restoreFile {{file}} ++ msg file restored successfully to its previous state ++ get {{change}} changeDetected {{file}} ++ run watcher:^
?else^

if getValue options ?cntn stop ?run^
stopWatching {{file}} ++ stopScript^
?else^

if getValue options ?cntn skip ?run^
msg changes ignored ++ get {{change}} changeDetected {{file}} ++ run watcher:^
?else^
run fileoptions:
end:

_error:
msg {{errortext}}
stop
end: