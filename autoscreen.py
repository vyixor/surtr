# -- coding: utf-8 -- 
# IMPORTS ORGANIZED BY PACKAGE SIZE (LARGEST TO SMALLEST)


import numpy
import cv2

# Medium packages (~50MB)
from PIL import Image, ImageGrab, ImageDraw  # Pillow - image processing

import customtkinter
import tkinter
from tkinter import *
from PIL import Image, ImageTk


# Small-medium packages (~10MB)
from sympy import sympify  # SymPy - symbolic math
from win32api import GetSystemMetrics  # PyWin32
from win32com.client import Dispatch
import pythoncom
import win32gui
import win32con

# Small packages (~1-3MB)
from watchdog.observers import Observer  # File system monitoring
from watchdog.events import FileSystemEventHandler
import psutil  # System utilities
from pynput.mouse import Controller  # Input control
import mss  # Multi-screen screenshot
import mss.tools
import pyperclip  # Clipboard

# Tiny packages & standard library
from colorama import init, Fore, Back, Style  # Terminal colors
import os
import re
import datetime as dt
import time
from pathlib import Path
import sys
from itertools import cycle  # for encryption of variables
import subprocess
import hashlib
import threading
import pygetwindow as gw
import shlex
import traceback
import json
import math
import credloader
import os
import time
import sys
import _tkinter
from tkinter import PhotoImage
from credloader import *
import platform
import socket
import getpass
import shutil
import getpass  # duplicate removed
import ctypes
from pystray import Icon, Menu, MenuItem
import random
import recorder
from typing import Union, Optional
import os
import types
import pyautogui as pyg
import pyscreeze


# Custom modules
import surtr_ocr
import surtr_request as srequest
#import activationlicence as vlicence
#import updater


#global error catcher (catches any error not handled by try catch)
def global_exception_handler(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Let Ctrl+C behave normally
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    #print(f"Uncaught Exception: {exc_type.__name__}: {exc_value}")
    print(f"Unknown error: {exc_type.__name__}: {exc_value}")

# Activate the global error catcher hook
sys.excepthook = global_exception_handler




# ctrl+c error catcher
# stops the script without errors when the ctrl+c is hit on the keyboard (for clean exit)
import signal
# Global stop flag
stop_event = threading.Event()
def handle_sigint(signum, frame):
    print("\nCleaning up please wait...")
    stop_event.set()       # Tell threads to stop
    time.sleep(0.3)        # Optional: Let threads wind down
    print("Closing...")
    #sys.exit(0)            # Exit silently without traceback
    os._exit(0)   #forcefully closes everything at once without warning or exceptions
        
# Register the signal handler

signal.signal(signal.SIGINT, handle_sigint)



#set surtr shell title window
APP_TITLE = "Surtr Automation Shell"
ctypes.windll.kernel32.SetConsoleTitleW(APP_TITLE)

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



# with open('file.txt', 'r') as f:
#     for line in f:
#         words = shlex.split(line)
#         for word in words:
#             print(word)
            
''' init(autoreset=True)
print(Fore.RED + "THIS IS")
print(Back.GREEN + "THIS IS")
print(Style.DIM + "THIS IS")
print(Fore.RED + "THIS IS") '''
# check for resources folder first (only for windows)
if(os.path.exists(os.path.normpath("resources")) and os.path.isdir(os.path.normpath("resources"))):
    resource_path = os.path.normpath("resources")  
elif (os.path.exists(os.path.normpath("C:\\Surtr\\surtr\\resources")) and os.path.isdir(os.path.normpath("C:\\Surtr\\surtr\\resources"))):
    resource_path = os.path.normpath("C:\\Surtr\\surtr\\resources")
else:
    print("cannot find 'resources' folder")  
    print(f"if you have it put it in (C:\\Surtr\\surtr\\resources) then start surtr")
    print("Closing after 10 seconds")
    time.sleep(10)
    sys.exit(1)
    
# FOR FULL WORKING IN ALL OPERATING SYSTEMS 
    
# to make sure my app detects all the required files and folders
# This will point to the location of the executable or the script
app_dir = os.path.dirname(sys.executable)

# For development mode (not compiled), fallback
if not getattr(sys, 'frozen', False):
    app_dir = os.path.dirname(os.path.abspath(__file__))

    
# Define all resource paths for all (FULL FUNCTIONALITY IN ALL OS)
# this will be used later for flexibleness in all os version like linux,ubutun,windows,androids and so on
# UNCOMMENT THIS IF YOU WANT IT TO RUN IN ALL OS 
#resource_path = os.path.join(app_dir, 'resources')
sysvars_path = os.path.join(resource_path, 'sysvars.sv')
surtr_modules = os.path.join(resource_path, 'modules')
process_path = os.path.join(resource_path, 'process')
desktop_path = os.path.join(process_path, 'desktop.png')
desktoprize_path = os.path.join(process_path, 'desktoprize.png')
imgedit_path = os.path.join(process_path,"imgedit.png")
readlogs_path = os.path.join(process_path, 'readlogs.tmp')
ocr_path = os.path.join(resource_path, 'OcR', 'tesseract.exe')
icons_path = os.path.join(resource_path, 'icons', 'icon.ico')
sbotpng_path = os.path.join(resource_path, 'icons', 'surt.png')
crefile = os.path.join(resource_path,"process","cred","awpdfs.sts")
configfile = os.path.join(resource_path,"surtrconfig.conf")
commandfile = os.path.join(resource_path,"entries.sts")
updatefile = os.path.join(resource_path,"updates","updatecheck.json")


#Surtr scurity manager file SSM
ssm_path = os.path.join(resource_path,"process","cred","SSM.pct")
''' 
# Create necessary directories if they don't exist
os.makedirs(process_path, exist_ok=True)
os.makedirs(os.path.dirname(ocr_path), exist_ok=True)
os.makedirs(os.path.dirname(icons_path), exist_ok=True)

'''

    
# Global settings (you can override these in your main script if needed)
pyg.FAILSAFE = False
pyscreeze.USE_IMAGE_NOT_FOUND_EXCEPTION = True




# FOR GUIS SETTINGS
def suppress_customtkinter_errors(exc_type, exc_value, traceback):
        if isinstance(exc_value, _tkinter.TclError) and "invalid command name" in str(exc_value):
           return  # Suppress the harmless TclError
        sys.__excepthook__(exc_type, exc_value, traceback)

try:
  app = customtkinter.CTk()
  pi = PhotoImage(file=sbotpng_path)
  app.iconphoto(True,pi)
  app.withdraw()  # Hide the main root window

except Exception as e:
  print(f"Surtr cannot start because of missing or corrupted files")
  print("Closing after 10 seconds")
  time.sleep(10)
  os._exit(1)


#GATEWAYS TO RUN SCRIPTS
#1) By writing it in an argument like autoscreen.py run .as script name or direct command
#2) by opening the app like python autoscreen.py

jsonvariants = {} #for json 

command_count = 0  # this variable prevents our functions from "maximum recursion depth exceeded" error
variants = {} #our dictionaries of variables
sessionset = {} #our dictionaries of session settings
labelcache = {} #our label holders

#our running script
returner = [False]
currentscript = ["default.as"]
#changes if the user is running a script
onscript = [False]

runonce = [False] #run one time and close if run with arguments

import ast



def parsestringsnormally(text_as_literal, cli_parse = True):
    """
    Safely parses dynamic inputs: Treats paths as literal strings (no escape processing),
    and other literals (strings, numbers, lists) via ast.literal_eval (e.g., \n → newline).
    Handles quoted/unquoted inputs gracefully.
    """
    # Quick strip outer quotes (common in dynamic/config inputs)
    #print(text_as_literal)
    
    original = text_as_literal
    if "quotestrip" in sessionset:
          if sessionset["quotestrip"] == "strip":
            original = text_as_literal.strip().strip("'\"")
            
          elif sessionset["quotestrip"] == "nostrip": 
            original = text_as_literal

    if cli_parse == True: #parse all strings in cli mode 
        # Paths: Raw literal, no eval (preserves \bin, etc.)
        return original
    else: #parse in string mode
        # Non-paths: Try to eval as literal (handles \n, numbers, lists)
        try:
            # Wrap in quotes only if not already a quoted literal
            if original[0] in "'\"" and original[-1] in "'\"":
                eval_str = original
            else:
                eval_str = f'"{original}"'
            return ast.literal_eval(eval_str)
        except (ValueError, SyntaxError):
            # Eval failed (e.g., malformed)—fallback to raw string
            return original
        except Exception:
            return original
   

def printer(word,noprint=False): #when printing turn to string in case of parsing
      if word == None:
        return ''
      
      tostrg = str(word)
      if returner[0] == True:
            returner[0] = False
            return parsestringsnormally(tostrg)
      else:
            if noprint == False:
               psn = parsestringsnormally(tostrg) #do not use cli method when printing
               print(psn)
               return ''

   
def elseremove(splt):
     #?else detector and removal
     rmels = []
     for e in splt:
        if e == "?else":
          break
        else:
          rmels.append(e)
     splt.clear()
     for s in rmels:
       splt.append(s)


#encryptions
#security features  
data = {} 
admin = [False]
logincnt = 0  
getcmdbyte={"bytes":""} #this stores our encrypted data so we dont have to always do encrypt and decrypt 






def welcome():
    # Initialize colorama
    init(autoreset=True)
    welcomeMessage = f"""
{Fore.CYAN}{'='*63}
{Fore.YELLOW}{'WELCOME TO SURTR 4.0':^63}
{Fore.CYAN}{'='*63}{Style.RESET_ALL}

{Fore.GREEN}Surtr 4.0 is a powerful automation tool designed to:{Style.RESET_ALL}
  • Simplify repetitive tasks
  • Enhance productivity
  • Enable advanced automation workflows

From simple automation to complex scenarios, Surtr covers:
  • Mouse clicks and keyboard input
  • Image recognition and processing
  • File operations
  • System monitoring

With its robust command set and flexible scripting,
Surtr is ideal for:
  - Developers
  - IT professionals
  - Gamers
  - Anyone who wants to automate Windows tasks

{Fore.CYAN}{'='*63}
{Fore.YELLOW}{'BEFORE USING SURTR 4.0':^63}
{Fore.CYAN}{'='*63}{Style.RESET_ALL}

{Fore.LIGHTBLUE_EX}1) Activate Security Mode{Style.RESET_ALL}
------------------------------------------------------------
• By default, Surtr starts in {Fore.RED}Guest Mode{Style.RESET_ALL} (security off).
• To enable security, run:
    {Fore.YELLOW}< activateSecurity >{Style.RESET_ALL}
• You will be prompted for a password.
  Default password:  {Fore.CYAN}surtrblade{Style.RESET_ALL}
• Once activated:
    - Guest users can only run limited commands
    - Full access requires logging in with:
        {Fore.YELLOW}< login <password> >{Style.RESET_ALL}
• Optionally disable guest mode:
    {Fore.YELLOW}< guestUser on/off >{Style.RESET_ALL}
  (If disabled, login is required on startup.)
• After {Fore.RED}5 failed login attempts{Style.RESET_ALL}, Surtr locks the session
  and must be restarted.

{Fore.LIGHTBLUE_EX}2) Change the Default Password{Style.RESET_ALL}
------------------------------------------------------------
• {Fore.RED}IMPORTANT:{Style.RESET_ALL} Do not leave the default password as "{Fore.CYAN}surtrblade{Style.RESET_ALL}".
• To set a new password:
    {Fore.YELLOW}< setSecurityPassword <newpassword> >{Style.RESET_ALL}
• Example:
    {Fore.YELLOW}< setSecurityPassword MyStrongPass123 >{Style.RESET_ALL}

{Fore.CYAN}{'='*63}{Style.RESET_ALL}
"""
    print(welcomeMessage)
    input(f"{Fore.GREEN}Press ENTER when you have completed the steps above...{Style.RESET_ALL}")
    print(f"\n{Fore.GREEN}Setup complete! You are now ready to start automating.")
    print(f"{Fore.CYAN}Happy Automation with Surtr !{Style.RESET_ALL}")

    while True:
        input("")


def hash_password(password):
    # Use PBKDF2 with SHA-256, a fixed (empty) salt, and high iterations for security.
    # This keeps output deterministic (same input -> same output) with no per-user storage needed.
    # High iterations slow down brute-force attacks without affecting legitimate use much.
    salt = b'surtrpassword$$$$#@yourapp.bot'  # Fixed salt; could be a hardcoded secret if you have one.
    iterations = 100000  # Adjust based on your performance needs (higher = more secure but slower).
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations).hex()
   
#cleardata()
def cleardata():
    global data
    print("Preparing files please wait")
    
    #resetting command register data
    getcmds = []
    command= "rundefault"
    tostring= "run default.as"
    getcmds.append(f"{command} {tostring}\n")
    print("loading default files")
    #encrypting
    credloader.encrypt_file("\n".join(getcmds),commandfile,text=True)
    #updating command holders
    getcmdbyte["bytes"] = "\n".join(getcmds).encode()
    
    
    #resetting password security data
    spassword = hash_password('surtrblade')
    data = {'password': 'set', 'securitypassword': spassword, 'security': 'notactive', 'guest': 'set', 'verified': 'no'}
    saver = json.dumps(data,indent=4)
    credloader.encrypt_file(saver,ssm_path,text=True)
    
    #resetting webui configurations settings
    #default webui credientials
    webuidefaults=['username=admin',
                   'password=admin',
                   'resolution=1280x720',
                   'framequality=90',
                   'usecursor=yes',
                   'useaudio=yes',
                   'defaultloopback=yes',
                   'chosenloopbackid=',
                   'usescreen=yes',
                   'usefile=yes',
                   'usescriptbuilder=yes',
                   'usecommand=yes',
                   'userecord=yes',
                   'blockedcommand=runCmd',
                   'permanent=no']
    
    credloader.encrypt_file("\n".join(webuidefaults),crefile,text=True)
    
    admin[0] = True
    welcome()
    

#reset surtr
def resetallsurtdata(warn="no"):
    if warn == "no":
          cleardata()
    else:
      cice = input(f"Cannot fetch important data \nTry restarting surtr\nIf the error persist type > reset < to reset surtr >")  # Output: "Decryption failed: Invalid token"
      if cice == "reset":
        verfy = input("This will clear all surtr data and configurations including saved commands and passwords\ntype yes if you want to continue >")
        if verfy == "yes":
            print("Reparing surtr please wait...")
            cleardata()
        else:
            print("closing in ten seconds")
            time.sleep(10)
            os._exit(10) 
      else:
        print("closing in ten seconds")
        time.sleep(10)
        os._exit(10)    
           
           
#error numbers
#100 general error
#102 incomplete arguments
#103 variable not found
#100 fatal error
#200 file not found error
#104 divison error 
#105 misuse datatype error
#108 invalid input error
#115 unrecognized method error
#300 system error
#500 log error

runcodecurrentcommand = None

def logger(logtext):
    global runcodecurrentcommand
    try:
      full_log = []
      full_log.append(f"Error: {logtext}")
      if runcodecurrentcommand != None:
            full_log.append(f"Command: #{variants['{{errornumber}}']} {runcodecurrentcommand}")
      variants.update({"{{errortext}}":logtext}) #update log text first
      
      if "{{logerror}}" in variants: #if the user dont want to show errors
            d = dt.datetime.now()
            lg = open(variants["{{logerror}}"], "a")
            lg.write(f"{d.strftime('%d %B %Y')} {show_time()} #{variants['{{errornumber}}']} {logtext}\n")
            
            if runcodecurrentcommand != None:
              lg.write(f"Command: {runcodecurrentcommand}\n") 
            lg.close()
            
      elif "{{showerror}}" in variants: 
        
         if variants["{{showerror}}"] == "full":
            print("\n".join(full_log)) 
              
         elif variants["{{showerror}}"] == "hide":
            #print(logtext)
            pass #dont do anything here
         else:
             print(logtext)  
      else:
         print(logtext)
    
    except RecursionError:
       print("A fatal error occured Detail:Loop overflowed")
       os._exit(800)
    except Exception as e:
      variants.update({"{{errornumber}}":"500"})
      variants.update({"{{errortext}}":f"Something happened while logging error {e}"}) 
      print(f"Something happened while logging error {e}")
     
     
onerrorfirstrun = [False]        
def closescript(e=None,text="",errornumber="100"):
  global runcodecurrentcommand
  #update error number
  #traceback.print_exception(e)
  if len(text) > 200:
       text = text[:200] + "..."
       
  variants.update({"{{errornumber}}":errornumber})
  if runcodecurrentcommand != None:
    rcc = runcodecurrentcommand
    if len(rcc) > 200:
           runcodecurrentcommand = rcc[:200] + "..."
    variants.update({"{{errorsource}}":runcodecurrentcommand})
    
  if not e == None: #show error if user specify an error 
    if isinstance(e, IndexError): # fix the list index out of range error (mostly from incomplete or invalid arguments)
        variants.update({"{{errornumber}}":"102"})
        logger(f"Invalid command arguments. Check the command syntax. {text}")
        
    elif isinstance(e, FileNotFoundError):
        variants.update({"{{errornumber}}":"200"})
        logger(f"File not found. Verify the file path and permissions. {text}")
    elif isinstance(e, PermissionError):
        variants.update({"{{errornumber}}":"201"})
        logger(f"Permission denied. Check file permissions or run with appropriate privileges. {text}")
        
    elif isinstance(e, IsADirectoryError):
        variants.update({"{{errornumber}}":"202"})
        logger(f"Expected a file but found a directory. Provide a valid file path. {text}")
        
    elif isinstance(e, NotADirectoryError):
        variants.update({"{{errornumber}}":"203"})
        logger(f"Expected a directory but found a file. Provide a valid directory path. {text}")
        
    elif isinstance(e, FileExistsError):
        variants.update({"{{errornumber}}":"204"})
        logger(f"Operation failed: target file already exists. {text}")
        
    elif isinstance(e, UnicodeDecodeError):
        variants.update({"{{errornumber}}":"205"})
        logger(f"File decoding error. The file may be corrupted or use an unsupported encoding. {text}")
        
    elif isinstance(e, UnicodeEncodeError):
        variants.update({"{{errornumber}}":"219"})
        logger(f"File encoding error. The file may be corrupted or use an unsupported encoding. {text}")
        
    elif isinstance(e, OSError):
        variants.update({"{{errornumber}}":"206"})
        logger(f"File system error. Check disk space and path validity. {text}")
        
    elif isinstance(e, ZeroDivisionError):
        variants.update({"{{errornumber}}":"104"})
        logger(f"Math error: division by zero. {text}")
        
    elif isinstance(e, TypeError):
        variants.update({"{{errornumber}}":"105"})
        logger(f"Invalid data type used. Check command inputs. {text}")
        
    elif isinstance(e, ValueError):
        variants.update({"{{errornumber}}":"108"})
        logger(f"Invalid value provided. Verify command parameters. {text}")
    
    elif isinstance(e,RecursionError):
        logger(f"loop overflowed {text}")
        print("A fatal error occured Detail:Loop overflowed")  
        os._exit(800)
        
    elif isinstance(e, AttributeError):
        variants.update({"{{errornumber}}":"115"})
        logger(f"Unexpected object type or missing attribute. {text}")
        
        
    elif isinstance(e, NameError): #for system variables
        variants.update({"{{errornumber}}":"556"})
        logger(f"Error in surtr system function. {text}")
    
    #for secure files decrypting    
    elif isinstance(e,InvalidToken): #IF KEYS DO NOT MATCH ASSUMES USING SURTR FOR THE FIRST TIME
          resetallsurtdata(warn="no")
    elif isinstance(e,InvalidSignature): 
          resetallsurtdata(warn="yes")
          
    else:
        variants.update({"{{errornumber}}":"300"})
        logger(f"System Error DETAILS:{text} {e}")
  else:
      variants.update({"{{errornumber}}":errornumber})
      logger(text) 
  
  #if the user sets it not to stop script after an error like: set {{onerror}} nostop
  if "{{onerror}}" in variants:
    if variants["{{onerror}}"] == "nostop":
        pass
    elif variants["{{onerror}}"].endswith(":"):
      try:
        if onerrorfirstrun[0]  == True:
            print(f"ERROR MANAGEMENT: cannot run {variants['{{onerror}}']}")
            onerrorfirstrun[0]  == False 
        else:
          onerrorfirstrun[0] = True
          runcodes(['run',variants["{{onerror}}"]])
          onerrorfirstrun[0] = False
          
          
      except Exception as e: #do not print details here because of accedentally printing a recursion error
         print(f"ERROR MANAGEMENT: cannot run {variants['{{onerror}}']}")
         onerrorfirstrun[0] = False
      finally:
        onerrorfirstrun[0] = False
    else:  
       try:
        getoptions(True)
       except Exception:
         print("SOMETHING WENT WRONG: ERROR UNKWOWN")
  else:
       try:
           getoptions(True)
       except Exception:
         print(f"SOMETHING WENT WRONG: ERROR UNKWOWN")
       

#for webui  settings
webuibyte = {"bytes":""}
setting = {}

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
      closescript(e,text=f"WEBUI CANNOT START, CONFIGURATION ERROR")
      sys.exit(1)
 
settingsparser()
    
 
def settings(index,webui=False):
 if webui == False:
  try:
    if os.path.exists(configfile) and os.path.isfile(configfile):
      f= open(configfile,"r")
      foundset = False
      for i in f:
        if index in i:
          foundset = True
          ans = i.split("=")
          return " ".join(ans[1:]).strip()
       
      f.close()
      if foundset == False:
        print("Fatal error:CORRUPT CONFIGURATION FILE")
        print("surtr will close in 10 seconds")
        time.sleep(10)
        os._exit(10000)
        
           
    else:
        print("Fatal error: NO OR CORRUPT CONFIGURATION FILE")
        print("surtr will close in 10 seconds")
        time.sleep(10)
        os._exit(10000)
  except:
      return ""
    
 else:  #for webui settings
  if index in setting:
          return setting[index]
  else:
      return ""
 
 
dontparsevariable = [False] 



# ===================================================================
# ADVANCED SHELL-STYLE PARSER - FINAL VERSION (Approved by Me)
# ===================================================================

def text_to_list(text, firstcall=False):
    """
    Primary fallback parser: preserves EXACT quoting as written.
    
    Examples:
        a "big bag"           → ['a', '"big bag"']
        'hello "world"'       → ["'hello \"world\"'"]
        this is 'cool'        → ['this', 'is', "'cool'"]
    
    Used as safe-mode fallback when shlex fails.
    """
    if not isinstance(text, str):
        return []

    # Regex matches: unquoted tokens, "double-quoted", or 'single-quoted' strings
    token_pattern = r'''(?:[^\s'"\\]+|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')+'''
    matches = re.finditer(token_pattern, text)

    result = []
    for match in matches:
        token = match.group(0)

        # If fully quoted → keep quotes exactly as written
        if (token.startswith('"') and token.endswith('"')) or \
           (token.startswith("'") and token.endswith("'")):
            result.append(token)
        else:
            result.extend(token.split())  # Split unquoted parts on whitespace

    # === Quote normalization for firstcall (used by interpreter/executer) ===
    if firstcall and result:
        i = 0
        while i < len(result):
            t = result[i]

            # Handle escaped quotes: \\"hello\\" → "hello"
            if t.startswith('\\"') and t.endswith('\\"'):
                result[i] = f'"{t[2:-2]}"'
            elif t.startswith("\\'") and t.endswith("\\'"):
                result[i] = f"'{t[2:-2]}'"
            # Normal quoted → strip outer quotes (standard behavior in execution)
            elif t.startswith('"') and t.endswith('"'):
                result[i] = t[1:-1]
            elif t.startswith("'") and t.endswith("'"):
                result[i] = t[1:-1]
            i += 1

    return result



def shellspliter(text, firstcall=False):
    """
    Ultimate hybrid parser: tries smart shlex → falls back to regex.
    
    Features:
      • Supports ~~comments (only on firstcall)
      • Handles (parentheses) as grouping
      • >> prefix for raw mode
      • Full quote preservation + optional stripping
      • Safe fallback on any error
      • Custom punctuation handling
    """

    def shellparse(text, firstcall=False, normal=False):
        try:
            # Special: skip parsing if line starts with ~~ (comment)
            if firstcall and text.startswith("~~"):
                return [""]

            # Configure shlex lexer
            lexer = shlex.shlex(text, posix=False, punctuation_chars=not normal)
            lexer.whitespace = ' '              # Only split on spaces
            lexer.whitespace_split = True

            # Comment handling: only active on first call
            lexer.commenters = '~~' if firstcall else ''

            tokens = list(lexer)

            # === Quote cleanup on firstcall (same logic as text_to_list) ===
            if firstcall and tokens:
                i = 0
                while i < len(tokens):
                    t = tokens[i]
                    if t.startswith('\\"') and t.endswith('\\"'):
                        tokens[i] = f'"{t[2:-2]}"'
                    elif t.startswith("\\'") and t.endswith("\\'"):
                        tokens[i] = f"'{t[2:-2]}'"
                    elif t.startswith('"') and t.endswith('"'):
                        tokens[i] = t[1:-1]
                    elif t.startswith("'") and t.endswith("'"):
                        tokens[i] = t[1:-1]
                    i += 1

            return tokens

        except ValueError as e:
            if not text.startswith("~~") and firstcall and settings("showSafeModeWarnings") == "yes":
                print('Warning: Unclosed or malformed quotes detected')
                print("Switching to safe mode parser...")
            return text_to_list(text, firstcall=firstcall)

        except RecursionError:
            print("FATAL: Parser recursion overflow")
            os._exit(800)

        except Exception:
            if not text.startswith("~~") and firstcall and settings("showSafeModeWarnings") == "yes":
                print(f'Warning: Parser error')
                print("Falling back to safe mode...")
            return text_to_list(text, firstcall=firstcall)

    # === First-call routing logic ===
    if firstcall:
        original = text.strip()

        # >> prefix = raw input mode
        if original.startswith(">>"):
            dontparsevariable[0] = True
            text = original[2:].strip()

        # ( ... ) = grouped expression
        if text.startswith("(") and text.endswith(")"):
            return shellparse(text[1:-1], firstcall=True, normal=False)
        else:
            return shellparse(text, firstcall=True, normal=True)
    else:
        return shellparse(text, firstcall=False, normal=True)

 
def sessionsettings(sets):
  try:
    if sets[1] == "quotestrip":
        sessionset["quotestrip"] = " ".join(sets[2:]).strip()
       
    
  except Exception as e:
    closescript(e,text="Error cannot modify surtr configurations")
    return
  
def mousemove(**opts):
 if "no" in opts["file"]:
    try:
        pyg.moveTo(int(float(opts["x"])),int(float(opts["y"])),int(float(opts["speed"])))
    except Exception as e:
        closescript(e,text="cannot move mouse")
        return # stops running the function
    else:
        print(f"moved mouse {opts['x']},{opts['y']} at the speed of {opts['speed']}")
      
 #if user uses a file
 else:
    try:
      rmnl = opts["image"]
      fileloc = pyg.locateOnScreen(rmnl, confidence=0.9)
      #print(fileloc)
      centerfile = pyg.center(fileloc)
      pyg.moveTo(centerfile[0],centerfile[1], int(opts["speed"]))
    except Exception as e:
        closescript(e,text="cannot move mouse check if the image is on the screen")
        return # stops running the function
    else:
        print(f"moved to {rmnl}")
  
        
def mousedrag(**opts):
  if "no" in opts["file"]:
    try:
        pyg.dragTo(int(float(opts["x"])),int(float(opts["y"])),int(float(opts["speed"])))
    except Exception as e:
        closescript(e,text="cannot drag mouse")
        return # stops running the function
    else:
        print(f"dragged mouse {opts['x']},{opts['y']} at the speed of {opts['speed']}")
  #if the user want to drag the mouse position to an image
  else:
   if "yes" in opts["oneimg"]:
    try:
      rmnl = opts["image"]
      fileloc = pyg.locateOnScreen(rmnl, confidence=0.9)
      #print(fileloc)
      centerfile = pyg.center(fileloc)
      pyg.dragTo(centerfile[0],centerfile[1], int(opts["speed"]))
    except Exception as e:
      closescript(e,text="error dragging mouse check if the image is on the screen")
      return # stops running the function
    else:
        print(f"dragged to {rmnl}")
   #if the user want to drag an image to an image
   else:
    try:
      rmnl = opts["image1"]
      rmnl2 = opts["image2"]
      #locate first image
      fileloc = pyg.locateOnScreen(rmnl, confidence=0.9)
      #print(fileloc)
      centerfile = pyg.center(fileloc)
      pyg.moveTo(centerfile[0],centerfile[1], int(float(opts["speed"])))
      #pyg.click()
      # move to second image
      fileloc2 = pyg.locateOnScreen(rmnl2, confidence=0.9)
      #print(fileloc2)
      centerfile2 = pyg.center(fileloc2)
      pyg.dragTo(centerfile2[0],centerfile2[1], int(float(opts["speed"])))
      #pyg.click()
    except Exception as e:
        closescript(e,text="error dragging mouse check if the images are on the screen")
        return # stops running the function
    else:
        print(f"dragged from {rmnl} to {rmnl2}")
          
          
#all mouse click functions 
def mouseclickhandler(**optns):
 if "rightclick" in optns["work"]:
    if "yes" in optns["file"]:
      try:
        rmnl = optns["image"]
        fileloc = pyg.locateOnScreen(rmnl, confidence=0.9)
        #print(fileloc)
        centerfile = pyg.center(fileloc)
        pyg.rightClick(centerfile[0],centerfile[1])
      except Exception as e:
        closescript(e,text="cannot RightClick check if the image is on the screen")
        return # stops running the function
      else:
          print(f"Right clicked {rmnl}")
        
        # if the user uses number instead
    else:
        try:
           pyg.rightClick(int(float(optns["x"])),int(float(optns["y"])))
        except Exception as e:
          closescript(e,text="cannot RightClick")
          return # stops running the function
        else:
          print(f"Right clicked {optns['x']},{optns['y']}")
          
 elif("justclick" in optns["work"]):
    if "yes" == optns["file"]:
      try:
        rmnl = optns["image"]
        fileloc = pyg.locateOnScreen(rmnl, confidence=0.9)
        #print(fileloc)
        centerfile = pyg.center(fileloc)
        pyg.click(x=centerfile[0],y=centerfile[1])
      except Exception as e:
        closescript(e,text="cannot Click check if the image is on the screen")
        return # stops running the function
      else:
          print("clicked mouse")
        
        # if the user uses number instead
    else:
        try:
           pyg.click(x=int(float(optns["x"])),y=int(float(optns["y"])))
        except Exception as e:
          closescript(e,text="cannot Click")
          return # stops running the function
        else:
          print("clicked mouse")
                
 elif("doubleclick" in optns["work"]):
    if "yes" == optns["file"]:
      try:
        rmnl = optns["image"]
        fileloc = pyg.locateOnScreen(rmnl, confidence=0.9)
        #print(fileloc)
        centerfile = pyg.center(fileloc)
        pyg.doubleClick(x=centerfile[0],y=centerfile[1])
      except Exception as e:
        closescript(e,text="cannot Click check if the image is on the screen")
        return # stops running the function
      else:
          print("doubleClicked mouse")
        
        # if the user uses number instead
    else:
        try:
           pyg.doubleClick(x=int(float(optns["x"])),y=int(float(optns["y"])))
        except Exception as e:
          closescript(e,text="cannot doubleClick")
          return # stops running the function
        else:
          print("doubleClicked mouse")
                
                         
 elif("tripleclick" in optns["work"]):
    if "yes" == optns["file"]:
      try:
        rmnl = optns["image"]
        fileloc = pyg.locateOnScreen(rmnl, confidence=0.9)
        #print(fileloc)
        centerfile = pyg.center(fileloc)
        pyg.tripleClick(x=centerfile[0],y=centerfile[1])
      except Exception as e:
        closescript(e,text="cannot Click check if the image is on the screen")
        return # stops running the function
      else:
          print("trippleClicked mouse")
        
        # if the user uses number instead
    else:
        try:
           pyg.tripleClick(x=int(float(optns["x"])),y=int(float(optns["y"])))
        except Exception as e:
          closescript(e,text="cannot doubleClick")
          return # stops running the function
        else:
          print("tripleClicked mouse")


def allmousehandler(mouseoptn):
   if mouseoptn[0] == "move":
      try:
        if (len(mouseoptn) > 4):
            closescript(text=f"error in move args {len(mouseoptn)} (more than 3)")
            return # stops running the function
        if(len(mouseoptn) == 4):
              mousemove(x = mouseoptn[1], y = mouseoptn[2], speed = mouseoptn[3],file="no")
        if(len(mouseoptn) == 3):
           rmnewline = re.sub("\n", "", mouseoptn[1])
           if(os.path.exists(rmnewline) and os.path.isfile(rmnewline)):
              mousemove(image=mouseoptn[1],speed=mouseoptn[2], file="yes")
           else:
             mousemove(x = mouseoptn[1], y = mouseoptn[2], speed = 0, file="no")
             
        if(len(mouseoptn) == 2):
           closescript(text=f"error in move args {len(mouseoptn)} (add a number)")
           return # stops running the function
             
      except Exception as e:
          closescript(e,text=f"error in move args {len(mouseoptn)} (Check your args)")
          return # stops running the function
                
   elif mouseoptn[0] == "drag":
      try:
        if (len(mouseoptn) > 4):
          closescript(text=f"error in drag args {len(mouseoptn)} (more than 3)")
          return # stops running the function
             
        if(len(mouseoptn) == 4):
          #drag an image to an image
          rmnewline1 = re.sub("\n", "", mouseoptn[1])
          rmnewline2 = re.sub("\n", "", mouseoptn[2])
          if(os.path.exists(rmnewline1) and os.path.isfile(rmnewline1) or os.path.exists(rmnewline2) and os.path.isfile(rmnewline2)):
            mousedrag(image1 = mouseoptn[1], image2 = mouseoptn[2], speed = mouseoptn[3],oneimg="no", file="yes")
          else:
              mousedrag(x = mouseoptn[1], y = mouseoptn[2], speed = mouseoptn[3],oneimg="no", file="no")
        if(len(mouseoptn) == 3):
            rmnewline = re.sub("\n", "", mouseoptn[1])
            if(os.path.exists(rmnewline) and os.path.isfile(rmnewline)):
              mousedrag(image=mouseoptn[1],speed=mouseoptn[2],oneimg="yes", file="yes")
        if(len(mouseoptn) == 2):
            closescript(text=f"error in drag args {len(mouseoptn)} (add a number)")
            return # stops running the function
             
      except Exception as e:
        closescript(e,text=f"error in drag args {len(mouseoptn)} (Check your args)")
        return # stops running the function
   
   #for mouse clicks      
   #pyg.pyautogui.rightClick(x=moveToX, y=moveToY)
   #pyg.middleClick(x=moveToX, y=moveToY)
   #pyg.doubleClick(x=moveToX, y=moveToY)
   #pyg.tripleClick(x=moveToX, y=moveToY)             
   elif mouseoptn[0] in ("rightClick","click","doubleClick","tripleClick"):
        try:
           if mouseoptn[0] == "rightClick":
             if (len(mouseoptn) > 3):
               closescript(text=f"error in move arguments {len(mouseoptn)} (more than 3)")
               return # stops running the function
             
             if (len(mouseoptn) == 2): # if the user types image path to rightclick instead
               rmnewline = re.sub("\n", "", mouseoptn[1])
               if(os.path.exists(rmnewline) and os.path.isfile(rmnewline)):
                mouseclickhandler(work= "rightclick", image = rmnewline, file = "yes")
               else:
                closescript(text=f"error in arguments >> {mouseoptn[1]} not a file")
                return # stops running the function
              
             else:
                if(len(mouseoptn) == 1):
                     try:
                      pyg.click(button='right', clicks=1, interval=0.25)
                     except Exception as e:
                       closescript(e,text="cannot rightClick")
                       return # stops running the function
                     
                     else:
                       print("right clicked mouse")
                else:
                  if(len(mouseoptn) == 3):
                    # if the user use only numbers
                    mouseclickhandler(work= "rightclick", x = mouseoptn[1], y = mouseoptn[2], file = "no") 
               
             #for click
           elif (mouseoptn[0] == "click"):
               if (len(mouseoptn) > 3):
                 closescript(text=f"error in move arguments {len(mouseoptn)} (more than 3)")
                 return # stops running the function
                
               if (len(mouseoptn) == 2): # if the user types image path to rightclick instead
                 rmnewline = re.sub("\n", "", mouseoptn[1])
                 if(os.path.exists(rmnewline) and os.path.isfile(rmnewline)):
                   mouseclickhandler(work = "justclick", image = rmnewline, file = "yes")
                 else:
                  closescript(text=f"Err: in arguments >> {mouseoptn[1]}  not a file")
                  return # stops running the function
                
               else:
                 if(len(mouseoptn) == 1):
                     try:
                      pyg.click()
                     except Exception as e:
                       closescript(e,text="cannot Click")
                       return # stops running the function
                     else:
                       print("clicked mouse")
                 else:
                  # if the user use only numbers
                  mouseclickhandler(work = "justclick", x = mouseoptn[1], y = mouseoptn[2], file = "no") 
                 

           elif (mouseoptn[0] == "doubleClick"):
               if (len(mouseoptn) > 3):
                 closescript(text=f"error in move arguments {len(mouseoptn)} (more than 3)")
                 return # stops running the function
               
               if (len(mouseoptn) == 2): # if the user types image path to rightclick instead
                 rmnewline = re.sub("\n", "", mouseoptn[1])
                 if(os.path.exists(rmnewline) and os.path.isfile(rmnewline)):
                   mouseclickhandler(work= "doubleclick", image = rmnewline, file = "yes")
                 else:
                  closescript(text=f"error in arguments >> {mouseoptn[1]}  not a file")
                  return # stops running the function
                
               else:
                 if(len(mouseoptn) == 1):
                     try:
                      pyg.doubleClick()
                     except Exception as e:
                       closescript(e,text=f"cannot doubleClick")
                       return # stops running the function
                     
                     else:
                       print("double clicked mouse")
                 else:
                    # if the user use only numbers
                   mouseclickhandler(work= "doubleclick",x = mouseoptn[1], y = mouseoptn[2], file = "no")         

           elif (mouseoptn[0] == "tripleClick"):
               if (len(mouseoptn) > 3):
                 closescript(text=f"error in move arguments {len(mouseoptn)} (more than 3)")
                 return # stops running the function
               
               if (len(mouseoptn) == 2): # if the user types image path to rightclick instead
                 rmnewline = re.sub("\n", "", mouseoptn[1])
                 if(os.path.exists(rmnewline) and os.path.isfile(rmnewline)):
                   mouseclickhandler(work = "tripleclick", image = rmnewline, file = "yes")
                 else:
                  closescript(text=f"error in arguments >> {mouseoptn[1]}  not a file")
                  return # stops running the function
                
               else:
                if(len(mouseoptn) == 1):
                     try:
                         mousepos = pyg.position() 
                         pyg.tripleClick(mousepos[0], mousepos[1])
                     except Exception as e:
                       closescript(e,text=f"cannot tripleClick")
                       return # stops running the function
                     
                     else:
                       print("triple clicked mouse")
                else:
                    # if the user use only numbers
                  mouseclickhandler(work = "tripleclick",x = mouseoptn[1], y = mouseoptn[2], file = "no")
        except Exception as e:         
             closescript(e,text=f"error in mouse command args {len(mouseoptn)} (Check your args)")
             return # stops running the function
         
   elif mouseoptn[0] in ("scroll","scrollV","scrollH"):
        try:
          mouse = Controller()
          if not len(mouseoptn) == 2:
               closescript(text=f"scroll accepts two arguments <{len(mouseoptn)}>") 
               return # stops running the function
             
          if mouseoptn[0] == "scroll":
            mouse.scroll(0, int(float(mouseoptn[1])))
            print(f"Scrolled the mouse {mouseoptn[1]}")
            
          elif mouseoptn[0] == "scrollV":
            mouse.scroll(0, int(float(mouseoptn[1])))
            print(f"Scrolled the mouse {mouseoptn[1]} vertically")
          #for horizontal
          elif mouseoptn[0] == "scrollH":
            mouse.scroll(int(float(mouseoptn[1])), 0)
            print(f"Scrolled the mouse {mouseoptn[1]} horizontally")
             
        except Exception as e:
           closescript(e,text=f"Scroll error")     
           return # stops running the function
         
       
    
    
def keywordsreplace(text, speed):
  stage = ""
  d = dt.datetime.now()
  relog = text.replace("{{login}}",os.getlogin())
  redate = relog.replace("{{date}}",d.strftime("%d %B %Y"))
  retime = redate.replace("{{time}}",show_time())
  
  fulltext = retime 
  pyg.write(fulltext, speed)    


def waiter(secnd):
  time.sleep(secnd)
       
def keyboardhandler(**optns):
  if("type" in optns["mode"]):
    if ( "yes" in optns["file"]):
     try:
      flerd = open(optns["text"], "r")
      for x in flerd:
        keywordsreplace(x,optns["speed"])
      flerd.close()
     except Exception as e:
      closescript(e,text="cannot type on screen")
      return # stops running the function
    else:
     try:
      keywordsreplace(optns["text"],optns["speed"])
     except Exception as e:
      closescript(e,text="cannot type on screen")
      return # stops running the function
      
  if("hold" in optns["mode"]):
    try:
      pyg.keyDown(optns["text"])
    except Exception as e:
      print(f"Err cannot hold key {e}")
      
  if("release" in optns["mode"]):
    try:
      pyg.keyUp(optns["text"])
    except Exception as e:
      print(f"Err cannot release key {e}")
      
  if("press" in optns["mode"]):
    try:
      pyg.press(optns["text"])
    except Exception as e:
      print(f"Err cannot press key {e}")

seeker = None
newlistrunrequest = False
stoplistexec = False
runcmdlist = []
arglist = []
listexecrunning = False
exitlabel = [False]
vip_run = [False]

def runhandler(**optns):
    global seeker, newlistrunrequest, stoplistexec, listexecrunning
    # if the user runs another script like run script2.as and did not use a label
    if ("yes" in optns["file"] and "no" in optns["fileargs"]):
        interpreter(optns["text"])

    # if the user runs a label from this script like run label:

    # if the user runs a label from the same script like run label:
    elif ("no" in optns["file"] and "no" in optns["fileargs"]):
        try:
            # print(optns)
            # handle text being list or string
            optxt = optns["text"][0] if isinstance(optns["text"], list) else optns["text"]

            # check for arguments
            arglist.clear()
            if isinstance(optns["text"], list):
                if len(optns["text"]) == 1:  # leave if user do not use argument
                    pass
                else:
                    if optns["text"][1] == "?arg" and len(optns["text"]) > 2:

                        for a in optns["text"][2:]:
                            arglist.append(a)
                    else:
                        closescript(text="please use a valid argument syntax \nrun label: ?arg argument0 argument1...")
                        return
            if optxt not in labelcache:
                closescript(text=f"label {optxt} not found", errornumber="180")
                return

            startrun = False
            with open(optns["currentscript"], "r") as f:

                """
                the surtr run label: works differently from other run types
                it uses a different running method that prevents recursion errors and other
                iterate errors that may occur during looping or iterating using run

                The run label: command uses a different executer called executer_list that
                executes commands given to it in a list instead of script like the main executer
                                  HOW IT WORKS
                when called it first finds the position of the label using labelcache when found
                it clears old command list then it starts adding commands after the label till it
                sees another label {not a transparent label (label that starts with _ )} it stops and
                now checks if executer_list is running commands if not running it calls executer_list
                with the new command list as argument.
                if executer_list is running the run label: cammand cannot call another executer_list to
                avoide colission errors and other recursion problems it sends a stop request by setting
                stoplistexec to True and send a request for executer (the main executer) to call executer_list
                by setting newlistrunrequest to True then closes for executer_list to see the request and then closes
                stopping all execution when all temporally execution is stopped executer now sees that a request to start
                executer_list has been set it quickly calls executer_list again with the new command saved in command list
                so executer list can now run a fresh new commands avoiding any iterate or loop errors.
                But if the command uses vip_run the command runs immediately without using the recursion guard method like
                the command joiner ^ if it has a label to run, it will run in vip mode (without recursion guard) because the
                recursion guard will can block or put label commands sent from the specialjoiners function on pending mode wich
                can cause errors or malfunctions

                """
                # jump to saved position

                f.seek(labelcache[optxt])
                startrun = True
                f.readline()  # skip label name

                # list method start here


                # clear old commands
                runcmdlist.clear()
                while True:
                    line = f.readline()
                    if not line:
                        break
                    spt = shellspliter(line.strip())
                    if len(spt) == 1 and spt[0].endswith(":") and spt[0].startswith("_") == False:  # stop at next transparent label
                        break
                    if len(spt) == 1 and spt[0].endswith(":"):  # stop at next label
                        break

                    runcmdlist.append(line)

                #Check VIP flag before using recursion guard
                # WARNING: any label command not using the recursion guard is a victim of recursion error use with care
                if vip_run[0] == True:
                    # VIP: Run immediately, no guard/request
                    stoplistexec = False
                    newlistrunrequest = False
                    
                    executer_list(runcmdlist[:])
                    runcmdlist.clear()  # Clear after
                    vip_run[0] = False
                    return  # Done, no queue
                  
                #RECURSION GUARD
                # stop old executor if running
                if listexecrunning == True:
                    stoplistexec = True
                    # print("request new list runner")
                    newlistrunrequest = True
                    # send the stop label commands stop execution message and stop
                    # to allow our executerlist,runcodes to stop
                    # so our main executer will be able to know that we have stopped old
                    # run label list executer and requesting to create a new one because runhandler
                    # cannot crete a new request if executer_list is still active (still running a code)
                    # to avoide recursion error will create a new one now
                    return



                # start fresh
                stoplistexec = False
                executer_list(runcmdlist[:])
                # list method stop here


            if startrun:
                # seeker = labelcache[optxt]
                pass
            else:
                closescript(text=f"label {optxt} not found", errornumber="180")
                return

        except Exception as e:
            closescript(e, text="run error")
            return

    # if the user runs a label from another script like run script2.as label:
    elif ("yes" in optns["file"] and "yes" in optns["fileargs"]):

        if settings("allowExternalScriptLabels") != "yes":
            closescript(text="External label disabled")
            return
        try:
            startrun = []
            startrun.insert(0, False)

            if ("list" in str(type(optns["label"]))):
                optlb = optns["label"][0]
            else:
                optlb = optns["label"]
            if os.path.exists(optns["text"]) and os.path.isfile(optns["text"]) and Path(optns["text"]).suffix == ".as":
                with open(optns["text"], "r") as f:
                    while True:
                        linepos = f.tell()  # holds the current line we are at the script
                        line = f.readline()
                        if not line:  # stop at the end of the script
                            break
                        sp = line.strip()
                        if (optlb == sp):
                            seeker = linepos  # position of the label
                            startrun[0] = True
                            break

                if (startrun[0] == True):
                    interpreter(optns["text"])
                else:
                    closescript(text=f"label {optlb} not found", errornumber="180")
                    return

        except Exception as e:
            closescript(e, text="run error")
            return  # stops running the function


def runmaster(splt):
    if len(splt) == 1:
        closescript(text="Invalid run syntax")
        return
    if len(splt) >= 2:
        # if user uses a script
        if os.path.exists(splt[1]) and os.path.isfile(splt[1]) and Path(splt[1]).suffix == ".as":
            allruns(splt, splt[1])
        # if user uses a label
        elif splt[1].endswith(":"):
            if onscript[0] == False:
                closescript(text="You cannot run a label if you are not running a script")
                return
            else:
                allruns(splt, currentscript[0])
        else:
            closescript(text="Invalid script file")
            return

   
   
   
#SCREEN SHOTS
    
def screenshot_handler(**optns):
 try:
  if("yes" in optns["mouse"]):
    #get the mouse position
    mpos = pyg.position()
    pyg.screenshot(region=(int(float(mpos[0])),int(float(mpos[1])),int(float(optns["width"])),int(float(optns["height"]))),imageFilename=optns["path"])
  if("no" in optns["mouse"] and "yes" in optns["onefile"]):
    pyg.screenshot(optns["path"])
  if("no" in optns["mouse"] and "no" in optns["onefile"]):  
    pyg.screenshot(region=(int(float(optns["left"])),int(float(optns["top"])),int(float(optns["width"])),int(float(optns["height"]))),imageFilename=optns["path"])
 except Exception as e:
    closescript(e,text="screenshot error")
    return # stops running the function
        

#multi monitor screenshot
def screenshot_monitor(monitor_index, filename="monitor.png"):
  """Screenshot a full monitor by index (1 = primary)."""
  try:
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        img = sct.grab(monitor)
        mss.tools.to_png(img.rgb, img.size, output=filename)
    print(f"Saved full monitor {monitor_index} -> {filename}")
  except Exception as e:
    closescript(e,"screenShotMonitor error")
    return

def screenshot_region_on_monitor(monitor_index, x, y, width, height, filename="region.png"):
  """Screenshot a region (x,y,width,height) on a specific monitor."""
  try:
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        region = {
            "left": monitor["left"] + x,
            "top": monitor["top"] + y,
            "width": width,
            "height": height
        }
        img = sct.grab(region)
        mss.tools.to_png(img.rgb, img.size, output=filename)
    print(f"Saved region on monitor {monitor_index} -> {filename}")
  except Exception as e:
    closescript(e,"screenShotMonitor error")
    return

def screenshot_at_position(monitor_index, width, height, filename="pos_region.png"):
  """Screenshot a region based on absolute coordinates (mouseposx, mouseposy, width, height)."""
  try:
    with mss.mss() as sct:
        monitor = sct.monitors[monitor_index]
        mouse_x, mouse_y = pyg.position()
        region = {
            "left": monitor["left"] + mouse_x,
            "top": monitor["top"] + mouse_y,
            "width": width,
            "height": height
        }
        img = sct.grab(region)
        mss.tools.to_png(img.rgb, img.size, output=filename)
    print(f"Saved position-based region on monitor {monitor_index} -> {filename}")
    
  except Exception as e:
    closescript(e,"screenShotMonitor error")
    return

#SCREEN SHOTS ENDS HERE


def screentextreadoptions(action,texts,findall,speed,language):
    try:
        windowswdth_height() #get a screen shot of the screen with the computer actual width and height saved to resources/process/desktoprize.png
        tesseractdata = surtr_ocr.screenread(language=language, ocr_path=ocr_path, desktop_path=desktoprize_path)          
        
        data = tesseractdata
       
        boxes = len(data['level'])
        word = " ".join(texts)
        findtext = False
        print("Looking for",word.lower())
        for i in range(boxes):
          if data['text'][i] != '':
                  
             if word.lower() in data['text'][i].lower():
                  findtext = True
                  # get the center using the formula x + w/2, y + h/2
                  xpos = int(data['left'][i]) + (int(data['width'][i]) / 2)
                  ypos = int(data['top'][i]) + (int(data['height'][i]) / 2)
                  if action == "move":
                    mousemove(x = xpos, y = ypos, speed = int(speed), file="no")
                  #pyg.moveTo(int(data['left'][i]), int(data['top'][i]), int(splt[2]))
                  if action == "drag":
                        mousedrag(x = xpos, y = ypos, speed = int(speed),oneimg="no", file="no")
                  
                  if action == "rightclick":
                        mousemove(x = xpos, y = ypos, speed = 0, file="no")
                        pyg.click(button='right', clicks=1, interval=0.25)
                        print("Right clicked mouse")
                        
                  if action == "click":
                        mousemove(x = xpos, y = ypos, speed = 0, file="no")
                        pyg.click()
                        print("Clicked mouse")
                        
                        
                  if action == "doubleclick":
                        mousemove(x = xpos, y = ypos, speed = 0, file="no")
                        pyg.doubleClick()
                        print("Double clicked mouse")
                        
                  if action == "tripleclick":
                        mousemove(x = xpos, y = ypos, speed = 0, file="no")
                        mousepos = pyg.position() 
                        pyg.tripleClick(mousepos[0], mousepos[1])
                        print("Tripple clicked mouse")
                        
                             
                  if findall == "one":
                     break
                      
                  #print(data['left'][i], data['top'][i], data['width'][i], data['height'][i], data['text'][i])
    
        if findtext == False:
              closescript(text=f"Word > {word} < not found")
              return
    except Exception as e:
          closescript(e,text="Text OCR error")
          return # stops running the function
              
              
def readimageshandler(splt,toreturn=False):
  if splt[0] == "readImageLanguages":
      if len(splt) > 1:
            closescript(text="readImageLanguages does not need argument")
            return # stops running the function
      lan = surtr_ocr.readimage(options="languages")
      #if toreturn == True: 
      #  return ", ".join(lan)
      #else:
      #  print(", ".join(lan)) 
      # we are using the return pinter method so the toreturn argument is useless
      if toreturn == False:      
          return printer(", ".join(lan)) 
      else: 
          return printer(", ".join(lan))
            
  elif splt[0] == "readImage":
     if len(splt) == 3:
            data = surtr_ocr.readimage(options="image", path=splt[1], language=splt[2], ocr_path=ocr_path, itype="")
            sentence_blocks = []
            current_sentence = None
            previous_y = None

            for i in range(len(data['text'])):
              text = data['text'][i].strip()
              if text == "":
                 continue
              x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

              if current_sentence is None:
               current_sentence = {
                "text": text,
                "x1": x,
                "y1": y,
                "x2": x + w,
                "y2": y + h
               }
               previous_y = y
              else:
               if abs(previous_y - y) < 10:  # Allow line tolerance
                   current_sentence["text"] += ' ' + text
                   current_sentence["x1"] = min(current_sentence["x1"], x)
                   current_sentence["y1"] = min(current_sentence["y1"], y)
                   current_sentence["x2"] = max(current_sentence["x2"], x + w)
                   current_sentence["y2"] = max(current_sentence["y2"], y + h)
               else:
                 sentence_blocks.append(current_sentence)
                 current_sentence = {
                    "text": text,
                    "x1": x,
                    "y1": y,
                    "x2": x + w,
                    "y2": y + h
                 }
               previous_y = y

            if current_sentence:
              sentence_blocks.append(current_sentence)
           
            final = []
            for sentence in sentence_blocks:
              final.append(sentence["text"])
              
            if toreturn == False:      
               return printer("\n".join(final))
            else: 
               return printer("\n".join(final))
          
     if len(splt) == 4:
           img = splt[1]
           if (splt[2] == "useBlackWhite"):
             data = surtr_ocr.readimage(options="image", path=img, language=splt[3], ocr_path=ocr_path, itype="useBlackWhite")
           elif (splt[2] == "useGray"):
              data = surtr_ocr.readimage(options="image", path=img, language=splt[3], ocr_path=ocr_path, itype="useGray")
           else:
              data = surtr_ocr.readimage(options="image", path=img, language=splt[3], ocr_path=ocr_path, itype="")        
           
           sentence_blocks = []
           current_sentence = None
           previous_y = None

           for i in range(len(data['text'])):
              text = data['text'][i].strip()
              if text == "":
                 continue
              x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

              if current_sentence is None:
               current_sentence = {
                "text": text,
                "x1": x,
                "y1": y,
                "x2": x + w,
                "y2": y + h
               }
               previous_y = y
              else:
               if abs(previous_y - y) < 10:  # Allow line tolerance
                   current_sentence["text"] += ' ' + text
                   current_sentence["x1"] = min(current_sentence["x1"], x)
                   current_sentence["y1"] = min(current_sentence["y1"], y)
                   current_sentence["x2"] = max(current_sentence["x2"], x + w)
                   current_sentence["y2"] = max(current_sentence["y2"], y + h)
               else:
                 sentence_blocks.append(current_sentence)
                 current_sentence = {
                    "text": text,
                    "x1": x,
                    "y1": y,
                    "x2": x + w,
                    "y2": y + h
                 }
               previous_y = y

           if current_sentence:
              sentence_blocks.append(current_sentence)
           
           final = []
           for sentence in sentence_blocks:
              final.append(sentence["text"])
              
           return printer("\n".join(final))
  
  
  elif splt[0] == "readScreen":
      if len(splt) > 2:
            closescript(text="readScreen uses only two arguments")
            return # stops running the function
        
      if len(splt) == 1:
            closescript(text="no language specified")
            return # stops running the function
  
      windowswdth_height() #get a screen shot of the screen with the computer actual width and height saved to resources/process/desktoprize.png
      data = surtr_ocr.screenread(language=splt[1], ocr_path=ocr_path, desktop_path=desktoprize_path)
               
      sentence_blocks = []
      current_sentence = None
      previous_y = None
      final = []
      for i in range(len(data['text'])):
          text = data['text'][i].strip()
          if text == "":
              continue
          x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

          if current_sentence is None:
             current_sentence = {
                "text": text,
                "x1": x,
                "y1": y,
                "x2": x + w,
                "y2": y + h
             }
             previous_y = y
          else:
            if abs(previous_y - y) < 10:  # Allow line tolerance
                   current_sentence["text"] += ' ' + text
                   current_sentence["x1"] = min(current_sentence["x1"], x)
                   current_sentence["y1"] = min(current_sentence["y1"], y)
                   current_sentence["x2"] = max(current_sentence["x2"], x + w)
                   current_sentence["y2"] = max(current_sentence["y2"], y + h)
            else:
                 sentence_blocks.append(current_sentence)
                 current_sentence = {
                    "text": text,
                    "x1": x,
                    "y1": y,
                    "x2": x + w,
                    "y2": y + h
                 }
            previous_y = y

      if current_sentence:
        sentence_blocks.append(current_sentence)
           
        
        for sentence in sentence_blocks:
          final.append(sentence["text"])
        
        if toreturn == False:      
           return printer("\n".join(final))
        else: 
           return printer("\n".join(final))
         
         
def windowswdth_height():
 #clear old images
 try:
    if os.path.exists(desktop_path):
      os.remove(desktop_path) 
    if os.path.exists(desktoprize_path):
      os.remove(desktoprize_path) 
    if os.path.exists(imgedit_path):
      os.remove(imgedit_path)
 except:
   pass
 
 try:  
   pyg.screenshot(desktop_path)
   width = int(GetSystemMetrics(0))
   height =int(GetSystemMetrics(1))
   img = Image.open(desktop_path)
   img = img.resize((width,height), Image.Resampling.LANCZOS)
   img.save(desktoprize_path) #If you are saving a .jpeg, use img.save('sompic.jpg', 'JPEG')
 except Exception as e:
   closescript(e,text="an error occured when getting system info")   
   return # stops running the function        

def read_screen_in_sentence(action, texts, findall="one",speed=2,language="eng"):
  try:  
    
    windowswdth_height()  # Your screenshot saver function
    ocr_out = surtr_ocr.read_screen_sentence(language=language,ocr_path=ocr_path, desktop_path=desktoprize_path)
    img = ocr_out[0]
    data = ocr_out[1]
    sentence_blocks = []
    current_sentence = None
    previous_y = None

    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if text == "":
            continue

        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

        if current_sentence is None:
            current_sentence = {
                "text": text,
                "x1": x,
                "y1": y,
                "x2": x + w,
                "y2": y + h
            }
            previous_y = y
        else:
            if abs(previous_y - y) < 10:  # Allow line tolerance
                current_sentence["text"] += ' ' + text
                current_sentence["x1"] = min(current_sentence["x1"], x)
                current_sentence["y1"] = min(current_sentence["y1"], y)
                current_sentence["x2"] = max(current_sentence["x2"], x + w)
                current_sentence["y2"] = max(current_sentence["y2"], y + h)
            else:
                sentence_blocks.append(current_sentence)
                current_sentence = {
                    "text": text,
                    "x1": x,
                    "y1": y,
                    "x2": x + w,
                    "y2": y + h
                }
            previous_y = y

    if current_sentence:
        sentence_blocks.append(current_sentence)

    # Scale correction (optional)
    screen_w, screen_h = pyg.size()
    img_h, img_w = img.shape[:2]
    scale_x = screen_w / img_w
    scale_y = screen_h / img_h
    findtext = False
    print(f"Looking for: {texts}")

    for sentence in sentence_blocks:
        if texts.lower() in sentence["text"].lower():
            findtext = True
            print(f"Found: {sentence['text']} <==> Coords: {sentence['x1']}, {sentence['y1']} to {sentence['x2']}, {sentence['y2']}")
            # Get scaled center position
            xpos = int((sentence["x1"] + sentence["x2"]) / 2 * scale_x)
            ypos = int((sentence["y1"] + sentence["y2"]) / 2 * scale_y)

            if action == "move":
                mousemove(x=xpos, y=ypos, speed=int(speed), file="no")

            if action == "drag":
                mousedrag(x = xpos, y = ypos, speed = int(speed),oneimg="no", file="no")
                  
            if action == "rightclick":
                  mousemove(x = xpos, y = ypos, speed = 0, file="no")
                  pyg.click(button='right', clicks=1, interval=0.25)
                  print("Right clicked mouse")
                        
            if action == "click":
                  mousemove(x = xpos, y = ypos, speed = 0, file="no")
                  pyg.click()
                  print("Clicked mouse")
                        
                        
            if action == "doubleclick":
                  mousemove(x = xpos, y = ypos, speed = 0, file="no")
                  pyg.doubleClick()
                  print("Double clicked mouse")
                        
            if action == "tripleclick":
                  mousemove(x = xpos, y = ypos, speed = 0, file="no")
                  mousepos = pyg.position() 
                  pyg.tripleClick(mousepos[0], mousepos[1])
                  print("Tripple clicked mouse")
                        
      
            if findall == "one":
                break

    if findtext == False:
          closescript(text=f"Text > {texts} < not found")
          return
  
  except Exception as e:
    closescript(e,text="Text OCR error")
    return     
  
  
def textloop(texts, command, language="eng"):
  try:
    windowswdth_height()  # Your screenshot function
    reader = surtr_ocr.read_screen_sentence(language=language, ocr_path = ocr_path, desktop_path = desktoprize_path)
    data = reader[1]
    img = reader[0]
    sentence_blocks = []
    current_sentence = None
    previous_y = None

    # Group words into lines/sentences
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if text == "":
            continue

        x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]

        if current_sentence is None:
            current_sentence = {
                "text": text,
                "x1": x,
                "y1": y,
                "x2": x + w,
                "y2": y + h,
                "words": [(text, x, y, x + w, y + h)]
            }
            previous_y = y
        else:
            if abs(previous_y - y) < 10:
                current_sentence["text"] += ' ' + text
                current_sentence["x1"] = min(current_sentence["x1"], x)
                current_sentence["y1"] = min(current_sentence["y1"], y)
                current_sentence["x2"] = max(current_sentence["x2"], x + w)
                current_sentence["y2"] = max(current_sentence["y2"], y + h)
                current_sentence["words"].append((text, x, y, x + w, y + h))
            else:
                sentence_blocks.append(current_sentence)
                current_sentence = {
                    "text": text,
                    "x1": x,
                    "y1": y,
                    "x2": x + w,
                    "y2": y + h,
                    "words": [(text, x, y, x + w, y + h)]
                }
            previous_y = y

    if current_sentence:
        sentence_blocks.append(current_sentence)

    screen_w, screen_h = pyg.size()
    img_h, img_w = img.shape[:2]
    scale_x = screen_w / img_w
    scale_y = screen_h / img_h

    search_text = texts.lower()
    findtext = False
    itervars = {}
    for sentence in sentence_blocks:
        sentence_text = sentence["text"].lower()

        if search_text in sentence_text:
            findtext = True
            start_index = sentence_text.index(search_text)
            end_index = start_index + len(search_text)

            char_count = 0
            found_coords = []

            for word, x1, y1, x2, y2 in sentence["words"]:
                word_len = len(word)
                word_start = char_count
                word_end = char_count + word_len

                overlap = max(0, min(word_end, end_index) - max(word_start, start_index))
                if overlap > 0:
                    found_coords.append((x1, y1, x2, y2))

                char_count += word_len + 1  # +1 for space

            if found_coords:
                min_x = min(c[0] for c in found_coords)
                min_y = min(c[1] for c in found_coords)
                max_x = max(c[2] for c in found_coords)
                max_y = max(c[3] for c in found_coords)

                # Compute scaled position
                cx = (min_x + max_x) / 2
                cy = (min_y + max_y) / 2
                w = max_x - min_x
                h = max_y - min_y
                itervars.clear()
                itervars["{{textx}}"] = str(min_x * scale_x)
                itervars["{{texty}}"] = str(min_y * scale_y)
                itervars["{{textwidth}}"] = str(w * scale_x)
                itervars["{{textheight}}"] = str(h * scale_y)
                itervars["{{textcenterx}}"] = str(cx * scale_x)
                itervars["{{textcentery}}"] = str(cy * scale_y)
                runiterate(command,itervars)
                

    itervars.clear()
    if findtext == False:
          closescript(text=f"Text > {search_text} < not found")
          return
  
  except Exception as e:
    closescript(e,text="Text OCR error")    
    return  
  

#credloader.encrypt_file(commandfile,commandfile)
#i want to decrypt our command data file so we can access it with getcmdbyte["bytes"]

try:
  decrp = credloader.decrypt_file(input_path=commandfile,save=False)
  getcmdbyte["bytes"] = decrp
  
except Exception as e:
  closescript(e,text="A fatal error occured surtr will shutdown in 10 seconds")
  time.sleep(10)
  os._exit(10)
#print(getcmdbyte["bytes"])

#credientials

''' 
{
    "password": "set",
    "securitypassword": "12345",
    "security": "active",
    "guest": "set",
    "verified": "no"
}

'''
#lets encrypt
#credloader.encrypt_file(input_path=ssm_path, output_path=ssm_path, text=False)
#os._exit(0)
#security variables

import winreg
          
def hash_guid():
    with winreg.OpenKey(
      winreg.HKEY_LOCAL_MACHINE,
      r"SOFTWARE\Microsoft\Cryptography"
    ) as key:
       wguid = winreg.QueryValueEx(key, "MachineGuid")[0] 
       # Use PBKDF2 with SHA-256, a fixed (empty) salt, and high iterations for security.
       # This keeps output deterministic (same input -> same output) with no per-user storage needed.
       # High iterations slow down brute-force attacks without affecting legitimate use much.
       salt = b'appproductguidforvalid$()&$#@bot_id.bot'  # Fixed salt; could be a hardcoded secret if you have one.
       iterations = 100000  # Adjust based on your performance needs (higher = more secure but slower).
       return hashlib.pbkdf2_hmac('sha256',wguid.encode('utf-8'), salt, iterations).hex()
     
          
      
try:
 ld = credloader.decrypt_file(input_path=ssm_path,save=False)
 decp = ld.decode()
 data = json.loads(decp)
 #print(data)

except Exception as e:
  closescript(e,text="A fatal error occured surtr will shutdown in 10 seconds")
  time.sleep(10)
  os._exit(10)
  

   
#all surtr commands
surtrcommands = {
    # mouse: Performs mouse functions including move, drag, click, rightClick, doubleClick, tripleClick, scroll, scrollH, and scrollV, supporting coordinate-based or image-based interactions.
    "mouse": """Performs mouse functions including move, drag, click, rightClick, doubleClick, tripleClick, scroll, scrollH, and scrollV, supporting coordinate-based or image-based interactions.

Examples:
- mouse move 100 200 5  ! Move to (100, 200) at speed 5
- mouse drag 300 400 5  ! Drag to (300, 400) at speed 5
- mouse click  ! Single left-click at current position
- mouse rightClick 500 600 0.5  ! Right-click at (500, 600) with 0.5s delay
- mouse scroll 5  ! Scroll down 5 units use negative -5 to scroll up
- mouse scrollH|scrollV 5 !Scroll vertically or horizontally 5 units""",
    
    # keyBoard: Simulates keyboard input, including typing text at a speed, pressing, holding, or releasing keys, with support for special variables like {{login}}, {{date}}, {{time}}.
    "keyBoard": """Simulates keyboard input, including typing text at a speed, pressing, holding, or releasing keys, with support for special variables like {{login}}, {{date}}, {{time}}.

Examples:
- keyBoard type 0.3 Hello, {{login}}! Today is {{date}}.  ! Type text with variables
- keyBoard hold ctrl  ! Hold Ctrl key
- keyBoard press c  ! Press C key
- keyBoard release ctrl  ! Release Ctrl key""",
    
    # clr: Clears the screen or shell output (inferred from category as clear screen command).
    "clr": """Clears the screen or shell output (inferred from category as clear screen command).

Examples:
- clr  ! Clear the screen""",
    
    # if: Executes commands based on conditions with logical operators like ?equ, ?nequ, ?cntn, ?grtn, ?lstn, supporting various commands for conditions.
    "if": """Executes commands based on conditions with conditional operators like ?equ, ?nequ, ?cntn, ?grtn, ?lstn, and logical operators ?and,?or supporting various commands for conditions.

Examples:
- if ( {{name}} ?equ john ) ?run msg Hi john! ?else msg not john!
- if  not ( 3 ?grtn 4 ) ?run emit too low

Switches with ctype:
- set {{ctype}} cmd|stmt  ! global switch 

- if ctype:cmd userInput Do you love Surtr? ?equ yes ?run msg Awesome! ?else msg Try it more!  ! Conditional with user input using inline switch
- if not seeImage save.png ?run msg Save button not found ?else click  ! Negative condition with image detection 

Note:
- the cmd statement switch does not support parentheses
- the cmd statement switch does not support logical operators """,

    #executes its commands as long as a specified condition remains True.
    "while":"""executes its commands as long as a specified condition remains True.
Examples:
- while msg ok ?run msg cool ! as long as the message returns true keep running the command 
    """,
    
    #executes its commands until a specified condition becomes True.
    "until":"""executes its commands until a specified condition becomes True.
Examples:
- until msg ok ?run msg cool  ! until the message returns true keep running the command   
    """,
    
    # ?run: Special argument used to run other commands in constructs like if, eachOnScreen, textOnScreen, splitRun.
    "?run": """Special argument used to run other commands in constructs like if, eachOnScreen, textOnScreen, splitRun.

Examples:
- if condition ?run msg Success  ! Run command if true
- eachOnScreen imagepath ?run command  ! Run for each image""",
    
    # ?else: Special argument used in if commands to specify actions when the condition is false.
    "?else": """Special argument used in if commands to specify actions when the condition is false.

Examples:
- if condition ?equ value ?run command ?else othercommand  ! Else action""",
    
    # not: Negates the condition in if statements.
    "not": """Negates the condition in if statements or other conditional commands.

Examples:
- if not command ?operator value ?run command ?else command  ! Negated condition
- emit ?exec "not msg 'is it true'" ! returns False if message is true or false otherwise 
- emit ?exec "not userInput username name ?equ micheal" ! if username is micheal return false or true otherwise """,

    # cwd: Handles the current working directory (inferred from category, likely retrieves or sets the cwd).
    "cwd": """Handles the current working directory (inferred from category, likely retrieves or sets the cwd).

Examples:
- cwd  ! Get current working directory""",
    
    # seeImage: Detects if an image is present on the screen, optionally in a specific region.
    "seeImage": """Detects if an image is present on the screen, optionally in a specific region.

Examples:
- seeImage imagepath  ! Check if image is found
- seeImage imagepath 100 100 300 300  ! Check in region""",
     
        # seeImage: Detects if an image is present on the screen, optionally in a specific region.
    
    #Convert text to lower case
    "textLower": """Convert text to lower case.

Examples:
- textLower WRITTEN IN LOWER CASE  ! Change to lower case """,

    
     #Convert text to upper case
    
    #Convert text to upper case
    "textUpper": """Convert text to upper case.

Examples:
- textUpper written in uppercase  ! Change to upper case """,

    #Convert text to base64 format
    "toBase64": """Convert text to base64 format.

Examples:
- toBase64 text  ! Change to base64 """,

    #Change base64 back to string
    "decodeBase64": """decode Base64 text.

Examples:
- decodeBase64 base64 text ! decode base64 """,
    
    #Check if a text starts with a specific text.
    "textStartWith": """Check if a text starts with a specific text.

Examples:
- textStartWith "this" this is my world  ! Check if text starts with this """,
    
    #Check if a text stops with a specific text.
    "textEndWith": """Check if a text ends with a specific text.

Examples:
- textEndWith "world" this is my world  ! Check if text ends with world """,

     
     #check if a text has a specific text
   
    #Check if a text has a specific text
    "textHas": """Check if a text has a specific text.

Examples:
- textHas "welcome" hello welcome everybody ! Check if welcome is in text """,

    #Check if a text or variable is empty 
    "empty": """Check if a text or variable is empty.

Examples:
- if empty {{emptyvariable}} ?run this is empty  ! Check if a variable is empty """,

    
    #Remove specific characters from a text
    "strip": """Remove specific characters from a text

Examples:
- strip "some" "let's write some script" ! Remove 'some' from text """,

    # eachOnScreen: Iterates over multiple instances of an image on the screen and executes a command for each, using variables like {{imageX}}, {{imageY}}.
    "eachOnScreen": """Iterates over multiple instances of an image on the screen and executes a command for each, using variables like {{imageX}}, {{imageY}}.

Examples:
- eachOnScreen textfile.png ?run move {{imageX}} {{imageY}} 5  ! Move to each instance""",
    
    # run: Executes external scripts, specific labels, or commands with arguments, supporting modular scripting.
    "run": """Executes external scripts, specific labels, or commands with arguments, supporting modular scripting.

Examples:
- run script.as  ! Run external script
- run label:  ! Run label in current script
- run script.as label  ! Run external script from label
- run processFiles: ?arg file1.txt file2.txt  ! Run with arguments""",
    
    # runCmd: Executes Windows Command Prompt (cmd) commands, with optional live output.
    "runCmd": """Executes Windows Command Prompt (cmd) commands, with optional live output.

Examples:
- runCmd dir  ! List directory contents
- runCmd live:yes dir /s  ! Live output of command""",
    
    "json": """Handles JSON data storage, retrieval, and modification of stored json. Supports nested paths with .[key] for dict keys (strings in brackets) and .0 for list indices (bare numbers). Values auto-type: JSON parses to dict/list/etc. Supports simple strings/numbers/bools/null.

Examples:
- json test {"a": "b", "list": [1, 2]}  ! Create/update 'test' with dict containing key and list
- json test  ! Retrieve and print entire 'test'
- json test.[a]  ! Retrieve value at 'test["a"]' (returns "b")
- json test.[list].0 42  ! Set index 0 of list to int 42 (list becomes [42, 2])
- json test.[newkey] hi  ! Set/add dict key "newkey" to string "hi"
- json test.[list].1 hello world  ! Set index 1 to string "hello world" (multi-word joined)
- json test true  ! Set to bool True
- json test.[key] null  ! Set to None""",
 
    #Retrieves and prints the length of a stored JSON value or nested path
    "lenJson": """Retrieves and prints the length of a stored JSON value or nested path.
Examples:
- lenJson test  ! Print length of entire 'test' (e.g., 2 for {"a": "b", "list": [1, 2]})
- lenJson test.[list]  ! Print length of array at 'test["list"]' (returns 2 for [1, 2])
- lenJson test.[a]  ! Print length of string at 'test["a"]' (returns 1 for "b")
- lenJson test.[list].0  ! Print length of value at index 0 of list (e.g., 1 if it's a string, or error if number)""",


    
    #Saves a specific JSON from jsonvariants to a file. Overwrites if exists
    "jsonSave": """Saves a specific JSON from stored json to a file. Overwrites if exists. Optional indentation.

Examples:
- jsonSave test output.json  ! Save 'test' to output.json (compact)
- jsonSave test pretty.json 2  ! Save with 2-space indent
- jsonSave missing save.json  ! Error: no json named 'missing'""",

     #Appends json to a stored json
    "jsonAppend": """Appends json to a stored json (List or Dict).

Examples:
- jsonAppend test [5, 6, 7, 8] ! Append list to json 'test' (if 'test' is a list)
- jsonAppend test.[mydict] {"name":"john"} ! Append dict to 'test["mydict"]' (if it's a dict)
- jsonAppend test 3 ! ! Append '3' to json 'test' (if 'test' is a list)
- jsonAppend test {"fish":"swim"} ! Append dict to json 'test' (if 'test' is a dict) """,


    #Parses provided JSON text and prints it (pretty for dict/list)
    "jsonParse": """Parses provided JSON text and returns output. Does NOT store outputs. Strict JSON only.

Examples:
- jsonParse {"key": "value", "arr": [1, 2]}  ! Parse and returns the output
- jsonParse "simple string"  ! Parse and returns the string
- jsonParse 42  ! Parse and returns the number
- jsonParse invalid  ! Error: invalid json 'invalid...'""",

    
    #Deletes a JSON entry or nested value.
    "jsonDelete": """Deletes a JSON entry or nested value.

Examples:
- jsonDelete test  ! Delete entire 'test' from jsonvariants
- jsonDelete test.[a]  ! Delete key "a" from 'test' dict
- jsonDelete test.[list].0  ! Delete index 0 from 'test["list"]'
- jsonDelete missing.[key]  ! Error: no json named 'missing' or path not found""",



    # quickRun: Executes a single command and terminates the script immediately.
    "quickRun": """Executes a single command and terminates surtr immediately.

Examples:
- quickRun msg Surtr completed the task!  ! Run and exit""",
    
    # end: Stops the script and exits Surtr cleanly.
    "end": """Stops the script and exits Surtr cleanly.

Examples:
- end  ! End script and close Surtr""",
    
    # stop: Stops the running script without exiting Surtr.
    "stop": """Stops the running script without exiting Surtr.

Examples:
- stop  ! Stop script""",
    
    # stopScript: Stops the running script without exiting Surtr (alias for stop).
    "stopScript": """Stops the running script without exiting Surtr (alias for stop).

Examples:
- stopScript  ! Stop script""",
    
    # exit: Stops the current running label without stopping the entire script.
    "exit": """Stops the current running label without stopping the entire script.

Examples:
- exit  ! Exit current label""",
    
    # wait: Pauses script execution for a specified number of seconds.
    "wait": """Pauses script execution for a specified number of seconds.

Examples:
- wait 5  ! Pause for 5 seconds""",
    
    # random: Generates random numbers or texts, with options for length and sources.
    "random": """Generates random numbers or texts, with options for length and sources.

Examples:
- random  ! Generate random number 0-9
- random len:5  ! Random number length 5
- random len:3 "text"  ! Random text length 3
- random len:3 text0 text1 text2  ! Random text text length 3
- random text0 text1 text2  ! Random from texts""",
    
    #display surtr commands.
    "define":""" display the functions of surtr commands with examples.
Examples:
- define ! display surtr commands and examples.
- define command ! display the function of a command with examples.""",
    
    #display the functions of surtr commands with examples (alias for define)
    "def":"""display the functions of surtr commands with examples (alias for define).
Examples:
- def ! display surtr commands and examples.
- def command ! display the function of a command with examples. """,

    #display all names of command that has contain a specific name.
    "define:name":"""display all names of command that has contain a specific name.
Examples:
- define:name say  ! display surtr commands that contain 'say' in their name. """,
     
     #display all surtr command names. 
    "define:nameList":"""display all surtr command names.
Examples:
- define:nameList  ! display all surtr command names. """,
   
   
    # say: Speaks text synchronously with specified voice, speed, and optional volume.
    "say": """Speaks text synchronously with specified voice, speed, and optional volume.

Examples:
- say voice-0 0 Welcome to Surtr!  ! Speak text
- say voice-0 0:50 Welcome  ! Speak with volume 50""",
    
    # talk: Speaks text or reads a file asynchronously, allowing other commands to run.
    "talk": """Speaks text or reads a file asynchronously, allowing other commands to run.

Examples:
- talk voice-1 0 notes.txt  ! Read file asynchronously""",

    "voices": """Lists available voices for say and talk commands.

Examples:
- voices  ! List available voices""",
    
    # talking: Returns true if a talk command is currently active.
    "talking": """Returns true if a talk command is currently active.

Examples:
- talking  ! Check if speaking""",
    
    # stopTalking: Stops any ongoing speech from talk or say.
    "stopTalking": """Stops any ongoing speech from talk or say.

Examples:
- stopTalking  ! Stop speech""",
    
    # ~~: Indicates the start of a comment line in scripts.
    "~~": """Indicates the start of a comment line in scripts.

Examples:
- ~~ This is a comment  ~~ Comment line""",
    
    # screenShot: Captures screenshots of the full screen, a region, or around the mouse.
    "screenShot": """Captures screenshots of the full screen, a region, or around the mouse.

Examples:
- screenShot desktop.jpg  ! Capture full screen
- screenShot 100 100 300 300 region.jpg  ! Capture region
- screenShot mouse 50 50 mouse_area.jpg  ! Capture around mouse""",
    
    # screenShotMonitor: Captures screenshots from a specific monitor, full screen, region, or around mouse.
    "screenShotMonitor": """Captures screenshots from a specific monitor, full screen, region, or around mouse.

Examples:
- screenShotMonitor 0 desktop.jpg  ! Full screen on monitor 0
- screenShotMonitor 2 100 100 300 300 region.jpg  ! Region on monitor 2
- screenShotMonitor 1 mouse 50 50 mouse_area.jpg  ! Around mouse on monitor 1""",
    
    # set: Sets a variable with a value,communicate with surtr error management, or customizes GUI elements like titles and buttons.
    "set": """Sets a variable with a value,communicate with surtr error management system,customizes GUI elements like titles and buttons.

Examples:
- set {{username}} JohnDoe  ! Set variable

Gui variables:
- set {{guititle}} My Title  ! Set GUI title
- set {{okbutton}} Yes  ! Set OK button text
- set {{cancelbutton}} No ! Customize Cancel button text.
- set {{guiboxposition}} <bottomright|bottomleft|topright|topleft|center> ! change the alertbox location

Error management variables:
- set {{onerror}} nostop ! dont stop script on error. You can also specify a label to execute on error
- set {{logerror}} file.log ! all errors to file,Warnings and information are not logged
- set {{showerror}} full ! show full error details. Use hide to suppress error dialogs

Error detail variables:
- {{errornumber}} ! error code
- {{errortext}} ! error message
- {{errorsource}} ! source of error. """,

    # resetEnvironment: Clears all variables and resets the environment.
    "resetEnvironment": """Clears all variables and resets the environment.

Examples:
- resetEnvironment  ! Clear variables and reset""",
    
    # get: Runs a command and stores its result in a variable.
    "get": """Runs a command and stores its result in a variable.

Examples:
- get {{inputs}} userInput Enter your name  ! Store user input
- get {{x}} getWindowX {{titlewindow}}  ! Store window X position""",
    
    # getValue: Retrieves the value of a variable for use in conditions or commands.
    "getValue": """Retrieves the value of a variable for use in conditions or commands.

Examples:
- getValue {{username}}  ! Get variable value
- if getValue {{errornumber}} ?equ 200 ?run msg File not found  ! Use in condition""",
    
    # msg: Displays an alert message.
    "msg": """Displays an alert message.

Examples:
- msg Hello, {{inputs}} !  ! Display message
- msg File not found: {{errortext}}  ! Error message""",
    
    # confirm: Displays a confirmation dialog returning true for OK, false for Cancel.
    "confirm": """Displays a confirmation dialog returning true for OK, false for Cancel.

Examples:
- confirm Proceed with deletion?  ! Confirmation prompt
- if confirm Proceed? ?run deleteFile data.txt  ! Use in if""",
    
    # userInput: Prompts the user for text input.
    "userInput": """Prompts the user for text input.

Examples:
- userInput Enter your email  ! Input prompt
- if userInput Enter email ?cntn @gmail.com ?run msg Valid!  ! Validate input""",
    
    # readImage: Reads text from an image using OCR, with options for processing mode and language.
    "readImage": """Reads text from an image using OCR, with options for processing mode and language.

Examples:
- readImage receipt.jpg <useBlackWhite|useGray> eng  ! Read English text from image""",
    
    # readImageLanguages: Lists available languages for OCR reading commands.
    "readImageLanguages": """Lists available languages for OCR reading commands.

Examples:
- readImageLanguages  ! List OCR languages""",
    
    # readScreen: Reads text from the entire screen using OCR.
    "readScreen": """Reads text from the entire screen using OCR.

Examples:
- readScreen eng  ! Read screen text in English""",
    
    # imageReader: Extracts and reconstructs text from an image using OCR with configurable layout and confidence.
"imageReader": """Extracts and reconstructs text from an image using OCR with configurable layout and confidence.

Examples:
- imageReader -image sample.png  ! Process an image with default settings
- imageReader -image receipt.png -lang eng -min-conf 40  ! Specify language and minimum confidence
- imageReader -image invoice.png -char-width 8 -line-height 20  ! Adjust layout reconstruction
- imageReader -image form.png -psm 6  ! Use page segmentation mode 6 for structured documents
- imageReader -image scan.png -transform gray|bw  ! Apply grayscale or black and white transformation before OCR
- imageReader -image receipt.png -psm 6 -char-width 8 -line-height 20 -save output.txt  ! Save output to a text file
- imageReader -image receipt.png -hide-output  ! Process silently without printing results
""",

    
    
    # moveToWord: Moves the mouse to the first or all instances of a word on the screen using OCR.
    "moveToWord": """Moves the mouse to the first or all instances of a word on the screen using OCR.

Examples:
- moveToWord one 5 eng Save  ! Move to first 'Save'
- moveToWord all 5 eng Edit  ! Move to all 'Edit'""",
    
    # dragToWord: Drags the mouse to the first or all instances of a word on the screen.
    "dragToWord": """Drags the mouse to the first or all instances of a word on the screen.

Examples:
- dragToWord one 5 eng Word  ! Drag to first 'Word'
- dragToWord all 5 eng Term  ! Drag to all 'Term'""",
    
    # rightClickWord: Right-clicks on the first or all instances of a word.
    "rightClickWord": """Right-clicks on the first or all instances of a word.

Examples:
- rightClickWord one eng Word  ! Right-click first 'Word'""",
    
    # ClickWord: Left-clicks on the first or all instances of a word.
    "ClickWord": """Left-clicks on the first or all instances of a word.

Examples:
- ClickWord one eng Word  ! Click first 'Word'""",
    
    # doubleClickWord: Double-clicks on the first or all instances of a word.
    "doubleClickWord": """Double-clicks on the first or all instances of a word.

Examples:
- doubleClickWord all eng Edit  ! Double-click all 'Edit'""",
    
    # tripleClickWord: Triple-clicks on the first or all instances of a word.
    "tripleClickWord": """Triple-clicks on the first or all instances of a word.

Examples:
- tripleClickWord one eng Word  ! Triple-click first 'Word'""",
    
    # moveToText: Moves the mouse to the first or all instances of specified text on the screen using OCR.
    "moveToText": """Moves the mouse to the first or all instances of specified text on the screen using OCR.

Examples:
- moveToText one 5 eng click this button  ! Move to text""",
    
    # dragToText: Drags the mouse to the first or all instances of specified text.
    "dragToText": """Drags the mouse to the first or all instances of specified text.

Examples:
- dragToText one 5 eng text here  ! Drag to text""",
    
    # textOnScreen: Runs a command on each instance of specified text found on the screen, saving details in variables like {{textx}}, {{texty}}.
    "textOnScreen": """Runs a command on each instance of specified text found on the screen, saving details in variables like {{textx}}, {{texty}}.

Examples:
- textOnScreen eng move run highlighter: ?arg {{textx}} {{texty}} {{textwidth}} {{textheight}}  ! Run on each 'move'""",
    
    # rightClickText: Right-clicks on the first or all instances of specified text.
    "rightClickText": """Right-clicks on the first or all instances of specified text.

Examples:
- rightClickText one eng text  ! Right-click text""",
    
    # ClickText: Left-clicks on the first or all instances of specified text.
    "ClickText": """Left-clicks on the first or all instances of specified text.

Examples:
- ClickText one eng text  ! Click text""",
    
    # doubleClickText: Double-clicks on the first or all instances of specified text.
    "doubleClickText": """Double-clicks on the first or all instances of specified text.

Examples:
- doubleClickText all eng click to open  ! Double-click all""",
    
    # tripleClickText: Triple-clicks on the first or all instances of specified text.
    "tripleClickText": """Triple-clicks on the first or all instances of specified text.

Examples:
- tripleClickText one eng text  ! Triple-click text""",
    
    # repeat: Executes a specified command a given number of times.
    "repeat": """Executes a specified command a given number of times.

Examples:
- repeat 3 msg Hello!  ! Display message 3 times""",
    
    # screenWidth: Retrieves the screen width and stores it as {{screenwidth}}.
    "screenWidth": """Retrieves the screen width and stores it as {{screenwidth}}.

Examples:
- screenWidth  ! Get screen width""",
    
    # screenHeight: Retrieves the screen height and stores it as {{screenheight}}.
    "screenHeight": """Retrieves the screen height and stores it as {{screenheight}}.

Examples:
- screenHeight  ! Get screen height""",
    
    # mousePositionX: Retrieves the current mouse X coordinate.
    "mousePositionX": """Retrieves the current mouse X coordinate.

Examples:
- mousePositionX  ! Get mouse X""",
    
    # mousePositionY: Retrieves the current mouse Y coordinate.
    "mousePositionY": """Retrieves the current mouse Y coordinate.

Examples:
- mousePositionY  ! Get mouse Y""",
    
    # mousePosition: Retrieves the current mouse position as text.
    "mousePosition": """Retrieves the current mouse position as text.

Examples:
- mousePosition  ! Get mouse position""",
    
    # fileman: Manages files and folders, including checking existence, reading/writing, deleting, listing content, etc.
    "fileman": """Manages files and folders, including checking existence, reading/writing, deleting, listing content, etc.

Examples:
- fileman fileExist data.txt  ! Check if file exists.
- fileman readFile data.txt  ! Read file contents.
- fileman writeFile file.txt content  ! Write to file.
- fileman deleteFile file.txt  ! Delete file.
- fileman appendFile filename content ! Append to a file.
- fileman deleteFile filename ! Delete a file or folder.
- fileman deleteFile filename -noerror ! Delete a file or folder does no stop on error.
- fileman startFile filename arguments ! starts a file or open a directory

- fileman copy|move <source> <destination> ! copies or moves a file or directory 
  flags:
  -retries 4 ! retry copy|move on error
  -skip-error ! do not end operation on error
  
- fileman isFile filename  ! check if path is a file
- fileman isFolder filename or fileman isDir filename !  check is path is a directory.
- fileman listContent foldername ! show content of a folder.
- fileman getType filename ! show file format.
- fileman getSize filename ! show the size of a file or folder.
- fileman newFolder foldername or fileman newDir foldername ! creates a new folder does nothing if folder exists.
- fileman absolutePath file|folder ! show an absolute path of the file or folder. """,
    
    # windowList: Lists all open windows.
    "windowList": """Lists all open windows.

Examples:
- windowList  ! List windows""",
    
    # focusWindow: Sets focus to a specified window.
    "focusWindow": """Sets focus to a specified window.

Examples:
- focusWindow Chrome  ! Focus on Chrome window""",
    
    # focusedWindow: Retrieves the name of the currently focused window.
    "focusedWindow": """Retrieves the name of the currently focused window.

Examples:
- focusedWindow  ! Get focused window""",
    
    # minimizeWindow: Minimizes a specified window.
    "minimizeWindow": """Minimizes a specified window.

Examples:
- minimizeWindow name  ! Minimize window""",
    
    # maximizeWindow: Maximizes a specified window.
    "maximizeWindow": """Maximizes a specified window.

Examples:
- maximizeWindow name  ! Maximize window""",
    
    # closeWindow: Closes a specified window.
    "closeWindow": """Closes a specified window.

Examples:
- closeWindow name  ! Close window""",
    
    # resetWindow: Resizes and repositions a specified window.
    "resetWindow": """Resizes and repositions a specified window.

Examples:
- resetWindow name 100 100 800 600  ! Reset window size and position""",
    
    # inWindowTitle: Finds and returns a window title containing the specified word.
    "inWindowTitle": """Finds and returns a window title containing the specified word.

Examples:
- inWindowTitle Chrome  ! Find window with 'Chrome' in title""",
    
    # getWindowX: Retrieves the X position of a window.
    "getWindowX": """Retrieves the X position of a window.

Examples:
- getWindowX title  ! Get window X""",
    
    # getWindowY: Retrieves the Y position of a window.
    "getWindowY": """Retrieves the Y position of a window.

Examples:
- getWindowY title  ! Get window Y""",
    
    # getWindowWidth: Retrieves the width of a window.
    "getWindowWidth": """Retrieves the width of a window.

Examples:
- getWindowWidth title  ! Get window width""",
    
    # getWindowHeight: Retrieves the height of a window.
    "getWindowHeight": """Retrieves the height of a window.

Examples:
- getWindowHeight title  ! Get window height""",
    
    # clipboardCopy: Copies text to the clipboard and stores as {{clipboard}}.
    "clipboardCopy": """Copies text to the clipboard and stores as {{clipboard}}.

Examples:
- clipboardCopy {{username}}  ! Copy variable to clipboard""",
    
    # clipboardPaste: Pastes the content from the clipboard.
    "clipboardPaste": """Pastes the content from the clipboard.

Examples:
- clipboardPaste  ! Paste clipboard""",

    #configure surtr session settings.
    "surtrset": """Configure surtr session settings.

Examples:
- surtrset <setting> <new value> ! Configure surtr settings""",
    
    # watchFile: Monitors a file for changes.
    "watchFile": """Monitors a file for changes.

Examples:
- watchFile filename  ! Monitor file""",
    
    # watchFolder: Monitors a folder for changes.
    "watchFolder": """Monitors a folder for changes.

Examples:
- watchFolder foldername  ! Monitor folder""",
    
    # watchStatus: Shows change status for monitored files or folders.
    "watchStatus": """Shows change status for monitored files or folders.

Examples:
- watchStatus filename  ! Show status for file
- watchStatus  ! Show all statuses""",
    
    # stopWatching: Stops monitoring a file or folder.
    "stopWatching": """Stops monitoring a file or folder.

Examples:
- stopWatching filename  ! Stop monitoring""",
    
    # changeDetected: Returns the number of changes detected for a monitored item.
    "changeDetected": """Returns the number of changes detected for a monitored item.

Examples:
- changeDetected filename  ! Get changes for file
- changeDetected ! show total changes for all monitored files""",
    
    # filesWatched: Lists all monitored files and folders.
    "filesWatched": """Lists all monitored files and folders.

Examples:
- filesWatched  ! List watched items""",
    
    # restoreFile: Restores a monitored file to its initial state.
    "restoreFile": """Restores a monitored file to its initial state.

Examples:
- restoreFile filename  ! Restore file""",
    
    # timerStart: Starts a background timer.
    "timerStart": """Starts a background timer.

Examples:
- timerStart  ! Start timer""",
    
    # timerStop: Stops the timer.
    "timerStop": """Stops the timer.

Examples:
- timerStop  ! Stop timer""",
    
    # timer: Retrieves the elapsed time in seconds.
    "timer": """Retrieves the elapsed time in seconds.

Examples:
- timer  ! Get elapsed time""",
    
    # pixelColor: Retrieves the color of a pixel at specified coordinates in RGB or hex.
    "pixelColor": """Retrieves the color of a pixel at specified coordinates in RGB or hex.

Examples:
- pixelColor 100 100 hex:yes  ! Get color in hex""",
    
    # waitPixelColor: Waits until a specific color appears at a pixel, with timeout.
    "waitPixelColor": """Waits until a specific color appears at a pixel (x,y), with timeout.

Examples:
- waitPixelColor 100 100 #FF0000 10  ! Wait for red 10 seconds""",
    
    # getPixelColorRegion: Retrieves all pixel colors in a specified region.
    "getPixelColorRegion": """Retrieves all pixel colors in a specified region.

Examples:
- getPixelColorRegion 100 100 200 200  ! Get region colors""",
    
    # colorExistsInRegion: Checks if specified colors exist in a region, from hex or file.
    "colorExistsInRegion": """Checks if specified colors exist in a region, from hex or file.

Examples:
- colorExistsInRegion 100 100 200 200 #FF0000  ! Check for red
- colorExistsInRegion 100 100 200 200 hexes.txt  ! Check from file""",
    
    # colorExistsInRegionSimilar: Checks for similar colors in a region with tolerance.
    "colorExistsInRegionSimilar": """Checks for similar colors in a region with tolerance.

Examples:
- colorExistsInRegionSimilar 100 100 200 200 10 #FF0000  ! Check similar red, tolerance 10""",
    
    # colorExistsInImage: Checks if specified colors exist in an image.
    "colorExistsInImage": """Checks if specified colors exist in an image.

Examples:
- colorExistsInImage image.png #FF0000  ! Check in image""",
    
    # colorExistsInImageSimilar: Checks for similar colors in an image with tolerance.
    "colorExistsInImageSimilar": """Checks for similar colors in an image with tolerance.

Examples:
- colorExistsInImageSimilar image.png 10 #FF0000  ! Check similar in image, tolerance 10""",
    
    # toPixel: Converts image to raw pixel data in RGB format.
    "toPixel": """Converts image to raw pixel data in RGB format.

Examples:
- toPixel image.png  ! Get RGB pixels""",
    
    # toHex: Converts image to raw pixel data in hex format.
    "toHex": """Converts image to raw pixel data in hex format.

Examples:
- toHex image.png  ! Get hex pixels""",
    
    # registerCommand: Registers a custom command that runs a script or label.
    "registerCommand": """Registers a custom command that runs a script or label.

Examples:
- registerCommand greet run welcome.as greet:  ! Register command""",
    
    # removeCommand: Removes a registered custom command.
    "removeCommand": """Removes a registered custom command.

Examples:
- removeCommand greet  ! Remove command""",
    
    # registeredCommand: Shows all registered custom commands.
    "registeredCommand": """Shows all registered custom commands.

Examples:
- registeredCommand  ! List registered commands""",
    
    # getEnv: Retrieves system information like OS, user, CPU usage, RAM, disk space, hostname.
    "getEnv": """Retrieves system information like OS, user, CPU usage, RAM, disk space, hostname.

Examples:
- getEnv os  ! Get OS name and version
- getEnv cpuUsage  ! Get CPU usage percentage
- getEnv ramFree  ! Get free RAM
- getEnv user ! Get current username.
- getEnv diskFree drive, getEnv diskTotal drive ! Get disk space (e.g., c:).
- getEnv hostname ! Get system hostname.""",    

    # setSecurityPassword: Sets a password for Surtr security.
    "setSecurityPassword": """Sets a password for Surtr security.

Examples:
- setSecurityPassword password  ! Set password""",
    
    # activateSecurity: Activates security mode (requires password set).
    "activateSecurity": """Activates security mode (requires password set).

Examples:
- activateSecurity  ! Activate security""",
    
    # deactivateSecurity: Deactivates security mode.
    "deactivateSecurity": """Deactivates security mode.

Examples:
- deactivateSecurity  ! Deactivate security""",
    
    # guestUser: Enables or disables guest mode for low-risk commands without password.
    "guestUser": """Enables or disables guest mode for low-risk commands without password.

Examples:
- guestUser on  ! Enable guest mode
- guestUser off  ! Disable guest mode""",
    
    # login: Log in to surtr when security is active (inferred from security features).
    "login": """Log in to surtr when security is active (inferred from security features).

Examples:
- login  ! Login <password>

You can logout any time using the > logout < command""",
    
    # splitRun: Splits text or file lines and runs a command on each part, saving in {{item}}.
    "splitRun": """Splits text or file lines and runs a command on each part, saving in {{item}}.

Examples:
- splitRun this is Surtr ?run msg {{item}}  ! Split and run on words
- splitRun splitfile.txt ?run msg {{item}}  ! Split file lines
- splitRun ?token B this is Surtr  ?run msg {{item}}  ! Split by token B""",
    
    # --version: Displays the version of Surtr.
    "--version": """Displays the version of Surtr.

Examples:
- --version  ! Show version""",
    
    # integer: Converts command output to integer (likely using ?int super argument).
    "integer": """Converts command output to integer.

Examples:
- integer command  ! Convert to integer """,
    
    #Replace a specified value with a value
    "replace": """Replace a specified value with a value.
Example:
- replace car boat "this is my car" ! replace car with boat """,

    #Records user keyboard and mouse actions and converts them into Surtr .as script format
    "startRecorder": """Records user keyboard,mouse actions and converts them into Surtr .as script format.
Example:
- startRecorder ! starts recording user actions
- startRecorder  filename.as ! save to filename.as
- startRecorder  filename.as 60 ! save to filename.as and stop recording after 60 seconds
- stopRecorder ! stop recording user actions """,

    #Records user keyboard and mouse actions and converts them into Surtr .as script format
    "stopRecorder": """stop recording user actions.
Example:
- stopRecorder ! stop recording user actions
- startRecorder ! starts recording user actions 
- startRecorder  filename.as ! save to filename.as """,




    # fetcher Universal web extraction and download utility
    "fetcher": """Universal web extraction and download utility, supporting fetch, download, JSON tasks, with options for methods, headers, proxies, etc.
fetcher [options]

Examples:
- fetcher  ! Launches interactive mode: prompts for URL, mode (fetch/download), etc.
- fetcher -fetch '["https://example.com","https://httpbin.org/json"]'  ! Inline URL array for text fetch
- fetcher -fetch '["url=https://example.com;parser=bs4;select=h1"] (https://example.com;parser=bs4;select=h1"])'  ! Shorthand with parser and selector
- fetcher -fetch-json tasks.json -save-json results.json  ! Batch from JSON file, save structured output
- fetcher -fetch '["https://example.com"] (https://example.com"])' -max-worker 5 -retries 3 -show-aggregated  ! Concurrent fetch with summary

fetch:
  Used for web page and API extraction. Supports plain URLs (full text), shorthand items (e.g., parser=bs4;select=h1), or explicit JSON objects with method/headers/body.

Options:
  -fetch [jsonlist]          Inline JSON array or shorthand items (e.g., '["url=...;parser=json"]').
  -fetch-json <file>         Load fetch tasks from JSON file.
  -save <file>               Save fetched plain text to file.
  -save-json <file>          Save fetched structured data to JSON.
  -show-aggregated           Show aggregated summary when all requests finish.
  -method <get|post|put|delete>  Override HTTP method.
  -headers <dict>                Custom headers (JSON-like dict, e.g., '{"Authorization":"Bearer TOKEN"}').
  -text-separator <string>       Separator between multiple text outputs (default: "\\n\\n-----\\n\\n").
  -result-separator <string>     Separator between full results (default: "\\n\\n######\\n\\n").Supported parsers: json, bs4, text.

Examples:
- fetcher -fetch '["url=https://example.com;parser=bs4;select=h1"] (https://example.com;parser=bs4;select=h1"])'  ! Extract H1 titles
- fetcher -fetch '["url=https://httpbin.org/json;parser=json"]'  ! Parse API JSON
- fetcher -fetch '[{"url":"https://api.example.com/search","method":"POST","headers":{"Auth":"token"},"body":{"q":"john"}}]'  ! POST with auth and body
- fetcher -fetch '["https://example.com"] (https://example.com"])' -save output.txt -text-separator "---"  ! Save text with custom separator
Note:
- The 'bs4' parser can accept raw html text syntax or a local html file path in the url field.
- The 'json' parser extracts JSON data from API responses.
- The 'text' parser returns full raw text content.
- The 'sbs4' stands for "strict bs4" and only accept http or https URLs.

fetch_download:
  Switches to download mode for files, audio, or video. Supports single URL or JSON batch with multi-threading for large files.

Options:
  -fetch-download            Perform direct download from arguments.
  -fetch-download-json <file> Use JSON configuration for downloads.
  -url <string>              Single URL for direct download mode.
  -saveto <string>           Save output file as given name.
  -split-download <num>      Enable segmented download with N parts.
  -chunk-size <num>          Per-read chunk size in bytes.
  -show-progress yes|no      Show live progress bar during download.
  -headers <dict>            Custom headers for download.
  -proxies <dict>            Proxy configuration (e.g., '{"http":"http://127.0.0.1:8080"} (http://127.0.0.1:8080"})').
Examples:
- fetcher -fetch-download -url https://example.com/file.zip -saveto file.zip  ! Simple download
- fetcher -fetch-download -url https://example.com/file.zip   ! Download and save to the downloads folder with original filename sent from the server
- fetcher -fetch-download -url https://example.com/bigfile.iso -saveto C:\\mypath ! Custom save path 
- fetcher -fetch-download -url https://example.com/bigfile.iso -saveto file.iso -split-download 6 -show-progress yes  ! Segmented with progress
- fetcher -fetch-download-json downloads.json  ! Batch from JSON: [{"url":"...","save_as":"...","download_parts":8}]
- fetcher -fetch-download -url https://example.com/video.mp4 -saveto video.mp4 -chunk-size 16384 -headers '{"Range":"bytes=0-"}'  ! Chunked with range header

advanced_options:
Global options for robustness and performance in both fetch and download.

Options:
  -max-worker <num>              Number of concurrent requests.
  -request-delays <float>        Delay between requests (seconds).
  -request-schedule [floats]     Custom schedule list, e.g. [0.0,5.0,10.0].
  -timeout <float>               Timeout per connection/request (seconds).
  -retries <num>                 Number of retry attempts on failure.
  -backoff-factor <float>        Backoff multiplier for retry delays.
  -rotate-user-agents yes|no     Enable random User-Agent rotation.
  -getdata                       Stream result to Surtr (-fetch only)
  -proxies <dict>                Proxy configuration (e.g., '{"https":"http://p1:port"} (http://p1:port"})').
  -headers <dict>                Custom headers (JSON-like).

Examples:
- fetcher -fetch '["https://example.com"] (https://example.com"])' -max-worker 5 -request-delays 2.0 -rotate-user-agents yes  ! Concurrent with delays and UA rotation
- get {{sitedata}} fetcher -fetch ["https://example.com"] -getdata  ! capture result to {{sitedate}}
- fetcher -fetch-download -url https://example.com/file -retries 3 -backoff-factor 1.5 -timeout 15 -proxies '{"http":"http://127.0.0.1:8080"} (http://127.0.0.1:8080"})'  ! Reliable download via proxy
- fetcher -fetch '["url1","url2"]' -request-schedule '[0,3,7]' -show-aggregated  ! Scheduled requests with summary

json_tasks:
Explicit JSON for advanced requests/downloads. Use with -fetch-json or -fetch-download-json. Items: plain URLs, shorthand strings, or full objects.

Simple URLs (fetch text):
- ["https://example.com", "https://httpbin.org/html"]

Compact Shorthand (fetch/parse):
- ["url=https://example.com;parser=bs4;select=div.article"] (https://example.com;parser=bs4;select=div.article"])

Explicit Fetch Objects:
- [{"url":"https://api.example.com/search","parser":"json","method":"GET","headers":{"Authorization":"Bearer TOKEN"},"queries":{"q":"john","limit":"5"}}]

POST with Body:
- [{"url":"https://api.example.com/submit","method":"POST","parser":"json","headers":{"Authorization":"Bearer TOKEN"},"body":{"name":"alice","score":42}}]

Save/Schedule/Retries:
- [{"url":"https://example.com","parser":"bs4","select":"div.article","save":"article.html","timeout":15,"retries":3,"delay":2.5}] (https://example.com","parser":"bs4","select":"div.article","save":"article.html","timeout":15,"retries":3,"delay":2.5}])

Simple Download:
- [{"url":"https://example.com/bigfile.zip","save_as":"bigfile.zip"}]

Segmented Download:
- [{"url":"https://example.com/large.mp4","save_as":"video.mp4","download_parts":6,"chunk_size":8192,"retries":2,"timeout":30,"show_progress":true,"proxies":{"http":"http://p1:port"}}]

Examples:
Create tasks.json with above, then: fetcher -fetch-json tasks.json -max-worker 3  ! Run batch fetch

For downloads: 
- fetcher -fetch-download-json dl.json ! Multi-part batch

interactive_mode: 
Running 'fetcher' without arguments enters guided mode for easy use.

Flow:
  |=[>>> fetcher
  fetcher — interactive starter
  Type 'exit' at any prompt to quit.

  Enter input mode:
  (1) Paste list,
  (2) Path to JSON file
  (3) Download file
  (4) Download using json
  ...Examples:fetcher  ! Interactive fetch: Prompts step-by-step for URL, mode, parser, options.
In mode: Enter JSON path for batch, or URL for single; it handles the rest interactively.""",




    
    # emit: Prints text to the shell with optional color modes, inline markers, or prompt.
    "emit": """Prints text to the shell with optional color modes, inline markers, or prompt.

Examples:
- emit Hello world  ! Print text
- emit:info Hello from emit  ! Info mode
- emit:error Something failed!  ! Error mode
- emit color magenta Custom text  ! Custom color
- emit:warn ?em-yellow Low battery  ! Warn with inline color""",
    
    # prompt: Prompts for user input in the shell.
    "prompt": """Prompts for user input in the shell.

Examples:
- prompt press enter to continue  ! Shell prompt""",
    
    # emit:prompt: Displays a prompt on the shell and waits for input using emit.
    "emit:prompt": """Displays a prompt on the shell and waits for input using emit.

Examples:
- emit:prompt This will display on shell and wait to get user input  ! Emit prompt"""
}

basic_safe_commands = [
    # GUI / DISPLAY
    "msg",               # Show a message box
    "confirm",           # Show a yes/no dialog
    "userInput",         # Get text input from user
    #PRINT COMMAND
    "emit",
    # BASIC MOUSE
    "mouse", #perform mouse functions
     
     #RANDOM
     "random",
     #REPLACE TEXT
     "replace",
    # CONDITIONS (SAFE USAGE)
    "if",
    #JSON
    "jsonParse",
    "lenJson",
    #TEXT COMMANDS
    "textLower",
    "textUpper",
    "textStartWith",
    "textEndWith",
    "textHas",
    "toBase64",
    "decodeBase64",
    "strip",
    #EMPTY TEXT CHECK
    "empty",
    #DEFINE COMMANDS
    "define",
    "def",
    # TIMING
    "wait",              # Wait for seconds
    "timerStart",        # Start timer
    "timerStop",         # Stop timer
    "timer",             # Read timer
    
    # VARIABLES
    "set",               # Set variable
    "get",               # Save command result to variable
    "getValue",          # Read variable content
    "resetEnvironment",  # Clear all variables

    # INFO COMMANDS
    "screenWidth",       # Get screen width
    "screenHeight",      # Get screen height
    "mousePosition",     # Get mouse position
    "mousePositionX",
    "mousePositionY",
    
    #iMMEDIATE RUN
    "quickRun",
    # COMMENT / STRUCTURE
    "~~",                 # Comment
    "repeat",            # Repeat a command
    "end",               # End script
    "stop",              # Stop script
    "stopScript",        # Stop without exiting
    "exit", #stop running labels
    #CURRENT WORKING DIRECTORY
    "cwd", 
    # SPEECH
    "say",               # Speak text
    "talk",              # Speak async
    "voices",            # List voices
    "talking",           # Check if still talking
    "stopTalking",       # Stop talking

    # BASIC SYSTEM INFO (READ-ONLY)
    "getEnv",         # OS info
    "login",
    #NUMBER
    "integer", #change float to integer
    #PROMPT ON SHELL
    "prompt",
    "emit:prompt",
    
    #VERSION
    "--version"
]


#this is the password function that asks for password and validates
def askpassword():
  global data
  if data["password"] == "set":
             cnt = 0
             correct = False
             while cnt < 5: #if the user input wrong password 5 times lock Surtr
               password = getpass.getpass("(:-]) Password >")
               passwordhash = hash_password(password)
               if data["securitypassword"] != passwordhash:
                  print("Incorrect password")
               else:
                  correct=True
                  break
               cnt += 1
             if not correct: # verify
                   while True:
                     input("Surtr is locked because of some security issue")
                   os._exit(100)


#this place handles security features saving,updating of values      
def surtrsecurity(splt):
  global data, logincnt
  #do not use security mode in script to avoide bruteforcing
  if onscript[0] == True:
    closescript(text="Surtr security features is not available in script mode")
    return
  else:
   try: 
    elseremove(splt)
    if splt[0] == "setSecurityPassword":
    
       if len(splt) > 1:   
         if " ".join(splt[1:]) == "None":
             closescript(text="Password type not accepted")
             return
         if " " in " ".join(splt[1:]) or " ".join(splt[1:]).isspace():
            closescript(text="Space not allowed!")
            return 
           
       #check if the user has a password
       askpassword()
            
       if len(splt) == 1: 
         data["securitypassword"] = "None"
         data["password"] = "notset"
       else:
         tohash = hash_password(" ".join(splt[1:]).strip())
         data["securitypassword"] = tohash
         data["password"] = "set"
       #save   and encrypt
       saver = json.dumps(data,indent=4)
       credloader.encrypt_file(saver,ssm_path,text=True)
       
       print("Secure password updated successfully")  
        
    elif splt[0] == "activateSecurity" or splt[0] == "deactivateSecurity":
         askpassword()
         if splt[0] == "activateSecurity":
            data["security"] = "active"
            
            if not data["password"] == "set":
                print("WARNING: no secure password found") 
            
         elif splt[0] == "deactivateSecurity":
               data["security"] = "notactive"
         
         saver = json.dumps(data,indent=4)
         credloader.encrypt_file(saver,ssm_path,text=True)
  
         print("Security updated")
            
    elif splt[0] == "guestUser":
       if not len(splt) == 2:
          closescript(text="Unsupported syntax. Expected: guestUser on/off")
          return
       askpassword()
       if splt[1] == "on":
          data["guest"] = "set"
              
       elif splt[1] == "off":
            data["guest"] = "notset"
       else:
          closescript(text="Unsupported syntax. Expected: guestUser on/off")
          return
       saver = json.dumps(data,indent=4)
       credloader.encrypt_file(saver,ssm_path,text=True)
       
       print("guest configurations updated")
    
    elif splt[0] == "login":
      #if already logged in
      if admin[0] == True:
          closescript(text="Already logged in")
          return     
      if len(splt) == 1:
        
        #first check if the user has a password
        if data["password"] == "set":
             cnt = 0
             correct = False
             while cnt < 5: #if the user input wrong password 5 times lock Surtr
               password = getpass.getpass("(:-]) Password >")
               tohash = hash_password(password.strip())
               if data["securitypassword"] != tohash:
                  print("Incorrect password")
               else:
                  correct=True
                  break
               cnt += 1
             if not correct: # verify
                   while True: #if not correct run an endless loop
                     input("Surtr is locked because of some security issue")
             else:
                admin[0] = True   
      else:
         tohash = hash_password(" ".join(splt[1:]).strip())
         if data["securitypassword"] != tohash:
              logincnt += 1
              if logincnt >= 5:
                while True: #if not correct run an endless loop
                     input("Surtr is locked because of some security issue")     
              closescript(text="Incorrect password")
              return
         else:
            admin[0] = True
            logincnt = 0
   except Exception as e:
    closescript(e,text="An error has occured")
    return


#handle guest mode
def guestmodevalidation(splt):
  if splt[0] in surtrcommands:
   if admin[0] == False:
     if not splt[0] in basic_safe_commands:
       print(f"You need to login to use the {splt[0]} command")
       getoptions(errorreturn = True)  
 
   
#login
def loginprompt():
      global data
      if data["security"] == "active" and data["guest"] != "set":
          askpassword()
          admin[0] = True
      elif data["security"] != "active":
          admin[0] = True 

def logoutfunc(splt):
      global data
      if len(splt) == 1 and splt[0] == "logout":
            if admin[0] != True:
                closescript(text="You do not have full control to use the logout command",errornumber="850")
                return
            if data["security"] != "active":
                print("WARNING: Security is not activated make sure Surtr security\nis activated if you want logout to be effective")  
            admin[0] = False
            print("logged out")
      else:
        closescript(text="logout command do not use arguments",errornumber="850")   
        return  
            
loginprompt()
            
            

   
def defaultvariable():
  global variants
  d = dt.datetime.now()
  d.strftime("%d %B %Y")
  variants.update({"{{date}}":d.strftime("%d %B %Y")})
  variants.update({"{{time}}":show_time()})
  variants.update({"{{login}}":os.getlogin()})
  variants.update({"{{screenwidth}}":str(GetSystemMetrics(0))})
  variants.update({"{{screenheight}}":str(GetSystemMetrics(1))})
  variants.update({"{{surtrpath}}":settings("surtrPath")})
  
#reset our error notifier variables
variants.update({"{{errornumber}}":"0"})
variants.update({"{{errortext}}":"No error reported"})  
variants.update({"{{errorsource}}":"Not yet available"})  
  
def variablesetup():
 global variants
 try: 
  variants.clear()
  defaultvariable()
 except Exception as e:
   closescript(e,text="variable environment setup error")
   return # stops running the function
   
variablesetup()
   

def updatedefaultvariable():
   global variants
   while not stop_event.is_set():
         time.sleep(1)
         defaultvariable()

threading.Thread(target=updatedefaultvariable,name="variable-updater",daemon=True).start()
        
def set_variables(splt):
 global variants
 try:
  elseremove(splt)
  if(len(splt) == 2):
    splt.append("") #add empty string
    #closescript(text="add a value to your variable")
    #return # stops running the function
  if(splt[1].startswith("{{") == False or splt[1].endswith("}}") == False):
    #print(splt)
    if (splt[1].startswith("{$") and splt[1].endswith("}")):
       closescript(text="Unresolved variable reference: " + splt[1] + ". Use {{variableName}}")
       return # stops running the function
    else:
       closescript(text="enclose your variable " + splt[1] + " with double braces eg. {{variablename}}")
       return # stops running the function
  
  blockedletters = [' ', '!', '"', '#', '$', '%', '&', "'", '(',
  ')', '*', '+', ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7',
  '8', '9', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '`',
  '|', '~']
  
  for x in splt[1]:
    for wd in blockedletters:
          if wd in x:
                closescript(text=f"Invalid character {wd}")
                return # stops running the function
                        
  if(len(splt[1]) == 4):
    closescript(text="invalid variable")
    return # stops running the function
  
  #lets add a variable
  #decrypt_file(sysvars_path, key, sysvars_path)
  # add a new variable
  #splt.pop(0) # remove set
  #splt.pop(0) # remove {{variable name}}
  if (splt[2] == "userInput"):
      name = userinputhandler(app,splt[3:])
      variants.update({splt[1]:name})
  else: 
      # Add quotes to elements with spaces
      #print(splt)
      processed_list = ' '.join(splt[2:])
      #processed_list = [
      #   f'"{item}"' if ' ' in item else item
      #   for item in splt[2:]
      #]
      # Join into a single string
      result = parsestringsnormally(processed_list)
      variants.update({splt[1]:result})
  #done adding our variables lets encriypt
  # encrypt_file(sysvars_path, key, sysvars_path)
 except Exception as e:
  # encrypt_file(sysvars_path, key, sysvars_path)
   closescript(e,text="cannot set variable")
   return # stops running the function
 
 

def iteratevariables(splt):   
    global variants

    # skip parsing once
    if dontparsevariable[0] is True:
        dontparsevariable[0] = False
        return splt

    # skip variable parsing for these commands
    if splt and splt[0] in ("set", "resetEnvironment", "get"):
        return splt

    try:
        leave = {
                "{$imageX}", "{$imageY}", "{$time}", "{$date}", "{$login}",
                "{$textx}", "{$texty}", "{$textwidth}", "{$textheight}",
                "{$textcenterx}", "{$textcentery}", "{$item}"
            }
        i = 0
        while i < len(splt):

            token = splt[i]

            # find {$variable} matches ONLY
            matches = re.findall(r"\{\$(.*?)\}", token)
            if matches:
                for match in matches:
                    raw = "{$"+ match +"}"
                    converted = f"{{{{{match}}}}}"

                    # only replace if exists in variants
                    if converted in variants:
                        token = token.replace(raw, variants[converted])
                    else:
                        if not raw in leave:
                           closescript(text=f"no available variable named {raw}")
                           return

            # update token after processing
            splt[i] = token
            i += 1
        
        return splt
    except Exception as e:
        closescript(e, text="cannot run command")
        return

 
def variables(splt):
    global variants

    # skip parsing once
    if dontparsevariable[0] == True:
        dontparsevariable[0] = False
        return
      
    splt = iteratevariables(splt) #parse for early variable
    
    #late parsing
    if "++" in splt: #if ++ in commands do not parse yet wait till it run single one by one before parsing vars
      return
    
    
    # ----------------------------------------
    # No divider "++" — normal single command
    # ----------------------------------------
    if not (splt[0] == "set" or splt[0] == "resetEnvironment" or splt[0] == "get"):
        try:
            i = 0
            leave = {
                "{{imageX}}", "{{imageY}}", "{{time}}", "{{date}}", "{{login}}",
                "{{textx}}", "{{texty}}", "{{textwidth}}", "{{textheight}}",
                "{{textcenterx}}", "{{textcentery}}", "{{item}}"
            }

            while i < len(splt):
                matches = re.findall(r"{{(.*?)}}", splt[i])
                if matches:
                    for match in matches:
                        var_name = f"{{{{{match}}}}}"
                        if var_name in variants:
                            splt[i] = splt[i].replace(var_name, variants[var_name])
                        elif var_name in leave:
                            pass
                        else:
                            closescript(text=f"no available variable named {var_name}")
                            return
                i += 1

        except Exception as e:
            closescript(e, text="cannot run command")
            return
 

  
#super arguments
def superargs(splt):
   try:
    """
    do not function if command dividers are in commands to allow iteration commands work correctly.
    Iterators like repeat and others may do something like ?calc "{{i}} + 1" and want it to 
    iterate if it was calculated before it even hit the repeat command the iteration will not work
    """
    if '++' in splt: 
          return
    i = 0
    splt = iteratevariables(splt) #parse for early variable
    while i < len(splt):
          
      if(splt[i] == "?calc"):
           calc = i + 1 # target the next index to calculate
           
           # Handle multi-token group: starts with '(' but doesn't end with ')'
           if splt[calc].startswith('(') and not splt[calc].endswith(')'):
              # First, find the end index without modifying the list yet
              findend = False
              end_index = calc
              while end_index < len(splt):
                if splt[end_index].endswith(')'):
                   findend = True
                   break
                end_index += 1
         
              if not findend:
                  closescript(text="unclosed text ')'")
                  return
        
              # Now collect and join the group (inclusive of closing ')')
              nxtcommand = splt[calc:end_index + 1]
              group_str = " ".join(nxtcommand)
              # Remove the old tokens
              del splt[calc:end_index + 1]
              # Insert the joined group back at calc
              splt.insert(calc, group_str[1:-1]) #remove '( )'
                 
           
           try:
              for v in variants:    
               if v in splt[calc]:
                 splt[calc] = splt[calc].replace(v, variants[v])  # Literal replace, no parsing
              result = sympify(f"{splt[calc]}")
              splt[calc] = str(result) 
              splt.pop(i)
           except Exception as e:
              closescript(e,text=f"super arguments error: error evaluating '{splt[calc]}'")
              return # stops running the function
                
      if(splt[i] == "?int"):
           calc = i + 1 # target the next index
           
           # Handle multi-token group: starts with '(' but doesn't end with ')'
           if splt[calc].startswith('(') and not splt[calc].endswith(')'):
              # First, find the end index without modifying the list yet
              findend = False
              end_index = calc
              while end_index < len(splt):
                if splt[end_index].endswith(')'):
                   findend = True
                   break
                end_index += 1
         
              if not findend:
                  closescript(text="unclosed text ')'")
                  return
        
              # Now collect and join the group (inclusive of closing ')')
              nxtcommand = splt[calc:end_index + 1]
              group_str = " ".join(nxtcommand)
              # Remove the old tokens
              del splt[calc:end_index + 1]
              # Insert the joined group back at calc
              splt.insert(calc, group_str[1:-1]) #remove '( )'
                 
           
           try:
              for v in variants:    
               if v in splt[calc]:
                 splt[calc] = splt[calc].replace(v, variants[v])  # Literal replace, no parsing
              result = sympify(f"{splt[calc]}")
              fl= float(result)
              
              splt[calc] = str(int(fl))
              splt.pop(i)
           except Exception as e:
              closescript(e,text=f"super arguments error: error converting '{splt[calc]}' to integer")
              return # stops running the function
      
      if(splt[i] == "?var"):
           calc = i + 1 # target the next index
           
           # Handle multi-token group: starts with '(' but doesn't end with ')'
           if splt[calc].startswith('(') and not splt[calc].endswith(')'):
              # First, find the end index without modifying the list yet
              findend = False
              end_index = calc
              while end_index < len(splt):
                if splt[end_index].endswith(')'):
                   findend = True
                   break
                end_index += 1
         
              if not findend:
                  closescript(text="unclosed text ')'")
                  return
        
              # Now collect and join the group (inclusive of closing ')')
              nxtcommand = splt[calc:end_index + 1]
              group_str = " ".join(nxtcommand)
              # Remove the old tokens
              del splt[calc:end_index + 1]
              # Insert the joined group back at calc
              splt.insert(calc, group_str[1:-1]) #remove '( )'
                 
           
           try:
              for v in variants:  
               if v in splt[calc]:
                 splt[calc] = splt[calc].replace(v, variants[v])  # Literal replace, no parsing
              splt.pop(i)
           except Exception as e:
              closescript(e,text=f"super arguments error: cannot look for variable in '{splt[calc]}'")
              return # stops running the function
                 
      if(splt[i] == "?exec"):
           calc = i + 1 # target the next index
           
           #if it starts with '(' and dod not ends with ')'
           
           # Handle multi-token group: starts with '(' but doesn't end with ')'
           if splt[calc].startswith('(') and not splt[calc].endswith(')'):
              # First, find the end index without modifying the list yet
              findend = False
              end_index = calc
              while end_index < len(splt):
                if splt[end_index].endswith(')'):
                   findend = True
                   break
                end_index += 1
         
              if not findend:
                  closescript(text="unclosed text ')'")
                  return
        
              # Now collect and join the group (inclusive of closing ')')
              nxtcommand = splt[calc:end_index + 1]
              group_str = " ".join(nxtcommand)
              # Remove the old tokens
              del splt[calc:end_index + 1]
              # Insert the joined group back at calc
              splt.insert(calc, group_str[1:-1]) #remove '( )' 
                 
                                     
           try:
              for v in variants:    
               if v in splt[calc]:
                  splt[calc] = splt[calc].replace(v, variants[v])  # Literal replace, no parsing 
                  
              shsp = shellspliter(splt[calc],firstcall=True)
              result = getcommandreturns(shsp,validate=False)
              psn = parsestringsnormally(result.strip())
              splt[calc] = psn
              splt.pop(i)
           except Exception as e:
              closescript(e,text=f"super arguments error: error executing '{splt[calc]}'")
              return # stops running the function
       
      if (splt[i] == "?raw"):
        calc = i + 1 # target the next index
        
        # Handle multi-token group: starts with '(' but doesn't end with ')'
        if splt[calc].startswith('(') and not splt[calc].endswith(')'):
            # First, find the end index without modifying the list yet
            findend = False
            end_index = calc
            while end_index < len(splt):
                if splt[end_index].endswith(')'):
                   findend = True
                   break
                end_index += 1
         
            if not findend:
              closescript(text="unclosed text ')'")
              return
        
            # Now collect and join the group (inclusive of closing ')')
            nxtcommand = splt[calc:end_index + 1]
            group_str = " ".join(nxtcommand)
            # Remove the old tokens
            del splt[calc:end_index + 1]
            # Insert the joined group back at calc
            splt.insert(calc, group_str[1:-1]) 
                 

        for v in variants:  
          if v in splt[calc]:
            splt[calc] = splt[calc].replace(v, variants[v])  # Literal replace, no parsing  
            #i avoid parsing strings here because of mismatch error (changing values before commands recognize them)
            #and that can cause misinterpretation in commands like set 
        #parse strings after working with variables which is more safer
        parsestring = parsestringsnormally(splt[calc])
        splt[calc] = parsestring
        splt.pop(i)
              
      if(splt[i].startswith("?str")):
           calc = i + 1 # target the next index
           
           # Handle multi-token group: starts with '(' but doesn't end with ')'
           if splt[calc].startswith('(') and not splt[calc].endswith(')'):
              # First, find the end index without modifying the list yet
              findend = False
              end_index = calc
              while end_index < len(splt):
                if splt[end_index].endswith(')'):
                   findend = True
                   break
                end_index += 1
         
              if not findend:
                  closescript(text="unclosed text ')'")
                  return
        
              # Now collect and join the group (inclusive of closing ')')
              nxtcommand = splt[calc:end_index + 1]
              group_str = " ".join(nxtcommand)
              # Remove the old tokens
              del splt[calc:end_index + 1]
              # Insert the joined group back at calc
              splt.insert(calc, group_str[1:-1]) #remove '( )'
                 
           try:
            if(splt[i] == "?str"): 
              
              for v in variants:  
                if v in splt[calc]:
                   splt[calc] = splt[calc].replace(v, variants[v])  # Literal replace, no parsing  
                   #i avoid parsing strings here because of mismatch error (changing values before commands recognize them)
                   #and that can cause misinterpretation in commands like set 
              #parse strings after working with variables which is more safer
              parsestring = parsestringsnormally(splt[calc],cli_parse=False) #parse special characters like \n
              splt[calc] = parsestring
              splt.pop(i)
            
            if(splt[i] == "?str-lower"): 
              for v in variants:  
                if v in splt[calc]:
                   splt[calc] = splt[calc].replace(v, variants[v])  # Literal replace, no parsing
                   #i avoid parsing strings here because of mismatch error (changing values before commands recognize them)
                   #and that can cause misinterpretation in commands like set 
              #parse strings after working with variables which is more safer
              parsestring = parsestringsnormally(splt[calc],cli_parse=False) #parse special characters like \n
              splt[calc] = parsestring.lower()
              splt.pop(i)
            
            if(splt[i] == "?str-upper"):
              for v in variants:  
                if v in splt[calc]:
                  splt[calc] = splt[calc].replace(v, variants[v])  # Literal replace, no parsing  
                  #i avoid parsing strings here because of mismatch error (changing values before commands recognize them)
                   #and that can cause misinterpretation in commands like set 
              #parse strings after working with variables which is more safer
              parsestring = parsestringsnormally(splt[calc],cli_parse=False) #parse special characters like \n
              splt[calc] = parsestring.upper()
              splt.pop(i) 
              
             
           except Exception as e:
              closescript(e,text=f"super arguments error: cannot parse '{splt[calc]}'")
              return # stops running the function
        
      i += 1 
      
   except Exception as e:
     closescript(e,text="An error occured while using superargs")
     return # stops running the function
#super arguments stop here
  
def resetallEnvironment():
    variablesetup()
    paramlist.clear()
    jsonvariants.clear()
    print("Cleaning up and refreshing...")
    try:
      if os.path.exists(readlogs_path):
        os.remove(readlogs_path)
      if os.path.exists(desktop_path):
         os.remove(desktop_path) 
      if os.path.exists(desktoprize_path):
         os.remove(desktoprize_path) 
      if os.path.exists(imgedit_path):
         os.remove(imgedit_path)
    except Exception as e:
      closescript(e,text="some temporary files cannot be removed")
      return # stops running the function
    #clear the cli screen multiple platform support
    os.system('cls' if os.name == 'nt' else 'clear')
 
#copying|moving starts here
def count_total_files(path: str) -> int:
    """Count total files in path (1 for files, sum for dirs)."""
    if not os.path.isdir(path):
        return 1
    total = 0
    for root, dirs, files in os.walk(path):
        total += len(files)
    return total

def count_total_size(path: str) -> int:
    """Count total size in path (getsize for files, sum for dirs)."""
    if not os.path.isdir(path):
        return os.path.getsize(path)
    total = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            total += os.path.getsize(os.path.join(root, file))
    return total

def format_size(size_bytes: int) -> str:
    """Format bytes to human-readable size."""
    if size_bytes == 0:
        return "0 B"
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    double_size = size_bytes
    while double_size >= 1024 and i < len(size_names) - 1:
        double_size /= 1024.0
        i += 1
    return f"{double_size:.1f} {size_names[i]}"

def copy_with_progress(
    src: str,
    dst: str,
    basename: str,
    size: int,
    current_num: int,
    total_files: int,
    rem_files: int,
    rem_size: int,
    retries: int,
    continue_on_error: bool,
    delay_seconds: float
) -> bool:
    """Copy file with byte-level progress and retries."""
    op_verb = "Copy"
    rem_str = f" ({rem_files} file(s), {format_size(rem_size)} rem)" if rem_files > 0 else ""
    print(f"{op_verb}ing file {current_num}/{total_files}{rem_str}: '{basename}' ({format_size(size)})")
    
    def print_progress(copied: int, total: int):
        percent = (copied / total * 100) if total > 0 else 0
        bar_length = 20
        filled_length = int(bar_length * copied / total) if total > 0 else 0
        bar = "#" * filled_length + "-" * (bar_length - filled_length)
        print(f"  [{bar}] {percent:.1f}% ({format_size(copied)}/{format_size(total)})", end='\r', flush=True)
    
    success = False
    for attempt in range(1, retries + 1):
        if attempt > 1:
            print(f"\n  Retrying attempt {attempt}/{retries}...")
            print_progress(0, size)  # Reset progress bar
        
        copied_bytes = 0
        try:
            with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                while True:
                    chunk = fsrc.read(1024 * 1024)  # 1MB chunks
                    if not chunk:
                        break
                    fdst.write(chunk)
                    copied_bytes += len(chunk)
                    print_progress(copied_bytes, size)
            
            print_progress(size, size)  # 100%
            print()  # New line after completion
            success = True
            break
        except Exception as e:
            if attempt == retries:
                print(f"\n  Failed after {retries} attempts: {e}")
                if not continue_on_error:
                    raise Exception(f"Failed to copy '{basename}': {e}") from e
                success = False
            else:
                time.sleep(delay_seconds)
    
    return success

def move_with_status(
    src: str,
    dst: str,
    basename: str,
    size: int,
    current_num: int,
    total_files: int,
    rem_files: int,
    rem_size: int,
    retries: int,
    continue_on_error: bool,
    delay_seconds: float
) -> bool:
    """Move file with status updates and retries (no byte progress, as it's atomic)."""
    op_verb = "Move"
    rem_str = f" ({rem_files} file(s), {format_size(rem_size)} rem)" if rem_files > 0 else ""
    print(f"{op_verb}ing file {current_num}/{total_files}{rem_str}: '{basename}' ({format_size(size)})")
    
    success = False
    for attempt in range(1, retries + 1):
        if attempt > 1:
            print(f"  Retrying attempt {attempt}/{retries}...")
        
        try:
            shutil.move(src, dst)
            print("  Completed")
            success = True
            break
        except Exception as e:
            if attempt == retries:
                print(f"  Failed after {retries} attempts: {e}")
                if not continue_on_error:
                    raise Exception(f"Failed to move '{basename}': {e}") from e
                success = False
            else:
                time.sleep(delay_seconds)
    
    return success

def safe_file_operation(
    src: Union[str, bytes, os.PathLike],
    dst: Union[str, bytes, os.PathLike],
    operation: str = 'copy',  # 'copy' or 'move'
    retries: int = 3,
    continue_on_error: bool = True,
    delay_seconds: float = 1.0
) -> bool:
    """
    Safely copies or moves a file or directory.
    
    - For 'move': Handles files or entire directories atomically with retries.
    - For 'copy': Handles files directly; for directories, recursively top-down (create outer folder first, then subdirs/files one by one) to allow per-file error skipping.
    
    Args:
        src: Source path.
        dst: Destination path.
        operation: 'copy' or 'move'.
        retries: Number of retry attempts (including initial).
        continue_on_error: If True, print error and skip/continue; else raise.
        delay_seconds: Delay between retries.
    
    Returns:
        True if successful, False if failed (only if continue_on_error=True).
    """
    if operation not in ['copy', 'move']:
        raise ValueError("operation must be 'copy' or 'move'")
    
    src_path = os.fspath(src)
    dst_path = os.fspath(dst)
    is_dir = os.path.isdir(src_path)
    
    total_files = count_total_files(src_path)
    total_size = count_total_size(src_path)
    print(f"Total to process: {total_files} files ({format_size(total_size)})\n")
    
    op_word = 'copied' if operation == 'copy' else 'moved'
    successful = 0
    errors = 0
    
    if operation == 'move' and is_dir:
        # Atomic directory move
        basename = os.path.basename(src_path)
        print(f"Moving directory: '{basename}' ({format_size(total_size)}, {total_files} files)")
        success = True
        for attempt in range(1, retries + 1):
            if attempt > 1:
                print(f"  Retrying attempt {attempt}/{retries}...")
            try:
                shutil.move(src_path, dst_path)
                print("  Completed")
                success = True
                break
            except Exception as e:
                if attempt == retries:
                    print(f"  Failed after {retries} attempts: {e}")
                    if not continue_on_error:
                        raise Exception(f"Failed to move directory: {e}") from e
                    success = False
                else:
                    time.sleep(delay_seconds)
        successful = total_files if success else 0
        errors = total_files - successful
    elif not is_dir:
        # Single file operation
        basename = os.path.basename(src_path)
        size = os.path.getsize(src_path)
        rem_files = 0
        rem_size = 0
        if operation == 'copy':
            success = copy_with_progress(src_path, dst_path, basename, size, 1, total_files, rem_files, rem_size, retries, continue_on_error, delay_seconds)
        else:
            success = move_with_status(src_path, dst_path, basename, size, 1, total_files, rem_files, rem_size, retries, continue_on_error, delay_seconds)
        successful = 1 if success else 0
        errors = 1 - successful
    else:
        # Recursive directory copy (only for copy; move is atomic above)
        os.makedirs(dst_path, exist_ok=True)
        # Collect all files and sizes for remaining calculations
        files_list = []
        sizes_list = []
        for root, _, files in os.walk(src_path):
            for file in files:
                full_path = os.path.join(root, file)
                files_list.append(full_path)
                sizes_list.append(os.path.getsize(full_path))
        
        if files_list:
            # Precompute cumulative sizes for remaining
            cumul_sizes = [0]
            for s in sizes_list:
                cumul_sizes.append(cumul_sizes[-1] + s)
            
            for idx, (src_file, size) in enumerate(zip(files_list, sizes_list)):
                basename = os.path.basename(src_file)
                rel_dir = os.path.relpath(os.path.dirname(src_file), src_path)
                dest_dir = os.path.join(dst_path, rel_dir) if rel_dir != '.' else dst_path
                os.makedirs(dest_dir, exist_ok=True)
                dst_file = os.path.join(dest_dir, basename)
                
                current_num = idx + 1
                rem_files = len(files_list) - current_num
                rem_size = total_size - cumul_sizes[current_num]
                
                file_success = copy_with_progress(src_file, dst_file, basename, size, current_num, total_files, rem_files, rem_size, retries, continue_on_error, delay_seconds)
                
                if file_success:
                    successful += 1
                else:
                    errors += 1
    
    overall_success = (errors == 0)
    not_op = total_files - successful
    percent = 100.0 if total_files == 0 else (successful / total_files * 100)
    
    # Professional summary (unchanged)
    sep_line = "-" * 60
    footer_line = "=" * 60
    
    print(f"\nOperation Summary — {operation.upper()}")
    print(f"Source      : {src_path}")
    print(f"Destination : {dst_path}")
    print(sep_line)
    print(f"Total Files              : {total_files}")
    print(f"Files {op_word}               : {successful}")
    print(f"Errors                   : {errors}")
    print(f"Files not {op_word}           : {not_op}")
    print(f"Success Rate             : {percent:.1f}%")
    print(footer_line)
    
    return overall_success

# Example usage:
# safe_file_operation('/path/to/source_dir', '/path/to/dest_dir', operation='copy', continue_on_error=True)  # Recursive top-down copy
# safe_file_operation('/path/to/source_dir', '/path/to/dest_dir', operation='move', retries=2)  # Atomic move
# safe_file_operation('/path/to/source.txt', '/path/to/dest.txt', operation='copy')  # Single file


#copying|moving ends here


def get_folder_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            # Ensure it’s a real file (not broken symlink, etc.)
            if os.path.isfile(file_path):
                total_size += os.path.getsize(file_path)
    return total_size   

def folder_delete_error():
      pass

def filemanager(fileoptn):
  try:    
    if fileoptn[0] == "fileExist":
          if not len(fileoptn) == 2:
            closescript(text="Unsupported syntax. Expected: fileman <fileExist> <filename>")
            return # stops running the function
          
          if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
              returner[0] = False
          if os.path.exists(fileoptn[1]):
            return True
          else:
            return False
          
    elif fileoptn[0] == "readFile":
          if not len(fileoptn) == 2:
            closescript(text=f"Unsupported syntax. Expected: fileman readFile <filename>") 
            return # stops running the function
          
          try:
            f = open(fileoptn[1], "r")
            return printer(f.read())
          except Exception as e :
            closescript(e,text=f"cannot read {fileoptn[1]}")
            return # stops running the function
          
    elif fileoptn[0] == "writeFile": 
          try:
            #we are using bytes to pass errors in some texts using different encoding
            f = open(fileoptn[1], "wb")
            opt = "?else"
            if opt in fileoptn:
             e = fileoptn.index(opt) - 1
             wr = fileoptn[2:]
             psn = parsestringsnormally(" ".join(wr[:e]))
             f.write(psn.encode("utf-8"))  #write in bytes 
            else:
             psn = parsestringsnormally(" ".join(fileoptn[2:]))
             f.write(psn.encode("utf-8"))     
          except Exception as e :
            closescript(e,text=f"cannot write to {fileoptn[1]}")
            return # stops running the function
            
    elif fileoptn[0] == "appendFile":
          try:
            #we are using bytes to pass errors in some texts using different encoding
            f = open(fileoptn[1], "ab")
            f.write("\n".encode("utf-8"))
            opt = "?else"
            if opt in fileoptn:
              e = fileoptn.index(opt) - 1
              wr = fileoptn[2:]
              psn = parsestringsnormally(" ".join(wr[:e]))
              f.write(psn.encode("utf-8"))
            else:
              psn = parsestringsnormally(" ".join(fileoptn[2:]))
              f.write(psn.encode("utf-8")) 
              
          except Exception as e :
            closescript(e,text=f"Err: cannot add to {fileoptn[1]}")
            return # stops running the function
        
    elif fileoptn[0] == "deleteFile":
          try:  
           if os.path.exists(fileoptn[1]):
                  if os.path.isfile(fileoptn[1]):
                     os.remove(fileoptn[1]) 
                     
                  if os.path.isdir(fileoptn[1]):
                        if len(fileoptn) > 2 and fileoptn[2] == "-noerror": #if the user doesn't want to stop at an error
                           shutil.rmtree(fileoptn[1],folder_delete_error)
                        else:
                           shutil.rmtree(fileoptn[1])
           else:
              closescript(text="File not exist",errornumber="200") 
              return
          except Exception as e:
            if len(fileoptn) > 2 and fileoptn[2] == "-noerror" : #if the user doesnt want to show errors at an error
                return
            else:
              closescript(e,text=f"Err: cannot delete {fileoptn[1]} {e}")
              return 
   
    elif fileoptn[0] == "startFile":
      try:
        if len(fileoptn) == 2:
          os.startfile(filepath=fileoptn[1])
        elif len(fileoptn) >= 3:
            os.startfile(filepath=fileoptn[1],arguments=" ".join(fileoptn[2:]))
        else:
             closescript(text="Unsupported syntax. Expected:  fileman startFile <filename> <arguments>")  
             return
           
      except Exception as e:
         closescript(e,text="Error starting file")  
         return
    
    elif fileoptn[0]  == "isFile":
      if (len(fileoptn) != 2 ):
            closescript(text="Unsupported syntax. Expected: fileman <isFile> <filename>")
            return
      else:
         if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
              returner[0] = False
         if os.path.isfile(fileoptn[1]):
            return True
         else:
            return False   
              
    elif fileoptn[0] == "isFolder" or fileoptn[0] == "isDir":
      if (len(fileoptn) != 2 ):
            closescript(text="Unsupported syntax. Expected: fileman <isFolder|isDir> <foldername>")
            return
      else:
         if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
              returner[0] = False
         if os.path.isdir(fileoptn[1]):
            return True
         else:
            return False
            
    elif fileoptn[0]  == "listContent":
      if (len(fileoptn) != 2 ):
            closescript(text="Unsupported syntax. Expected: fileman <listContent> <folder>")
            return
      else:
         if os.path.isdir(fileoptn[1]):
            content = os.listdir(fileoptn[1])
            return printer("\n".join(content))
         else:
            closescript(text="fileman error: use a correct directory path")
            return 
          
    elif fileoptn[0]  == "getType":
      if (len(fileoptn) != 2 ):
            closescript(text="Unsupported syntax. Expected: fileman <getType> <file>")
            return
      else:
         if os.path.isfile(fileoptn[1]):
             get_text = Path(fileoptn[1]).suffix
             return printer(get_text)
         else:
            closescript(text="fileman error: use correct file path")
            return  
           
    elif fileoptn[0]  == "getSize":
         if (len(fileoptn) != 2 ):
            closescript(text="Unsupported syntax. Expected: fileman <getSize> <file|folder>")
            return
         else:
           if os.path.isfile(fileoptn[1]):
              fsize = os.path.getsize(fileoptn[1])
           elif os.path.isdir(fileoptn[1]):
              fsize = get_folder_size(fileoptn[1])
           else:
              closescript(text="fileman error: check if your file path is correct")
              return
            
           return printer(fsize)
    
    elif fileoptn[0]  == "absolutePath":
        if (len(fileoptn) != 2 ):
            closescript(text="Unsupported syntax. Expected: fileman <absolutePath> <file|folder>")
            return
        else:
           fabs = os.path.abspath(fileoptn[1])
           return printer(fabs)
         
    elif fileoptn[0] == "newFolder" or fileoptn[0] == "newDir":
      if (len(fileoptn) != 2 ):
            closescript(text="Unsupported syntax. Expected: fileman <newFolder|newDir> <foldername>")
            return
      else:
        try:
          os.makedirs(fileoptn[1],exist_ok=True) 
        except Exception as e:
          closescript(e,text=f"Cannot create folder {fileoptn[1]}")  
          return
     
    elif fileoptn[0] in ("copy","move"):
      try:
          rtry = None
          nostop = False
          work = fileoptn[0]
          srce = fileoptn[1]
          dest = fileoptn[2]
          if ("-retries" in fileoptn):
            ind = fileoptn.index("-retries") + 1 
            rtry = int(ind)
          if ("-skip-error" in fileoptn):
            nostop = True
            
          if rtry is None:
              rtry = 2
              
          safe_file_operation(srce, dest, operation=work, retries=rtry, continue_on_error=nostop)   
      
      except Exception as e:
        closescript(e,text="fileman error: cannot launch operation")
        return
      
    else:
      closescript(text="fileman error: Unknown argument\nSupported arguments fileExist,readFile,writeFile,appendFile,deleteFile,startFile,isFile,isFolder,listContent,getType,getSize")
      return
  
  except Exception as e:
    closescript(e,text="fileman error: cannot run command") 
    return 
  
       
def list_windows(caller=True):
    def callback(hwnd, windows):
        if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd):
            windows.append((hwnd, win32gui.GetWindowText(hwnd)))
    windows = []
    win32gui.EnumWindows(callback, windows)
    if caller == True:
        return windows
    else:
      extract = []
      for i in windows:
         extract.append(i[1])
         #print(extract)
      return printer("\n".join(extract))
    
def find_window(title_part):
    for hwnd, title in list_windows():
        if title_part.lower() in title.lower():
            return hwnd
    return None
  
def focus_window(title_part):
    hwnd = find_window(title_part)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)  # Restore if minimized
        win32gui.SetForegroundWindow(hwnd)
        return printer(f"focused {title_part}")
    return printer("focus failed")
 
def maximize_window(title_part):
    hwnd = find_window(title_part)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
        return printer(f"maximized {title_part}")
    return printer("maximize failed")

def close_window(title_part):
    hwnd = find_window(title_part)
    if hwnd:
        win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
        return printer(f"closed {title_part}")
    return printer(f"close failed")


def minimize_window(title_part):
    hwnd = find_window(title_part)
    if hwnd:
        win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
        
        return printer(f"minimized {title_part}")
    return printer(f"minimize failed")

def move_resize_window(title_part, x, y, width, height):
    hwnd = find_window(title_part)
    if hwnd:
        win32gui.MoveWindow(hwnd, x, y, width, height, True)
        return printer(f"reset successful")
    return printer(f"reset failed")


def windowcommand(splt):
 try:
  if splt[0] == "windowList":
       if not len(splt) == 1:
             closescript(text="windowList does not support arguments")
             return # stops running the function
       return list_windows(False)
     
  elif splt[0] == "inWindowTitle":
   if not len(splt) == 2:
         closescript(text="inWindowTitle takes only one argument")
         return # stops running the function
       
   def get_visible_window_titles():
     titles = []
     def callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title.strip():
                titles.append(title)

     win32gui.EnumWindows(callback, None)
     return titles
  
   for title in get_visible_window_titles():
      if splt[1] in title:
          return printer(title)
   return printer(f"no title has {splt[1]}")
 
  elif splt[0] == "focusWindow":
      if not len(splt) == 2:
             closescript(text="Unsupported syntax. Expected: <focusWindow> <window name>")
             return # stops running the function
      #Focus a window (activate/bring to front)
      return focus_window(splt[1])
    
  elif splt[0] == "focusedWindow":
      if not len(splt) == 1:
            closescript(text="focusedWindow does not support arguments")
            return # stops running the function
          
      hwnd = win32gui.GetForegroundWindow()  # Get handle of the focused window
      title = win32gui.GetWindowText(hwnd)   # Get window title
      return printer(title)

  elif  splt[0] == "minimizeWindow":
      if not len(splt) == 2:
             closescript(text="Unsupported syntax. Expected: <minimizeWindow> <window name>")  
             return # stops running the function
                    
      return minimize_window(splt[1])
      
  elif splt[0] == "maximizeWindow":
    if not len(splt) == 2:
             closescript(text="Unsupported syntax. Expected: <maximizeWindow> <window name>")
             return # stops running the function
           
    return maximize_window(splt[1])
  
  elif splt[0] == "resetWindow":
        if not len(splt) == 5:
             closescript(text="Unsupported syntax. Expected: <resetWindow> <window name> x y width height")
             return # stops running the function
           
        return move_resize_window(splt[1],int(float(splt[2])),int(float(splt[3])),int(float(splt[4])),int(float(splt[5])))
          
  elif splt[0] == "closeWindow":
        if not len(splt) == 2:
             closescript(text="Unsupported syntax. Expected: <closeWindow> <window name>")
             return # stops running the function
        close_window(splt[1])
      
 except Exception as e:
    closescript(e,text="something went wrong")
    return # stops running the function
  
def windowsize(splt):
   
   def get_window_info(title_match: str):
        def callback(hwnd, results):
         if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if title_match.lower() in title.lower():
                rect = win32gui.GetWindowRect(hwnd)
                x, y, x2, y2 = rect
                width = x2 - x
                height = y2 - y
                results.append((title, x, y, width, height))

        found_windows = []
        win32gui.EnumWindows(callback, found_windows)
    
        if found_windows:
          for info in found_windows:
            if splt[0] == "getWindowX":
                  return printer(info[1])
            elif splt[0] == "getWindowY":
                  return printer(info[2])
            elif splt[0] == "getWindowWidth":
                  return printer(info[3])
            elif splt[0] =="getWindowHeight":
                  return printer(info[4])
        else:
          return printer(f"No window found with '{title_match}'")

      # Replace with part of your target window's title
   
   return get_window_info(" ".join(splt[1:]))


watchlist = {"files":[],"folders":[],"status":""}
change = []
fileholder = []
reloadwatch = [False]
filesbackup = {}

class FileOrFolderHandler(FileSystemEventHandler):
    def __init__(self, target_path, is_file=True):
        super().__init__()
        self.target_path = os.path.abspath(target_path)
        self.is_file = is_file

    def on_any_event(self, event):
        d = dt.datetime.now()
        d.strftime("%d %B %Y")
        udate = d.strftime("%d %B %Y")
        utime = show_time()
        event_path = os.path.abspath(event.src_path)
        if self.is_file:
            if event_path == self.target_path:
                #print(f"[{event.event_type.upper()}] {event_path}")
                logger = f"{event_path},{udate} {utime} {event.event_type.upper()}"
                
                if not watchlist["status"].endswith(logger): # to avoide duplicate logs
                  change.append(event_path)
                  watchlist.update({"status":f"{watchlist['status']}\n{logger}"})
        else:
            if event_path.startswith(self.target_path):
                #print(f"[{event.event_type.upper()}] {event_path}")
                logger = f"{event_path},{udate} {utime} {event.event_type.upper()}"
                
                if not watchlist["status"].endswith(logger): # to avoide duplicate logs
                  change.append(event_path)
                  watchlist.update({"status":f"{watchlist['status']}\n{logger}"})

def start_watch():
    global watchlist
    global reloadwatch
    global fileholder
    global change
    
    for p in fileholder:
      abs_path = os.path.abspath(p)
      if os.path.isfile(abs_path):
        handler = FileOrFolderHandler(abs_path, is_file=True)
        folder_to_watch = os.path.dirname(abs_path)
        
        #observer = Observer()
        #observer.schedule(handler, path=folder_to_watch, recursive=(mode == 'watchfolder'))
        #observer.start()
        observer = Observer()
        observer.schedule(handler, path=folder_to_watch, recursive=False) 
        observer.start()
        #print(f"Watching {abs_path}")
        
      if os.path.isdir(abs_path):
        handler = FileOrFolderHandler(abs_path, is_file=False)
        folder_to_watch = abs_path
      
        observer = Observer()
        observer.schedule(handler, path=folder_to_watch, recursive=True) # recursive will be true it is a folder
        observer.start()
        #print(f"Watching {abs_path}")
        
      else:
        continue
      

    try:
        while not stop_event.is_set():
            time.sleep(1)
            if reloadwatch[0] == True:
                reloadwatch[0] = False
                #observer.stop()
                start_watch()
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()
    #observer.join() #uncomment this if the watch command stops working

    
def addwatch(file, remove=False):
      apth = os.path.abspath(file)
      if remove == True:
            fileholder.remove(file)
            if os.path.isfile(file): # save a copy of the file for the restoreFile command
              
              if apth in filesbackup:
                filesbackup.pop(apth)
              
            reloadwatch[0] = True
      else:
       if file in fileholder:
             closescript(text=f"{file} is being watched already")
             return # stops running the function
       fileholder.append(file)
       
       if settings("autoBackupFileOnWatch") == "yes": #backup if the user allows it in settings
        if os.path.isfile(file): # save a copy of the file for the restoreFile command
          try:
           rd = open(apth,"rb")
           filesbackup.update({apth:rd.read()})
           rd.close()
          except Exception as e:
            print(f"Warning restoreFile command may not work for this file {e}")
            reloadwatch[0] = True
            
       reloadwatch[0] = True

 
threading.Thread(target=start_watch, daemon=True).start()

  
def watcher(splt):
    if len(splt) != 2:
      closescript(text="Unsupported syntax. Expected: watchFile <filename> or watchFolder <foldername>")
      return # stops running the function
    
    #mode = splt[0]
    #target = splt[1]
    #start_watch(mode, target)
    if splt[0] == "watchFile" or splt[0] == "watchFolder":
      if splt[0] == "watchFile":
            if os.path.isfile(splt[1]) == False:
                 closescript(text=f"{splt[1]} is not a file")
                 return # stops running the function
                 
            elif splt[0] == "watchFolder":
              if os.path.isdir(splt[1]) == False:
                 closescript(text=f"{splt[1]} is not a folder") 
                 return # stops running the function
               
      if os.path.exists(splt[1]): # add to watch list
        addwatch(splt[1])
      else:
        closescript(text=f"{splt[1]} path not exist!")
        return # stops running the function
      
      
      
    elif splt[0] == "stopWatching":
          if splt[1] in fileholder:
            addwatch(splt[1], True)   
          else:
            closescript(text=f"error {splt[1]} is not being watched")    
            return # stops running the function
          
def viewwatched(splt):
   if splt[0] == "watchStatus":
          if len(splt) == 2:
            divide = watchlist["status"].split("\n")
            divideget = []
            for d in divide:
                  if splt[1] in d:
                        divideget.append(d)
            return printer("\n".join(divideget))
            
          elif len(splt) == 1:
            return printer(watchlist["status"])
          
   elif splt[0] == "filesWatched":
        return printer("\n".join(fileholder))
         
   elif splt[0] == "changeDetected":
     if len(splt) == 1:
          return printer(str(len(change)))
     elif len(splt) == 2:
       abspth = os.path.abspath(splt[1])
       i = 0
       for c in change:
          if abspth in c :
            i += 1 
       return printer(str(i))   
    
   elif splt[0] == "restoreFile":
     if len(splt) != 2:
       closescript(text="Unsupported syntax. Expected: restoreFile <filename>")
       return # stops running the function
     
     if os.path.isdir(splt[1]):
       closescript(text="Restoring folders is not supported")
       return # stops running the function 
      
     try:
      if settings("autoBackupFileOnWatch") != "yes": #do not run restore if the user disabled it in the configuration file
        closescript(text="You turned off file backup in the Surtr configuration file")
        return
      ap = os.path.abspath(splt[1])
      for r in filesbackup:
         if r == ap:
            wr = open(ap, "wb")
            wr.write(filesbackup[r]) 
            wr.close()
            return printer(f"Restored one file {r}")
      closescript(text="the file is not being watched")
      return # stops running the function
    
     except Exception as e:
       closescript(e,text="something went wrong")
       return # stops running the function
     
       
       
#timers
timerstop = [False]
timeindex = 0
def timercount():
    global timerstop
    global timeindex
    timeindex = 0
    while timerstop[0] != True:
      time.sleep(1)
      timeindex += 1
    timerstop[0] = False
    
def timertrigger(splt):
     if splt[0] == "timerStart":
       timerstop[0] = True
       time.sleep(1) # wait for thread to close if its still running
       timerstop[0] = False # clear path for new timer
       threading.Thread(target=timercount,daemon=True).start()
     elif splt[0] == "timerStop":
       timerstop[0] = True
     elif splt[0] == "timer":
           return printer(str(timeindex))
       
  
def pixelcommands(splt):
    elseremove(splt) # remove  ?else
    try:
     if splt[0] == "pixelColor":
        if len(splt) != 4:
              closescript(text="incomplete arguments")
              return # stops running the function
            
        else:
           r, g, b = pyg.pixel(int(float(splt[1])),int(float(splt[2])))   
           if splt[3] == "hex:no":
             return printer(f"{r},{g},{b}")
           elif splt[3] == "hex:yes":
                return printer('#{0:02X}{1:02X}{2:02X}'.format(r, g, b))  
           else:
             closescript(text="invalid argument for hex")  
             return # stops running the function
               
     elif splt[0] == "waitPixelColor":
        #print(f"waiting for {splt[3]}")
        if len(splt) != 5:
            closescript(text="incomplete arguments")
            return # stops running the function
          
        else:
           i = 0
           if int(splt[4]) <= 0:
                 closescript(text="Invalid timeout")
                 return # stops running the function
                 
           while i < int(float(splt[4])):
              time.sleep(1)
              r, g, b = pyg.pixel(int(float(splt[1])),int(float(splt[2])))
              tohex = '#{0:02X}{1:02X}{2:02X}'.format(r, g, b)
              if splt[3] == tohex:
                    return printer("match found")
                  
              i += 1
           return printer("no match") 
         
     elif splt[0] == "getPixelColorRegion":
        if len(splt) != 5:
            closescript(text="incomplete arguments")
            return # stops running the function
          
        x = int(float(splt[1]))
        y= int(float(splt[2]))
        width = int(float(splt[3]))
        height = int(float(splt[4]))
        img = ImageGrab.grab(bbox=(x, y, x + width, y + height)).convert("RGB")
        #cimg = Image.open("text.jpg")
        #cimg.getdata()
        pixels = list(img.getdata()) # [(r, g, b), (r, g, b), ...]
        adder = []
        for p in pixels:
              adder.append(str(p))
        return printer(",".join(adder))  
     
     elif splt[0] == "colorExistsInRegion":
        x = int(float(splt[1]))
        y= int(float(splt[2]))
        width = int(float(splt[3]))
        height = int(float(splt[4]))
        hexes = splt[5:]
        
        if "?else" in hexes:
          filter = []
          for ad in hexes:
            if ad == "?else":
                  break
            else:
               filter.append(ad) 
          hexes = filter 
          
        img = ImageGrab.grab(bbox=(x, y, x + width, y + height)).convert("RGB")
        pixels = list(img.getdata())
        total = []
        found = []
        notfound = []
        #hex to rgb
        def hex_to_rgb(hex_color):
          hex_color = hex_color.lstrip('#')
          return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        #print(hexes) 
        if len(hexes) == 1 and os.path.isfile(hexes[0]):
            fo = open(hexes[0] ,"r")
            rd = fo.read()
            hxs = rd.split(",")
            for fi in hxs:
                if fi == "" or fi == "\n" or fi.isspace():
                      hxs.remove(fi)
            for h in hxs:
              trm = h.strip()
              target = hex_to_rgb(trm)         
              if target in pixels:
                total.append(f"{trm},{str(target)} found")
                found.append(trm)
              else:
                total.append(f"{trm},{str(target)} not found")
                notfound.append(trm)
        else:      
         for h in hexes:
          target = hex_to_rgb(h)         
          if target in pixels:
                total.append(f"{h},{str(target)} found")
                found.append(h)
          else:
                total.append(f"{h},{str(target)} not found")
                notfound.append(h)
                
        percent = (len(found)/len(total)) * 100
        total.insert(0,f"Summary (total = {len(total)} found = {len(found)} not found = {len(notfound)} aprox = {percent:.2f}%)")
        return printer("\n".join(total))
      
     elif splt[0] == "colorExistsInRegionSimilar":
        x = int(float(splt[1]))
        y = int(float(splt[2]))
        width = int(float(splt[3]))
        height = int(float(splt[4]))
        tolerance = int(float(splt[5]))
        hexes = splt[6:]
        
        if "?else" in hexes:
          filter = []
          for ad in hexes:
            if ad == "?else":
                  break
            else:
               filter.append(ad) 
          hexes = filter 
          
        imgdata = ImageGrab.grab(bbox=(x, y, x + width, y + height)).convert("RGB")
        pixeldata = list(imgdata.getdata())
        total = []
        found = []
        notfound = []
        
        def hex_to_rgb(hex_color):
          hex_color = hex_color.lstrip('#')
          return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def color_distance(c1, c2):
          return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
        
        if len(hexes) == 1 and os.path.isfile(hexes[0]):
            fo = open(hexes[0] ,"r")
            rd = fo.read()
            hxs = rd.split(",")
            for fi in hxs:
                if fi == "" or fi == "\n" or fi.isspace():
                      hxs.remove(fi)
            for h in hxs:
              trm = h.strip()
              target = hex_to_rgb(trm) 
              foundmatch = False 
              loc = "" 
              for pix in pixeldata:
                if color_distance(target, pix) <= tolerance:
                 foundmatch = True
                 loc = pix
                 break
           
              if foundmatch:
                total.append(f"{trm},{str(target)} similar {str(loc)} found")
                found.append(trm)
              else:
                 total.append(f"{trm},{str(target)} not found")
                 notfound.append(trm)      
          
        else:
         for h in hexes:
           target = hex_to_rgb(h)
           foundmatch = False
           loc = ""
           for pix in pixeldata:
              if color_distance(target, pix) <= tolerance:
                 foundmatch = True
                 loc = pix
                 break
           
           if foundmatch:
              total.append(f"{h},{str(target)} similar {str(loc)} found")
              found.append(h)
           else:
              total.append(f"{h},{str(target)} not found")
              notfound.append(h)
        percent = (len(found)/len(total)) * 100     
        total.insert(0,f"Summary (total = {len(total)} found = {len(found)} not found = {len(notfound)} aprox = {percent:.2f}%)")
        return printer("\n".join(total))

     elif splt[0] == "toPixel":
        if len(splt) != 2:
              closescript(text="Incomplete arguments")
              return # stops running the function
            
        img = Image.open(splt[1]).convert("RGB")
        pixels = list(img.getdata()) # [(r, g, b), (r, g, b), ...]
        adder = []
        for p in pixels:
              adder.append(str(p))
        return printer(",".join(adder))  
      
     elif splt[0] == "toHex":
        if len(splt) != 2:
            closescript(text="Incomplete arguments")
            return # stops running the function
          
        img = Image.open(splt[1]).convert("RGB")
        pixels = list(img.getdata()) # [(r, g, b), (r, g, b), ...]
        adder = []
        for imgtuple in pixels:
             r = imgtuple[0]
             g=imgtuple[1]
             b=imgtuple[2]
             #print(r g b)
             hex_color = '#{:02x}{:02x}{:02x}'.format(r, g, b)
             adder.append(hex_color) 
        return printer(",".join(adder)) 
    
     elif splt[0] == "colorExistsInImage":
        chosenimage = splt[1]
        hexes = splt[2:]
        
        if "?else" in hexes:
          filter = []
          for ad in hexes:
            if ad == "?else":
                  break
            else:
               filter.append(ad) 
          hexes = filter 
       
        img = Image.open(chosenimage).convert("RGB")
        pixels = list(img.getdata()) # [(r, g, b), (r, g, b), ...]  
        total = []
        found = []
        notfound = []
        #hex to rgb
        def hex_to_rgb(hex_color):
          hex_color = hex_color.lstrip('#')
          return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        #print(hexes) 
        if len(hexes) == 1 and os.path.isfile(hexes[0]):
            fo = open(hexes[0] ,"r")
            rd = fo.read()
            hxs = rd.split(",")
            for fi in hxs:
                if fi == "" or fi == "\n" or fi.isspace():
                      hxs.remove(fi)
            for h in hxs:
              trm = h.strip()
              target = hex_to_rgb(trm)       
              if target in pixels:
                total.append(f"{trm},{str(target)} found")
                found.append(trm)
              else:
                total.append(f"{trm},{str(target)} not found")
                notfound.append(trm)
        else:      
         for h in hexes:
          target = hex_to_rgb(h)         
          if target in pixels:
                total.append(f"{h},{str(target)} found")
                found.append(h)
          else:
                total.append(f"{h},{str(target)} not found")
                notfound.append(h)
                
        percent = (len(found)/len(total)) * 100
        total.insert(0,f"Summary (total = {len(total)} found = {len(found)} not found = {len(notfound)} aprox = {percent:.2f}%)")
        return printer("\n".join(total))
      
     elif splt[0] == "colorExistsInImageSimilar":
        image = splt[1]
        tolerance = int(splt[2])
        hexes = splt[3:]
        
        if "?else" in hexes:
          filter = []
          for ad in hexes:
            if ad == "?else":
                  break
            else:
               filter.append(ad) 
          hexes = filter 
          
        imgdata = Image.open(image).convert("RGB")
        pixeldata = list(imgdata.getdata()) # [(r, g, b), (r, g, b), ...]  
        total = []
        found = []
        notfound = []
        
        def hex_to_rgb(hex_color):
          hex_color = hex_color.lstrip('#')
          return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

        def color_distance(c1, c2):
          return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))
        
        if len(hexes) == 1 and os.path.isfile(hexes[0]):
            fo = open(hexes[0] ,"r")
            rd = fo.read()
            hxs = rd.split(",")
            for fi in hxs:
                if fi == "" or fi == "\n" or fi.isspace():
                      hxs.remove(fi)
            for h in hxs:
              trm = h.strip()
              target = hex_to_rgb(trm) 
              foundmatch = False 
              loc = "" 
              for pix in pixeldata:
                if color_distance(target, pix) <= tolerance:
                 foundmatch = True
                 loc = pix
                 break
           
              if foundmatch:
                total.append(f"{trm},{str(target)} similar {str(loc)} found")
                found.append(trm)
              else:
                 total.append(f"{trm},{str(target)} not found")
                 notfound.append(trm)      
          
        else:
         for h in hexes:
           target = hex_to_rgb(h)
           foundmatch = False
           loc = ""
           for pix in pixeldata:
              if color_distance(target, pix) <= tolerance:
                 foundmatch = True
                 loc = pix
                 break
           
           if foundmatch:
              total.append(f"{h},{str(target)} similar {str(loc)} found")
              found.append(h)
           else:
              total.append(f"{h},{str(target)} not found")
              notfound.append(h)
        percent = (len(found)/len(total)) * 100     
        total.insert(0,f"Summary (total = {len(total)} found = {len(found)} not found = {len(notfound)} aprox = {percent:.2f}%)")
        return printer("\n".join(total))
      
    except Exception as e:
      closescript(e,text="cannot get pixel")
      return # stops running the function
    
def commandregister(splt,remove=False):
   elseremove(splt)
   try:
    command = splt[1]
    
    if command.isalpha() == False or len(command) < 3:
      closescript(text="command name must be more than three letters,only letters no numbers or symbols")
      return # stops running the function
    
    if not splt[0] == "removeCommand":
      if splt[2] != "run":
         closescript(text="your command must start with run")
         return # stops running the function
          
    oldcommand = []
    if getcmdbyte["bytes"] == "":
        closescript(text="Internal command error occured\nYou can try restarting Surtr to fix the problem")
        return # stops running the function
    
    #ask password before continue
    askpassword()
    
    
    getcmds = getcmdbyte["bytes"].decode().split("\n")    
    
    #if the command is already there remove it first to avoid duplicates
    assigned = False
    for s in getcmds:
      sp = shellspliter(s)
      if len(sp) == 0: #skip empty lines
        continue
      if sp[0] == command:
        assigned = True
        continue
      else:
        oldcommand.append(s)
    
    #for remove command only verify if the command is assigned
    if splt[0] == "removeCommand":
      if not assigned:
          closescript(text=f"Err: {command} has never been registered")
          return # stops running the function
          
    #filtering and updating
    getcmds.clear()
    for old in oldcommand:
      if old == "" or old=="\n" or old.isspace():
        continue
      else:
        getcmds.append(old.strip())
    
    #mind words in quote
    def list_to_string(words):
        return ' '.join(f'"{w}"' if ' ' in w or '"' in w else w for w in words)
      
    tostring = list_to_string(splt[2:])
    
    #register the command
    if not remove:
      getcmds.append(f"{command} {tostring}\n")
    
    #encrypting
    credloader.encrypt_file("\n".join(getcmds),commandfile,text=True)
    #updating command holders
    getcmdbyte["bytes"] = "\n".join(getcmds).encode()
    print(f"request was successfull")
    
   except Exception as e:
     closescript(e,text="Surtr cannot register command because of an error") 
     return # stops running the function
 
def externalcommands(splt):
  command = splt[0]
  
  if getcmdbyte["bytes"] == "":
        closescript(text="Internal command error occured\nYou can try restarting Surtr to fix the problem")
        return # stops running the function
      
  getcmds = getcmdbyte["bytes"].decode().split("\n")
  if splt[0] == "registeredCommand":
        if len(splt) != 1:
              closescript(text="registeredCommand does not support arguments")
              return
        else:
           return printer("\n".join(getcmds))
  else:
    valid = False
    for r in getcmds:
      stp = r.strip()
      sp = shellspliter(stp)
      if len(sp) == 0: #make sure our commands list is not empty to prevent errors
        sp.append(" ") 
        
      if sp[0] == command:
        valid = True
        action = sp[1:]
        paramlist.clear()
        if len(splt) > 1:
          paramlist.extend(splt[1:]) #send the rest of the command parameters to paramlist
          runcodes(action)
        else:
          runcodes(action)  
        paramlist.clear()
    if valid == False:
      closescript(text=f"{splt[0]} command not found")
      return # stops running the function
    

def getEnv(splt):
    if splt[1] == "os":
        system = platform.system()
        release = platform.release()
        return printer(f"{system} {release}")
    elif splt[1] == "user":
        return printer(getpass.getuser())
    elif splt[1] == "cpuUsage":
        return printer(psutil.cpu_percent(interval=1))
    elif splt[1] == "ramFree":
        return printer(round(psutil.virtual_memory().available / (1024 * 1024), 1))
    elif splt[1] == "ramTotal":
        return printer(round(psutil.virtual_memory().total / (1024 * 1024), 1))
    elif splt[1].startswith("diskFree"):
        drive = f"{splt[2]}\\"
        return printer(round(shutil.disk_usage(drive).free / (1024**3), 1))
    elif splt[1].startswith("diskTotal"):
        drive = f"{splt[2]}\\"
        return printer(round(shutil.disk_usage(drive).total / (1024**3), 1))
    elif splt[1] == "hostname":
        return printer(socket.gethostname())


def allrandom(splt):
  try:
   """
    SYNTAX
    random  > generate random numbers length 0 to 9
    random len:n  > generate random numbers length 0 to n
    random "text" > generate random text from text

    random len:n "text"  > generate random text from text length n
    
    random len:n text0 text1 text2...  > generate random texts from texts length n
    random text0 text1 text2... > generate random text from texts
   """
   length = None
   try:
    if len(splt) > 1 and splt[1].startswith("len:"): #for length
         getnum = splt[1].split(":")[1]
         length = int(getnum)
   except:
     closescript(text=f"Cannot get length >>> {splt[1]}")  
     return    
   
   if len(splt) == 1: #for random
     rlist = ['0','1','2','3','4','5','6','7','8','9']
     random.shuffle(rlist) #shuffle list
     return printer("".join(rlist))
   
   elif len(splt) == 2: #for random len:
      if length != None:
        i = 0
        rlist = []
        while i < length:
             rlist.append(str(i))
             i += 1
        random.shuffle(rlist)
        return printer("".join(rlist))
      else:  #for random "text"
        rlist = list(splt[1])
        random.shuffle(rlist)
        return printer("".join(rlist))
      
   elif len(splt) == 3: #for random len:n "text"
       if length == None:#for random text0 text1 text2..
          rlist = splt[1:]
          randomout = random.choices(rlist)
          return printer(" ".join(randomout))
       else:
        rlist = list(splt[2])
        randomout = random.choices(rlist, k = length)
        return printer("".join(randomout))
  
   elif len(splt) >= 3: 
      if length != None: #for random len:n text0 text1 text2...
         rlist = splt[2:]
         randomout = random.choices(rlist, k = length)
         return printer(" ".join(randomout))  
       
      else: #for random text0 text1 text2...
         rlist = splt[1:]
         randomout = random.choices(rlist)
         return printer(" ".join(randomout))  
  
  except Exception as e:
    closescript(e,text="random command error")
    return    
  
  

def alltext(txtoptn):
  try:
    if txtoptn[0] == "textLower":
      text = " ".join(txtoptn[1:]).strip()
      return printer(text.lower())
    
    elif txtoptn[0] == "textUpper":
        text = " ".join(txtoptn[1:]).strip()
        return printer(text.upper())
      
    elif txtoptn[0] == "textStartWith":
          stxt = txtoptn[1]
          text = " ".join(txtoptn[2:]).strip()
          if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
              returner[0] = False
          return text.startswith(stxt)
        
    elif txtoptn[0] == "textEndWith":
          stxt = txtoptn[1]
          text = " ".join(txtoptn[2:]).strip()
          if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
              returner[0] = False
          return text.endswith(stxt)
    elif txtoptn[0] == "textHas":
          hasin = txtoptn[1]
          text = " ".join(txtoptn[2:]).strip()
          if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
              returner[0] = False
          if hasin in text:  
             return True
          else:
             return False 
    elif  txtoptn[0] == "toBase64":
       text = " ".join(txtoptn[1:]).strip()   
       base64_string = base64.b64encode(text.encode('utf-8')).decode('utf-8')

       return printer(base64_string)
        
    elif  txtoptn[0] == "decodeBase64":
          text = " ".join(txtoptn[1:]).strip()
          decoded_text = base64.b64decode(text.encode('utf-8')).decode('utf-8')
          return printer(decoded_text)
       
  except Exception as e:
    closescript(e,text="Failed to process text command")         
    return      
           
           
           
           
#all jsons

def jsonprinter(x):
    """Pretty-print values."""
    if isinstance(x, (dict, list)):
        return printer(json.dumps(x, indent=2))
    else:
        return printer(x)


def parsejson(jsonoptn):
  """
    syntax
    json name  access json
    json name.[key].0.[key] access json
   
    json name {"key":"value"}   create json
    json name.[key].0.[key] {"key":"value"} change value
   
    Supports simple unquoted strings like 'hi', numbers like 42, true/false/null.
    For JSON objects/arrays, provide valid JSON (may need shell quoting).
  """
  try:
    if len(jsonoptn) < 2:
        closescript(text="json error: insufficient arguments", errornumber="412")
        return
    
    path = jsonoptn[1]
    
    if len(jsonoptn) == 2:
        # Retrieve
        if '.' not in path:
            top_name = path
            if top_name not in jsonvariants:
                closescript(text=f"json error: no json named {top_name}", errornumber="412")
                return
            return jsonprinter(jsonvariants[top_name])
        
        # Nested get
        jsonkeys = path.split('.')
        top_name = jsonkeys[0]
        if top_name not in jsonvariants:
            closescript(text=f"json error: no json named {top_name}", errornumber="412")
            return
        
        current = jsonvariants[top_name]
        for k in jsonkeys[1:]:
            if not k or k.isspace():
                continue
            if k.startswith('[') and k.endswith(']'):
                key = k[1:-1]
                try:
                    current = current[key]
                except (KeyError, TypeError):
                    closescript(text="json error: key not found", errornumber="412")
                    return
            else:
                try:
                    idx = int(float(k))
                    current = current[idx]
                except (ValueError, IndexError, TypeError):
                    closescript(text="json error: invalid index", errornumber="412")
                    return
        
        return jsonprinter(current)
    
    # len >2, set
    value_str = " ".join(jsonoptn[2:]).strip()
    if not value_str:
        closescript(text="json error: empty value", errornumber="412")
        return
    
    # Try JSON first
    try:
        value = json.loads(value_str)
    except json.JSONDecodeError:
        # Fallback to simple types
        val_lower = value_str.lower().strip()
        if val_lower == 'true':
            value = True
        elif val_lower == 'false':
            value = False
        elif val_lower == 'null':
            value = None
        else:
            # Check for number
            try:
                if '.' in value_str or 'e' in value_str.lower() or value_str.startswith(('-', '+')):
                    value = float(value_str)
                else:
                    value = int(value_str)
            except ValueError:
                # Treat as string
                value = value_str
    
    if '.' not in path:
        jsonvariants[path] = value
        #print(f"Created/Updated json '{path}'")
        return
    
    jsonkeys = path.split('.')
    top_name = jsonkeys[0]
    keys = [k for k in jsonkeys[1:] if k and not k.isspace()]
    if not keys:
        jsonvariants[top_name] = value
        #print(f"Updated json '{top_name}'")
        return
    
    if top_name not in jsonvariants:
        closescript(text=f"json error: no json named {top_name}", errornumber="412")
        return
    
    # Navigate to parent
    current = jsonvariants[top_name]
    for k in keys[:-1]:
        if k.startswith('[') and k.endswith(']'):
            key = k[1:-1]
            try:
                current = current[key]
            except (KeyError, TypeError):
                closescript(text="json error: key not found", errornumber="412")
                return
        else:
            try:
                idx = int(float(k))
                current = current[idx]
            except (ValueError, IndexError, TypeError):
                closescript(text="json error: invalid index", errornumber="412")
                return
    
    # Set last
    last_k = keys[-1]
    try:
        if last_k.startswith('[') and last_k.endswith(']'):
            lkey = last_k[1:-1]
            current[lkey] = value
        else:
            lidx = int(float(last_k))
            if isinstance(current, list) and lidx < len(current):
                current[lidx] = value
            else:
                raise IndexError("Invalid index for set")
    except (KeyError, IndexError, TypeError, ValueError) as e:
        closescript(text="json error: cannot set value", errornumber="412")
        return
    
    #print(f"Updated value at path '{path}'")

  except Exception as e:
    closescript(e,text="json error", errornumber="412")
    return
  
def jsonSave(jsonoptn):
  """
    syntax
    jsonSave name filename.json [indent]
    Saves jsonvariants[name] to filename.json (creates/overwrites file).
    indent: optional integer (e.g., 2 for pretty-print; defaults to None for compact).
  """
  try:
    if len(jsonoptn) < 3:
        closescript(text="jsonSave error: insufficient arguments (need name and filename)", errornumber="416")
        return
    
    name = jsonoptn[1]
    filename = jsonoptn[2]
    indent = None
    if len(jsonoptn) > 3:
        try:
            indent = int(jsonoptn[3])
        except ValueError:
            closescript(text="jsonSave error: invalid indent (must be integer)", errornumber="416")
            return
    
    if name not in jsonvariants:
        closescript(text=f"jsonSave error: no json named {name}", errornumber="416")
        return
    
    data = jsonvariants[name]
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=indent)
        #print(f"Saved '{name}' to '{filename}'")
    except (IOError, OSError) as e:
        closescript(text=f"jsonSave error: cannot write to '{filename}'", errornumber="416")
        return
  
  except Exception as e:
      closescript(e,text=f"jsonSave error: cannot write to '{filename}'", errornumber="416")
      return
     
def jsonParse(jsonoptn):
  """
    syntax
    jsonParse {"key":"value"} [or any valid JSON text]
    Parses and prints the JSON text; does NOT save to jsonvariants.
  """
  try:
    if len(jsonoptn) < 2:
        closescript(text="jsonParse error: insufficient arguments (need JSON text)", errornumber="413")
        return
    
    jsontext = " ".join(jsonoptn[1:]).strip()
    if not jsontext:
        closescript(text="jsonParse error: empty JSON text", errornumber="413")
        return
    
    try:
        value = json.loads(jsontext)
        return jsonprinter(value)
    except json.JSONDecodeError as e:
        closescript(text=f"jsonParse error: invalid json '{jsontext[:50]}...' (line {e.lineno}, col {e.colno})", errornumber="413")
        return

  except Exception as e:
    closescript(e,text="jsonParse error: cannot parse json", errornumber="413")
    return

def jsonAppend(jsonoptn):
    """
    syntax:
    jsonAppend name value
    jsonAppend name.[key].0.[subkey] value
    """
    try:
        if len(jsonoptn) < 3:
            closescript(text="jsonAppend error: insufficient arguments (need path and value)", errornumber="489")
            return

        path = jsonoptn[1]
        value_str = " ".join(jsonoptn[2:]).strip()
        if not value_str:
            closescript(text="jsonAppend error: empty value", errornumber="489")
            return

        # Parse value (same as before)
        try:
            value = json.loads(value_str)
        except json.JSONDecodeError:
            val_lower = value_str.lower().strip()
            if val_lower == 'true':
                value = True
            elif val_lower == 'false':
                value = False
            elif val_lower == 'null':
                value = None
            else:
                try:
                    value = float(value_str) if '.' in value_str or 'e' in value_str.lower() else int(value_str)
                except ValueError:
                    value = value_str

        # ─── Resolve target with proper parent tracking ─────────────────────
        if '.' not in path:
            top_name = path
            if top_name not in jsonvariants:
                closescript(text=f"jsonAppend error: no json named '{top_name}'", errornumber="489")
                return
            target = jsonvariants[top_name]
        else:
            jsonkeys = path.split('.')
            top_name = jsonkeys[0]
            if top_name not in jsonvariants:
                closescript(text=f"jsonAppend error: no json named '{top_name}'", errornumber="489")
                return

            current = jsonvariants[top_name]
            parent = None
            last_key = None

            for i, k in enumerate(jsonkeys[1:]):
                if not k or k.isspace():
                    continue
                parent = current
                last_key = k

                if k.startswith('[') and k.endswith(']'):
                    key = k[1:-1]
                    try:
                        current = current[key]
                    except (KeyError, TypeError):
                        closescript(text=f"jsonAppend error: key '{key}' not found", errornumber="489")
                        return
                else:
                    try:
                        idx = int(float(k))
                        current = current[idx]
                    except (ValueError, IndexError, TypeError):
                        closescript(text=f"jsonAppend error: invalid index '{k}'", errornumber="489")
                        return

            if parent is None or last_key is None:
                closescript(text="jsonAppend error: invalid path", errornumber="489")
                return

            target = current

        # ─── Append / merge logic ───────────────────────────────────────────
        if isinstance(target, list):
            target.append(value)
        elif isinstance(target, dict):
            if isinstance(value, dict):
                target.update(value)
            else:
                closescript(text="jsonAppend error: cannot append non-dict value to dict", errornumber="489")
                return
        else:
            closescript(text=f"jsonAppend error: target at '{path}' is not a list or dict (cannot append)", errornumber="489")
            return

        # Optional: print success (comment out if not wanted)
        # print(f"Appended to '{path}'")

    except Exception as e:
        closescript(e, text="jsonAppend error: failed to append value", errornumber="489")
        return


def jsonDelete(jsonoptn):
  """
    syntax
    jsonDelete name  (deletes entire json)
    jsonDelete name.[key].0.[key]  (deletes nested value)
  """
  try:
    if len(jsonoptn) < 2:
        closescript(text="jsonDelete error: insufficient arguments (need path)", errornumber="414")
        return
    
    path = jsonoptn[1]
    
    if '.' not in path:
        top_name = path
        if top_name not in jsonvariants:
            closescript(text=f"jsonDelete error: no json named {top_name}", errornumber="414")
            return
        del jsonvariants[top_name]
        #print(f"Deleted json '{top_name}'")
        return
    
    # Nested delete
    jsonkeys = path.split('.')
    top_name = jsonkeys[0]
    if top_name not in jsonvariants:
        closescript(text=f"jsonDelete error: no json named {top_name}", errornumber="414")
        return
    
    keys = [k for k in jsonkeys[1:] if k and not k.isspace()]
    if not keys:
        del jsonvariants[top_name]
        #print(f"Deleted json '{top_name}'")
        return
    
    # Navigate to parent
    current = jsonvariants[top_name]
    for k in keys[:-1]:
        if k.startswith('[') and k.endswith(']'):
            key = k[1:-1]
            try:
                current = current[key]
            except (KeyError, TypeError):
                closescript(text="jsonDelete error: key not found", errornumber="414")
                return
        else:
            try:
                idx = int(float(k))
                current = current[idx]
            except (ValueError, IndexError, TypeError):
                closescript(text="jsonDelete error: invalid index", errornumber="414")
                return
    
    # Delete last
    last_k = keys[-1]
    try:
        if last_k.startswith('[') and last_k.endswith(']'):
            lkey = last_k[1:-1]
            del current[lkey]
        else:
            lidx = int(float(last_k))
            if isinstance(current, list) and 0 <= lidx < len(current):
                del current[lidx]
            else:
                raise IndexError("Invalid index for delete")
        #print(f"Deleted value at path '{path}'")
    except (KeyError, IndexError, TypeError, ValueError) as e:
        closescript(text="jsonDelete error: cannot delete value", errornumber="414")
        return
      
  except  Exception as e:
    closescript(e,text="jsonDelete error: cannot remove index", errornumber="414")
    return  

def lenJson(jsonoptn):
    """
    syntax
    lenJson json name  prints length of json
    lenJson json name.[key].0.[key]  prints length of nested json part
    
    Length for objects (dicts): number of keys
    Length for arrays (lists): number of elements
    Length for strings: character count
    Error for other types (numbers, bool, null)
    """
    try:
        if len(jsonoptn) < 2:
            closescript(text="lenJson error: insufficient arguments", errornumber="418")
            return
        
        if len(jsonoptn) > 2:
            closescript(text="lenJson error: too many arguments", errornumber="418")
            return
        
        path = jsonoptn[1]
        
        # Retrieve the target
        if '.' not in path:
            top_name = path
            if top_name not in jsonvariants:
                closescript(text=f"lenJson error: no json named {top_name}", errornumber="418")
                return
            current = jsonvariants[top_name]
        else:
            jsonkeys = path.split('.')
            top_name = jsonkeys[0]
            if top_name not in jsonvariants:
                closescript(text=f"lenJson error: no json named {top_name}", errornumber="418")
                return
            
            current = jsonvariants[top_name]
            for k in jsonkeys[1:]:
                if not k or k.isspace():
                    continue
                if k.startswith('[') and k.endswith(']'):
                    key = k[1:-1]
                    try:
                        current = current[key]
                    except (KeyError, TypeError):
                        closescript(text="lenJson error: key not found", errornumber="418")
                        return
                else:
                    try:
                        idx = int(float(k))
                        current = current[idx]
                    except (ValueError, IndexError, TypeError):
                        closescript(text="lenJson error: invalid index", errornumber="418")
                        return
        
        # Compute and print length
        try:
            length = len(current)
            return printer(length)
        except TypeError:
            closescript(text="lenJson error: target is not a sequence, mapping, or string", errornumber="418")
            return
    
    except Exception as e:
        closescript(text="lenJson error", errornumber="418")
        return

#jsons ends here
     
     
     
       
       
def runiterate(original_command, ivariants):
    # Always rebuild fresh from the original template
    parsed_command = []

    # replace variables for onelined command
    for part in original_command:
        if isinstance(part, str):
            replaced_part = part
            for key, value in ivariants.items():
                replaced_part = replaced_part.replace(key, str(value))
            parsed_command.append(replaced_part)

    # set variables for label command
    # add to variables
    for key, value in ivariants.items():
        variants[key] = value
    #use vip run for iterate runs do not use #RECURSION GUARD is user calls run in iterate
    vip_run[0] = True
    runcodes(parsed_command)
    vip_run[0] = False
    # remove from variables when done
    for key in list(ivariants.keys()):
        variants.pop(key, None)


def splitandrun(splt):
    token = None
    if len(splt) > 2 and splt[1] == "?token":
        token = splt[2]
    elif len(splt) > 2 and splt[1] == "?token-es": # for escape characters
          escapechar = splt[2]
          if escapechar == "\\n":
               token = "\n" 
          elif escapechar == "\\r":
               token = "\r" 
          elif escapechar == "\\t":
               token = "\t" 
          elif escapechar == "\\b":
               token = "\b" 
          elif escapechar == "\\b":
               token = "\b" 
          elif escapechar == "\\f":
               token = "\f" 
          else:
              token = splt[2]
              
    if "?run" not in splt:
        closescript(text="> ?run < missing in text split")
        return

    # Get text before ?run
    txtsp = []
    for br in splt:
        if br == "?run":
            break
        txtsp.append(br)

    # Get command after ?run
    indx = splt.index("?run") + 1
    commandtorun = splt[indx:]
    if token:
        spltr = " ".join(txtsp[3:])  # Skip initial words before actual content
        divde = spltr.split(token)
        for wrds in divde:
            # call runiterate because using variables function to replace {{item}} is very risky and can develope error quickly
            runiterate(commandtorun, {"{{item}}": wrds.strip()})
    else:
        filename = " ".join(txtsp[1:])
        if len(txtsp[1:]) == 1 and os.path.exists(filename) and os.path.isfile(filename):
            with open(filename, "r") as frd:
                for rd in frd:
                    runiterate(commandtorun, {"{{item}}": rd.strip()})
        else:
            for wrds in txtsp[1:]:  # Skip the first item in txtsp
                runiterate(commandtorun, {"{{item}}": wrds.strip()})

    # clear variable in case of rerun
    # variants.pop("{{item}}", None) # added None to stop python from raising an error if key not found


 
paramlist = []
def registeredcommandparams(splt):
    if len(paramlist) == 0:
      pass
    else:
      i = 0
      while i < len(paramlist):
        # now lets replace our parameters with values
        for wrd in splt:
          ag = "?param" + str(i)
          agall = "?param*"
          aglen = "?param#"
          if ag == wrd:
            ind = splt.index(wrd)
            splt[ind] = wrd.replace(ag, paramlist[i])  # Literal replace, no parsing 

          elif agall == wrd:
            ind = splt.index(wrd)
            splt[ind] = wrd.replace(agall, " ".join(paramlist))  # Literal replace, no parsing 
   
          elif aglen == wrd:
            ind = splt.index(wrd)
            splt[ind] = wrd.replace(aglen, str(len(paramlist)))  # Literal replace, no parsing 

        i += 1

  
   
allowreturncommands = [
"seeImage",
"msg",
"confirm",
"userInput",
"readImage",
"readImageLanguages",
"readScreen",
"talking",
"runCmd",
"voices",
"not",
"screenWidth",
"screenHeight",
"fileman",
"inWindowTitle",
"windowList",
"random",
"focusWindow",
"focusedWindow",
"minimizeWindow",
"maximizeWindow",
"resetWindow",
"json",
"textLower",
"textUpper",
"textStartWith",
"textEndWith",
"textHas",
"empty",
"toBase64",
"decodeBase64",
"strip",
"jsonParse",
"lenJson",
"fetcher",
"closeWindow",
"clipboardPaste",
"watchStatus",
"changeDetected",
"filesWatched",
"restoreFile",
"timer",
"pixelColor",
"replace",
"waitPixelColor",
"registeredCommand",
"getPixelColorRegion",
"colorExistsInRegion",
"colorExistsInRegionSimilar",
"toPixel",
"toHex",
"colorExistsInImage",
"colorExistsInImageSimilar",
"getEnv",
"mousePositionX",
"mousePositionY",
"mousePosition",
"getValue",
"getWindowX",
"getWindowY",
"integer",
"getWindowWidth",
"getWindowHeight",
"prompt",
"emit:prompt",
"--version"]


# ────────────────────────────────────────────────
# State flags (authoritative base + extensions)
# ────────────────────────────────────────────────
commandcut      = [False]   # single ^ continuation
commandlns      = [False]   # <++ ... ++> block
caretjoin       = [False]   # ^^ multiline join
autojoin        = [False]
vip_run         = [False]
parentcommands  = [False]

commandsplit    = []        # ^ buffer
commandsjoins   = []        # ^^ and <++ buffers


# ────────────────────────────────────────────────
# Reset helpers (SECURITY HARDENED, NO BEHAVIOR CHANGE)
# ────────────────────────────────────────────────
def reset_full():
    commandcut[0] = False
    commandlns[0] = False
    caretjoin[0]  = False
    autojoin[0]   = False
    vip_run[0]    = False
    parentcommands[0] = False
    commandsplit.clear()
    commandsjoins.clear()


def reset_blocks_only():
    commandlns[0] = False
    caretjoin[0]  = False
    commandsjoins.clear()


# ────────────────────────────────────────────────
# Block runner (UNMODIFIED LOGIC + MORE SAFETY CLEAN)
# ────────────────────────────────────────────────
def runparts(splt, parentend=False):
    """
    Split command list into blocks and run each block.
    - If parentend=True, split by '+>' only
    - Otherwise split by '++'
    """

    if parentend or "+>" in splt:
        blocks = []
        current = []

        for token in splt:
            if token == "+>":
                blocks.append(current)
                current = []
            else:
                current.append(token)

        if current:
            blocks.append(current)

        for block in blocks:
            if not block:
                continue

            first = block[0] if isinstance(block[0], str) else None
            if first in ["if","repeat","splitRun","eachOnScreen",
                         "textOnScreen","while","until"]:
                runcodes(block, usespecialjoiner=False)
            else:
                runcodes(block)
        return True

    # ───── NORMAL ++ SPLIT
    parts = []
    current = []

    while splt and splt[0] == "++":
        splt.pop(0)
    while splt and splt[-1] == "++":
        splt.pop()

    first = splt[0] if splt else None
    if first in ["if","repeat","splitRun","eachOnScreen",
                 "textOnScreen","while","until"]:
        runcodes(splt, usespecialjoiner=False)
        return True

    for token in splt:
        if token == "++":
            if current:
                parts.append(current)
            current = []
        else:
            current.append(token)

    if current:
        parts.append(current)

    for p in parts:
        if p:
            runcodes(p)
    return True


# ────────────────────────────────────────────────
# Unified parser (BASE LOGIC PRESERVED)
# ────────────────────────────────────────────────
def specialjoiners(splt):
    try:
        # ───── Parent command continuation
        if parentcommands[0]:
            parentcommands[0] = False
            return runparts(splt, parentend=True)

        if not splt or all(x.strip() == "" for x in splt):
            return True

        # =======================================================
        # 1. ^^ MULTILINE JOIN (ADDED FEATURE — SAFE INSERTION)
        # =======================================================
        
        if splt and splt[0].startswith("^^"):
            commandsjoins.clear()

            first = splt[0]
            if first == "^^":
              content = splt[1:]
            else:
               content = [first[2:]] + splt[1:]

            commandsjoins.append(content)
            caretjoin[0] = True
            return True

        if caretjoin[0]:
            if splt and splt[-1].endswith("^^"):
                last = splt[-1]
                if last == "^^":
                   content = splt[:-1]
                else:
                   content = splt[:-1] + [last[:-2]]

                commandsjoins.append(content)

                final = []
                for line in commandsjoins:
                    final.extend(x for x in line if x != "")

                caretjoin[0] = False
                commandsjoins.clear()

                reset_full()
                runcodes(final)
                return True

            # still inside ^^ block
            commandsjoins.append(splt)
            return True

        
        # =======================================================
        # 2. SINGLE-LINE ^ CONTINUATION (UNCHANGED)
        # =======================================================
        if splt and splt[-1].endswith("^"):
            last = splt[-1][:-1]
            commandsplit.extend(splt[:-1])
            if last:
                commandsplit.append(last)
            commandcut[0] = True
            return True

        if commandcut[0]:
            if len(splt) == 0 or (len(splt) == 1 and splt[0] == ""):
                return True

            commandcut[0] = False
            commandsplit.extend(splt)
            final = commandsplit[:]
            commandsplit.clear()

            vip_run[0] = True
            reset_blocks_only()
            runcodes(final)
            vip_run[0] = False
            return True

        # =======================================================
        # 3. <++ MULTILINE BLOCK (UNCHANGED CORE)
        # =======================================================
        if "<++" in splt:
            commandsjoins.clear()
            filtered = [x for x in splt if x != "<++"]
            commandsjoins.append(filtered)
            commandlns[0] = True
            return True

        if commandlns[0]:
            if not splt or (len(splt) == 1 and splt[0] == ""):
                return True

            if splt[-1].endswith("++>"):
                commandlns[0] = False
                last = splt[-1][:-3]
                if last:
                    splt[-1] = last
                else:
                    splt.pop()

                commandsjoins.append(splt[:])

                final_list = []
                for i, line in enumerate(commandsjoins):
                    final_list.extend(line)
                    if i < len(commandsjoins) - 1:
                        final_list.append("++")

                commandsjoins.clear()

                while final_list and final_list[0] in ("<++","++"):
                    final_list.pop(0)
                while final_list and final_list[-1] in ("++","++>"):
                    final_list.pop()

                autojoin[0] = True
                runcodes(final_list)
                return True

            commandsjoins.append(splt[:])
            return True

        # =======================================================
        # 4. NORMAL ++ SPLITTING (UNCHANGED + SAFETY)
        # =======================================================
        if "++" in splt:

            if splt[0] == "if":
                if autojoin[0]:
                    autojoin[0] = False
                if "+>" in splt:
                    parentcommands[0] = True
                runcodes(splt, usespecialjoiner=False)
                return True

            if autojoin[0]:
                autojoin[0] = False
                idx = 1 if splt[0] == "++" else 0
                if len(splt) > idx:
                    if splt[idx] in ["repeat","splitRun","eachOnScreen",
                                     "textOnScreen","while","until","if"]:
                        if "+>" in splt:
                            parentcommands[0] = True
                        runcodes(splt, usespecialjoiner=False)
                        return True

            return runparts(splt)

        # =======================================================
        # No joiners → normal execution
        # =======================================================
        return False

    except Exception as e:
        reset_full()
        closescript(e, text="Command parser error")
        return False



inwebui = [False]
dontexecute = False


quickrunexit = [False]

def runcodes(splt,usespecialjoiner=True,returnfunction=None):
     global inwebui,dontexecute,listexecrunning,runcodecurrentcommand
       
     #print(splt)
     #skip comments !
     if splt[0].startswith("~~"):
           return
    
     runcodecurrentcommand = " ".join(splt) #update current command
     
     
     
     if usespecialjoiner == True: 
        muststop = specialjoiners(splt)
        if muststop:
          return   
      
     variables(splt)
  
     #super arguments
     superargs(splt)
     #register commands parameters
     registeredcommandparams(splt)
     #handle guest mode 
     guestmodevalidation(splt)
     
     if inwebui[0] == True: 
        blocked = settings("blockedcommand",webui=True)
        #sblocked = blocked.split(" ")
        sblocked = shellspliter(blocked) 
        if splt[0] in sblocked:
          if splt[0] != "webui":
             inwebui[0] = False
             closescript(text=f"{splt[0]} command access blocked")
             return # stops running the function
        if splt[0] in ["end","quickRun"]:
               inwebui[0] = False
               closescript(text=f"Command failed {splt[0]} is not available in webui mode")
               return       
              
     
     
       #print(len(splt))
       #for mouse movement
       #pyg.moveTo(0,0,5)
         
     #before the begining of any command this is the starter command
     if returnfunction is not None:
       return returnfunction(splt)   
     
     
          
     #for emit command
     if splt[0].startswith("emit"):
        return  emit_command(splt) 
             
     job = splt[0]
         
     match job:
       
       case "mouse":
         if len(splt) > 1:
            allmousehandler(splt[1:])
         else:
           closescript(text="Unknown mouse arguments") 
           return

       # for keyboard typing    
       case "keyBoard":
        if (splt[1] == "type"):
          try:
           float(splt[2])
          except Exception as e:
            closescript(e,text=f"{splt[2]} must be a number")
            return # stops running the function
        
          if (len(splt) == 4 and os.path.exists(splt[3]) and os.path.isfile(splt[3])):
            keyboardhandler(mode=splt[1],speed=float(splt[2]),file="yes",text=splt[3])
            print("typed text from file")
          else:
              compkeys = " ".join(splt[3:])
              keyboardhandler(mode=splt[1],speed=float(splt[2]),file="no",text=compkeys)
              print("typed some keys")
              
        elif (splt[1] == "hold"):
            compkeys = " ".join(splt[2:])
            keyboardhandler(mode=splt[1],text=compkeys)
            print("Hold keys")      
        elif (splt[1] == "release"):
            compkeys = " ".join(splt[2:])
            keyboardhandler(mode=splt[1],text=compkeys)
            print("Release keys")  
          
        elif (splt[1] == "press"):
            compkeys = " ".join(splt[2:])
            keyboardhandler(mode=splt[1],text=compkeys)
            print("pressed keys")  
        else:
          closescript(text="keyBoard error: missing arguments")
          return # stops running the function
       
       case "wait":
         if (len(splt) > 2):
            closescript(text=f"error in wait arguments {len(splt)} (more than 2)")
            return # stops running the function
          
         else:
            try:
             toint =  float(splt[1])
             waiter(toint)
            except Exception as e:
               closescript(e,text="cannot execute command") 
               return # stops running the function
      
       case "seeImage":
         return printer(cmdtrueorfalse(splt))
      
       case "if":
          runif_else(splt)
         
       case "not":
         return run_not(splt) 
       
       case "while":
         runwhile(splt)
         
       case "until":
         run_until(splt) 
         
         
       #closes the script
       case "end":
         if(len(splt) > 2):
            closescript(text=f"error in end arguments {len(splt)} (more than 2)")
            return # stops running the function
          
         elif(len(splt) == 2):
            try:
             toint = int(float(splt[1]))
             print(f"Closed script <ExitCode {splt[1]}>")
             os._exit(toint)
            except Exception as ex:
               closescript(ex,text="cannot execute command")
               return # stops running the function
               
         elif(len(splt) == 1):
                os._exit(0)

       case "prompt":
          prmpt_txt = parsestringsnormally(" ".join(splt[1:]))
          prmpt = input(prmpt_txt)
          return printer(prmpt,noprint=True)
        
       case "eachOnScreen":
           run_eachonscreen(splt)    
       
       case "say" | "talk" | "voices" | "talking" | "stopTalking":
         return speaker(splt)
   
       case "screenShot":
         if(splt[1] == "mouse"):
           #screenShot mouse 10 10 sshot.jpg
           screenshot_handler(mouse="yes",width=splt[2],height=splt[3],path=splt[4])      
           #if its an image path
         elif(len(splt) == 2):
           #screenShot sshot.jpg
           screenshot_handler(mouse="no",onefile="yes",path=splt[1])
         elif(len(splt) > 2):
           #screenShot 0 0 300 500 sshot.jpg
          screenshot_handler(mouse="no",onefile="no",left=splt[1],top=splt[2],width=splt[3],height=splt[4],path=splt[5])
         else:
          closescript(text="error in taking screenshot check your args")
          return # stops running the function
       
       case "screenShotMonitor":
          if len(splt) == 3:
              if splt[1].isnumeric() == False:
                 closescript(text=f"the monitor index {splt[1]} is not a number")
                 return   
              index = int(splt[1])
              screenshot_monitor(monitor_index=index, filename=splt[2])
            
          elif len(splt) == 7:
              if splt[1].isnumeric() == False:
                 closescript(text=f"the monitor index {splt[1]} is not a number")
                 return   
              index = int(splt[1])
              # Screenshot 400x300 region starting at (100, 100) on monitor index
              screenshot_region_on_monitor(monitor_index=index, x=int(splt[2]), y=int(splt[3]), width=int(splt[4]), height=int(splt[5]),filename=splt[6])
            
          elif len(splt) == 6:
              if splt[1].isnumeric() == False:
                 closescript(text=f"the monitor index {splt[1]} is not a number")
                 return 
              if splt[2] != "mouse":
                 closescript(text=f"Unsupported syntax. Expected: screenShotMonitor index mouse width height filename")
                 return  
              index = int(splt[1])
              # Screenshot 200x200 region starting at mousepos (500, 400) on monitor 2
              screenshot_at_position(monitor_index=index, width=int(splt[3]), height=int(splt[4]), filename=splt[5])
          
          else:
             closescript(text="screenShotMonitor Syntax error")
             return 


       case  "set":
         set_variables(splt)                  
       
       case "resetEnvironment":
         resetallEnvironment()
        
        
       case "msg" | "confirm":
         cmdtrueorfalse(splt)
         
       case "userInput":
          userinputhandler(app,splt)
          
       case "runCmd":
         try:
          if splt[1] == "live:yes":
                 commds = " ".join(splt[2:])
                 run_live_shell_windows(commds)
          else:       
            opt = "?else"
            if opt in splt:
              e = splt.index(opt) - 1
              wr = splt[1:]
              #we are not using shell=True in this because we are using list command
              subcmd = subprocess.run(wr[:e],shell=True, stdout=subprocess.PIPE,text=True,stderr=subprocess.PIPE,creationflags=subprocess.CREATE_NO_WINDOW)
              if (subcmd.stdout) != "":
                   return printer(subcmd.stdout)  
              elif (subcmd.stderr) != "":
                   return printer(subcmd.stderr)
              else:
                 return printer("")
           
            else:      
              subcmd = subprocess.run(splt[1:],shell=True, stdout=subprocess.PIPE,text=True,stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
              if (subcmd.stdout) != "":
                   return printer(subcmd.stdout)  
              elif (subcmd.stderr) != "":
                   return printer(subcmd.stderr)
              else:
                 return printer("")

         except Exception as e:
            closescript(e,text="cannot run command")
            return # stops running the function
          
       case "readImage" | "readImageLanguages" | "readScreen":
        try:
           readimageshandler(splt, False)  
        except Exception as e:
          closescript(e,text="Cannot run command") 
          return # stops running the function
        
       case "moveToText" | "dragToText":
         if splt[0] == "moveToText":
           read_screen_in_sentence(action="move",texts=" ".join(splt[4:]), findall=splt[1],speed=splt[2],language=splt[3]) 
         elif splt[0] == "dragToText":
           read_screen_in_sentence(action="drag",texts=" ".join(splt[4:]),findall=splt[1],speed=splt[2],language=splt[3])
           
       case "rightClickText" | "clickText" | "doubleClickText" | "tripleClickText":
         if splt[0] == "rightClickText":
               read_screen_in_sentence(action="rightclick",texts=" ".join(splt[3:]),findall=splt[1],language=splt[2])
           
         elif splt[0] == "clickText":
               read_screen_in_sentence(action="click",texts=" ".join(splt[3:]),findall=splt[1],language=splt[2])
           
         elif splt[0] == "doubleClickText":
               read_screen_in_sentence(action="doubleclick",texts=" ".join(splt[3:]),findall=splt[1],language=splt[2])
           
         elif splt[0] == "tripleClickText":
               read_screen_in_sentence(action="trippleclick",texts=" ".join(splt[3:]),findall=splt[1],language=splt[2])
           

       case "moveToWord" | "dragToWord":
          if not(splt[1] == "one" or splt[1] == "all"):
              closescript(text="error >one< or >all< needed after moveToText")
              return # stops running the function
            
          if splt[0] == "moveToWord":
              screentextreadoptions("move",splt[4:],splt[1],splt[2],splt[3])
          elif splt[0] == "dragToWord":
              screentextreadoptions("drag",splt[4:],splt[1],splt[2],splt[3])
      
       case "imageReader":
          try:
            lang="eng"
            min_conf=40
            char_width=8.0
            transform="gray"
            line_height=20
            psm=6
            save_txt=None
            print_result=True
            if "-image" in splt:
                image_path = splt[splt.index("-image") + 1]
            else:
                closescript(text="No image specifed")
                return
            if "-lang" in splt:
                lang = splt[splt.index("-lang") + 1]
            if "-min-conf" in splt:
                min_conf = splt[splt.index("-min-conf") + 1]
            if "-char-width" in splt:
                char_width = splt[splt.index("-char-width") + 1]
            if "-line-height" in splt:
                line_height = splt[splt.index("-line-height") + 1]
            if "-transform" in splt:
                transform = splt[splt.index("-transform") + 1]
            if "-psm" in splt:
                psm = splt[splt.index("-psm") + 1]
            if "-save" in splt:
                save_txt = splt[splt.index("-save") + 1]
            if "-hide-output" in splt:
                print_result = False
            
            lines = surtr_ocr.reconstruct_text_layout(
            image_path=image_path,
            ocr_path=ocr_path,
            lang=lang,
            min_conf=int(float(min_conf)),
            transform=transform,
            char_width=float(char_width),
            line_height=int(float(line_height)),
            psm=int(float(psm)),
            save_txt=save_txt,
            print_result=print_result
            )
          except Exception as e:
              closescript(e,text="imageReader command failed")
              return
          
          
       case "rightClickWord" | "clickWord" | "doubleClickWord" | "tripleClickWord":
         
          if not(splt[1] == "one" or splt[1] == "all"): 
              closescript(text="error >one< or >all< needed after moveToText")
              return # stops running the function
            
          if splt[0] == "rightClickWord":
              screentextreadoptions("rightclick",splt[3:],splt[1],None,splt[2])
                 
          elif  splt[0] == "ClickWord":  
              screentextreadoptions("click",splt[3:],splt[1],None,splt[2])
              
          elif  splt[0] == "doubleClickWord":
               screentextreadoptions("doubleclick",splt[3:],splt[1],None,splt[2])
               
          elif  splt[0] == "tripleClickWord":
               screentextreadoptions("tripleclick",splt[3:],splt[1],None,splt[2])
       
       case "repeat":
         repeater(splt)
         
       case "screenWidth" | "screenHeight":
           if not len(splt) == 1:
                 closescript(text="uses only screenWidth or screenHeight no additional argument")
                 return # stops running the function
               
           width = GetSystemMetrics(0)
           height = GetSystemMetrics(1)
           if splt[0] == "screenWidth":
             return printer(width)
           else:
             return printer(height)   
           
       case "fileman":
            return filemanager(splt[1:]) 
       
       # all window commands
       case "inWindowTitle" | "windowList" | "focusWindow" | "focusedWindow" | "minimizeWindow" | "maximizeWindow" | "resetWindow" | "closeWindow":   
          return windowcommand(splt)
        
       case "getWindowX" | "getWindowY" | "getWindowWidth" | "getWindowHeight":   
          return windowsize(splt) 
        
       case "clipboardCopy" | "clipboardPaste":
         if splt[0] == "clipboardCopy":
          pyperclip.copy(" ".join(splt[1:]))
          variants.update({"{{clipboard}}": pyperclip.paste()})
         elif splt[0] == "clipboardPaste":
            return printer(pyperclip.paste())
          
       case "watchFile" | "watchFolder" | "watchStatus" | "stopWatching" | "changeDetected" | "filesWatched" | "restoreFile":
         
            if splt[0] == "watchFile" or splt[0] == "watchFolder" or splt[0] == "stopWatching":
                  watcher(splt)
            elif splt[0] == "watchStatus" or splt[0] == "changeDetected" or splt[0] == "filesWatched" or splt[0] == "restoreFile":
                 return viewwatched(splt)
            
       case "get":
          getcommandvalue(splt)
      
       case "timerStart" | "timerStop" | "timer":
            if  len(splt) != 1 :
                  closescript(text="timer commands do not need arguments")
                  return # stops running the function
                
            else:
              return timertrigger(splt)    
            
       case "pixelColor" | "waitPixelColor" | "getPixelColorRegion" | "colorExistsInRegion" | "colorExistsInRegionSimilar" | "toPixel" | "toHex" | "colorExistsInImage" | "colorExistsInImageSimilar":
             return pixelcommands(splt)
       
       case "registerCommand" | "removeCommand":
           if splt[0] == "removeCommand":
              commandregister(splt, remove=True) 
           else:
              commandregister(splt)    
          
       case "getEnv":
         return getEnv(splt)    
      
       case "mousePositionX" | "mousePositionY" | "mousePosition":
         x,y = pyg.position()
         if splt[0] == "mousePositionX":
               return printer(x)
         elif splt[0] == "mousePositionY":
               return printer(y)
         elif splt[0] == "mousePosition":
               return printer(f"{x},{y}")
      
       case "integer":
         try:
          cmds = splt[1:]
          result = getcommandreturns(cmds,validate=False)
          tofloat = float(result)
          toint = int(tofloat)
          return printer(toint)
         except Exception as e:
            closescript(e,text="integer error : failed to convert to integer")
            return  
          
       case "getValue":
         if not len(splt) == 2:
           closescript(text="getValue takes 1 argument",errornumber="102")
           return # stops running the function
         
         getvar = "{{"+str(splt[1])+"}}" 
         if getvar in variants:
           return printer(variants[getvar])  
         else:
           closescript(text=f"No variable named {getvar}",errornumber="103")
           return # stops running the function
         
       case "quickRun":
         quickrunexit[0] = True #set the must exit flag
         elseremove(splt)
         runcodes(splt[1:])  
         os._exit(0)
      
       case "stop" | "stopScript":
         if not len(splt) == 1:
           closescript(text="stop command does not support arguments")           
           return
         else:
           try:
              dontexecute = False
              getoptions(True)
           except Exception:
              print("SOMETHING WENT WRONG: ERROR UNKWOWN")
       
       case "exit":
         if onscript[0] == True:
            exitlabel[0] = True
            if len(splt) > 1: 
              variants.update({"{{exitmessage}}" : " ".join(splt[1:])})
         else:
            closescript(text="the exit command only works in script mode")
            return
          
       case "define" | "def" | "define:name" | "define:nameList":
         if len(splt) == 1:
               if splt[0] == "define:nameList":
                 for c in surtrcommands:
                    print(f"{c}\n")
                 return 
               elif splt[0] in ["def", "define"]:
                  for c in surtrcommands:
                    print(f"{c}\n{surtrcommands[c]}\n")
                    
         elif len(splt) == 2:
             
             if splt[0] == "define:name":
                 cfound = False
                 searchword = splt[1].lower()
                 for c in surtrcommands:
                    if c.lower().startswith(searchword):
                        print(f"{c}\n")
                        cfound = True
                 if not cfound:
                    closescript(text="No command found.")
                 return
             elif splt[1] in surtrcommands:
                  print(f"{splt[1]}\n{surtrcommands[splt[1]]}\n")  
                  
             else:
               closescript(text=f"{splt[1]} definition not available")       
               return
       
       case "json":
          return parsejson(splt)
         
       case "jsonParse":
           return jsonParse(splt)
           
       case "jsonDelete":
           jsonDelete(splt)
           
       case "jsonAppend":
           jsonAppend(splt)
              
       case "jsonSave":  
           jsonSave(splt)
           
       case  "lenJson":
          return lenJson(splt)
          
       case "startRecorder" | "stopRecorder":
        if splt[0] ==  "startRecorder":
          try:
           
           if len(splt) == 1:
             recorder.start_recording(file=None)    
           elif len(splt) == 2:
             recorder.start_recording(file=splt[1])
           elif len(splt) == 3:
             recorder.start_recording(file=splt[1], stime=splt[2])
           else:
              closescript(text="Unsupported syntax. Expected: startRecorder filename.as [stopTime]")
              return   
          except Exception as e:
           closescript(e,text="recorder error")
           return
       
        elif splt[0] == "stopRecorder":
         try:
           if (len(splt) != 1):
             closescript(text="stopRecorder does not support arguments")
             return 
           else:   
             recorder.stop_recording()
         except Exception as e:
           closescript(e,text="recorder error")
           return
         
       case "replace":
         try:
          replaceword = splt[1]
          replacer = splt[2]
          text = " ".join(splt[3:])
          completed = text.replace(replaceword, replacer)
          return printer(completed)  
         except:
           closescript(text="replace error")
           return
        
       case "setSecurityPassword" | "activateSecurity" | "deactivateSecurity" | "guestUser" | "login":
         surtrsecurity(splt)
         
       case "surtrset":
         sessionsettings(splt)
         
       case "logout":
         logoutfunc(splt)   
         
      #  case "thread": # maybe for future use
      #    th = threading.Thread(target=interpreter,args=(splt[1:],),daemon=True)
      #    th.start()
         
      #    user_input = input("surtr |=[>>> ")
      #    interpreter(user_input)
      
   
       case "run":
         runmaster(splt)

       case "cwd":
         try:
          if len(splt) == 1:
            return printer(os.getcwd())
          else:
            closescript(text="cwd command does not support arguments")
            return
         except Exception as e:
           closescript(e,text="cwd error")
           return
       
       case "empty":
         if returner[0] == True:
                returner[0] = False 
         try:
          
          if len(splt) == 1:
            return True
          else:
                
            txt = " ".join(splt[1:]).strip()
            if txt == "":
               return True  
            
            else:
                return False   
            
         except Exception as e:
            return False
           
       case "random":   
          return allrandom(splt)
          
       case "textLower" | "textUpper" | "textStartWith" | "textEndWith" | "textHas" | "toBase64" | "decodeBase64":
           return alltext(splt)
         
       case "strip":
        try:
         if len(splt) < 3:
           closescript(text="Unsupported syntax. Expected: strip <char> <text>")  
           return
         else:
           token = splt[1]
           text = " ".join(splt[2:])
           striped = text.replace(token,"")
           return printer(striped)
        except Exception as e:
          closescript(e,text= "strip error") 
          return
        
       case "textOnScreen":
             textloop(language=splt[1],texts=splt[2],command=splt[3:])
      
       case "splitRun":
           splitandrun(splt)  
            
       case "--version":
         if not len(splt) == 1:
              closescript(text="Command not valid")
         else:
            return printer("Surtr version 4.0 ") #uncomment for free 
            #return printer("Surtr pro version 4.0 ")  #uncomment for pro
        
       case "clr":
         if len(splt) != 1:
               closescript(text="cls does not support arguments")
               return
         os.system('cls' if os.name == 'nt' else 'clear')           
      
       case "fetcher":
          return fetchsite(splt) 
               
       case "webui":
              blocked = settings("blockedcommand",webui=True)
              #sblocked = blocked.split(" ")
              sblocked = shellspliter(blocked)
               
              if splt[1] in sblocked:
                 closescript(text=f"{splt[1]} command access blocked")
                 return # stops running the function
                           
              else:
                inwebui[0] = True
                splt.remove(splt[0])
                runcodes(splt)
                inwebui[0] = False 
                     
       case _:
         if not (splt[0] == ""):
           if (len(splt) == 1 and splt[0].endswith(":")):
            pass
           elif(splt[0].startswith("~~")):
              pass
            
           elif splt[0] == "?else" and len(splt) > 1 and splt[1] == "if":
                # Handle chained ?else if as if
                splt = splt[1:]
                runif_else(splt)
                return
                  
           elif(splt[0].endswith(":") == False):
                 return externalcommands(splt)
                 #closescript()
           else:
             closescript(text=f"{splt[0]} command not found")
             return # stops running the function
           
         elif (splt[0] == "" or splt[0] == "" and len(splt) > 1):
           pass
         elif (len(splt) == 1 and splt[0].endswith(":")):
            pass

def fetchsite(commandlist):
  try:
    fetchworld = srequest.main(commandlist)  
    return fetchworld
  except Exception as e:
    closescript(e,text="request fetcher error")
    return
  
  
def run_live_shell_windows(command: str):
    """
    Runs a shell command and streams output live (line by line),
    just like a real Windows shell.
    """
    try:
        process = subprocess.Popen(
            command,
            shell=True,  # Required for internal commands like `dir`
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True  # Text mode, line-by-line output
        )

        # Stream output live
        for line in process.stdout:
            print(line, end='')  # Already includes newline

        process.wait()
        print(f"\n[Done] Command exited with code {process.returncode}")
    except KeyboardInterrupt:
        process.terminate()
        
def getcommandvalue(splt):
  try:
   for v in allowreturncommands:
    if splt[2] == v:
      #specials = ['msg','confirm','userInput','readImage','readImageLanguages','readScreen','talking']
      if  'msg' == splt[2] or 'confirm' == splt[2] or 'talking' == splt[2]:
        returncmd = cmdtrueorfalse(splt[2:])
        
      elif "userInput" == splt[2]:
         returncmd = userinputhandler(app,splt[2:])
         
      elif splt[2] == "readImage" or splt[2] == "readImageLanguages" or splt[2] == "readScreen":
            returner[0] = True
            cmmnd = splt[2:]
            returncmd = readimageshandler(cmmnd,True)
      else:     
         returner[0] = True
         cmmnd = splt[2:]
         returncmd = runcodes(cmmnd) 
        
      if returncmd == None:
            closescript(text="This command Either terminated in an abnormal way or returned an Unsupported object type")
            return # stops running the function
         
      value = shellspliter(str(returncmd))
      
      value.insert(0,splt[1])
      value.insert(0,"set")
      #print(value)
      set_variables(value)
      
      #stop
      return
   
   closescript(text=f"{splt[2]} is not supported")
   return # stops running the function
   
  except Exception as e:
    closescript(e,text="Something went wrong")   
    return # stops running the function
 

def getcommandreturns(splt,validate=True):
  try:
   for v in allowreturncommands:
    if splt[0] == v:
      #specials = ['msg','confirm','userInput','readImage','readImageLanguages','readScreen','talking']
      if  'msg' == splt[0] or 'confirm' == splt[0] or 'talking' == splt[0]:
        returncmd = cmdtrueorfalse(splt)
        
      elif "userInput" == splt[0]:
         returncmd = userinputhandler(app,splt)
         
      elif splt[0] == "readImage" or splt[0] == "readImageLanguages" or splt[0] == "readScreen":
            returner[0] = True
            cmmnd = splt
            returncmd = readimageshandler(cmmnd,True)
      else:     
         returner[0] = True
         cmmnd = splt
         returncmd = runcodes(cmmnd) 
        
      if returncmd == None:
            closescript(text="This command Either terminated in an abnormal way or returned an Unsupported object type")
            return # stops running the function
          
      return  str(returncmd)  
   
   if validate == True: 
     closescript(text=f"{splt[2]} is not supported")
     return # stops running the function
   else:
      #if not validate do just run command do not replace
      returner[0] = True 
      cmmnd = splt
      returncmd = runcodes(cmmnd) 
      if returncmd == None:
        return ""
      else:
         return  str(returncmd)
     
  except Exception as e:
    closescript(e,text="Something went wrong")   
    return # stops running the function
 

init(autoreset=False)

# Foreground and background mappings (extend as needed)
_FORE = {
    "black": Fore.BLACK,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "blue": Fore.BLUE,
    "magenta": Fore.MAGENTA,
    "cyan": Fore.CYAN,
    "white": Fore.WHITE,
    # bright / light variants
    "lightblack": Fore.LIGHTBLACK_EX,
    "lightred": Fore.LIGHTRED_EX,
    "lightgreen": Fore.LIGHTGREEN_EX,
    "lightyellow": Fore.LIGHTYELLOW_EX,
    "lightblue": Fore.LIGHTCYAN_EX,   # alias for requested "light blue"
    "lightmagenta": Fore.LIGHTMAGENTA_EX,
    "lightcyan": Fore.LIGHTCYAN_EX,
    "lightwhite": Fore.LIGHTWHITE_EX,
}

_BACK = {
    "black": Back.BLACK,
    "red": Back.RED,
    "green": Back.GREEN,
    "yellow": Back.YELLOW,
    "blue": Back.BLUE,
    "magenta": Back.MAGENTA,
    "cyan": Back.CYAN,
    "white": Back.WHITE,
    # bright / light variants
    "lightblack": Back.LIGHTBLACK_EX,
    "lightred": Back.LIGHTRED_EX,
    "lightgreen": Back.LIGHTGREEN_EX,
    "lightyellow": Back.LIGHTYELLOW_EX,
    "lightblue": Back.LIGHTBLUE_EX,
    "lightmagenta": Back.LIGHTMAGENTA_EX,
    "lightcyan": Back.LIGHTCYAN_EX,
    "lightwhite": Back.LIGHTWHITE_EX,
}

# Convenience default modes
_DEFAULT_MODE_COLOR = {
    "info": ("lightblue", None),  # light blue foreground
    "warn": ("yellow", None),
    "error": ("red", None),
}

_MARKER_RE = re.compile(r'^\?em-([A-Za-z]+)(?:-([A-Za-z]+))?$')

def _get_codes(fg_name, bg_name=None):
    """Return (fore_code_or_None, back_code_or_None) or raise ValueError on unknown color."""
    fore = None
    back = None
    if fg_name:
        key = fg_name.lower()
        fore = _FORE.get(key)
        if fore is None:
            raise ValueError(f"Unknown foreground color '{fg_name}'")
    if bg_name:
        key = bg_name.lower()
        back = _BACK.get(key)
        if back is None:
            raise ValueError(f"Unknown background color '{bg_name}'")
    return fore, back

def emit_command(tokens):
    """
    tokens: list of strings, for example:
      ['emit:info', 'Hello', 'from', '?em-red', 'this part is red', 'normal']
      ['emit:color', 'magenta', 'Custom', 'color', 'text']
      ['emit:magenta', 'All', 'this', 'is', 'magenta']
      ['emit', 'plain', 'text']
      ['emit:prompt', 'plain', 'text']
      
    Returns True on success, False on handled failure.
    """
    try:
        # basic validation
        if len(tokens) == 0:
           closescript(text="No tokens provided. Expected: emit ... or 'emit:info ...")
           return
        first = tokens[0]
        if not isinstance(first, str):
            closescript(text="First token must be a string like 'emit' or 'emit:info'.")
            return
        # parse first token for mode / initial color
        mode = None
        initial_fg = None
        initial_bg = None
        prompter = False
        rest = []
       
        if first.startswith("emit:"):
            suffix = first.split(":", 1)[1].strip().lower()
            if suffix == "" or suffix == "plain":
                mode = "plain"
                rest = tokens[1:]
            elif suffix == "prompt":
                  prompter = True
                  mode = "plain"
                  rest = tokens[1:]
            elif suffix in ("info", "warn", "error"):
                mode = suffix
                rest = tokens[1:]
            elif suffix == "color":
                # expect next token as color name
                if len(tokens) < 2:
                    closescript(text="emit:color requires a color name: eg emit:color magenta text...")
                    return
                initial_fg = tokens[1].lower()
                rest = tokens[2:]
                mode = "custom"
            else:
                # treat suffix as color name (e.g. emit:magenta)
                initial_fg = suffix
                rest = tokens[1:]
                mode = "custom"
        else:
            # first token is plain 'emit' or something else
            if first.lower() != "emit":
                closescript(text="Command must start with 'emit' or 'emit:<mode|color>'.")
                return
            # look ahead for alternate syntax: ['emit', 'info', 'text...'] or ['emit', 'magenta', 'text...']
            if len(tokens) >= 2 and isinstance(tokens[1], str):
                second = tokens[1].strip().lower()
                if second in ("info", "warn", "error", "plain"):
                    mode = second
                    rest = tokens[2:]
                elif second == "color":
                    if len(tokens) < 3:
                        closescript(text="emit color eg. emit color magenta text...")
                        return
                    initial_fg = tokens[2].lower()
                    mode = "custom"
                    rest = tokens[3:]
                elif second in _FORE:
                    # color name directly: ['emit', 'magenta', 'text...']
                    initial_fg = second
                    mode = "custom"
                    rest = tokens[2:]
                else:
                    # assume plain text: ['emit', 'text...']
                    mode = "plain"
                    rest = tokens[1:]
            else:
                # ['emit'] only
                closescript(text="emit requires text or a mode. Example: emit hello or emit:info hi")
                return
        # if plain mode: print without colors (but still support inline markers that change colors)
        if mode == "plain":
            # If no rest tokens, error
            if not rest:
                closescript(text="emit plain requires text to print. Example: emit hello")
                return
            # BUT still allow inline markers in rest (they will apply)
            # fall through to normal processing; initial colors are None
        elif mode in ("info", "warn", "error"):
            fg_name, bg_name = _DEFAULT_MODE_COLOR[mode]
            initial_fg = fg_name
            initial_bg = bg_name

        # Prepare current color codes
        current_fore, current_back = None, None
        if initial_fg is not None:
            current_fore, _ = _get_codes(initial_fg, None)
        if initial_bg is not None:
            _, current_back = _get_codes(None, initial_bg)

        # if no rest tokens, error
        if not rest:
            closescript(text="emit error: empty tokens.")
            return
        # Iterate tokens and apply inline markers ?em-foreground[-background]
        pieces = []
        for tok in rest:
            # ensure token is string-like
            if tok is None:
                tok = ""
            token_str = str(tok)

            # check if token is solely a marker (after stripping whitespace)
            stripped = token_str.strip()
            m = _MARKER_RE.match(stripped)
            if m:
                fg_marker = m.group(1)
                bg_marker = m.group(2)
                # set new current colors (validate)
                new_fore, new_back = _get_codes(fg_marker, bg_marker)  # raises ValueError if unknown
                current_fore = new_fore
                current_back = new_back
                # marker does not emit text itself
                continue

            # Otherwise, emit the token using current color codes (if any)
            prefix = ""
            suffix = ""
            if current_fore:
                prefix += current_fore
            if current_back:
                prefix += current_back
            if prefix:
                suffix = Style.RESET_ALL
            pieces.append(prefix + token_str + suffix)

        # Join pieces with single spaces (tokens were separated)
        out = parsestringsnormally(" ".join(pieces))
        if prompter == True:
              getprmpt = input(out)
              return printer(getprmpt,noprint=True)
        else:   
          print(out)
          return

    except (TypeError, ValueError) as e:
        closescript(e,text=f"emit error")
        return

    except Exception as e:
        closescript(e,text=f"emit unexpected error")
        return



         
         
def userinputhandler(app, splt):
  try: 
   returns = [None]
   def userinputget():
     returns[0] = inp.get()
     dialog.destroy()
   dialog = customtkinter.CTkToplevel(app)
   dialog.config(background="white")
   # i replaced customtkinter default icon file CustomTkinter_icon_Windows.ico in py python venv folder with my own icon file so 
   # i dont need to set a default icon here
   #dialog.iconbitmap('resources\\icons\\icon.ico') # to change taskbar icon
   if "{{guititle}}" in variants:
      dialog.title(variants["{{guititle}}"]) 
   else:     
     dialog.title("Input")
     
   dialog.geometry("400x200")
   # Get screen size
   screen_width = dialog.winfo_screenwidth()
   screen_height = dialog.winfo_screenheight()
   
   if "{{guiboxposition}}" in variants:
        # Get window size
        window_width = 400
        window_height = 200
        x = None
        y = None
        if variants["{{guiboxposition}}"] == "bottomright":
          # Calculate bottom-right position
          x = screen_width - window_width - 20  # 10px margin from right
          y = screen_height - window_height - 100  # 50px margin from bottom (for taskbar)
          
        elif variants["{{guiboxposition}}"] == "bottomleft":
          # Calculate bottom-left position
          x = 30  # 10px margin from left
          y = screen_height - window_height - 100  # 50px margin from bottom (for taskbar)
          
        elif variants["{{guiboxposition}}"] == "topright":
          x = screen_width - window_width - 20
          y = 20  
        elif variants["{{guiboxposition}}"] == "topleft":   
          x = 20 
          y = 20 
        elif variants["{{guiboxposition}}"] == "center":
              
          # Calculate center position
          x = round(screen_width / 2) - round(window_width / 2)
          y = round(screen_height / 2) - round(window_height / 2)
        
        elif ":" in variants["{{guiboxposition}}"]:
            vrts = variants["{{guiboxposition}}"]
            pos = str(vrts).split(":")
            try:
                x = int(float(pos[0].strip()))
                y = int(float(pos[1].strip()))
            except:
                x = None
                y = None  
        if x is None and y is None:
            dialog.geometry(f"{window_width}x{window_height}")
        else:
           dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
   else: #default position
          # Get window size
          
          window_width = 400
          window_height = 200
          # Calculate bottom-right position
          x = screen_width - window_width - 50  # 10px margin from right
          y = screen_height - window_height - 100  # 50px margin from bottom (for taskbar)

           # Move the window
          dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
          
           
   dialog.resizable(width=False,height=False)
   dialog.grid_columnconfigure(0, weight=1)
   dialog.grid_rowconfigure(0, weight=1)
   inp = StringVar()
   info = customtkinter.CTkTextbox(dialog,width=400,height=150,wrap="word",fg_color="white",text_color="black",font=customtkinter.CTkFont(family="Calibri",size=20))
   note = [False]
   notin = ["?equ","?nequ","?cntn","?grtn","?lstn","?else"]
   for x in notin:
     if x in splt:
        note[0] = True
        e = splt.index(x) - 1
        wr = splt[1:]
        psn = parsestringsnormally(" ".join(wr[:e]))
        info.insert(1.0,psn)
        break
   if note[0] == False:
     psn = parsestringsnormally(" ".join(splt[1:]))     
     info.insert(1.0,psn)
     
   info.configure(state="disabled")
   info.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
   
   field = customtkinter.CTkEntry(dialog,width=400,height=50,fg_color="white",text_color="black",textvariable=inp,font=customtkinter.CTkFont(family="Calibri",size=20))
   field.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
   field.focus()
   button = customtkinter.CTkButton(dialog, text="OK",hover_color="grey",corner_radius=10,fg_color="black",text_color="white",command=userinputget,font=customtkinter.CTkFont(family="Calibri",size=20))
   button.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
   
   if "{{okbutton}}" in variants:
      button.configure(text=variants["{{okbutton}}"])


   dialog.grab_set()  # Make it modal
   app.wait_window(dialog)
  
   return returns[0]
 
  except Exception as e:
    closescript(e,text=f"user input error")
    return # stops running the function
  
  
def repeater(splt):
    try:
        n = int(float(splt[1]))
        if n <= 0:
           if n != -1:
              closescript(text=f"error >> {n} << must be more than zero")
              return

        commands = splt[2:]            # keep the original token list
        if n == -1:
              while True:
                runcodes(commands[:])   
        else: 
          i = 0
          while i < n:
             runcodes(commands[:])      # refresh command
             i += 1

    except Exception as e:
        closescript(e, text="repeat command error")
        return
    
def returncommand(splt):
      returner[0] = True
      if splt[0] == "runCmd":
        return runcodes(splt)
      elif splt[0] == "voices":
            return runcodes(splt)
      elif splt[0] == "screenWidth" or splt[0] == "screenHeight":
            return runcodes(splt)
          
      elif splt[0] == "fileExist" or splt[0] == "readFile" or splt[0] == "writeFile" or splt[0] == "appendFile" or splt[0] == "deleteFile":
            return runcodes(splt)
          
      elif splt[0] == "windowList" or splt[0] == "minimizeWindow" or splt[0] == "maximizeWindow" or splt[0] == "resetWindow" or splt[0] == "focusWindow" or splt[0] == "closeWindow":
            return runcodes(splt)
      elif splt[0] == "clipboardPaste":
            return printer(pyperclip.paste())
      elif splt[0] == "watchStatus" or splt[0] == "changeDetected" or splt[0] == "filesWatched" or splt[0] == "restoreFile":
            return runcodes(splt)
      elif splt[0] in allowreturncommands: # i added this new method for simplicity
            return runcodes(splt)
      else:
        closescript(text=f"error >> {splt[0]} << not supported")
        return # stops running the function
        
logicals = ["?equ","?nequ","?cntn","?grtn","?lstn"]   
    
def show_custom_dialog(app, splt):    
    returns = [None]
    def msgtruefunc():
      dialog.destroy()
      returns[0] = True
    def contruefunc():
      dialog.destroy()
      returns[0] = True
    def confalsefunc():
      dialog.destroy()
      returns[0] = False
      
    dialog = customtkinter.CTkToplevel(app)
    dialog.config(background="white")
    if "{{guititle}}" in variants:
       dialog.title(variants["{{guititle}}"]) 
    else:     
       dialog.title("Message")
       
    dialog.geometry("400x200")
    
    # Get screen size
    screen_width = dialog.winfo_screenwidth()
    screen_height = dialog.winfo_screenheight()
    
    # Get window size
    window_width = 400
    window_height = 200
   
    if "{{guiboxposition}}" in variants:
        # Get window size
        window_width = 400
        window_height = 200
        x = None
        y = None
        if variants["{{guiboxposition}}"] == "bottomright":
          # Calculate bottom-right position
          x = screen_width - window_width - 20  # 10px margin from right
          y = screen_height - window_height - 100  # 50px margin from bottom (for taskbar)
          
        elif variants["{{guiboxposition}}"] == "bottomleft":
          # Calculate bottom-left position
          x = 30  # 10px margin from left
          y = screen_height - window_height - 100  # 50px margin from bottom (for taskbar)
          
        elif variants["{{guiboxposition}}"] == "topright":
          x = screen_width - window_width - 20
          y = 20  
        elif variants["{{guiboxposition}}"] == "topleft":   
          x = 20 
          y = 20 
        elif variants["{{guiboxposition}}"] == "center":
              
          # Calculate center position
          x = round(screen_width / 2) - round(window_width / 2)
          y = round(screen_height / 2) - round(window_height / 2)
          
        elif ":" in variants["{{guiboxposition}}"]:
              vrts = variants["{{guiboxposition}}"]
              pos = str(vrts).split(":")
              try:
                x = int(float(pos[0].strip()))
                y = int(float(pos[1].strip()))
              except:
                x = None
                y = None
        if x is None and y is None:
            dialog.geometry(f"{window_width}x{window_height}")
        else:
           dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
           
    else: #default position
          # Get window size
          
          window_width = 400
          window_height = 200
          # Calculate bottom-right position
          x = screen_width - window_width - 50  # 10px margin from right
          y = screen_height - window_height - 100  # 50px margin from bottom (for taskbar)

           # Move the window
          dialog.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    #
    # i replaced customtkinter default icon file CustomTkinter_icon_Windows.ico in py python venv folder with my own icon file so 
    # i dont need to set a default icon here
    #dialog.iconbitmap('resources\\icons\\icon.ico') # to change taskbar icon
    dialog.resizable(width=False,height=False)
    dialog.grid_columnconfigure(0, weight=1)
    #dialog.grid_columnconfigure((0, 1), weight=1)  # CONFIGURE COLUMNS FOR BOTH OK AND CANCEL
    dialog.grid_rowconfigure(0, weight=1)
    info = customtkinter.CTkTextbox(dialog,width=400,height=200,fg_color="white",wrap="word",text_color="black",font=customtkinter.CTkFont(family="Calibri",size=20))
    note = [False]
    notin = ["?equ","?nequ","?cntn","?grtn","?lstn","?else"]
    for x in notin:
     if x in splt:
        note[0] = True
        e = splt.index(x) - 1
        wr = splt[1:]
        psn = parsestringsnormally(" ".join(wr[:e]))
        info.insert(1.0,psn)
        break
    if note[0] == False:  
     psn = parsestringsnormally(" ".join(splt[1:]))   
     info.insert(1.0,psn)

    info.configure(state="disabled")
    info.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    
    button_frame = customtkinter.CTkFrame(dialog, fg_color="white")
    button_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
    button_frame.grid_columnconfigure((0, 1), weight=1)   # two equal buttons
    
    if splt[0] == "msg":
      # Override the close button
      dialog.protocol("WM_DELETE_WINDOW", confalsefunc)
      
      button = customtkinter.CTkButton(button_frame, text="OK",hover_color="grey",corner_radius=10,fg_color="black",text_color="white",command=msgtruefunc,font=customtkinter.CTkFont(family="Calibri",size=20))
      button.grid(row=0, column=0, columnspan=2, padx=(0, 10), sticky="ew")  # full width OK
     
      
    if splt[0] == "confirm":
      button = customtkinter.CTkButton(button_frame, text="OK",hover_color="grey",corner_radius=10,fg_color="black",text_color="white",command=contruefunc,font=customtkinter.CTkFont(family="Calibri",size=20))
      button.grid(row=0, column=0, padx=(0, 10), pady=5, sticky="ew")
      
      button2 = customtkinter.CTkButton(button_frame, text="CANCEL",hover_color="grey",corner_radius=10,fg_color="black",text_color="white",command=confalsefunc,font=customtkinter.CTkFont(family="Calibri",size=20))
      button2.grid(row=0, column=1, padx=(0, 0), pady=5, sticky="ew")

    
    if "{{okbutton}}" in variants:
          button.configure(text=variants["{{okbutton}}"])
    
    if "{{cancelbutton}}" in variants:
          if splt[0] != "msg": #we dont need to configure button2 in msg alerts because msg dont have 2 buttons (only uses 1st button)
            button2.configure(text=variants["{{cancelbutton}}"])
          
    dialog.grab_set()  # Make it modal
    app.wait_window(dialog)  # Block until it's closed
    return returns[0]
  
    
def cmdtrueorfalse(splt):
    if not splt or len(splt) < 1:
        return False

    cmd = splt[0]
    logicals = ["?equ", "?nequ", "?cntn", "?grtn", "?lstn"]  # Define logicals globally or here if not defined

    def handle_logicals(user_cmd, handler_func):
        # Generic handler for ?equ, ?nequ, ?cntn, ?grtn, ?lstn
        for op in logicals:
            if op in user_cmd:
                # Check for multiple logical operators
                for x in logicals:
                    if x in user_cmd and x != op:
                        closescript(text="multiple logical operators")
                        return None  # Invalid

                # Divide command from operator
                userinput = user_cmd[:user_cmd.index(op)]
                logic = user_cmd[user_cmd.index(op):]
                logic.remove(op)

                # Check for duplicate same op
                if op in logic:
                    closescript(text="multiple logical operators")
                    return None  # Invalid

                logicop = " ".join(logic)

                try:
                    result = handler_func(userinput)
                    if result is None:
                        return False

                    if op == "?equ":
                        return result == logicop
                    elif op == "?nequ":
                        return result != logicop
                    elif op == "?cntn":
                        return logicop in str(result)
                    elif op == "?grtn":
                        return int(result) > int(logicop)
                    elif op == "?lstn":
                        return int(result) < int(logicop)
                except (ValueError, TypeError):
                    return False
        return None  # No logical found
    
    if cmd == "seeImage":
        if len(splt) < 2 or not (os.path.exists(splt[1]) and os.path.isfile(splt[1])):
            return False
        try:
            if len(splt) > 5:  # img x y w h
                region = (int(float(splt[2])), int(float(splt[3])), int(float(splt[4])), int(float(splt[5])))
                return pyg.locateOnScreen(splt[1], region=region) is not None
            else:  # img only
                return pyg.locateOnScreen(splt[1], confidence=0.9) is not None
        except:
            return False

    elif cmd in ["msg", "confirm"]:
        return show_custom_dialog(app, splt)

    elif cmd == "getValue":
        if len(splt) == 2:  # Simple var fetch
            getvar = "{{" + splt[1] + "}}"
            if getvar in variants:
                return bool(variants[getvar])
            return False
        elif len(splt) >= 4:
            varname = splt[1]
            op = splt[2]
            arg = " ".join(splt[3:])
            getvar = "{{" + varname + "}}"
            if getvar not in variants:
                return False
            val = variants[getvar]
            if op == "?cntn":
                return arg in str(val)
            elif op == "?equ":
                return str(val) == arg
            elif op == "?nequ":
                return str(val) != arg
            elif op == "?grtn":
                try:
                    return float(val) > float(arg)
                except ValueError:
                    return False
            elif op == "?lstn":
                try:
                    return float(val) < float(arg)
                except ValueError:
                    return False
            # Add more ops
        return False

    elif cmd in ["userInput"]:
        def handler_userinput(cmd_list):
            return userinputhandler(app,cmd_list)  # Assumes returns str/int

        logical_result = handle_logicals(splt, handler_userinput)
        if logical_result is not None:
            return logical_result
        # Fallback if no logical: just run and bool
        try:
            return bool(userinputhandler(app,splt))
        except:
            return False

    elif cmd in ["readImage", "readImageLanguages", "readScreen"]:
        returner[0] = True  # Assuming global flag

        def handler_readimage(cmd_list):
            return readimageshandler(cmd_list, True)  # Returns str/int

        logical_result = handle_logicals(splt, handler_readimage)
        if logical_result is not None:
            return logical_result
        # Fallback
        try:
            return bool(readimageshandler(splt, True))
        except:
            return False

    elif cmd == "talking":
        return speaker(splt)  # Assumes returns bool

    else:
        # For other commands
        # Check if no logicals: direct returncommand
        has_logical = any(op in splt for op in logicals)
        if not has_logical:
            try:
                return bool(returncommand(splt))
            except:
                return False

        def handler_return(cmd_list):
            return returncommand(cmd_list)  # Assumes returns str/int

        logical_result = handle_logicals(splt, handler_return)
        if logical_result is not None:
            return logical_result
        # Fallback
        try:
            return bool(returncommand(splt))
        except:
            return False    
  
  
   
def trueorfalse(splt):
  try:
    #print(splt)
    """
    Evaluates a boolean expression given as a list of tokens.
    
    Token format:
    - Values: strings or numbers (left and right operands)
    - Comparison operators: "?equ", "?nequ", "?cntn", "?grtn", "?lstn"
    - Logical operators: "?and", "?or"
    - Parentheses for nesting: "(", ")" (added for dynamic support)
    
    Example tokens: ["a", "?equ", "1", "?and", "b", "?grtn", 2, "?or", "(", "c", "?nequ", "d", ")"]
    
    Supports nesting with parentheses for more dynamic expressions.
    AND has higher precedence than OR.
    Handles empty input as False.
    
    Returns: bool - True or False
    """
    if not splt:
        return False
    
    # Define the comparison operators
    comparison_ops = {"?equ": lambda l, r: str(l) == str(r),
                      "?nequ": lambda l, r: str(l) != str(r),
                      "?cntn": lambda l, r: str(r) in str(l),
                      "?grtn": lambda l, r: float(l) > float(r),
                      "?lstn": lambda l, r: float(l) < float(r)}
    
    class Parser:
        def __init__(self, tokens):
            self.tokens = tokens[:]
            self.pos = 0
        
        def current(self):
            if self.pos < len(self.tokens):
                return self.tokens[self.pos]
            return None
        
        def eat(self, expected=None):
            tok = self.current()
            if expected is not None and tok != expected:
                raise ValueError(f"Expected {expected}, got {tok}")
            if tok is not None:
                self.pos += 1
            return tok
        
        def parse_expression(self):
            # expression = term { ("?or" | "?or") term }*
            expr = self.parse_term()
            while self.current() == "?or":
                op = self.eat()
                term = self.parse_term()
                if op == "?or":
                    expr = expr or term
            return expr
        
        def parse_term(self):
            # term = factor { ("?and" | "?and") factor }*
            term = self.parse_factor()
            while self.current() == "?and":
                self.eat("?and")
                factor = self.parse_factor()
                term = term and factor
            return term
        
        def parse_factor(self):
            # factor = "(" expression ")" | comparison
            if self.current() == "(":
                self.eat("(")
                expr = self.parse_expression()
                self.eat(")")
                return expr
            else:
                return self.parse_comparison()
        
        def parse_comparison(self):
            # comparison = left op right
            left = self.parse_value()
            if left is None:
                return False
            
            op_tok = self.current()
            if op_tok not in comparison_ops:
                closescript(text=f"Expected comparison operator, got {op_tok}")
                return
              
            op = self.eat()
            right = self.parse_value()
            if right is None:
                return False
            
            # Handle None values as False
            if left is None or right is None:
                return False
            
            compare_func = comparison_ops[op]
            try:
                return compare_func(left, right)
            except (ValueError, TypeError):
                # Handle conversion errors (e.g., non-numeric for ?grtn)
                closescript(text="Unsupported condition statement format")
                return
        
        def parse_value(self):
            # Value is any non-operator token
            tok = self.current()
            if tok in ["?or", "?and", "?equ", "?nequ", "?cntn", "?grtn", "?lstn", "(", ")"]:
                return None
            self.eat()  # Consume the value
            return tok
        
        def evaluate(self):
            try:
                result = self.parse_expression()
                if self.current() is not None:
                    closescript(text=f"Extra tokens: {self.tokens[self.pos:]}")
                    return
                return result
            except (ValueError, IndexError):
                # On parse error, return False (graceful failure)
                closescript(text="Unsupported condition statement format")
                return
    
    parser = Parser(splt)
    return parser.evaluate()
  
  except Exception as e:
    closescript(e,text="cannot run command")
    return

# continue 

def run_eachonscreen(splt):
  # get our image
   imagepath = []
   imagepath.insert(0,splt[1])
   
   # check if we have a valid image
   if(os.path.exists(splt[1]) and os.path.isfile(splt[1])):
     splt = splt[3:]
     try: 
      
       for pos in pyg.locateAllOnScreen(imagepath[0]):
        runiterate(splt, {"{{imageX}}":str(pos[0]),"{{imageY}}":str(pos[1])} )
  
     except Exception as e:
        closescript(e,"cannot run command check if this is a valid image or your image is on the screen")
        return # stops running the function
  
   else:
     closescript(text="cannot find image path")
     return # stops running the function
   
talktd = None
talk = [True]
def speaker(splt):
  global talk   
  
  talk[0] = [True]
  if len(splt) == 1 and splt[0] == "talking":
    try:
     # Check the status if our bots is still talking
        if "talkthread" in str(threading.enumerate()):
              return True
        else:
              return False
    except:
        return False
  
  # stops bot from talking in async mode    
  elif len(splt) == 1 and splt[0] == "stopTalking":
        talk[0] = False
  
  elif len(splt) == 1 and splt[0] == "voices":
        try:
          
          #stops voice if any voice is talking in background
          pythoncom.CoUninitialize()
          
          """Start the TTS engine and return the voice object"""
          pythoncom.CoInitialize()  # Required for COM (Windows API)
          tts = Dispatch("SAPI.SpVoice")
          #print(f"Available voices")
          """Get list of all installed voices"""
          voices = []
          voiceget = []
          for voice in tts.GetVoices():
            voices.append(voice.GetDescription())
          """Print all available voices with their indexes"""
          for index, name in enumerate(voices):
             #print(f"voice-{index} > {name}")
             voiceget.append(f"voice-{index} > {name}")
             
          """Properly close the TTS engine"""
          pythoncom.CoUninitialize()
          return printer("Available voices\n" + "\n".join(voiceget))
        except Exception as e:
             closescript(e,text="Something went wrong")
             return # stops running the function
          
  else:
   try:
     
     
    #stops voice if any voice is talking in background
    pythoncom.CoUninitialize()
    sp =  splt[2]
    try:
     if ":" in sp :
       spt = sp.split(":")
       if (spt[0].isnumeric() == False or spt[1].isnumeric() == False):
             closescript(text=f"only numbers allowed in speed and volume {sp}")
             return # stops running the function
         
       elif(int(spt[0]) > 10):
             closescript(text=f"speed only takes 0-10 {spt[0]}")
             return # stops running the function
           
       elif(int(spt[1]) > 100):
             closescript(text=f"volume only takes 0-100 {spt[1]}")
             return # stops running the function
       else:
             speed = int(spt[0])
             volume = int(spt[1])
     else:
          speed = int(splt[2])
          volume = 100
    except:
      closescript("Invalid syntax")        
      return # stops running the function
      
    """Start the TTS engine and return the voice object"""
    pythoncom.CoInitialize()  # Required for COM (Windows API)
    tts = Dispatch("SAPI.SpVoice")
    
    #get all voices
    voices = []
    for voice in tts.GetVoices():
      voices.append(voice.GetDescription())
    vlen =  len(voices)
    
    if splt[1].startswith("voice-"): #check if the user uses voice-
          gettype = splt[1].split("-") 
          
          if not str(gettype[1]).isnumeric():
            closescript(text="cannot run command use a number (voice-0)\nuse >> voices << to see list of available voices")
            return # stops running the function
            
          vtype = int(gettype[1])    
          if vtype +1 > vlen:
            closescript(text=f"cannot run command no voice found for (voice-{gettype[1]})\nuse >> voices << to see list of available voices")
            return # stops running the function
          
          voices = tts.GetVoices()      
          tts.Voice = voices.Item(vtype)
          print(f"Host: {voices.Item(vtype).GetDescription()}")
    else:
      closescript(text="cannot run command select your voice type (voice-0)\nuse >> voices << to see list of available voices")
      return # stops running the function
     #set the speed of the voice

    tts.Rate = speed
    
    #set the volume of the voice
    # volume from 0-100 only
    tts.Volume = volume
    #speak the voice
    #remove arguments and leave only the words to say
    if splt[0] == "say":
      splt.remove(splt[0]) #remove say the main command now the first list item will be voice type(male or female)
      splt.remove(splt[0]) #remove voice type now the first list item will be voice speed
      splt.remove(splt[0]) # remove the voice speed now the remaining items on the list will be our words we want to speak
      #print(splt)
      tostr = " ".join(splt)
      print("Saying...")
      #checking if it ia a file
      if len(splt) == 1:
        if os.path.exists(splt[0]) and os.path.isfile(splt[0]):
            f= open(splt[0],"r")
            tostr = f.read()
      tts.Speak(tostr)
      print("Done Saying")
    
    elif splt[0] == "talk":
         #runtalk(splt)
         print("Talking (async mode)")
         talktd = threading.Thread(name="talkthread",target=runtalk,args=[splt],daemon=True)
         talktd.start()  
   except Exception as e:
     closescript(e,text=f"cannot run command")
     return # stops running the function
    
def runtalk(splt):
    global talk
    #stops voice if any voice is talking in background
    pythoncom.CoUninitialize()
    sp =  splt[2]
    try:
     if ":" in sp :
       spt = sp.split(":")
       if (spt[0].isnumeric() == False or spt[1].isnumeric() == False):
             closescript(text=f"only numbers allowed in speed and volume {sp}")
             return # stops running the function
       elif(int(spt[0]) > 10):
             closescript(text=f"speed only takes 0-10 {spt[0]}")
             return # stops running the function
       elif(int(spt[1]) > 100):
             closescript(text=f"volume only takes 0-100 {spt[1]}")
             return # stops running the function  
       else:
             speed = int(spt[0])
             volume = int(spt[1])
     else:
          speed = int(splt[2])
          volume = 100
    except Exception as es:
      closescript(es,text="Invalid syntax")        
      return # stops running the function
    """Start the TTS engine and return the voice object"""
    pythoncom.CoInitialize()  # Required for COM (Windows API)
    tts = Dispatch("SAPI.SpVoice")
    
    #get all voices
    voices = []
    for voice in tts.GetVoices():
      voices.append(voice.GetDescription())
    vlen =  len(voices)
    
    if splt[1].startswith("voice-"): #check if the user uses voice-
          gettype = splt[1].split("-") 
          
          if not str(gettype[1]).isnumeric():
            closescript(text="cannot run command use a number (voice-0)\nuse >> voices << to see list of available voices")
            return # stops running the function
          vtype = int(gettype[1])    
          if vtype +1 > vlen:
            closescript(text=f"cannot run command no voice found for (voice-{gettype[1]})\nuse >> voices << to see list of available voices")
            return # stops running the function
          voices = tts.GetVoices()      
          tts.Voice = voices.Item(vtype)
          #print(f"Host: {voices.Item(vtype).GetDescription()}") #already defined in speaker function
    else:
      closescript(text="cannot run command select your voice type (voice-0)\nuse >> voices << to see list of available voices")
      return # stops running the function
     #set the speed of the voice

    tts.Rate = speed
    
    #set the volume of the voice
    # volume from 0-100 only
    tts.Volume = volume
    splt.remove(splt[0]) #remove talk the main command now the first list item will be voice type(male or female)
    splt.remove(splt[0]) #remove voice type now the first list item will be voice speed
    splt.remove(splt[0]) # remove the voice speed now the remaining items on the list will be our words we want to speak
    #print(splt)
    tostr = " ".join(splt)
    #checking if it ia a file
    if len(splt) == 1:
        if os.path.exists(splt[0]) and os.path.isfile(splt[0]):
            f= open(splt[0],"r") 
            tostr = f.read()
    tts.Speak(tostr,1)
      
    # dont stop speech because its talking in background
    #pythoncom.CoUninitialize()
    while not stop_event.is_set():
       time.sleep(1)
       if talk[0] == False:
        pythoncom.CoUninitialize()  
        #print("Talking stopped")
        talk[0] = True
        break



def runif_else(splt):
    if_type = "cmd" #cmd mode normal. Use stmt for command statement 
    # Skip leading ?else for chained conditions
    while len(splt) > 0 and splt[0] == "?else":
        splt = splt[1:]
    #check for statement type g;obal
    if "{{ctype}}" in variants:
        if variants["{{ctype}}"] == "stmt":
            if_type = "stmt"
        elif variants["{{ctype}}"] == "cmd":
            if_type = "cmd"  
     
    #inline statement type         
    if splt[1] == "ctype:stmt":
        if_type = "stmt"
        splt.pop(1)
    elif splt[1] == "ctype:cmd":
       if_type = "cmd" 
       splt.pop(1)
    
    
    
       
    # for "not"
    if len(splt) > 1 and splt[1] == "not":
        runnot_else(splt[1:],type=if_type)
        return

    elsecode = []  # always define it

    # for ?else - extract from full splt before ?run
    original_splt = splt.copy()
    if "?else" in original_splt:
        e = original_splt.index("?else")
        elsecode = original_splt[e + 1:]  # get else block
        splt = original_splt[:e]  # keep everything before ?else

    # extract ?run from if command
    if "?run" not in splt:
        closescript(text="error >> ?run << missing in if command")
        return

    rn = splt.index("?run")
    rncode = splt[rn + 1:]  # commands after ?run
    splt = splt[:rn]  # condition part only

    # remove "if"
    if splt and splt[0] == "if":
        splt = splt[1:]

    # evaluate condition
    #normal statement
    if if_type == "stmt":
      if trueorfalse(splt):
         runcodes(rncode)
      else:
        if elsecode:
            runcodes(elsecode)
    #command statement
    else:
      if cmdtrueorfalse(splt):
             runcodes(rncode)
      else:
        if elsecode:
            runcodes(elsecode)      

def runnot_else(splt, type="cmd"):
    # Skip leading ?else for chained conditions
    while len(splt) > 0 and splt[0] == "?else":
        splt = splt[1:]

    # always define elsecode
    elsecode = []

    # for ?else - extract from full splt before ?run
    original_splt = splt.copy()
    if "?else" in original_splt:
        e = original_splt.index("?else")
        elsecode = original_splt[e + 1:]  # get else block
        splt = original_splt[:e]  # keep everything before ?else

    # extract ?run
    if "?run" not in splt:
        closescript(text="error >> ?run << missing in not-if command")
        return

    rn = splt.index("?run")
    rncode = splt[rn + 1:]  # commands after ?run
    splt = splt[:rn]  # condition part only

    # remove the "not"
    if splt and splt[0] == "not":
        splt = splt[1:]

    # invert condition
    #normal statement
    if type == "stmt":
      if not trueorfalse(splt):
        runcodes(rncode)
      else:
        if elsecode:
            runcodes(elsecode)
    #command statement
    else:
      if not cmdtrueorfalse(splt):
            runcodes(rncode)
      else:
        if elsecode:
            runcodes(elsecode)    

def run_not(splt):
      if_type = "cmd"
      if "{{ctype}}" in variants:
        if variants["{{ctype}}"] == "stmt":
          if_type = "stmt"
        elif variants["{{ctype}}"] == "cmd":
          if_type = "cmd"
            
      if splt[1] == "ctype:stmt":
            if_type = "stmt"
            splt.pop(1)
      elif splt[1] == "ctype:cmd":
           if_type = "cmd" 
           splt.pop(1)
    
      if if_type == "cmd":
       if cmdtrueorfalse(splt[1:]):
            if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
              returner[0] = False
            return False
       else:
          if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
              returner[0] = False
          return True
        
      else:
        if trueorfalse(splt[1:]):
          if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
            returner[0] = False
          return False
        else:
          if returner[0] == True: #handle if command returner variable becauuse we are not using printer()
            returner[0] = False
          return True
 
    
def runwhile(original_splt):
    # Work on a copy so we don't destroy the original line
    splt = original_splt[:]

    if_type = "cmd"
    if "{{ctype}}" in variants:
        if variants["{{ctype}}"] == "stmt":
            if_type = "stmt"

    negate = False

    # Handle inline ctype
    if len(splt) > 1 and splt[1] in ("ctype:stmt", "ctype:cmd"):
        if splt[1] == "ctype:stmt":
            if_type = "stmt"
        splt.pop(1)

    # Handle 'not'
    if len(splt) > 1 and splt[1] == "not":
        negate = True
        splt.pop(1)

    # Must have ?run
    if "?run" not in splt:
        closescript("error >> ?run << missing in while")
        return

    run_idx = splt.index("?run")

    # Extract condition tokens: everything after 'while' and before '?run'
    condition_part = splt[1:run_idx]  # skip the "while" keyword itself
    if condition_part and condition_part[0] == "while":
        condition_part = condition_part[1:]

    # Body = everything after ?run
    body = splt[run_idx + 1:]

    # MAIN LOOP: re-evaluate condition fresh every single time
    while True:
        # ←←← CRITICAL: Make a FRESH copy of condition tokens every loop
        cond_tokens = condition_part[:]

        # Evaluate condition using latest variable state
        if if_type == "stmt":
            condition_met = trueorfalse(cond_tokens)  # this MUST read from global vars/variants
        else:
            condition_met = cmdtrueorfalse(cond_tokens)

        if negate:
            condition_met = not condition_met

        # If condition is false → exit loop
        if not condition_met:
            break

        # ←←← Execute body (this updates your variables!)
        runcodes(body)

        # Optional: safety net against true infinite loops
        # (remove or increase in production)
        # global loop_counter
        # loop_counter += 1
        # if loop_counter > 10000:
        #     closescript("error >> infinite loop detected")
        #     return

def run_until(splt):
    if_type = "cmd" #cmd mode normal. Use stmt for command statement 

    #check for statement type global
    if "{{ctype}}" in variants:
        if variants["{{ctype}}"] == "stmt":
            if_type = "stmt"
        elif variants["{{ctype}}"] == "cmd":
            if_type = "cmd"  
     
    #inline statement type         
    if splt[1] == "ctype:stmt":
        if_type = "stmt"
        splt.pop(1)
    elif splt[1] == "ctype:cmd":
       if_type = "cmd" 
       splt.pop(1)
   
    negate = False
    if splt[1] == "not":
        splt.pop(1)  
        negate = True

    # extract ?run from until command
    if "?run" not in splt:
        closescript(text="error >> ?run << missing in if command")
        return

    rn = splt.index("?run")
    rncode = splt[rn + 1:]  # commands after ?run
    splt = splt[:rn]  # condition part only

    # remove "if"
    if splt and splt[0] == "until":
        splt = splt[1:]

    # evaluate condition
    #normal statement
    
    if if_type == "stmt":
      if negate:    
         while trueorfalse(splt):
           runcodes(rncode)
      else:
         while not trueorfalse(splt):
             runcodes(rncode)   
    #command statement
    else:
      if negate:
          while cmdtrueorfalse(splt):
             runcodes(rncode)
      else:
          while not cmdtrueorfalse(splt):
                 runcodes(rncode)  





def allruns(splt,runner):
  
  elseremove(splt)
  try:
    # if user runs a only file  .as script  
   if(len(splt) == 2): 
     if(os.path.exists(splt[1]) and os.path.isfile(splt[1]) and Path(splt[1]).suffix == '.as'):
         runhandler(text=splt[1],file="yes",fileargs="no") 
         
     elif(splt[1].endswith(":") == True): 
         runhandler(text=splt[1],file="no",fileargs="no",currentscript=runner)
         
   # if user run only a label from the current script            
   elif(splt[1].endswith(":") == True):  
     # use splt[1:] in case of arguments
     #check if it as args
     
     if (len(splt) > 2 ):
       if(splt[2] == "?arg"):
          runhandler(text=splt[1:],file="no",fileargs="no",currentscript=runner)
     else:
          runhandler(text=splt[1],file="no",fileargs="no",currentscript=runner)
   # if user runs a label from another script 
   elif(splt[2].endswith(":")):             
          #check if first option  is a file
     
     if (os.path.exists(splt[1]) and os.path.isfile(splt[1]) and Path(splt[1]).suffix == '.as'):
       if(splt[2].endswith(":") == True):
          if (len(splt) > 3 ):
             if(splt[3] == "?arg"):
               runhandler(text=splt[1],label=splt[2:],file="yes",fileargs="yes")
          else:
             runhandler(text=splt[1],label=splt[2],file="yes",fileargs="yes")
     else:
         closescript(text=f"error in run arguments {splt[2]} not a label")
         return # stops running the function
   else:
      closescript(text=f"error in run arguments {splt[1]} is not a valid script")
      return # stops running the function
  
  except Exception as e:
    closescript(e,text="cannot run command") 
    return # stops running the function
    

def interpreter(runner):
    global dontexecute
    if isinstance(runner, str) and os.path.exists(runner):
        if os.path.isfile(runner) and Path(runner).suffix == '.as':
            try:
                labelcache.clear()
                dontexecute = False
                onscript[0] = True  # notify user is using a script
                with open(runner, 'r') as f:
                    # print(f"Command file size is {os.path.getsize(runner)} bytes")
                    currentscript[0] = runner
                    # print("RUNNING...")
                    # for line in f:
                    # we are using while true to allow us to use f.tell() to know our label positions in script
                    while True:
                        linepos = f.tell()  # holds the current line we are at the script
                        line = f.readline()
                        if not line:  # stop at the end of the script
                            break
                        strp = line.strip()
                        if not strp:
                            continue

                        # handles comments
                        if strp.startswith("~~"):
                            continue

                        # splt = strp.split()
                        splt = shellspliter(strp,firstcall=True)
                        if not splt:
                            continue

                        # if a label is found add to labelcache
                        if len(splt) == 1 and splt[0].endswith(":"):
                            labelcache.update({splt[0]: linepos})

                executer(runner)

            except Exception as e:
                onscript[0] = False
                closescript(e, text="error reading file")
                return  # stops running the function
        else:
            closescript(text="error .as file not found or incorrect format")
            return  # stops running the function

    else:
        # If runner is not a file, treat it as raw input or list of args
        if not isinstance(runner, list):
            runner = runner.strip()
            # splt = runner.split()
            splt = shellspliter(runner,firstcall=True)
        else:
            splt = runner

        splt = [token for token in splt if token]  # remove empty strings

        if not splt:
            splt.append("")

        # variables(splt)
        muststop = specialjoiners(splt)
        if muststop:
            return

        runcodes(splt)


def executer(runner):
  global seeker, dontexecute, newlistrunrequest, stoplistexec
  try:
    with open(runner, 'r') as f:
        while True:
            # before reading another script line check if a run executer_list
            # has been requested to avoide skipping commands
            if newlistrunrequest == True:
                # print(f"request accepted stop status: {stoplistexec}")
                newlistrunrequest = False
                executer_list(runcmdlist)
                continue

            # linepos = f.tell() #holds the current line we are at the script
            if seeker != None:
                f.seek(seeker)  # jump to the label
                seeker = None
                f.readline()  # skip first label

            line = f.readline()
            if not line:  # stop at the end of the script
                break
            strp = line.strip()
            if not strp:
                continue

            # handles comments
            if strp.startswith("~~"):
                continue

            # splt = strp.split()
            splt = shellspliter(strp,firstcall=True)
            if not splt:
                continue

            # handle labels starting with _
            if len(splt) == 1 and splt[0].endswith(":") and splt[0].startswith("_"):
                dontexecute = True
                continue
            # if dontexecute is on dont run till you find a label
            if dontexecute:
                if len(splt) == 1 and splt[0].endswith(":"):
                    dontexecute = False
                    continue
                else:
                    continue

            muststop = specialjoiners(splt)
            if muststop:
                continue  # am using continue instead of return because i dont want to stop the loop
            # run the code
            runcodes(splt)
            
    paramlist.clear()
    onscript[0] = False  # notify when done executing commands in script
  finally:
    paramlist.clear()
    onscript[0] = False  # notify when done executing commands in script
    
    
def executer_list(label_commands_list):
  global stoplistexec, listexecrunning, dontexecute, newlistrunrequest, commandcut, commandsplit
  """
    Executes commands from a list instead of a script file.
    Mimics the behavior of 'executer'.
  """
  # Clear continuation state for fresh execution
  try:
    #commandsplit.clear()
    #commandcut[0] = False
    index = 0
    commands = label_commands_list.copy() #get a copy of commands in case of runhandler unanounced clearing

    total = len(commands)
    dontexecute = False
    listexecrunning = True  # set the running flag
    while index < total:
        line = commands[index]
        strp = line.strip()
        if not strp:
            index += 1
            continue

        # handles comments
        if strp.startswith("~~"):
            index += 1
            continue

        # Split command
        splt = shellspliter(strp,firstcall=True)
        if not splt:
            index += 1
            continue

        # Handle labels starting with '_'
        if len(splt) == 1 and splt[0].endswith(":") and splt[0].startswith("_"):
            dontexecute = True
            index += 1
            continue

        if dontexecute:
            if len(splt) == 1 and splt[0].endswith(":"):
                dontexecute = False
            index += 1
            continue

        # Check for special joiners
        muststop = specialjoiners(splt)
        if muststop:
            index += 1
            continue

        
        #if the stop label flag is set stop the label (before any execution happens)
        if exitlabel[0] == True:
           exitlabel[0] = False
           listexecrunning = False
           break
         
        # Normal execution 
        # check if there are arguments    
        if len(arglist) == 0:
            runcodes(splt)
        else:
            i = 0
            while i < len(arglist):
                # now lets replace our argument with values
                for wrd in splt:
                    ag = "?arg" + str(i)
                    agall = "?arg*"
                    argtotal = "?arg#"
                    
                    if ag == wrd:
                        ind = splt.index(wrd)
                        #argrp = re.sub(rega, arglist[i], wrd)
                        splt[ind] = wrd.replace(ag, arglist[i])  # Literal replace, no parsing  
                        #splt[ind] = argrp

                    elif agall == wrd:
                        ind = splt.index(wrd)
                        splt[ind] = wrd.replace(agall, " ".join(arglist))  # Literal replace, no parsing  
                        #argrp = re.sub(regall, " ".join(arglist), wrd)
                        #splt[ind] = argrp
                        
                    elif argtotal == wrd:
                        ind = splt.index(wrd)
                        splt[ind] = wrd.replace(argtotal, str(len(arglist)))  # Literal replace, no parsing  
                        #argrp = re.sub(argtotal, str(len(arglist)), wrd)
                        #splt[ind] = argrp

                i += 1

            runcodes(splt)

        
        #on every complete run check if a stop request is called 
        if stoplistexec == True:
              #print("stopped request detected stopping")
              stoplistexec = False
              listexecrunning = False
              exitlabel[0] = False
              break


        # Move to next line
        index += 1
    listexecrunning = False
    exitlabel[0] = False
  
  finally:
        listexecrunning = False
        exitlabel[0] = False

def create_icon():
    # Transparent background – perfect for tray
    img = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # === Even bigger red-metal blade (taller & wider for more presence) ===
    # Main blade body (dark red metal with metallic gradient)
    blade_points = [(32, 2), (22, 50), (42, 50)]  # made taller & wider
    d.polygon(blade_points, fill='#990000', outline='#DD4444', width=3)

    # Metallic shine (brighter red highlights for realistic metal glow)
    d.line((32, 4, 32, 48), fill='#FF4444', width=4)  # strong center glow
    d.line((32, 4, 32, 48), fill='#FF7777', width=2)  # softer glow layer
    d.line((24, 50, 32, 2), fill='#CC3333', width=2)  # left edge shine
    d.line((40, 50, 32, 2), fill='#CC3333', width=2)  # right edge shine

    # Cross-guard (wider metallic)
    d.rectangle((16, 50, 48, 56), fill='#777777', outline='#BBBBBB', width=2)

    # Hilt (longer, textured red-metal)
    d.rectangle((29, 56, 35, 64), fill='#550000')
    for y in range(56, 64, 2):
        d.line((29, y, 35, y), fill='#770000', width=1)  # texture

    # Pommel (bigger round metallic)
    d.ellipse([24, 62, 40, 78], fill='#888888', outline='#AAAAAA', width=2)

    return img
  
  
def hide_console_window():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 0)  # 0 = SW_HIDE

def show_console_window():
    hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if hwnd:
        ctypes.windll.user32.ShowWindow(hwnd, 1)  # 1 = SW_SHOWNORMAL

def exit_action(icon, item):
    icon.stop()
    os._exit(0)

def start_tray_icon():
    icon_img = create_icon()

    menu = Menu(
        MenuItem("HideWindow", lambda icon, item: hide_console_window()),
        MenuItem("ShowWindow", lambda icon, item: show_console_window()),
        MenuItem("Exit", exit_action)
    )

    tray_icon = Icon("SurtrTrayIcon", icon_img, "Surtr", menu)
    tray_icon.run()



def getoptions(errorreturn = False):
    global dontexecute,seeker,newlistrunrequest,stoplistexec,runcmdlist,arglist,listexecrunning
    #reset everything
    seeker = None
    newlistrunrequest = False
    stoplistexec = False
    runcmdlist.clear()
    arglist.clear()
    listexecrunning = False
    dontexecute = False  
    labelcache.clear()
    onscript[0] = False
    vip_run[0] = False
    paramlist.clear()
    commandcut[0] = False
    commandsplit.clear()
    commandsjoins.clear()
    commandlns[0] = False
    autojoin[0] = False
    dontparsevariable[0] = False
    exitlabel[0] = False
    parentcommands[0] = False
    
    if returner[0] == True:
            returner[0] = False
            
    #if quickrun exit is set
    if quickrunexit[0] == True:
          os._exit(0) 
         
    try:
        if errorreturn == True:
            if runonce[0] == True: #check if it is a run once command
               sys.exit(0) 
           
            while True:  
                dontparsevariable[0] = False
                if returner[0] == True:
                  returner[0] = False          
                user_input = input("|=[>>> ")
                interpreter(user_input)   
              
              
        usrargs = sys.argv[1:]  # skip the script/exe name
        if len(usrargs) == 1:
            # Normalize path to avoid issues like \UXXXXXXXX errors
            user_path = os.path.normpath(usrargs[0])
            if os.path.exists(user_path) and os.path.isfile(user_path):
                #print(f"Using .as script |=[>>> {user_path}")
                interpreter(user_path)
            else:
                interpreter(usrargs)

        elif len(usrargs) > 1:
            if usrargs[0] == "run":
                interpreter(usrargs)
            else:
                runcodes(usrargs)

        elif len(usrargs) == 0:
            default_script = os.path.normpath("default.as")
            if os.path.exists(default_script) and os.path.isfile(default_script) and Path(default_script).suffix == ".as":
                interpreter(default_script)
            else:
                user_input = input("surtr |=[>>> ")
                interpreter(user_input)
        
        # when finished running commands wait for more only if runonce is not set
        if runonce[0] == True:
            sys.exit(0) 
            
        while True:
          dontparsevariable[0] = False
          if returner[0] == True:
                returner[0] = False
          user_input = input("|=[>>> ")
          interpreter(user_input)
          
    except Exception as e:
        closescript(e,text=f"cannot execute, Error detected")
        return # stops running the function
        
    except KeyboardInterrupt as e:
        closescript(e,text="Keyboard interupt (closing)")
        return # stops running the function


if __name__ == '__ main __':
  #interpreter(input("surtr |=[>>> "))
  pass

if settings("trayIcon") == "yes":
   threading.Thread(target=start_tray_icon, daemon=True).start()

#before starting surtr
if len(sys.argv[1:]) > 0: #if it has arguments run and exit
  runonce[0] = True
  
getoptions()