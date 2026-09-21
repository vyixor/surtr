~~ Auto Login & Dashboard Extractor
~~ Required images: login.png, dashboard.png
resetEnvironment
set {{ctype}} cmd

~~ Ask user for inputs
get {{url}} prompt Enter login url >
get {{loginname}} prompt Enter user name or email e.g user@example.com >
get {{password}} prompt Enter password >

~~ Open Chrome (find a Chrome window) and navigate
get {{titlewindow}} inWindowTitle Chrome
if getValue titlewindow ?cntn no title ?run msg "Chrome window not found; please open Chrome and try again" ++ end ?else focusWindow {{titlewindow}}
wait 0.5

keyBoard type 0.1 {{url}}
keyBoard press enter
wait 5

~~ Click login button / fields using image (save login button image as login.png)
~~ Try to move to the image then click. If not found, warn and stop.
if seeImage login.png ?run move login.png 1 ?run click ?else msg "Login button not found" ++ stop

~~ Type credentials (use carefull delay)
wait 0.3
keyBoard type 0.15 {{loginname}}
keyBoard press tab
wait 0.2
keyBoard type 0.15 {{password}}
keyBoard press enter

~~ Wait for dashboard and verify
wait 5
if seeImage dashboard.png ?run emit Dashboard found starting capture ?else msg "Dashboard not detected" ++ stop

~~ Get the window bounds for the Chrome window we focused (titlewindow)
get {{x}} getWindowX {{titlewindow}}
get {{y}} getWindowY {{titlewindow}}
get {{width}} getWindowWidth {{titlewindow}}
get {{height}} getWindowHeight {{titlewindow}}

~~ Perform a screenshot of the window area and OCR it
screenShot {{x}} {{y}} {{width}} {{height}} dashboard.jpg
get {{ocr}} readImage dashboard.jpg useGray eng
fileman writeFile dashboard-data.txt {{ocr}}
msg "Dashboard data saved to dashboard-data.txt"
end
