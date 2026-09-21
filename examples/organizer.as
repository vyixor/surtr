~~Bulk Organizer
~~start fresh
resetEnvironment
set {{ctype}} cmd

~~hide errors
set {{showerror}} hide

~~handle all errors
set {{onerror}} _errorhandler:



get {{filepath}} prompt ?str "Enter the folder path you plan to organize >"

set {{images}} ?var "{{filepath}}\\IMAGES"
set {{zips}} ?var "{{filepath}}\\ARCHIVES"
set {{docs}} ?var "{{filepath}}\\DOCUMENTS"
set {{apps}} ?var "{{filepath}}\\APPLICATIONS"
set {{music}} ?var "{{filepath}}\\MUSIC"
set {{video}} ?var "{{filepath}}\\VIDEO"
set {{diskimage}} ?var "{{filepath}}\\DISKIMAGE"
set {{others}} ?var "{{filepath}}\\OTHERS"


emit:info creating organize directories

fileman newFolder {{images}}
fileman newFolder {{zips}}
fileman newFolder {{docs}}
fileman newFolder {{apps}}
fileman newFolder {{music}}
fileman newFolder {{video}}
fileman newFolder {{diskimage}}
fileman newFolder {{others}}


emit:info Starting organizer  for {{filepath}} in a few seconds


process:
emit:info Scanning...
~~ Move recently added files by extension

wait 1
clr
emit:info these following files will be organized
fileman listContent {{filepath}}
emit:warn We are going to move all files found in {{filepath}} to organized folders
wait 3
clr
emit:info Fasten your seatbelts because file Organizer is moving with top speed
wait 2
clr
splitRun  ?token-es "\n" ?exec "fileman listContent '{{filepath}}'" ?run  run _handleFile:
emit:info file organize completed
stop
end:


_handleFile:
~~ splitRun will feed each filename as {{item}}
~~get file paths
set {{fname}} ?var "{{filepath}}\\{{item}}"

~~check if its a folder
if fileman isFolder {{fname}} ?run exit

~~ get extension
set {{ext}} ?exec "fileman getType '{{fname}}'"
set {{ext}} ?str-lower "{{ext}}"
clr
emit:info filename {{fname}}
emit:info filetype {{ext}}

~~archives
if getValue ext ?equ .zip ?run runCmd move "{{fname}}"  "{{zips}}" ++ exit
if getValue ext ?equ .rar ?run runCmd move "{{fname}}"  "{{zips}}" ++ exit
if getValue ext ?equ .7z ?run runCmd move "{{fname}}"  "{{zips}}" ++ exit

~~images
if getValue ext ?equ .jpg ?run runCmd move "{{fname}}" "{{images}}" ++ exit
if getValue ext ?equ .png ?run runCmd move "{{fname}}" "{{images}}" ++ exit
if getValue ext ?equ .gif ?run runCmd move "{{fname}}" "{{images}}" ++ exit

~~documents
if getValue ext ?equ .txt ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .pdf ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .chm ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .doc ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .xls ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .ppt ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .vsd ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .mpp ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .pub ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .docx ?run runCmd move "{{fname}}" "{{docs}}" ++ exit
if getValue ext ?equ .pptx ?run runCmd move "{{fname}}" "{{docs}}" ++ exit



~~applications
if getValue ext ?equ .exe ?run runCmd move "{{fname}}" "{{apps}}" ++ exit
if getValue ext ?equ .msi ?run runCmd move "{{fname}}" "{{apps}}" ++ exit

~~audio
if getValue ext ?equ .mp3 ?run runCmd move "{{fname}}" "{{music}}" ++ exit
if getValue ext ?equ .wav ?run runCmd move "{{fname}}" "{{music}}" ++ exit



~~video
if getValue ext ?equ .mp4 ?run runCmd move "{{fname}}" "{{video}}" ++ exit
if getValue ext ?equ .mkv ?run runCmd move "{{fname}}" "{{video}}" ++ exit

~~disk image files
if getValue ext ?equ .iso ?run runCmd move "{{fname}}" "{{diskimage}}" ++ exit
if getValue ext ?equ .img ?run runCmd move "{{fname}}" "{{diskimage}}" ++ exit

~~others

runCmd move "{{fname}}" "{{others}}"

end:



_errorhandler:
emit:error We got an error while trying to organize your folders
emit:error Errornumber #{{errornumber}}
emit:error Info {{errortext}}
emit:error Cause {{errorsource}}

get {{choice}} emit:prompt  ?str "Do you want to continue (y/n)"

~~to lower case

set {{choice}} ?str-lower "{{choice}}"

if getValue choice ?nequ y ?run stop

end: