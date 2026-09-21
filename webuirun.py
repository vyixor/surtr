import sys
from flask import Flask, session, redirect, url_for, render_template,render_template_string, request, jsonify, Response, flash,send_from_directory,stream_with_context
from flask import Response
import os 
import random
import io
import mss
import threading
import time
from flask_sock import Sock
from PIL import Image
import io
import sys
import ctypes
import os
import win32gui
import win32ui
import win32con
import win32api
from win32api import GetSystemMetrics
import ctypes, win32gui, win32ui
from PIL import Image
import threading
import time
import queue # For a more robust audio buffer
import ctypes, win32gui, win32ui, win32con, win32api
import pyaudiowpatch as pyaudio # <--- Use this instead of sounddevice and ctypes
from waitress import serve # Add this import
import secrets # For generating a strong secret key
from colorama import Fore,init,Back,Style,Cursor
import winpty
import threading
from pathlib import Path
import re
import time 
import credloader
import subprocess
import logging
import warnings
import datetime as dt
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.text import Text
from rich.console import Group
from rich.align import Align 
import customtkinter as ctk
import random
import getpass
import traceback
import credloader
from credloader import *
import json
import traceback
#global error catcher (catches any error not handled by try catch)
def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Let Ctrl+C behave normally
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    #print(f"Uncaught Exception: {exc_type.__name__}: {exc_value}")
    #traceback.print_exception()
    print(f"Unknown error: {exc_type.__name__}: {exc_value}")

# Activate the global error catcher hook
sys.excepthook = global_exception_handler


# ctrl+c error catcher
# stops the script without errors when the ctrl+c is hit on the keyboard (for clean exit)
import signal
# Global stop flag
stop_event = threading.Event()
system_running = False  # system running flag



def handle_sigint(signum, frame):
    global system_running
    print("\nCleaning up please wait...")
    stop_event.set()     # Tell threads to stop
    system_running = False
    time.sleep(2)        # Optional: Let threads wind down
    print("Closing...")
    #sys.exit(0)            # Exit silently without traceback
    os._exit(0)   #forcefully closes everything at once without warning or exceptions
# Register the signal handler
signal.signal(signal.SIGINT, handle_sigint)


APP_TITLE = "Surtr webui"
ctypes.windll.kernel32.SetConsoleTitleW(APP_TITLE)
  
if(os.path.exists(os.path.normpath("resources")) and os.path.isdir(os.path.normpath("resources"))):
    resource_path = os.path.normpath("resources")  
elif (os.path.exists(os.path.normpath("C:\\Surtr\\surtr\\resources")) and os.path.isdir(os.path.normpath("C:\\Surtr\\surtr\\resources"))):
    resource_path = os.path.normpath("C:\\Surtr\\surtr\\resources")
else:
    print("cannot find 'resources' folder")  
    sys.exit()

batchfolder = os.path.join(resource_path,"process","batchrun")
crefile = os.path.join(resource_path,"process","cred","awpdfs.sts")
weblogins = os.path.join(resource_path,"process","cred","webhandles.list")
configfile = os.path.join(resource_path,"surtrconfig.conf")
ssm_path = os.path.join(resource_path,"process","cred","SSM.pct")
logins = {"settings": "surtr",}
configs={"settings": "surtr",}

#for settings
webuibyte = {"bytes":""}
setting = {}

maxuser = 3
usercount = 0
SAVE_LOGS = None
#activation detection
try:
 ld = credloader.decrypt_file(input_path=ssm_path,save=False)
 decp = ld.decode()
 data = json.loads(decp)
 #print(data)
 #CHECK FOR ACTIVATION

 if data["verified"] == "no":
    print("Start request rejected DETAIL: Surtr professional not activated")
    time.sleep(5)
    os._exit(5)

except Exception as e:
  print("A fatal error occured could be a non existing or corrupt file")
  time.sleep(10)
  os._exit(10)


def settingsparser():
 try:
     setting.clear()
     decrp = credloader.decrypt_file(input_path=crefile,save=False)
     webuibyte["bytes"] = decrp
     prse = webuibyte["bytes"].decode()
     f = prse.split("\n")
     for i in f:
        stp = i.strip()
        ans = stp.split("=")
        setting[ans[0]] = " ".join(ans[1:]).strip()
 except Exception as e:
      print(f"WEBUI CANNOT START, CONFIGURATION ERROR")
      sys.exit(1)
 
settingsparser() 

    
def settings(index):
    if index in setting:
          return setting[index]
    else:
      return ""

def surtrconfig(index):
  try:
    if os.path.exists(configfile) and os.path.isfile(configfile):
      f= open(configfile,"r")
      foundset = False
      for i in f:
        if index in i:
          foundset = True
          ans = i.split("=")
          return " ".join(ans[1:]).strip()
      if foundset == False:
          print("corrupt configuration file")
          time.sleep(5)
          os._exit(100)
    else:
      print("cannot find surtr configuration file")
      time.sleep(5)
      os._exit(100)
  except:
    return "" 



if settings("permanent") == "no":
    try:
      subprocess.run(['start','/wait','webuiconfig.exe'],shell=True,creationflags=subprocess.CREATE_NO_WINDOW)
      settingsparser()
    except:
      print("WARNING: Cannot start webuiconfig.exe, Please check if surtr directory is added to path \nor webuiconfig.exe is available in surtr directory")
 

 #for dash board settings 






if settings("usescreen") == "no":
  configs.update({"usescreen":"no"})
else:
      configs.update({"usescreen":"yes"})
      
if settings("useaudio") == "no":
      configs.update({"useaudio":"no"})
else:
      configs.update({"useaudio":"yes"})
#add for theme
surtrtheme = surtrconfig("useWebuiDefaultSurtrTheme")  

configs.update({"usesurtrtheme":surtrtheme}) 
    
os.system('cls' if os.name == 'nt' else 'clear') 
  
app = Flask(__name__, static_folder='webui/static', template_folder='webui/templates')
sock = Sock(app)

# --- IMPORTANT: Configure Secret Key ---
# This is CRUCIAL for session security.
# Generate a strong, random key and keep it secret!
# Do NOT hardcode it in production. Use environment variables.
sessionkey = secrets.token_hex(32)
app.config['SECRET_KEY'] = os.environ.get('FLASK_SECRET_KEY', sessionkey) # Good practice for local/dev
#print(f"secreet key = {sessionkey}")
# For production, fetch from a secure environment variable or vault.

# Optional: Make sessions permanent (they won't expire when browser closes)
#app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30) # Example: 30 minutes

def show_time():
    now = dt.datetime.now()
    
    try:
        # Try to detect Windows time format setting
        LOCALE_USER_DEFAULT = 0x0400
        LOCALE_ITIME = 0x0023
        buffer = ctypes.create_unicode_buffer(2)
        if ctypes.windll.kernel32.GetLocaleInfoW(LOCALE_USER_DEFAULT, LOCALE_ITIME, buffer, 2):
            if buffer.value == '0':  # 12-hour format
                return now.strftime("%I:%M:%S %p")
        # Default to 24-hour format if detection fails or setting is 24-hour
        return now.strftime("%H:%M:%S")
    except:
        # Fallback to 12-hour format if any error occurs
        return now.strftime("%I:%M:%S %p")

VALID_SERVER_SESSION_IDS = set()

init(autoreset=True)
left = 0
loginfailed = 0
loginsuccess = 0
webuiwarnings = []
webuierrors = []
webui_info = []


# Toggle states for collapsible sections
show_info = True
show_warnings = True
show_errors = True

console = Console()
log_console = Console(stderr=True)



def showlog(logtype ='info',text=''):
  global SAVE_LOGS
  try:
    time = show_time()
    if logtype == "info":
        webui_info.append(f"({time}) {text}")
        if SAVE_LOGS is not None:
            with open(SAVE_LOGS,"a") as f:
                f.write(f"[INFO] ({time}) {text}\n")
                
    elif logtype == "error":
        webuierrors.append(f"({time}) {text}")
        if SAVE_LOGS is not None:
            with open(SAVE_LOGS,"a") as f:
                f.write(f"[ERROR] ({time}) {text}\n")
    
    elif logtype == "warning":
        webuiwarnings.append(f"({time}) {text}") 
        if SAVE_LOGS is not None:
            with open(SAVE_LOGS,"a") as f:
                f.write(f"[WARNING] ({time}) {text}\n")  
   
  except Exception as e:
       print(f"Cannot log eror: {e}")       
    
    
            
# ---------------- Dashboard builder ----------------
def build_dashboard():
  try:
    current_time = show_time()
    # Header
    header = Text("WEBUI STATUS DASHBOARD", style="bold green")

    # Status
    status_text = Text("RUNNING", style="green") if system_running else Text("STOPPED", style="red")

    # Summary Table
    summary = Table.grid(expand=True)
    summary.add_column(justify="center")
    summary.add_column(justify="center")
    summary.add_column(justify="center")
    summary.add_column(justify="center")
    summary.add_column(justify="center")
    summary.add_column(justify="center")
    summary.add_row(
        "[white on blue] USERS [/]", f"[green]{len(VALID_SERVER_SESSION_IDS)}[/]",
        "[white on blue] LEFT [/]", f"[yellow]{left}[/]",
        "[white on blue] LOGIN FAIL [/]", f"[red]{loginfailed}[/]"
    )
    summary.add_row(
        "[white on blue] LOGIN OK [/]", f"[green]{loginsuccess}[/]",
        "[white on red] ERRORS [/]", f"[red]{len(webuierrors)}[/]",
        "[black on yellow] WARNINGS [/]", f"[yellow]{len(webuiwarnings)}[/]"
    )

    # INFO section
    if show_info:
        info_text = Text(str(len(webui_info)), style="cyan") if webui_info else Text("No info available.", style="cyan")
    else:
        info_text = Text("[Collapsed]", style="cyan")

    # Warnings section
    if show_warnings:
        warnings_text = Text(str(len(webuiwarnings)), style="yellow") if webuiwarnings else Text("No warnings.", style="green")
    else:
        warnings_text = Text("[Collapsed]", style="yellow")

    # Errors section
    if show_errors:
        errors_text = Text(str(len(webuierrors)), style="red") if webuierrors else Text("No errors.", style="green")
    else:
        errors_text = Text("[Collapsed]", style="red")

    # Combine all sections using Group
    panel_group = Group(
      Align.center(header),
      Text("\n"),
      Text("STATUS: ") + status_text,
      Text("\n"),
      summary,
      Text.from_markup("\n[bold cyan]INFO[/bold cyan]\n"),
      info_text,
      Text.from_markup("\n[bold yellow]WARNINGS[/bold yellow]\n"),
      warnings_text,
      Text.from_markup("\n[bold red]ERRORS[/bold red]\n"),
      errors_text,
      Text.from_markup(f"\nLast update: {current_time}")
    )


    return Panel(panel_group, expand=True, border_style="cyan")
  except Exception as e:
     print(f"Cannot build dashboard {e}")
     time.sleep(5)
     os._exit(100)
     
root = None
def infogui(): 
 global webui_info,webuierrors,webuiwarnings,root   
 try: 
  # Initialize main app
  ctk.set_appearance_mode("dark")
  ctk.set_default_color_theme("dark-blue")
  root = ctk.CTk()
  root.withdraw() #hides window at startup
  root.title("WebUI Logs")
  root.geometry("600x500")

  def on_close():
    root.withdraw()  # hide instead of closing

  # Override the close button
  root.protocol("WM_DELETE_WINDOW", on_close)
  
  # Create frames for collapsible sections
  def create_section(parent, title, list_ref, color):
    frame = ctk.CTkFrame(parent)
    header = ctk.CTkButton(
        frame,
        text=title + f" ({len(list_ref)})",
        fg_color=color,
        hover_color=color,
        command=lambda: toggle_content(content)
    )
    header.pack(fill="x")

    content = ctk.CTkTextbox(frame, height=150)
    content.configure(state="disabled")
    content.pack(fill="both", expand=True)

    last_len = {"count": 0}  # keep track of how many lines we already printed

    def update_content():
        current_len = len(list_ref)
        if current_len > last_len["count"]:
            new_items = list_ref[last_len["count"]:]  # get only new entries
            content.configure(state="normal")
            for item in new_items:
                content.insert("end", item + "\n")
            content.configure(state="disabled")

            # Auto-scroll only if the user is already at the bottom
            if float(content.yview()[1]) == 1.0:
                content.see("end")

            last_len["count"] = current_len

            header.configure(text=title + f" ({current_len})")

        # Schedule next update
        frame.after(1000, update_content)

    def toggle_content(widget):
        if widget.winfo_ismapped():
            widget.pack_forget()
        else:
            widget.pack(fill="both", expand=True)

    update_content()
    return frame

  # Create sections
  info_section = create_section(root, "INFO", webui_info, "#007F7F")      # cyan
  warn_section = create_section(root, "WARNINGS", webuiwarnings, "#7F6B00")  # yellow
  error_section = create_section(root, "ERRORS", webuierrors, "#7F2200")  # red

  info_section.pack(fill="x", padx=10, pady=5)
  warn_section.pack(fill="x", padx=10, pady=5)
  error_section.pack(fill="x", padx=10, pady=5)
  root.mainloop()
 except Exception as e:
   print(f"ui log error {e}")
  # Start simulation in background thread
threading.Thread(target=infogui, daemon=True).start()


# ---------------- Dashboard thread ----------------
def dashboard_thread():
    global show_info, show_warnings, show_errors
    with Live(build_dashboard(), refresh_per_second=2, screen=False) as live:
        while True:
            
            live.update(build_dashboard())
            time.sleep(0.5)  # update more frequently for smooth toggling

# ---------------- Key listener thread for collapsible toggles ----------------
def toggle_thread():
    global show_info, show_warnings, show_errors
    try:
        import msvcrt  # Windows
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getwch().lower()
                if key == "i":
                    show_info = not show_info
                elif key == "w":
                    show_warnings = not show_warnings
                elif key == "e":
                    show_errors = not show_errors
            time.sleep(0.1)
    except ImportError:
        pass  # Non-Windows: could add getch alternative

# ---------------- Start dashboard and toggle threads ---------------- 

threading.Thread(target=dashboard_thread, daemon=True).start()
threading.Thread(target=toggle_thread, daemon=True).start()


console.show_cursor() #prevent hiding cursor in console when closed



    
def newuser(uniqid):
        # Simulate adding to a list of active sessions
     # In a real app, this would be a database interaction
     global VALID_SERVER_SESSION_IDS
     if uniqid not in VALID_SERVER_SESSION_IDS:
         VALID_SERVER_SESSION_IDS.add(uniqid)
         return "success"
     return "unsuccessfull"


# Helper function to check authentication

def is_authenticated():
    """
    Checks if the current Flask session is authenticated and valid.
    """
    # 1. Check if 'unique_browser_id' exists in the Flask session (from the cookie)
    # 2. Check if that ID is present in our server's list of valid active sessions
    return 'unique_browser_id' in session and session['unique_browser_id'] in VALID_SERVER_SESSION_IDS



#videostream
cursorhold = ""
streaming = [True]

def get_cursor():
    try:
        
        # cursor settings
        if not settings("usecursor") == "yes":
          return False  
      
        hcursor = win32gui.GetCursorInfo()[1]
        if hcursor == 0: # No cursor visible or error
            return False

        # It's safer to get icon info before potentially destroying the cursor handle elsewhere
        # or if the handle becomes invalid.
        try:
            icon_info = win32gui.GetIconInfo(hcursor)
            hotspot = icon_info[1:3] # (x, y)
            # Remember to destroy these new handles if they are created:
            if icon_info[3]: # hbmMask
                win32gui.DeleteObject(icon_info[3])
            if icon_info[4]: # hbmColor
                win32gui.DeleteObject(icon_info[4])
        except win32gui.error: # If GetIconInfo fails for some reason
            # Attempt to clean up the cursor handle we got if GetIconInfo failed
            try:
                win32gui.DestroyIcon(hcursor) 
            except win32gui.error: # If it's already invalid or destroyed
                pass
            return False


        hdc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))
        hbmp = win32ui.CreateBitmap()
        # Standard cursor size, adjust if needed. Consider getting actual cursor dimensions.
        # For simplicity, 36x36 is a common max.
        hbmp.CreateCompatibleBitmap(hdc, 36, 36) 
        mem_dc = hdc.CreateCompatibleDC() 
        
        old_bmp = mem_dc.SelectObject(hbmp) # Store the old bitmap to select it back
        mem_dc.DrawIcon((0,0), hcursor)
        mem_dc.SelectObject(old_bmp) # Deselect hbmp by selecting the old one back

        bmpinfo = hbmp.GetInfo()
        bmpstr = hbmp.GetBitmapBits(True)
        
        if bmpinfo['bmWidth'] == 0 or bmpinfo['bmHeight'] == 0:
            try:
                win32gui.DestroyIcon(hcursor)
            except win32gui.error: pass
            win32gui.DeleteObject(hbmp.GetHandle())
            mem_dc.DeleteDC()
            hdc.DeleteDC() 
            return False

        cursor_img = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1).convert("RGBA")

        # Clean up GDI objects
        try:
            win32gui.DestroyIcon(hcursor) 
        except win32gui.error: pass # It might have been destroyed if GetIconInfo failed and then DestroyIcon was called
        win32gui.DeleteObject(hbmp.GetHandle()) 
        mem_dc.DeleteDC() 
        hdc.DeleteDC() 

        pixdata = cursor_img.load()
        width, height = cursor_img.size
        for y in range(height):
            for x in range(width):
                if pixdata[x, y] == (0, 0, 0, 255): # Making black opaque parts transparent
                    pixdata[x, y] = (0, 0, 0, 0)
        
        return (cursor_img, hotspot)
    except Exception as e:
        # print(f"Error in get_cursor: {e}") # Good for debugging
        # Attempt to clean up resources if an error occurs mid-function
        # This is a best-effort cleanup. Using try/finally for each resource is more robust.
        if 'hcursor' in locals() and hcursor:
            try: win32gui.DestroyIcon(hcursor)
            except: pass
        if 'hbmp' in locals() and hbmp.GetHandle(): # Check if hbmp is a valid object with GetHandle
            try: win32gui.DeleteObject(hbmp.GetHandle())
            except: pass
        if 'mem_dc' in locals() and mem_dc.GetSafeHdc(): 
            try: mem_dc.DeleteDC()
            except: pass
        if 'hdc' in locals() and hdc.GetSafeHdc(): 
            try: hdc.DeleteDC()
            except: pass
        return False


resizing = [False]
def randomimage():
  try:
    ipath = os.path.join(resource_path,"filler")
    allowedimages = [".png",".jpg",".gif",".jpeg",".jfif",".svg",".apng",".ico",".pjp"]
    imgs = []
    for p in os.listdir(ipath):
      full = os.path.join(resource_path,"filler",p)
      sufx = Path(full).suffix
      if sufx.lower() in allowedimages and os.path.isfile(full):
          imgs.append(full)   
    if imgs:
        #pick one randomly
        pick = random.choice(imgs)
        imgs.clear()
        return pick
    else:
      print("Cannot find a capable filler image")
      os._exit(5)
  except:
      print("Fatal error: Cannot load filler image\nCheck if the filler directory is available in the surtr resources dorectory\nCheck if you have permission to the filler image path")     
      os._exit(5)  
        
        
         
#fillerimagepath = os.path.join(resource_path,"filler","framefiller.png")  # path to your PNG file
fillerimagepath = randomimage()
try:
    if not os.path.exists(fillerimagepath):
            print("Cannot find filler image")
            os._exit(5)
            
    with open(fillerimagepath, "rb") as f:
      frame_bytes = f.read()
    #print ("filler image loaded")
    showlog("info", "filler image loaded")
except:
    #print("Error loading filler image")
    showlog("info", "Error loading filler image")
    
def generate_frames(check = False):
  global cursorhold,frame_bytes  
  # screen settings
  if settings("usescreen") == "no" and check == True:
      return
  
    
    # Initialize mss outside the loop for efficiency
    
  with mss.mss() as sct:
        # Get monitor data (assuming primary monitor)
        monitor = sct.monitors[1] # 0 is all monitors, 1 is the primary
        
        while True:
          try:
              
            if streaming[0] == False: #if the user pauses streaming show the frame filler instead
                yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                continue
            
            #cursor_data = get_cursor() 
            cursor_data = cursorhold
            if cursor_data:
                cursor_img, (hotspotx, hotspoty) = cursor_data
            else:
                cursor_img = None
                hotspotx, hotspoty = 0, 0 # Default if no cursor

            try:
                ctypes.windll.shcore.SetProcessDpiAwareness(2) 
                ratio = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100.0
            except (AttributeError, OSError):
                try:
                    hdc_main = win32gui.GetDC(0)
                    dpi_x = win32ui.GetDeviceCaps(hdc_main, win32con.LOGPIXELSX) # Using win32ui for GetDeviceCaps
                    win32gui.ReleaseDC(0, hdc_main)
                    ratio = dpi_x / 96.0 
                except Exception: # Catch specific exceptions if possible
                    ratio = 1.0 


            # --- Start of MSS specific code ---
            sct_img = sct.grab(monitor)
            
            # Corrected line: Interpret sct_img.rgb as 'RGB'
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb, 'raw', 'RGB')
            # --- End of MSS specific code ---
            # Define your target resolution (e.g., 1280x720 is a common HD resolution, or 800x600 for a very fast test)
            # target_width = 1280
            # target_height = 720
            
            #width and height resolution settings
            if not settings("resolution") == "normal":
              target_width = int(settings("resolution").split("x")[0])
              target_height = int(settings("resolution").split("x")[1])
              # You might want to calculate aspect ratio to maintain proportions:
              current_aspect_ratio = img.width / img.height
              if img.width > target_width or img.height > target_height:
                
                resizing[0] = True
                #leave aspect ratio calculation for now
                
                #if img.width / img.height > target_width / target_height:
                #     new_width = target_width
                #     new_height = int(target_width / current_aspect_ratio)
                #else:
                #     new_height = target_height
                #     new_width = int(target_height * current_aspect_ratio)
                #     img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS) # Use LANCZOS for good quality downscaling
            
            pos_win = win32gui.GetCursorPos()
            
            physical_cursor_x = round(pos_win[0] * ratio)
            physical_cursor_y = round(pos_win[1] * ratio)
            
            paste_hotspotx = hotspotx if cursor_img else 0
            paste_hotspoty = hotspoty if cursor_img else 0

            pos = (physical_cursor_x - paste_hotspotx, 
                   physical_cursor_y - paste_hotspoty)
            #calculate new cursor position if the image resize
            if (resizing[0] == True):
              
              screenwidth = int(GetSystemMetrics(0))
              screenheight =int(GetSystemMetrics(1))
              #calculate the new posithon of cursor
            
              x = round(pos[0] * (target_width / screenwidth))
              y = round(pos[1] * (target_height / screenheight))
              pos = (x,y)
            
            
            
            if cursor_img: 
                if cursor_img.mode != 'RGBA':
                    cursor_img = cursor_img.convert('RGBA')
                # Ensure paste position is within image bounds, though PIL handles this gracefully usually
                img.paste(cursor_img, pos, cursor_img) 

            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG', quality=90) # Increased quality slightly
            img.save(img_byte_arr, format='JPEG', quality=int(settings("framequality"))) # Increased quality slightly
            img_byte_arr = img_byte_arr.getvalue()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + img_byte_arr + b'\r\n')
            
          except Exception as e:
               yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
               #print(f"Cannot send frames for the moment {e} waiting 1 sec...")
               showlog("info", f"Cannot send frames for the moment {e} waiting 1 sec...")
               time.sleep(1)
               continue





# --- Global Audio Queue ---
audio_queue = queue.Queue()


# --- Global variables for audio format (ensure these are initialized) ---
actual_audio_channels = 0
actual_audio_sample_rate = 0
actual_audio_bits_per_sample = 0
audio_queue = queue.Queue(maxsize=100) # Added maxsize to prevent unbounded growth

# load filler audio
filler_audio_path = os.path.join(resource_path,"filler","sound","filler.wav")
try:
   with open(filler_audio_path, 'rb') as f:
     filler_audio_data = f.read()
     #print(f"Loaded filler audio from: {filler_audio_path}")
     showlog("info", f"Loaded filler audio from: {filler_audio_path}")
except FileNotFoundError:
    print(f"Error: Filler audio file not found at {filler_audio_path}. Please check the path.")
    sys.exit(1)
except Exception as e:
    print(f"Error loading filler audio: {e}")
    sys.exit(1)


def audio_capture_worker():
    
    # audio settings
    if not settings("useaudio") == "yes":
        return
    
    global actual_audio_channels, actual_audio_sample_rate, actual_audio_bits_per_sample


    p = None
    stream = None

    try:
        p = pyaudio.PyAudio()

        # Find the default WASAPI loopback device
        try:
            #use settings to get default loopback
            if settings("defaultloopback") == "yes":
               loopback_device_info = p.get_default_wasapi_loopback()
            else:
                if not settings("chosenloopbackid") == "":
                 loopback_device_info = p.get_wasapi_loopback_analogue_by_index(int(settings("chosenloopbackid")))
                else:
                    #print("No audio loopback selected switching to default")
                    showlog("info", f"audio loopback selected switching to default")
                    loopback_device_info = p.get_default_wasapi_loopback()
        except AttributeError:
            showlog("error", "ERROR: Default wasapi not available")
            return
        except Exception as e_wasapi:
            showlog("error", f"Error getting WASAPI loopback device: {e_wasapi}")
            return


        if not loopback_device_info:
            showlog("warning", "No WASAPI loopback device found. Please ensure an audio output device is active and selected.")
            # print("Available devices:")
            # for i in range(p.get_device_count()):
            #     try:
            #         info = p.get_device_info_by_index(i)
            #         print(f"  ID {info['index']}: {info['name']} (Input: {info['maxInputChannels']}, Output: {info['maxOutputChannels']})")
            #     except Exception as e_dev_info:
            #         print(f"  Could not get info for device index {i}: {e_dev_info}")
            # return
            showlog("info", f"Open the surtr webui settings and select a capable audio loopback device to use")
            return
        channels_to_use = loopback_device_info.get('maxInputChannels')
        if channels_to_use is None or channels_to_use == 0:
            showlog("warning", f"Warning: maxInputChannels not found or is 0 for loopback device '{loopback_device_info['name']}'. Defaulting to 2 channels.")
            channels_to_use = 2 # Default to stereo

        rate_to_use = int(loopback_device_info.get('defaultSampleRate', 44100))
        format_to_use = pyaudio.paInt16 # Common format for WASAPI loopback

        actual_audio_channels = channels_to_use
        actual_audio_sample_rate = rate_to_use
        actual_audio_bits_per_sample = pyaudio.get_sample_size(format_to_use) * 8

        showlog("info", f"Audio capture will use device: {loopback_device_info['name']}")
        showlog("info", f"Capture format: Channels={actual_audio_channels}, SampleRate={actual_audio_sample_rate}, BitsPerSample={actual_audio_bits_per_sample}")

        stream = p.open(format=format_to_use,
                        channels=actual_audio_channels,
                        rate=actual_audio_sample_rate,
                        input=True,
                        input_device_index=loopback_device_info['index'],
                        frames_per_buffer=1024) # pyaudio.paFramesPerBufferUnspecified can also be used

        showlog("info", f"Audio stream opened successfully. Starting capture")

        while not stop_event.is_set():
            try:
                # Read a chunk of audio data
                data = stream.read(1024, exception_on_overflow=False)
                audio_queue.put(data, timeout=0.1) # Add timeout to put to prevent indefinite block if queue is full
                #audio_queue.put(data)
            except queue.Full:
                #print("Audio queue is full, dropping a frame. Consumer might be slow.")
                # Optionally, clear a very old item if queue remains full:
                # try: audio_queue.get_nowait() except queue.Empty: pass
                continue # Skip this frame and try to read next
            except IOError as e:
                if e.errno == pyaudio.paInputOverflowed:
                    showlog("warning", "Audio input overflowed, data lost.")
                else:
                    showlog("error", f"IOError during audio read: {e}")
                    break # Exit loop on other IOErrors
            except Exception as e_loop:
                showlog("error", f"Error in audio capture loop: {e_loop}")
                break # Exit loop on other errors

            # time.sleep(0.001) # This sleep might be too short or unnecessary if read() blocks appropriately

    except Exception as e:
        showlog("error", f"Error in audio_capture_worker setup: {e}")
        #import traceback
        #traceback.print_exc()
        #if p and hasattr(p, 'get_last_error_text') and p.get_last_error_text(): # PyAudio specific error
        #     print(f"error: {p.get_last_error_text()}")
        #elif p and hasattr(p, 'get_last_error') and p.get_last_error(): # Older PyAudio
        #     print(f"error code: {p.get_last_error()}")


    finally:
        if stream and stream.is_active():
            print("Stopping audio stream...")
            stream.stop_stream()
            stream.close()
        if p:
            #print("Terminating PyAudio instance...")
            print("Terminating Audio Instance...")
            p.terminate()
        print("Audio capture terminated.")

def generate_audio_stream(check=False):
    # Wait briefly for actual format to be set by the worker thread
    # This is a simple way; a more robust way would use an event or condition.
    
  # audio settings
  if not settings("useaudio") == "yes" and check == True:
          return False 
  # Load the filler audio data once   


  if streaming[0] == True:
    init_wait_time = 0
    max_wait_time = 5 # seconds
    while actual_audio_channels == 0 and init_wait_time < max_wait_time:
        showlog("info", f"Waiting for audio format to be initialized...")
        time.sleep(0.5)
        init_wait_time += 0.5

    channels = actual_audio_channels
    sample_rate = actual_audio_sample_rate
    bits_per_sample = actual_audio_bits_per_sample
    
    if channels == 0 or sample_rate == 0 or bits_per_sample == 0:
        showlog("info", f"Audio format not initialized, using defaults for header.")
        channels = 2
        sample_rate = 44100
        bits_per_sample = 16 # Common default

    sample_width_bytes = bits_per_sample // 8
    
    # --- WAV Header for Streaming ---
    # For streaming, set ChunkSize and Subchunk2Size to a large value (0xFFFFFFFF)
    # or a very large theoretical max if your player needs something concrete but large.
    # 0xFFFFFFFF is often interpreted as "unknown/streaming size".
    max_size_placeholder = (2**32 - 1).to_bytes(4, 'little') # 0xFFFFFFFF

    # RIFF header (12 bytes)
    header = b'RIFF'
    header += max_size_placeholder # ChunkSize (overall file size - 8 bytes)
    header += b'WAVE'
    
    # FMT sub-chunk (24 bytes)
    header += b'fmt ' # Subchunk1ID
    header += (16).to_bytes(4, 'little') # Subchunk1Size (16 for PCM)
    header += (1).to_bytes(2, 'little') # AudioFormat (1 for PCM)
    header += channels.to_bytes(2, 'little') # NumChannels
    header += sample_rate.to_bytes(4, 'little') # SampleRate
    header += (sample_rate * channels * sample_width_bytes).to_bytes(4, 'little') # ByteRate
    header += (channels * sample_width_bytes).to_bytes(2, 'little') # BlockAlign
    header += bits_per_sample.to_bytes(2, 'little') # BitsPerSample
    
    # DATA sub-chunk header (8 bytes)
    header += b'data' # Subchunk2ID
    header += max_size_placeholder # Subchunk2Size (data size)
    
    yield header
    #print(f"Sent WAV header for {channels}ch, {sample_rate}Hz, {bits_per_sample}bps audio stream.")

    while True:
        try:
            if streaming[0] == False:
               yield filler_audio_data  #if the user pauses desktop streamind show filler audio
               continue   
           
            chunk_data = audio_queue.get(timeout=1.0) # Increased timeout slightly
            if chunk_data is None: # Sentinel value to stop stream
                #print("No audio chunk data recieved, stopping audio stream generation.")
                showlog("warning", "No audio chunk data recieved, stopping audio stream generation.")
                break
            yield chunk_data
        except queue.Empty:
            # Yield the loaded filler audio data
            yield filler_audio_data
            # We don't need a print statement here, as it would be very frequent.
            # The loop will continue to yield filler_audio_data until the queue is no longer empty.
            # Check if capture thread is alive
            if not audio_capture_thread.is_alive() and audio_queue.empty():
                #print("Audio capture thread is no longer alive and queue is empty. Stopping stream.")
                #print("No audio left to fetch. Stopping stream.")
                showlog("warning", "No audio left to fetch. Stopping stream.")
                break
            continue # Continue to try getting from queue
        except Exception as e:
            #print(f"Error in audio stream generation: {e}")
            showlog("error", f"Error in audio stream generation: {e}")
            break
    showlog("info", f"Audio stream generation finished.")


def cursorstatus():
  global cursorhold
  while not stop_event.is_set():
    time.sleep(0.1)
    cursorhold = get_cursor()
  
  
"""     
init(autoreset=True)
print(Fore.RED + "THIS IS")
print(Back.GREEN + "THIS IS")
print(Style.DIM + "THIS IS")
print(Fore.RED + "THIS IS")
""" 
def webui_path(relative_path):
    """ Get absolute path to resource, works for dev and for Nuitka """
    if getattr(sys, 'frozen', False):
        # The application is frozen (compiled with Nuitka)
        # sys.executable is the path to the .exe
        base_path = os.path.dirname(sys.executable)
    else:
        # The application is running as a normal .py script
        # __file__ is the path to the script
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)

class SurtrShell:
    
    def __init__(self, exe_path="cmd.exe"):
        # Start Surtr safely
        try:
            # keep cmd open (/K) and quiet (/Q) to reduce echo noise
            
            envmnt = os.environ.copy() #starts in system environment
            self.pty = winpty.PtyProcess.spawn(["C:\\Windows\\System32\\cmd.exe", "/K"],env=envmnt)
        except Exception as e:
            raise Exception(f"Failed to start {exe_path}: {e}")

        self.lock = threading.Lock()
        self.output_buffer = ""
        self.ready = False

        # Start reader thread
        threading.Thread(target=self._reader_thread, daemon=True).start()

        # Wait for the surtr first initial prompt
        try:
            # set prompt to a sentinel we watch for, then wait for it
            # don't use test=True here — allow normal prompt detection
            #self.pty.write("echo Hello from inside CMD\r\n")
            #for line in self.run_command(f"prompt {CMDPROMPT}"):
                
                # consume any lines produced while changing prompt
            #    pass
            
            self.pty.write(f"prompt {CMDPROMPT}\r\n")
            self.pty.write("cls\r\n")
            surtr_path = surtrconfig("surtrPath")
            wait_timeout = surtrconfig("webuiSurtrWaitTimeout")
            if not wait_timeout.isnumeric():
                print("error in wait timeout in surtr configuration file")
                time.sleep(5)
                os._exit(100)
            else:
                try:
                  tmeout = int(wait_timeout)
                except:
                  tmeout = 120
            with open(webui_path("launcher.bat"), "w") as f:
                f.write("@echo off\n")
                #f.write("echo launcher.bat is running\n")
                f.write(":: Change directory to the location\n")
                f.write('title surtr launcher\n')
                f.write(f'CD /D "{surtr_path}"\n')
                f.write(":: Start surtr.exe\n")
                f.write("start /WAIT /B surtr.exe\n")
                f.write("exit\n")
                f.close()

            try:
                with self.lock: #clear old outputs to log new ones after finished waiting for new prompts
                    self.output_buffer = ""
                self.pty.write(f'"{webui_path("launcher.bat")}"\r\n')
                    
                self._wait_for_prompt(timeout=tmeout)
            except Exception as e:
                # _wait_for_prompt already logged outputs; re-raise for upstream handling
                raise Exception(f"Error waiting for surtr prompt: {e}")    


            # run the launcher.bat (quote the path in case of spaces)
            #for line in self.run_command(f'"{webui_path("launcher.bat")}"'):
                  # optionally print/log the lines for debugging
            #print("LAUNCHER:", line)
            
            # Wait until we see the custom prompt indicating surtr ready
            
        except Exception as e:
            raise Exception(f"Error preparing surtr for new session: {e}")

        showlog("info", f"A new session has been created for new user")


    def _reader_thread(self):
      """Continuously read from PTY and append to buffer. Only treat the process as dead when isalive() is False."""
      while True:
        try:
            chunk = self.pty.read(1024)
            # normalize bytes->str if needed
            if isinstance(chunk, bytes):
                chunk = chunk.decode(errors="ignore")
            chunk = clean_output(chunk)

            # If empty chunk, check if child is alive; otherwise sleep and continue
            if not chunk:
                try:
                    alive = getattr(self.pty, "isalive", lambda: True)()
                except Exception:
                    alive = True
                if not alive:
                    with self.lock:
                        showlog("error", "PTY closed (child process died).")
                        self.ready = False
                    break
                time.sleep(0.02)
                continue

            with self.lock:
                self.output_buffer += chunk
                # Print only the new data to avoid reprinting the whole buffer
                #print(chunk, end="")

        except Exception as e:
            showlog("error", f"Pipe reader exception: {e}")
            self.ready = False
            break
        time.sleep(0.05)


    def _wait_for_prompt(self, timeout=None):
       """Wait until PROMPT appears. Always log collected output (success or failure)."""
       start = time.time()
       collected = ""
       try:
          while True:
            time.sleep(0.02)
            if timeout and (time.time() - start) > timeout:
                showlog("error", f"Timed out waiting for surtr.exe after {timeout}s.")
                raise TimeoutError("Timed out waiting for surtr prompt.")

            with self.lock:
                if self.output_buffer:
                    collected += self.output_buffer
                    self.output_buffer = ""

                    if PROMPT in collected:
                        before, after = collected.split(PROMPT, 1)
                        # put leftover after the prompt back into buffer for later reads
                        self.output_buffer = after + self.output_buffer
                        # log startup lines
                        #for ln in (l.strip() for l in before.splitlines() if l.strip()):
                        #    showlog(ln)
                        self.ready = True
                        return before

       except Exception as e:
         # On any exception, ensure we log everything we captured
         with self.lock:
            if self.output_buffer:
                self.output_buffer = ""
         showlog("error", f"waiting for surtr.exe failed: {e}")
         raise Exception(f"waiting for surtr.exe failed: {e}")
    
    def addline(self,line):
        try:
            self.pty.write(line + "\r\n")
        except Exception as e:
            showlog("error", f"Failed to add {line} to shell")
            return
        
    def run_command(self, cmd, test=False):
        """
        Send a command to surtr and yield output line by line.
        If test=True, just write the command and return (keeps behavior but avoid using it for prompt handshake).
        """
        try:
            self.pty.write(cmd  + "\r\n")
        except Exception as e:
            showlog("error", "Failed to send command: surtr is not responding")
            return

        collected = ""
        while True:
            try:
                time.sleep(0.02)
                with self.lock:
                    if test:
                        # test mode: don't wait for prompt; caller expects quick return
                        time.sleep(0.5)
                        break

                    if PROMPT in self.output_buffer:
                        chunk, self.output_buffer = self.output_buffer.split(PROMPT, 1)
                        collected += chunk
                        break
                    #elif CMDPROMPT in self.output_buffer:
                    #    showlog("error", "ERROR: surtr was terminated in a session")
                    #    self.closeshell()
                    #    return

                    else:
                        chunk = self.output_buffer
                        self.output_buffer = ""
                        collected += chunk

                # Yield complete lines
                while "\n" in collected:
                    line, collected = collected.split("\n", 1)
                    # Skip echoed command
                    if line.strip() == cmd.strip():
                        continue
                    yield line

            except Exception as e:
                showlog("error", f"Error while collecting output: {e}")
                return

        # Yield any remaining output
        remaining = collected.strip()
        if remaining and remaining != cmd.strip():
            yield remaining

    def closeshell(self):
        try:
            self.pty.close(force=True)
        except Exception:
            pass
        self.ready = False
   
        
surtrsessions = {}
    
  
@app.route('/')
def index():
     # If the user is authenticated, redirect to dashboard directly
    if is_authenticated():
           return redirect(url_for('dashboard'))

    return render_template('index.html')

newsessionhtml = """
<!doctype html>
<html>
<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Arial', sans-serif;
}
body {
    font-family: Arial, sans-serif;
    padding: 2rem;
    background: linear-gradient(120deg, #1c1f26, #2f3640);
    color: white;
    overflow: auto;
}


/* Headings */
h1, h3, h2 {
    color: #ffffff;
    text-align: center;
    margin: 1rem 0;
}
</style>
<body>
 <h1>Environment setup</h1><br>
 <p id="info" style="color:red;"></p>
     {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            <ul class="flashes">
            {% for category, message in messages %}
                <li class="{{ category }}" style="color:yellow;">{{ message }}</li>
            {% endfor %}
            </ul>
        {% endif %}
    {% endwith %}
    
<script>
let info = document.getElementById("info");

    if (sessionStorage.getItem("surtenvironmentsessionrunning") === null){
        sessionStorage.setItem("surtenvironmentsessionrunning", "running")
        const xhttp = new XMLHttpRequest();
        var recv = null
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) { 
                const contentType = xhttp.getAllResponseHeaders();
                if (contentType.includes('application/json')) {
                recv = JSON.parse(this.responseText);
                }else{
                    recv = {"url":xhttp.responseURL};
                }

                try {
                    sessionStorage.removeItem("surtenvironmentsessionrunning")
                    window.location.href = recv.url;
                } catch (err) { 
                    sessionStorage.removeItem("surtenvironmentsessionrunning")
                    console.error("JSON parsing error:", err);
                    info.textContent = "A JavaScript error occurred (parsing response)!";
                }
            } else {
                sessionStorage.removeItem("surtenvironmentsessionrunning")
            }
        };
        xhttp.open("GET", "/newsession", true);
        xhttp.send();
    
    }else{
        info.textContent = "Your session is being created please wait for a minute then reload the page";
    }


</script>  

  
</body>
</html>
"""

@app.route("/newsession")
def newsession():
  #create a surtr session for the user
  if not is_authenticated():
        flash("Please log in first", 'warning')
        return redirect(url_for('index'))
  if session['unique_browser_id'] in surtrsessions: #if user already has a session
     return redirect(url_for('dashboard')) 
 
  try:
    surtrsessions[session['unique_browser_id']] = SurtrShell()
    # Return success with dashboard URL. No need to send the ID back to JS.
    #return jsonify({"url": url_for('dashboard')}), 200
    return jsonify({"url":url_for('dashboard')}),200

  except Exception as e:
    showlog("error", f"Cannot create a session for new user {e}")
    flash("Failed to request a new session for you", 'info')
    return redirect(url_for('logout')) # remove session
    
    
    
    
@app.route('/parse',methods=['POST'])
def route():
    global loginfailed, loginsuccess,maxuser,usercount
    
    if request.method == 'POST':
      fname = request.form['name']
      fpass = request.form['password']
      if fname  != settings("username"):
          loginfailed += 1
          
          return "Username not match",401
      if fpass  != settings("password"):
          loginfailed += 1
          
          return "Password not match",401
      if usercount >= maxuser:
          loginfailed += 1
          
          return "Maximum users reached",401
       # --- Authentication Successful, now manage session ---
       
        # 1. Generate a cryptographically strong unique ID for this session
        # This replaces your random.randrange + string choices approach for security.
        # This ID will be stored in the Flask session (which goes into the signed cookie)
        # and on your server-side list of active sessions.
      session_id = secrets.token_hex(16) # 16 bytes = 32 hex characters
        
         # 2. Add this session ID to your server's trusted list
      VALID_SERVER_SESSION_IDS.add(session_id)
      session['unique_browser_id'] = session_id # Store in Flask session
      
      # 3. Regenerate the session ID to prevent session fixation attacks.
      # This invalidates any old session ID that might have been present before login.
      #session.regenerate_id()
      loginsuccess += 1
      usercount += 1
      
      
      return jsonify({"url":url_for('yourenv')}),200
    
    loginfailed += 1
    return "Method Not Allowed", 405 # For non-POST requests to /parse
      
@app.route('/yourenv')
def yourenv():
    if not is_authenticated():
      flash("Please log in first", 'warning')
      return redirect(url_for('index'))
    flash("Requesting for a new evironment", 'info')
    flash("Do not close or reload this page", 'warning')
    flash("Starting a new surtr session. please wait...", 'info') 
    return render_template_string(newsessionhtml), 200


@app.route('/dashboard')
def dashboard():
    if not is_authenticated():
        flash("You need to log in to access the dashboard.", 'warning')
        return redirect(url_for('index')) # Redirect to index (login page)
    
    return render_template('dashboard.html',configs=configs)
    

@app.route('/video_feed')
def video_feed():
    if not is_authenticated():
        # You might return a static "not authorized" video, or simply stop the stream
        # For a live feed, it's better to terminate the response.
        # Or redirect if it's a browser request.
        return "Unauthorized Access", 401
    return Response(generate_frames(check=True), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/audio_feed')
def audio_feed():
    if not is_authenticated():
        # Similar to video feed, handle unauthorized access.
        return "Unauthorized Access", 401

    """Streams the live audio feed."""
    user_ip = request.remote_addr

    # The host device IP (localhost) do not send audio if using local host to prevent the disturbing sound produced
    if user_ip == '127.0.0.1' or user_ip == '::1':
        return "AUDIO BLOCKED ON LOOPBACK", 200
    return Response(generate_audio_stream(check=True), mimetype='audio/wav')


#surtr starter starts here
PROMPT = "|=[>>> "
CMDPROMPT = "surtrwebui4cmd4prompt3776b5789f644yk7tytbot4:"

def clean_output(text):
    """
    Remove ANSI escape sequences and normalize carriage returns
    """
    text = re.sub(r'\x1B\[[0-9;?]*[A-Za-z]', '', text)
    modifiedtext = text.replace("\r", "\n")
    return modifiedtext
     

#print("wait while we start surtr")
#shell = SurtrShell("surtr.exe")
#print("Type commands (exit/quit to stop):")

''' while True:
  try:
    cmd = input("Shell2> ")
    if cmd.strip().lower() in ["exit", "quit"]:
        break
    shell.run_command(cmd)
  except KeyboardInterrupt:
      print("\nExiting...")
      break
 '''
#surtr starter stops here

@app.route('/logout')
def logout():
    global left,usercount
    # Remove the ID from the server's list of valid sessions
    isuser = False
    if session['unique_browser_id'] in surtrsessions:
       isuser = True
       try:
         currentsession = session['unique_browser_id']
         surtrsessions[currentsession].closeshell()  #terminate shell
       except Exception as e:
           pass #if it didnt work assumes surtr is already terminated
       
       surtrsessions.pop(session['unique_browser_id']) 
          
    if 'unique_browser_id' in session and session['unique_browser_id'] in VALID_SERVER_SESSION_IDS:
        isuser = True
        VALID_SERVER_SESSION_IDS.remove(session['unique_browser_id'])
        
        #print(f"User logged out. Removed {session['unique_browser_id']}. Active sessions: {VALID_SERVER_SESSION_IDS}")
    if isuser:
      left += 1
      usercount -= 1
      # Clear the Flask session for the current user
      session.clear() # Clears all data from the session
      showlog("info", "A user has left")
      flash("You have been logged out.", 'info')
    
    return redirect(url_for('index'))

audio_capture_thread = threading.Thread(target=audio_capture_worker, daemon=True)

cursorget = threading.Thread(target=cursorstatus, daemon=True)

 
# run Surtr scripts
def run_surtr_script(script_content):
    scriptname = ["Unknown"]
    try:  
      #batch settings
      if settings("usescriptbuilder") == "no":
        return {"status": "error", "message":"You do not have permission to run scripts"}
      
      filerun = f"script{random.randrange(1000000000, 900000000000)}.as"
      flejoin = os.path.join(batchfolder,filerun)
      fle = open(flejoin,"w")
      fle.write(script_content)
      fle.close()
      #full = f"surtr.exe run {flejoin}"
      #splt = full.split(" ")
      #subcmd = subprocess.check_output(full, shell=True, stderr=subprocess.STDOUT, text=True)
      showlog("info", f"script {flejoin} is running")
      scriptname[0] = flejoin
      currentsession = session['unique_browser_id']
      
      shell = surtrsessions[currentsession]
      #stream_with_context preserves Flask request/session context while the generator yields.
      #The X-Accel-Buffering: no header helps prevent nginx from buffering chunks; other proxies may need similar config.
      def generate():
         try:
            shellparse = flejoin.replace("\\","\\\\") #use double quotes for surtr shell
            fullpath = os.path.abspath(shellparse)
            runs = shell.run_command(f'run "{fullpath}"')
            for item in runs:
                text = str(item)
                # ensure newline so client receives clear line boundaries
                if not text.endswith("\n"):
                    text += "\n"
                yield text
                # tiny sleep to yield CPU, optional
                # time.sleep(0.005)
         except Exception as e:
            showlog("error", f"cli stream error: {e}")
            yield f"cli stream error: {e}\n"
            
      showlog("info", f"script {flejoin} is terminated")
      headers = {"X-Accel-Buffering": "no"}  # helps nginx not to buffer
      return Response(stream_with_context(generate()), mimetype='text/plain; charset=utf-8', headers=headers)


      #return {"status": "success", "message": f"{result}"}
  
    except Exception as e:
       showlog("info", f"A script has been terminated because of an error scriptname:{scriptname[0]}")
       showlog("error", e)
       return {"status": "error", "message": str(e)}
   
@app.route("/script_builder", methods=["GET", "POST"])

def script_builder():
    if not is_authenticated():
        flash("You need to log in to use script builder.", 'warning')
        return redirect(url_for('index')) # Redirect to index (login page)
    
    if settings("usescriptbuilder") == "no":
        return jsonify({"status": "error", "message": "You do not have permission to use script builder"}), 500
    if request.method == "GET":
        return render_template("script_builder.html", configs=configs)
    elif request.method == "POST":
        script_content = request.json.get("script")
        if not script_content:
            return jsonify({"status": "error", "message": "No script provided"}), 400
        return run_surtr_script(script_content)


@app.route('/run', methods=['POST'])

def run_terminal():
    #command settings
    if not is_authenticated():
       result = "You are not allowed,login first"
       return jsonify({"output": result})
    
    if settings("usecommand") == "no":
        result = "You dont have permission to run commands"
        return jsonify({"output": result})
    
    data = request.get_json()
    command = data.get('command')
    if command == "":
      result = "surtr |=[>>> "
      return jsonify({"output": result})
    else:   
      try:
        #result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        #result = subprocess.check_output(f"surtr.exe {command}", shell=True, stderr=subprocess.STDOUT, text=True)
        #if command.strip().lower() in ["exit", "quit"]:
        #    break
           #execute with the user current session
        showlog("info", f"command {command} is being executed")
        currentsession = session['unique_browser_id']
        #runs = surtrsessions[currentsession].run_command(f"webui {command}")
        #result = "\n".join(runs) 
        #showlog(f"command {command} has ended")
        

        shell = surtrsessions[currentsession]
        #stream_with_context preserves Flask request/session context while the generator yields.
        #The X-Accel-Buffering: no header helps prevent nginx from buffering chunks; other proxies may need similar config.
        def generate():
         try:
            runs = shell.run_command(f"webui {command}")
            for item in runs:
                text = str(item)
                # ensure newline so client receives clear line boundaries
                if not text.endswith("\n"):
                    text += "\n"
                yield text
                # tiny sleep to yield CPU, optional
                # time.sleep(0.005)
         except Exception as e:
            showlog("error", f"cli stream error: {e}")
            yield f"cli stream error: {e}\n"
            
        showlog("info", f"command ended")
        headers = {"X-Accel-Buffering": "no"}  # helps nginx not to buffer
        return Response(stream_with_context(generate()), mimetype='text/plain; charset=utf-8', headers=headers)

      except Exception as e:
        showlog("info", f"command {command} has ended because of an error")
        showlog("error", e)
        result = "Something went wrong"
        return jsonify({"output": result})



@app.route('/addline', methods=['POST'])
def add_cli_line():
    #command settings
    if not is_authenticated():
       return 
    
    if settings("usecommand") == "no":
        return
    if request.method != 'POST':
        return
    fline = request.form['line']
    currentsession = session['unique_browser_id']
    shell = surtrsessions[currentsession]
    shell.addline(fline)
    
    
    
# ========================
# SYSTEM TRAY
# ========================
def create_system_tray():
    """Create system tray icon for easy control"""
    from pystray import Icon, Menu, MenuItem
    from PIL import Image, ImageDraw
    
    # Create blank image for icon
    image = Image.new('RGB', (64, 64), 'white')
    dc = ImageDraw.Draw(image)
    dc.rectangle([16, 16,50, 50], fill='blue')
    dc.rectangle([16, 16, 40, 40], fill='white')
    dc.rectangle([16, 16, 30, 30], fill='blue')
    dc.rectangle([16, 16, 20, 20], fill='white')
    dc.rectangle([16, 16, 18, 18], fill='blue')
    
    def start_stream(icon, item):
       showlog("info", "Streaming resumed")
       streaming[0] = True
        
    def stop_stream(icon, item):
        showlog("info", "Streaming paused")
        streaming[0] = False
     
    def showgui(icon, item):
        global root
        if root != None:
            root.deiconify() #show window
    
    def hide_console_window(icon, item):
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
           ctypes.windll.user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE

    def show_console_window(icon, item):
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        if hwnd:
            ctypes.windll.user32.ShowWindow(hwnd, 1)  # 1 = SW_SHOWNORMAL

    def exit_app(icon, item):
        global system_running
        stop_event.set()
        system_running = False
        icon.stop()
        time.sleep(2)
        os._exit(0)
           
    menu = Menu(
        MenuItem("Hide Webui Shell Window", hide_console_window),
        MenuItem("Show Webui Shell Window", show_console_window),
        MenuItem('Pause Desktop Stream', stop_stream),
        MenuItem('Resume Desktop Stream', start_stream),
        MenuItem('Show logs Window', showgui),
        MenuItem('Exit', exit_app)
    )
    
    icon = Icon('Surtr webui', image, menu=menu)
    icon.run()

tray = threading.Thread(target=create_system_tray, daemon=True)

#for files
    
BASE_DIR = os.path.normpath('static/files')

@app.route('/browse', methods=['GET'])
def browse():
    
    #file settings
    if not is_authenticated():
       result = "You are not allowed,login first"
       return jsonify({"error": result})
    
    if settings("usefile") == "no":
        return jsonify({"error": "You do not have permission to see files"}), 500
    
    path = request.args.get("path", BASE_DIR)
    path = os.path.abspath(path)

    #if not path.startswith(BASE_DIR):
    #   return jsonify({"error": "Access denied"}), 403

    if not os.path.exists(path):
        return jsonify({"error": "Path not found"}), 404
    
    if not settings("blockedfolder") == "":
      if ";" in settings("blockedfolder") == False:
          return jsonify({"error": "CONFIGURATION ERROR NO ; IN BLOCKEDFOLDER DATA"}), 500
      
      chk = settings("blockedfolder").split(";")
      
      for i in chk:
          if i == "":
              chk.remove(i)
      
      for f in chk:
        mod_i = os.path.abspath(f.strip())
        #print(f"path={path} and blck={mod_i}")
        #print(path.startswith(mod_i) or mod_i == path)
        if path.startswith(mod_i):
           #print(f"entered now path={path} and blck={mod_i}")
           #return jsonify({"error": "ACCESS DENIED"}), 403
           #flash(f"{path} \n ACCESS DENIED!.", 'error')
           showlog("info", f"A user file browser tab has been blocked when trying to access a restricted path pathname:{path}")
           return jsonify({"error": f"THIS PATH {path} IS RESTRICTED"}), 500
    
    items = []
    try:
        for entry in os.scandir(path):
            items.append({
                "name": entry.name,
                "path": entry.path,
                "is_dir": entry.is_dir()
            })
        return jsonify({"current_path": path, "items": items})
    except Exception as e:
        showlog("error", e)
        
        return jsonify({"error": str(e)}), 500
        
@app.route('/download')
def download():
    if not is_authenticated():
       result = "You are not allowed,login first"
       return jsonify({"output": result})
    
    #file settings
    if settings("usefile") == "no":
        return "You do not have permission to download files",500
    
    path = request.args.get('path')
    if not path:
        return "Invalid file", 400

    path = os.path.abspath(path)
    #if not path.startswith(BASE_DIR) or not os.path.isfile(path):
    if not os.path.isfile(path):
        return "Invalid file", 404

    directory = os.path.dirname(path)
    filename = os.path.basename(path)
    return send_from_directory(directory, filename, as_attachment=True)

#to ping connection
@app.route("/ping")
def ping():
    return "ok", 200
    
def start_webgui(host='127.0.0.1', port=4444):
    global system_running
    print(f"Starting Web GUI at http://{host}:{port}")
    showlog("info", f"Starting server")
    cursorget.start()
    audio_capture_thread.start()
    tray.start()
    #for screen recording
    #startrecord()
    
    # ignore all warnings
    warnings.filterwarnings("ignore")
    
    # Disable Flask debug messages
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)  # only errors, no warnings/info

    # Disable Waitress logging
    waitress_log = logging.getLogger('waitress')
    waitress_log.setLevel(logging.ERROR)
    
    
    #app.run(host=host, port=port,debug=True)
    try:
       system_running = True 
       serve(app, host=host, port=port, threads=8)
    except Exception as e:
       system_running = False 
       showlog("error", f"Error: cannot start server {e}")
       
if __name__ == "__main__":
    if len(sys.argv) == 1:
      start_webgui()  
    elif len(sys.argv) >= 5 and sys.argv[1] == "start" and sys.argv[2] == "webui":
        host = sys.argv[3]
        port = int(sys.argv[4])
        
        if "-savelogs" in sys.argv: 
           try:
             ind =  sys.argv.index("-savelogs") + 1
             SAVE_LOGS = sys.argv[ind]
           except:
               print(f"Unsupported syntax")
               sys.exit(100)  
               
        
        for usr in sys.argv:
           try:
             if usr.startswith("maxuser:"):
                 usrsp= usr.strip().split(":")
                 if usrsp[0] == "maxuser":
                     maxuser = int(usrsp[1])
                     showlog("info", f"Maximum user updated ({maxuser})")
                     break
           except:
               print(f"Unsupported syntax")
               sys.exit(100)  
        
        
        start_webgui(host, port)
    else:
        print("Usage: start webui <host> <port>")
