~~SURTR WINDOW SCREENSHOT SCRIPT
~~starts with a new fresh environment

resetEnvironment

set {{ctype}} cmd
set {{showerror}} full
set {{guiboxposition}} center


get {{openwindows}}  windowList
get {{windowname}} userInput ?str " {{openwindows}}, Type the title of the window you want to screenshot"
get {{imagelocation}} userInput Type the location you want to save the image (use .jpg or .png for better quality)

_focus:
set {{name}} ?arg*
focusWindow {{name}}
end:

~~look for the window title that contains the name
get {{titlewindow}} inWindowTitle {{windowname}}

~~checks if there is a title found
if not getValue titlewindow ?cntn no title ?run run _focus: ?arg {{titlewindow}} ?else run error:

emit:green found {{windowname}} window full title = ?em-yellow {{titlewindow}}

~~prompt for save locatioon

~~get the size

get {{x}} getWindowX {{titlewindow}}
get {{y}} getWindowY {{titlewindow}}
get {{width}} getWindowWidth {{titlewindow}}
get {{height}} getWindowHeight {{titlewindow}}

~~perform a screen shot and save
screenShot {{x}} {{y}} {{width}} {{height}} {{imagelocation}}


emit:green Screenshot completed

~~close the script
stop

error:
msg No window found
stop
