~~  environment setup
resetEnvironment
set {{onerror}} _restart:
set {{ctype}} cmd
set {{cachelink}}
set {{guiboxposition}} center


~~ begin

start:
get {{link}} clipboardPaste

if getValue cachelink ?equ {{link}} ?run run start:

if textStartWith "http://" {{link}} ?run run _alerter:
?else if textStartWith "https://" {{link}} ?run run _alerter:

run start:
end:


_alerter:
set {{cachelink}} ?var "{{link}}"
set {{guititle}} Link option
set {{okbutton}} "Yes"
if msg ?str "We have detected that you have copied a link {{link}}.\nDo you plan to Download something?"  ?run run _downloadlink:
end:

_downloadlink:
set {{okbutton}} "Continue"

get {{paths}} userInput path default to ?var "C:\Users\{{login}}\Downloads\downloaded.zip"

>> if empty ?var {{paths}} ?run set {{paths}} ?var "C:\Users\{{login}}\Downloads\downloaded.zip"

 set {{okbutton}} "Start Download"
 if not  msg ?var "Start Download now\nWe will alert you when download is complete" ?run run start: 
 
 fetcher -fetch-download -url {{link}} -saveto {{paths}}  -split-download 6
 
 set {{okbutton}} "Copy that!"
 msg Download complete
 set {{okbutton}} "Ok"
 run start:
 end:
 
 
_restart:

if not msg Something went wrong restart ?run stop
 set {{okbutton}} "Ok"
set {{cachelink}}

run start:

end: