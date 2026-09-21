import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog, Menu
import json
import os
import time
from datetime import datetime, timedelta
from threading import Thread, Event
from queue import Queue
import subprocess
import random
import tempfile
import winreg
from typing import Optional
import sys
import re
from pygments import highlight
from pygments.token import Token, Keyword, Name, Comment, String, Operator, Number, Generic, Text
from pygments.lexer import RegexLexer, bygroups, include

ctk.set_appearance_mode("dark")


# ────────────────────────────────────────────────
# Globals
# ────────────────────────────────────────────────

PATH = None  # last saved script path
info = []
output_queue = Queue()
stop_event = Event()


# check for resources folder first (only for windows)
if(os.path.exists(os.path.normpath("resources")) and os.path.isdir(os.path.normpath("resources"))):
    resource_path = os.path.normpath("resources")  
elif (os.path.exists(os.path.normpath("C:\\Surtr\\surtr\\resources")) and os.path.isdir(os.path.normpath("C:\\Surtr\\surtr\\resources"))):
    resource_path = os.path.normpath("C:\\Surtr\\surtr\\resources")
else:
    messagebox.showerror("Error","cannot find 'resources' folder\nif you have it put it in (C:\\Surtr\\surtr\\resources) then start surtr")
    
configfile = os.path.join(resource_path,"surtrconfig.conf")
taskfile = os.path.join(resource_path, "updates", "tasksbot.json")
themefile = os.path.join(resource_path, "theme", "theme.json")


TASKS_FILE = taskfile
 
def settings(index):
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

if settings("useSurtrTheme") == "yes":
    ctk.set_default_color_theme(themefile)
else:
    ctk.set_default_color_theme("dark-blue")
    
    
    
# ===============================
# Registry configuration
# ===============================

APP_KEY = r"Software\Surtr"
VALUE_NAME = "LastScriptPath"


# ===============================
# Core functions
# ===============================

def save_last_script(path: str) -> None:
    """
    Save (or overwrite) the last opened script path.
    Safe to call repeatedly.
    """
    if not isinstance(path, str):
        messagebox.showerror("Error", "path must be a string")
        return

    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, APP_KEY) as key:
        winreg.SetValueEx(
            key,
            VALUE_NAME,
            0,
            winreg.REG_SZ,
            path
        )


def load_last_script() -> Optional[str]:
    """
    Load the last opened script path.
    Returns None if not set.
    """
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, APP_KEY) as key:
            value, regtype = winreg.QueryValueEx(key, VALUE_NAME)
            if regtype == winreg.REG_SZ and value:
                return value
    except FileNotFoundError:
        pass

    return None


def clear_last_script() -> None:
    """
    Remove the stored script path from the registry.
    """
    try:
        with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            APP_KEY,
            0,
            winreg.KEY_SET_VALUE
        ) as key:
            winreg.DeleteValue(key, VALUE_NAME)
    except FileNotFoundError:
        pass


# ===============================
# Safety / validation helpers
# ===============================

def load_last_script_if_exists() -> Optional[str]:
    """
    Load last script path only if the file still exists.
    Auto-cleans registry if invalid.
    """
    path = load_last_script()
    if path and os.path.exists(path):
        return path

    # Cleanup invalid path
    if path:
        messagebox.showinfo("Info", "Last opened script not found, clearing record.")
        clear_last_script()

    return None


def has_last_script() -> bool:
    """
    Check if a last script path is stored.
    """
    return load_last_script() is not None





def shorten_last_file_path(max_path_len: int = 20) -> str:

    path = load_last_script_if_exists()
    if path:
        full_path = path
        full_path = os.path.normpath(full_path)

        directory, filename = os.path.split(full_path)

    else:
        full_path = "[NEW SCRIPT]"
        return full_path
    
    if len(directory) > max_path_len:
        directory = directory[:max_path_len] + "..."

    return os.path.join(directory, filename)




# ────────────────────────────────────────────────
# Tasks persistence
# ────────────────────────────────────────────────
def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_tasks(tasks):
    with open(TASKS_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=2)



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

def shorten(text, max_len=120):
    return text if len(text) <= max_len else text[:max_len] + "..."

def runsurtrcommand(
    command: str,
    scriptmode: bool = False,
    path: str | None = None,
) -> str:
    """
    Run surtr.exe in a new visible CMD window every time.
    Handles output based on surtrUiOutput and keepOutputShellOpen settings.
    """
    exe_path = "surtr.exe"
    info.clear()

    commandlist = text_to_list(command)
    shortentext = shorten(command)

    # Prepare base command
    if scriptmode:
        if path:
            script_path = path
            info.append(f"[Surtr] Using existing script: {script_path}")
        else:
            tmpdir = tempfile.mkdtemp(prefix="surtr_tmp_")
            random_number = random.randint(10000, 99999)
            script_name = f"scrpt{random_number}.as"
            script_path = os.path.join(tmpdir, script_name)
            info.append(f"[Surtr] Creating temporary script: {script_path}")

            try:
                with open(script_path, "w", encoding="utf-8", errors="replace") as f:
                    f.write(command)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to write script: {e}")
                return ""

        base_cmd = [exe_path, "run", script_path]
        cwd = os.path.dirname(script_path) or os.getcwd()
    else:
        info.append(f"[Surtr] Running command directly: {shortentext}")
        base_cmd = [exe_path] + commandlist
        cwd = os.getcwd()

    # ────────────────────────────────────────────────
    # Determine settings
    # ────────────────────────────────────────────────
    keep_open = settings("keepOutputShellOpen") == "yes"
    output_mode = settings("surtrUiOutput")

    # Always wrap with cmd.exe for new console control
    if keep_open:
        cmd_prefix = ["cmd", "/k"]
        info.append("[Surtr] Keep open: yes (window stays after finish)")
    else:
        cmd_prefix = ["cmd", "/c"]
        info.append("[Surtr] Keep open: no (window auto-closes)")

    base_cmd = cmd_prefix + base_cmd

    # Output handling
    if output_mode == "app":
        # Capture to GUI → pipe output (window opens but blank)
        stdout_setting = subprocess.PIPE
        stderr_setting = subprocess.STDOUT
        capture = True
        info.append("[Surtr] Output mode: app (captured to GUI, console blank)")
    else:  # shell
        # Live in console → no pipes
        stdout_setting = None
        stderr_setting = None
        capture = False
        info.append("[Surtr] Output mode: shell (live in console, no capture)")

    # ────────────────────────────────────────────────
    # Launch
    # ────────────────────────────────────────────────
    try:
        info.append("[Surtr] Opening new CMD window...")

        process = subprocess.Popen(
            base_cmd,
            stdout=stdout_setting,
            stderr=stderr_setting,
            text=True,
            encoding="utf-8",
            errors="replace",
            cwd=cwd,
            creationflags=subprocess.CREATE_NEW_CONSOLE
        )

        if capture:
            stdout, _ = process.communicate()
            output = stdout.strip() if stdout else ""
        else:
            process.wait()
            output = ""

        returncode = process.returncode

        info.append("[Surtr] Process finished.")
        if returncode != 0:
            info.append(f"[Surtr] Exit code: {returncode}")
        if output:
            info.append(f"[Surtr] Captured output:\n{output}")
        elif not capture:
            info.append("[Surtr] Output shown live in console window.")

        # Cleanup temp if needed
        if scriptmode and path is None and os.path.exists(script_path):
            try:
                os.remove(script_path)
                os.rmdir(tmpdir)
                info.append("[Surtr] Temp cleaned up.")
            except Exception as e:
                info.append(f"[Surtr] Cleanup failed: {e}")

        return output

    except Exception as e:
        if scriptmode and path is None and 'script_path' in locals() and os.path.exists(script_path):
            try:
                os.remove(script_path)
                os.rmdir(tmpdir)
            except:
                pass
        info.append(f"[Surtr] Failed to launch: {e}")
        return ""
    
       
# ────────────────────────────────────────────────
# Main App
# ────────────────────────────────────────────────
class SurtrApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
      
        lastscript = shorten_last_file_path()
        self.title(f"Surtr - Automation UI {lastscript}")
        self.geometry("1100x720")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        ##
        # NEW: Create a horizontal PanedWindow for the main layout
        main_paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=5, bg="#222")
        main_paned.grid(row=0, column=0, sticky="nsew")
        ##
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        ##
        # Sidebar (tabs area)
        sidebar = ctk.CTkFrame(self, width=220, corner_radius=0) 
        # sidebar.grid(row=0, column=0, sticky="nsew")  # REMOVED this line
        # sidebar.grid_propagate(False)  # REMOVED this line (PanedWindow handles sizing)
        
        
        ctk.CTkLabel(sidebar, text="Surtr v4", font=("Arial", 26, "bold")).pack(pady=(40, 20))

        ctk.CTkButton(sidebar, text="Terminal", command=lambda: self.show_frame("terminal")).pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(sidebar, text="Script Builder", command=lambda: self.show_frame("builder")).pack(fill="x", padx=20, pady=6)
        ctk.CTkButton(sidebar, text="Surtr Bot Tasks", command=lambda: self.show_frame("tasks")).pack(fill="x", padx=20, pady=6)

        # Add sidebar to the new paned (fixed initial width, but now resizable)
        main_paned.add(sidebar, minsize=150, width=220)  # minsize prevents collapsing too small

        # Main area (container for frames)
        self.container = ctk.CTkFrame(self)
        # self.container.grid(row=0, column=1, sticky="nsew")  # i REMOVED this line
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # Add container to the new paned (stretches to fill remaining space)
        main_paned.add(self.container, stretch="always")

        self.frames = {}
        for F, name in [
            (TerminalFrame,   "terminal"),
            (ScriptBuilderFrame, "builder"),
            (TasksFrame,      "tasks")
        ]:
            frame = F(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("terminal")


        # Poll output
        self.after(250, self.process_queue)
        self.after(2000, self.titlechecker)

    def show_frame(self, name):
        if name in self.frames:
            self.frames[name].tkraise()
        else:
            messagebox.showerror("Error", f"Tab '{name}' not found")

    def process_queue(self):
        while not output_queue.empty():
            line = output_queue.get()
            for frame in self.frames.values():
                if hasattr(frame, "append_output"):
                    frame.append_output(line)
        self.after(250, self.process_queue)
                    
    def titlechecker(self):
        lastscript = shorten_last_file_path()
        self.title(f"Surtr - Automation UI {lastscript}")
        self.after(2000, self.titlechecker)

    def on_closing(self):
        stop_event.set()
        self.destroy()



# ────────────────────────────────────────────────
# Terminal
# ────────────────────────────────────────────────
class TerminalFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.output = ctk.CTkTextbox(self, state="disabled", font=("Consolas", 13))
        self.output.pack(fill="both", expand=True, padx=12, pady=12)

        entry_frame = ctk.CTkFrame(self)
        entry_frame.pack(fill="x", padx=12, pady=8)

        self.entry = ctk.CTkEntry(entry_frame, placeholder_text="Enter command...")
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", self.on_enter)

        ctk.CTkButton(entry_frame, text="Run", width=90, command=self.on_enter).pack(side="right", padx=5)

    def append_output(self, text):
        self.output.configure(state="normal")
        self.output.insert("end", text)
        self.output.see("end")
        self.output.configure(state="disabled")

    def on_enter(self, event=None):
        cmd = self.entry.get().strip()
        if cmd:
            runsurtrcommand(cmd, scriptmode=False)
            output = "\n".join(info)
            self.append_output(f"  [Execution Complete]\n{output}\n\n")
        self.entry.delete(0, "end")

# ────────────────────────────────────────────────
# Script Builder
# ────────────────────────────────────────────────
script_commands = {
    "Basic": [
        ("Comment", "~~ <comment>"),
        ("Wait", "wait <seconds>"),
        ("Message Box", "msg <message>"),
        ("Confirm", "confirm <question>"),
        ("User Input", "userInput <prompt>"),
        ("Speak", "say <text>"),
        ("Talk (async)", "talk <text>"),
        ("Stop Script", "stopScript"),
        ("End Surtr", "end"),
        ("Stop Current Label", "stop"),
        ("Exit Current Label", "exit"),
        ("Clear Screen", "clr"),
        ("Version", "--version"),
    ],

    "Logic & Conditions": [
        ("If", "if <condition> ?run <command> [?else <else_command>]"),
        ("While", "while <condition> ?run <command>"),
        ("Until", "until <condition> ?run <command>"),
        ("Repeat", "repeat <times> <command>"),
        ("Each On Screen", "eachOnScreen <imagefile> ?run <command>"),
        ("Split Run", "splitRun <text> ?run <command>"),
        ("Not", "not <condition>"),
        ("Else", "?else <command>"),
    ],

    "Screen & Image": [
        ("See Image", "seeImage <imagefile> [region x y w h]"),
        ("Text On Screen", "textOnScreen <lang> <text> <command>"),
        ("Pixel Color", "pixelColor <x> <y> [hex:yes]"),
        ("Wait Pixel Color", "waitPixelColor <x> <y> <colorhex> [timeout]"),
        ("Color Exists In Region", "colorExistsInRegion <x> <y> <w> <h> <color> [similar]"),
        ("Color Exists In Image", "colorExistsInImage <imagepath> <color> [similar]"),
        ("Screen Width", "screenWidth"),
        ("Screen Height", "screenHeight"),
        ("Mouse Position", "mousePosition"),
        ("Mouse Position X", "mousePositionX"),
        ("Mouse Position Y", "mousePositionY"),
        ("Screen Shot", "screenShot [path]"),
        ("Screen Shot Monitor", "screenShotMonitor <monitor> [path]"),
    ],

    "Mouse": [
        ("Move To", "mouse move <x> <y> [speed]"),
        ("Move To Image", "mouse move <imagefile> [speed]"),
        ("Drag To", "mouse drag <x> <y> [speed]"),
        ("Drag To Image", "mouse drag <imagefile> [speed]"),
        ("Click", "mouse click"),
        ("Right Click", "mouse rightClick [x y | image] [interval]"),
        ("Double Click", "mouse doubleClick [x y | image] [interval]"),
        ("Triple Click", "mouse tripleClick [x y | image] [interval]"),
        ("Scroll", "mouse scroll <amount>"),
        ("Scroll Horizontal", "mouse scrollH <amount>"),
        ("Scroll Vertical", "mouse scrollV <amount>"),
    ],

    "Keyboard": [
        ("Type Text", "keyBoard type <speed> <text>"),
        ("Press Key", "keyBoard press <key>"),
        ("Hold Key", "keyBoard hold <key>"),
        ("Release Key", "keyBoard release <key>"),
    ],

    "Text Processing": [
        ("Text Lower", "textLower <text>"),
        ("Text Upper", "textUpper <text>"),
        ("To Base64", "toBase64 <text>"),
        ("Decode Base64", "decodeBase64 <base64>"),
        ("Text Starts With", "textStartWith <prefix> <text>"),
        ("Text Ends With", "textEndWith <suffix> <text>"),
        ("Text Contains", "textHas <substring> <text>"),
        ("Is Empty", "empty <{{var}}>"),
        ("Strip Characters", "strip <chars> <text>"),
        ("Replace Text", "replace <old> <new> <text>"),
        ("To Integer", "integer <text>"),
    ],

    "Variables & JSON": [
        ("Set Variable", "set <{{var}}> <value>"),
        ("Get Command Value", "get <{{var}}> <command>"),
        ("Get Value", "getValue <var>"),
        ("Create JSON", "json <name> <json>"),
        ("Get JSON", "json <name>"),
        ("Append JSON", "jsonAppend <path> <value>"),
        ("Save JSON", "jsonSave <name> <filename> [indent]"),
        ("Delete JSON", "jsonDelete <path>"),
        ("Length of JSON", "lenJson <path>"),
        ("Parse JSON", "jsonParse <json>"),
    ],

    "File & Folder": [
        ("File Exists", "fileman fileExist <path>"),
        ("Read File", "fileman readFile <path>"),
        ("Write File", "fileman writeFile <path> <content>"),
        ("Append File", "fileman appendFile <path> <content>"),
        ("Delete File/Folder", "fileman deleteFile <path>"),
        ("Copy File/Folder", "fileman copy <source> <destination>"),
        ("Move File/Folder", "fileman move <source> <destination>"),
        ("Is File", "fileman isFile <path>"),
        ("Is Folder", "fileman isFolder <path>"),
        ("List Folder", "fileman listContent <folder>"),
        ("Get File Type", "fileman getType <path>"),
        ("Get Size", "fileman getSize <path>"),
        ("New Folder", "fileman newFolder <folder>"),
        ("Absolute Path", "fileman absolutePath <path>"),
        ("Start File", "fileman startFile <path> [arguments]"),
    ],

    "Window": [
        ("List Windows", "windowList"),
        ("Focus Window", "focusWindow <title>"),
        ("Focused Window", "focusedWindow"),
        ("Minimize Window", "minimizeWindow <title>"),
        ("Maximize Window", "maximizeWindow <title>"),
        ("Close Window", "closeWindow <title>"),
        ("Reset Window", "resetWindow <title> <x> <y> <width> <height>"),
        ("In Window Title", "inWindowTitle <word>"),
        ("Get Window X", "getWindowX <title>"),
        ("Get Window Y", "getWindowY <title>"),
        ("Get Window Width", "getWindowWidth <title>"),
        ("Get Window Height", "getWindowHeight <title>"),
    ],

    "Clipboard": [
        ("Copy to Clipboard", "clipboardCopy <text>"),
        ("Paste from Clipboard", "clipboardPaste"),
    ],

    "Network / Fetcher": [
        ("Fetcher", "fetcher [options]"),
        ("Fetch Download", "fetcher -fetch-download -url <url> -saveto <path>"),
    ],

    "System & Security": [
        ("Get Environment", "getEnv <os|cpuUsage|ramFree|ramTotal|user|diskFree drive|diskTotal drive|hostname>"),
        ("Random", "random [len:<n>] [text]"),
        ("Timer Start", "timerStart"),
        ("Timer Stop", "timerStop"),
        ("Timer Value", "timer"),
        ("Set Security Password", "setSecurityPassword <password>"),
        ("Activate Security", "activateSecurity"),
        ("Deactivate Security", "deactivateSecurity"),
        ("Guest User", "guestUser <on|off>"),
        ("Login", "login <password>"),
        ("Logout", "logout"),
        ("Reset Environment", "resetEnvironment"),
    ],

    "Recorder": [
        ("Start Recorder", "startRecorder [filename.as]"),
        ("Stop Recorder", "stopRecorder"),
    ],

    "Custom Commands": [
        ("Define Commands", "define"),
        ("Define Command", "define <command>"),
        ("Define Name", "define:name <word>"),
        ("List All Names", "define:nameList"),
        ("Register Command", "registerCommand <name> <action>"),
        ("Remove Command", "removeCommand <name>"),
        ("Registered Commands", "registeredCommand"),
    ],

    "Other": [
        ("Emit Message", "emit <text> [color]"),
        ("Prompt", "prompt <message>"),
        ("Emit Prompt", "emit:prompt <message>"),
        ("Current Working Directory", "cwd"),
    ]
}


# ────────────────────────────────────────────────
# Custom Surtr Lexer
# ────────────────────────────────────────────────
class SurtrLexer(RegexLexer):
    name = 'Surtr'
    aliases = ['surtr', 'as']
    filenames = ['*.as']

    tokens = {
        'root': [
            # Labels
            (r'^[ \t]*([a-zA-Z_][a-zA-Z0-9_]*):[ \t]*$', bygroups(Name.Label)),
            (r'^[ \t]*(_[a-zA-Z_][a-zA-Z0-9_]*):[ \t]*$', bygroups(Name.Label.Hidden)),

            # ─── Multi-line raw text block ───────────────────────────────────
            # Opening ^^ → must be at the beginning of a line (with optional leading whitespace)
            # but can be immediately followed by text on the same line
            (r'^[ \t]*\^\^', String.Multiline, 'multiline_text'),

            # Command separator:   ++   (spaces required on both sides)
            (r'(?<=\s)\+\+(?=\s)', Operator.Separator),

            # Line continuation:   ^   at end of line
            (r'\^[ \t]*$', Operator.Continuation),

            # Block open:   <++   (spaces around)
            (r'(?<=\s)<\+\+(?=\s)', Operator.BlockStart),

            # Inner block separator:   +>   (spaces around or at end of line)
            (r'(?<=\s)\+>(?=\s|$)', Operator.BlockEnd),

            # <<< NEW: Full block closer   ++>   (spaces around or at end of line) >>>
            (r'(?<=\s)\+\+>(?=\s|$)', Operator.BlockEnd),          # ← this was missing

            # Comments
            (r'~~.*$', Comment.Single),

            # Super arguments
            (r'\?(\w+)(?::\w+)?', Name.Decorator),
            
            #Commands
            # Normal keywords (use word boundaries) for only words a-z
            (r'\b(keyBoard|mouse|clr|if|while|until|not|cwd|'
            r'seeImage|textLower|textUpper|toBase64|decodeBase64|textStartWith|'
            r'textEndWith|textHas|empty|strip|eachOnScreen|run|runCmd|'
            r'json|lenJson|jsonSave|jsonAppend|jsonParse|jsonDelete|quickRun|'
            r'end|stop|stopScript|exit|wait|random|define|def|'
            r'define:name|define:nameList|say|talk|voices|talking|stopTalking|'
            r'screenShot|screenShotMonitor|set|resetEnvironment|get|getValue|msg|'
            r'confirm|userInput|readImage|readImageLanguages|readScreen|imageReader|'
            r'moveToWord|dragToWord|rightClickWord|ClickWord|doubleClickWord|'
            r'tripleClickWord|moveToText|dragToText|textOnScreen|rightClickText|'
            r'ClickText|doubleClickText|tripleClickText|repeat|screenWidth|'
            r'screenHeight|mousePositionX|mousePositionY|mousePosition|fileman|'
            r'windowList|focusWindow|focusedWindow|minimizeWindow|maximizeWindow|'
            r'closeWindow|resetWindow|inWindowTitle|getWindowX|getWindowY|'
            r'getWindowWidth|getWindowHeight|clipboardCopy|clipboardPaste|surtrset|'
            r'watchFile|watchFolder|watchStatus|stopWatching|changeDetected|'
            r'filesWatched|restoreFile|timerStart|timerStop|timer|pixelColor|'
            r'waitPixelColor|getPixelColorRegion|colorExistsInRegion|'
            r'colorExistsInRegionSimilar|colorExistsInImage|'
            r'colorExistsInImageSimilar|toPixel|toHex|registerCommand|'
            r'removeCommand|registeredCommand|getEnv|setSecurityPassword|'
            r'activateSecurity|deactivateSecurity|guestUser|login|splitRun|'
            r'integer|replace|startRecorder|stopRecorder|fetcher|'
            r'emit|prompt|emit:prompt)\b',
            Keyword.Parent),

            # Keyword
            # Flags / options (no word boundaries needed for args starting with - )
            (r'(?:^|\s)(ctype:cmd|ctype:stmt|one|all|eng|move|drag|click|rightClick|'
            r'doubleClick|tripleClick|scroll|scrollH|scrollV|mouse|desktop|'
            r'region|useBlackWhite|useGray|true|false|null|label:|\?arg|'
            r'live:yes|len:|hex:yes|rgb|hex|voice-|bottomright|'
            r'bottomleft|topright|topleft|center|nostop|full|hide|on|off|'
            r'fileExist|readFile|writeFile|appendFile|deleteFile|startFile|'
            r'copy|move|isFile|isFolder|isDir|listContent|getType|getSize|'
            r'newFolder|newDir|absolutePath|-retries|-skip-error|-noerror|'
            r'-fetch|-fetch-json|-fetch-download|-fetch-download-json|'
            r'parser=json|parser=bs4|parser=text|parser=sbs4|select=|'
            r'-method|get|post|put|delete|-headers|-proxies|-timeout|'
            r'-backoff-factor|-rotate-user-agents|-save|-save-json|-saveto|'
            r'-getdata|-show-aggregated|-text-separator|-result-separator|'
            r'-max-worker|-request-delays|-request-schedule|-url|--version|'
            r'-split-download|-chunk-size|-show-progress|-image|-lang|'
            r'-min-conf|-char-width|-line-height|-psm|-transform|gray|bw|'
            r'-hide-output|emit:info|emit:error|emit:warn|emit:prompt)(?=\s|$)',
            Keyword),
            
            
            (r'\?run|\?else|\?arg|\?int|\?calc|\?var|\?exec|\?raw|\?str(-\w+)?', Operator),

            (r'\{\{[^}]+\}\}', Name.Variable),
            (r'"[^"]*"', String),
            (r"'[^']*'", String),
            (r'\b\d+(\.\d*)?|\.\d+\b', Number),

            (r'.', Text),
        ],

        'multiline_text': [
            # Closing ^^ → can be anywhere on the line, but must be at the end of text
            # (nothing non-whitespace after it)
            (r'\^\^[ \t]*$', String.Multiline, '#pop'),

            # All content inside the block
            (r'.', String.Multiline),
            (r'\n', String.Multiline),
        ]
    }   
    
# ────────────────────────────────────────────────
# ScriptBuilderFrame with Pygments highlighting
# ────────────────────────────────────────────────
class ScriptBuilderFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.script_commands = script_commands  # assuming this is defined globally

        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, sashwidth=5, bg="#222")
        paned.pack(fill="both", expand=True)

        # Left: Commands list
        left = ctk.CTkFrame(paned, width=260)
        paned.add(left)

        ctk.CTkLabel(left, text="Commands", font=("Arial", 18)).pack(pady=15)

        scroll = ctk.CTkScrollableFrame(left)
        scroll.pack(fill="both", expand=True, padx=8, pady=5)

        for cat, items in self.script_commands.items():
            ctk.CTkLabel(scroll, text=cat, font=("Arial", 14, "bold")).pack(anchor="w", pady=(12, 4))
            for name, syntax in items:
                btn = ctk.CTkButton(scroll, text=name, anchor="w",
                                    command=lambda s=syntax: self.insert_text(s))
                btn.pack(fill="x", pady=3)

        # Right: Editor + toolbar
        right = ctk.CTkFrame(paned)
        paned.add(right, stretch="always")

        toolbar = ctk.CTkFrame(right)
        toolbar.pack(fill="x", pady=8, padx=12)
        #save notifier
        self.saveicon = ctk.CTkLabel(toolbar, text="", width=10)
        self.saveicon.pack(side="left", padx=4)

        # Font settings button
        ctk.CTkButton(
            toolbar,
            text="Font",
            width=80,
            command=self.open_font_settings
        ).pack(side="left", padx=4)
        
        for txt, cmd in [("New", self.new_file), ("Open", self.open_file),
                         ("Save", self.save_file), ("Run", self.run_script)]:
            ctk.CTkButton(toolbar, text=txt, width=80, command=cmd).pack(side="left", padx=4)
        
        
        
        self.editor = ctk.CTkTextbox(right, font=("Consolas", 16), undo=True)
        self.editor.pack(fill="both", expand=True, padx=12, pady=(0,12))

        # ─── Pygments Setup ─────────────────────────────────────────────────
        self.lexer = SurtrLexer(stripall=True)

        # Color mapping (dracula-inspired dark theme friendly)
        self.tag_colors = {
            Keyword.Parent:    "#c708e0",    # bright blue       main commands if while etc.
            Keyword:           "#ff79c6",    # pink/magenta      secondary keywords  true false null
            Name.Decorator:    "#8be9fd",    # cyan               ?run ?else ?str
            Operator:          "#ffb86c",    # orange             ?calc ?exec
            String:            "#f1fa8c",    # yellow             "text"
            Comment.Single:    "#6272a4",    # muted blue-gray    ~~ comment
            Name.Variable:     "#bd93f9",    # purple             {{var}}
            Number:            "#bd93f9",    # purple             123  45.67
            # ─── label colors ────────────────────────────────────────────────
            Name.Label:        "#50fa7b",    # bright green       normal labels  mylabel:
            Name.Label.Hidden: "#ff5555",    # bright red         hidden labels  _hiddenlabel:
            
            Operator.Continuation:   "#bd93f9",     # ^
            Operator.Separator:      "#ffb86c",     #  ++ 
            Operator.BlockStart:     "#8be9fd",     # <++
            Operator.BlockEnd:       "#8be9fd",     # +>
            String.Multiline:        "#50fa7b",     # ^^ ... ^^
           
            Generic:           "#f8f8f2",    # light gray         fallback
            
        }

        # Configure all tags
        for tokentype, color in self.tag_colors.items():
            self.editor._textbox.tag_configure(str(tokentype), foreground=color)
           
        # Load last file if exists
        path = load_last_script_if_exists()
        if path:
            try:
                with open(path, encoding="utf-8") as f:
                    self.editor.insert("1.0", f.read())
                save_last_script(path)
                global PATH
                PATH = path
                self.saveicon.configure(text="")
            except Exception as e:
                messagebox.showerror("Error", str(e))

        self.firstload = 2 # skip first two modifications (initial load)

        # ─── Bindings ───────────────────────────────────────────────────────
        self.editor.bind("<<Modified>>", self.on_text_modified)
        self.editor.bind("<KeyRelease>", self.debounce_highlight)
        self.editor.bind("<<Paste>>", self.debounce_highlight)
        self.editor.bind("<Control-s>", self.on_ctrl_s)
        self.editor.bind("<Control-c>", self.on_ctrl_c)
        self.editor.bind("<Control-v>", self.on_ctrl_v)
        self.editor.bind("<Control-x>", self.on_ctrl_x)
        self.editor.bind("<Control-n>", lambda e: self.new_file())

        # Right-click context menu
        self.context_menu = Menu(self.editor, tearoff=0)
        self.context_menu.add_command(label="Undo", command=self.undo_action)
        self.context_menu.add_command(label="Redo", command=self.redo_action)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Cut",   command=self.cut_action)
        self.context_menu.add_command(label="Copy",  command=self.copy_action)
        self.context_menu.add_command(label="Paste", command=self.paste_action)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Select All", command=self.select_all_action)
        self.editor.bind("<Button-3>", self.show_context_menu)

        self.highlight()  # initial highlight
        self.saveicon.configure(text="")

        # Debounce control
        self._highlight_after_id = None

    # ─── Highlight with debounce (150 ms) ────────────────────────────────────
    def debounce_highlight(self, event=None):
        if self._highlight_after_id:
            self.after_cancel(self._highlight_after_id)
        self._highlight_after_id = self.after(150, self.highlight)

    def highlight(self):
        content = self.editor.get("1.0", "end-1c")
        if not content.strip():
            return

        # Clear previous tags
        for tag in list(self.tag_colors.keys()):
            self.editor._textbox.tag_remove(str(tag), "1.0", "end")

        # Get tokens from Pygments
        tokens = list(self.lexer.get_tokens_unprocessed(content))
        
        # === Debug: see which token types are actually used uncomment for debug ===
        #token_types = set()
        #for _, token, value in tokens:
        #  if value.strip():
        #    token_types.add(str(token))
        #print("Detected token types:", sorted(token_types))
        ####
        
        for index, token, value in tokens:
            if not value.strip():
                continue

            start = f"1.0 + {index} chars"
            end   = f"1.0 + {index + len(value)} chars"

            # Use the most specific token type
            tag = str(token)
            if token in self.tag_colors:
                self.editor._textbox.tag_add(tag, start, end)
            elif token.parent and token.parent in self.tag_colors:
                self.editor._textbox.tag_add(str(token.parent), start, end)


    # ─── Your original methods (unchanged) ──────────────────────────────────
    def on_text_modified(self, event=None):
        if self.firstload > 0:
            self.firstload -= 1
            self.editor.edit_modified(False)
            return
        self.editor.edit_modified(False)
        self.saveicon.configure(text="*")
        self.debounce_highlight()

    def show_context_menu(self, event):
        # Check states
        has_selection = bool(self.editor.tag_ranges("sel"))
        try:
           has_clipboard = bool(self.winfo_toplevel().clipboard_get())
        except tk.TclError:
           has_clipboard = False

        # Enable/disable menu items dynamically
        self.context_menu.entryconfig("Cut",   state="normal" if has_selection else "disabled")
        self.context_menu.entryconfig("Copy",  state="normal" if has_selection else "disabled")
        self.context_menu.entryconfig("Paste", state="normal" if has_clipboard else "disabled")
        self.context_menu.entryconfig("Undo",  state="normal" if self.editor.edit_modified() else "disabled")
        # Redo is hard to detect reliably → leave always enabled or track manually

        try:
           self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def undo_action(self):
      try:
        self.editor.edit_undo()
      except tk.TclError:
        pass

    def redo_action(self):
      try:
        self.editor.edit_redo()
      except tk.TclError:
        pass

    def cut_action(self):
      try:
        selected_text = self.editor.get("sel.first", "sel.last")
        self.winfo_toplevel().clipboard_clear()
        self.winfo_toplevel().clipboard_append(selected_text)
        self.editor.delete("sel.first", "sel.last")
      except tk.TclError:
        pass

    def copy_action(self):
      try:
        selected_text = self.editor.get("sel.first", "sel.last")
        self.winfo_toplevel().clipboard_clear()
        self.winfo_toplevel().clipboard_append(selected_text)
      except tk.TclError:
        pass

    def paste_action(self):
      try:
        text = self.winfo_toplevel().clipboard_get()
        self.editor.insert("insert", text)
      except tk.TclError:
        pass  # clipboard empty or not text

    def select_all_action(self):
      self.editor._textbox.tag_add("sel", "1.0", "end")

    def insert_text(self, text):
        self.editor.insert("insert", text + "\n")
        self.editor.focus()

    def new_file(self):
        global PATH
        if messagebox.askyesno("New", "Clear editor?"):
            self.editor.delete("1.0", "end")
            clear_last_script()
            PATH = None
            
    def open_file(self):
        global PATH
        path = filedialog.askopenfilename(filetypes=[("Scripts", "*.as *.txt"), ("All", "*.*")])
        if path:
            try:
                with open(path, encoding="utf-8") as f:
                    self.editor.delete("1.0", "end")
                    self.editor.insert("1.0", f.read())
                save_last_script(path)
                PATH = path
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def save_file(self):
        global PATH
        path = None
        if PATH:
           if os.path.isfile(PATH):
             try:
                with open(PATH, "w", encoding="utf-8") as f:
                    f.write(self.editor.get("1.0", "end").rstrip())
                save_last_script(PATH)
                self.saveicon.configure(text="")  # mark saved
                #messagebox.showinfo("Saved", "Script saved")
             except Exception as e:
                 messagebox.showerror("Error", str(e)) 
             return    
        else:
            path = filedialog.asksaveasfilename(defaultextension=".as", filetypes=[("Script", "*.as"), ("Text", "*.txt")])    
        if path:
            try:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(self.editor.get("1.0", "end").rstrip())
                save_last_script(path)
                PATH = path
                self.saveicon.configure(text="")  # mark saved
                #messagebox.showinfo("Saved", "Script saved")
            except Exception as e:
                messagebox.showerror("Error", str(e))
    
    def on_ctrl_s(self, event=None):
        self.save_file()
        return "break"  # prevent default behavior
    def on_ctrl_c(self, event=None):
        self.copy_action()
        return "break"  # prevent default behavior
    
    def on_ctrl_v(self, event=None):
        self.paste_action()
        return "break"  # prevent default behavior
    def on_ctrl_x(self, event=None):
        self.run_script()
 
    def run_script(self):
        global PATH
        content = self.editor.get("1.0", "end").strip()
        if not content:
            messagebox.showwarning("Empty", "Nothing to run")
            return
        self.controller.frames["terminal"].append_output(f"[Task] Running script:\n\n")
        runsurtrcommand(content, scriptmode=True, path=PATH)
        output = "\n".join(info)
        self.controller.frames["terminal"].append_output(f"[Task] Output:\n{output}\n\n")

    def open_font_settings(self):
        win = ctk.CTkToplevel(self)
        win.title("Editor Font Settings")
        win.geometry("380x220")
        win.resizable(False, False)
        win.transient(self)
        win.grab_set()

        ctk.CTkLabel(win, text="Font Size:", anchor="w").pack(pady=(20, 5), padx=20, fill="x")
        
        size_var = ctk.StringVar(value="16")
        size_entry = ctk.CTkEntry(win, textvariable=size_var, width=100)
        size_entry.pack(pady=5, padx=20)

        ctk.CTkLabel(win, text="Font Family:", anchor="w").pack(pady=(15, 5), padx=20, fill="x")
        
        families = ["Consolas", "Courier New", "JetBrains Mono", "Fira Code", "Cascadia Code", "Lucida Console", "DejaVu Sans Mono"]
        family_var = ctk.StringVar(value="Consolas")
        family_menu = ctk.CTkOptionMenu(
            win,
            values=families,
            variable=family_var,
            width=220
        )
        family_menu.pack(pady=5, padx=20)

        def apply_font():
            try:
                size = int(size_var.get())
                if size < 8 or size > 36:
                    raise ValueError
                family = family_var.get()
                self.editor.configure(font=(family, size))
                # Optional: save preference (you can add json/pickle later)
            except:
                messagebox.showerror("Invalid", "Size must be a number between 8–36")
            win.destroy()

        ctk.CTkButton(win, text="Apply", command=apply_font).pack(pady=6)
# ────────────────────────────────────────────────
# Tasks Frame
# ────────────────────────────────────────────────
class TasksFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        top = ctk.CTkFrame(self)
        top.pack(fill="x", padx=15, pady=12)

        ctk.CTkLabel(top, text="Surtr Bot Tasks", font=("Arial", 20)).pack(side="left", padx=10)
        ctk.CTkButton(top, text="New Task", command=self.new_task).pack(side="right", padx=5)

        columns = ("name", "command", "interval", "next_run")
        self.tree = tk.ttk.Treeview(self, columns=columns, show="headings")
        self.tree.heading("name", text="Task Name")
        self.tree.heading("command", text="Command / Script")
        self.tree.heading("interval", text="Interval")
        self.tree.heading("next_run", text="Next Scheduled")
        self.tree.column("name", width=180, anchor="w")
        self.tree.column("command", width=340, anchor="w")
        self.tree.column("interval", width=140, anchor="center")
        self.tree.column("next_run", width=180, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=15, pady=10)

        btns = ctk.CTkFrame(self)
        btns.pack(fill="x", padx=15, pady=8)

        ctk.CTkButton(btns, text="Refresh", command=self.refresh).pack(side="left", padx=5)
        ctk.CTkButton(btns, text="Delete Selected", fg_color="#c62828", command=self.delete_task).pack(side="left", padx=5)

        self.refresh()

    def refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        tasks = load_tasks()
        for name, task in sorted(tasks.items()):
            interval = f"Every {task['interval_value']} {task['interval_type']}"
            next_run = task.get("next_run", "—")
            self.tree.insert("", "end", values=(name, task["command"], interval, next_run))

    def new_task(self):
        win = ctk.CTkToplevel(self)
        win.title("New Task")
        win.geometry("520x480")
        win.grab_set()

        ctk.CTkLabel(win, text="Task Name (unique)").pack(pady=(20,4))
        name_entry = ctk.CTkEntry(win, width=460)
        name_entry.pack(pady=6)

        ctk.CTkLabel(win, text="Command / Script").pack(pady=(16,4))
        cmd_entry = ctk.CTkEntry(win, width=460)
        cmd_entry.pack(pady=6)

        ctk.CTkLabel(win, text="Repeat every").pack(pady=(20,4))

        interval_frame = ctk.CTkFrame(win)
        interval_frame.pack(pady=8)

        val_entry = ctk.CTkEntry(interval_frame, width=80)
        val_entry.insert(0, "30")
        val_entry.pack(side="left", padx=8)

        unit_var = ctk.StringVar(value="seconds")
        ctk.CTkOptionMenu(interval_frame, values=["seconds", "minutes", "hours", "days"], variable=unit_var).pack(side="left", padx=8)

        def save():
            name = name_entry.get().strip()
            cmd = cmd_entry.get().strip()
            try:
                val = int(val_entry.get().strip())
                if val <= 0: raise ValueError
            except:
                messagebox.showerror("Invalid", "Interval must be positive integer")
                return

            if not name or not cmd:
                messagebox.showerror("Missing", "Name and command required")
                return

            tasks = load_tasks()
            if name in tasks:
                messagebox.showerror("Duplicate", "Task name already exists")
                return

            sec = val
            u = unit_var.get()
            if u == "minutes": sec *= 60
            elif u == "hours": sec *= 3600
            elif u == "days": sec *= 86400

            now = datetime.now()
            tasks[name] = {
                "command": cmd,
                "interval_type": u,
                "interval_value": val,
                "interval_seconds": sec,
                "last_run": None,
                "next_run": (now + timedelta(seconds=sec)).isoformat()
            }
            save_tasks(tasks)
            messagebox.showinfo("Success", f"Task '{name}' created")
            self.refresh()
            win.destroy()

        ctk.CTkButton(win, text="Create", command=save).pack(pady=30)

    def delete_task(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a task first")
            return

        name = self.tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Delete", f"Remove '{name}'?"):
            tasks = load_tasks()
            tasks.pop(name, None)
            save_tasks(tasks)
            self.refresh()

# ────────────────────────────────────────────────
if __name__ == "__main__":
    if len(sys.argv[1:]) > 0: #if it has arguments save as a new path
         file = sys.argv[1]
         if os.path.isfile(file) and os.path.exists(file):
             try:
                
                PATH = file
                save_last_script(PATH)
             except Exception as e:
                 messagebox.showerror("Error", str(e))
         else:
                messagebox.showerror("Error", f"File not found: {file}")
                sys.exit(1)
    app = SurtrApp()
    app.mainloop()