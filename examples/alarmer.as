resetEnvironment

set {{ctype}} cmd
get {{timer}} userInput "set alarm time eg 12:00"

get {{choice}}  userInput ?str "What will i do if the alarm triggers \n1) say something \n2) start application \n3) run surtr command"

set {{task}} ""
set {{action}} ""
if getValue choice ?equ 1 ?run get {{task}} userInput "Enter what to say" ++  set {{action}} say ++ set {{task}} ?var "{{task}}"^
?else if getValue choice ?equ 2 ?run get {{task}}  userInput "Enter application path to start" ++ set {{action}} start ++ set {{task}} ?var  "{{task}}"^
?else if getValue choice ?equ 3 ?run get {{task}}  userInput "Enter your command" ++ set {{action}} run ++ set {{task}} ?var "{{task}}"


alarmchecker:
emit Alarm set at ?em-blue {{timer}}

if getValue action ?equ say ?run emit Action: ?em-yellow Say something...
?else if getValue action ?equ start ?run emit Action: ?em-yellow Start An Application ^
?else if getValue action ?equ run ?run emit Action: ?em-yellow Execute some cool surtr commands

emit:yellow [----------( ?em-white {{time}} ?em-yellow )----------]

if getValue time ?cntn "{{timer}}" ?run run _executeTask:
wait 1
clr
run alarmchecker:
end:

_executeTask:
emit:green ((({{timer}})))
wait 1
emit:warn running task
if getValue action ?equ say ?run say voice-0 0 {{task}}^
?else if getValue action ?equ start ?run fileman startFile {{task}}^
?else if getValue action ?equ run ?run emit ?exec "{{task}}"^
?else talk voice-0 0 ?var "Alert,Alert time {{timer}}" ++ msg ?var "Alert time {{timer}}"
stop
end:
