~~ Multi-Monitor Screenshot Archiver
set {{ctype}} cmd
set {{onerror}} nostop

set {{outdir}} ?var "C:\Users\{{login}}\Pictures\ScreenArchives"
get {{num}} prompt Enter the total number of monitor screens to capture
set {{count}} 0


set {{i}} ?var {{count}}
loopScreens:
if getValue i ?grtn {{num}} ?run run doneScreens: ?else run capture:
end:

capture:
screenShotMonitor {{count}} monitor_{{count}}_{{date}}_{{time}}.png
msg Captured monitor {{count}}
set {{count}} ?calc "{{count}} + 1"
run loopScreens:
end:

doneScreens:
msg All monitors captured
end
