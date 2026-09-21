# surtr_task_runner.py
# Background scheduler for Surtr Bot Tasks
# Edit SHOW_SHELL below to control whether the Surtr shell window appears

import json
import os
import time
import sys
import subprocess
import logging
from datetime import datetime, timedelta
from tkinter import messagebox
import re

# check for resources folder first (only for windows)
if(os.path.exists(os.path.normpath("resources")) and os.path.isdir(os.path.normpath("resources"))):
    resource_path = os.path.normpath("resources")  
elif (os.path.exists(os.path.normpath("C:\\Surtr\\surtr\\resources")) and os.path.isdir(os.path.normpath("C:\\Surtr\\surtr\\resources"))):
    resource_path = os.path.normpath("C:\\Surtr\\surtr\\resources")
else:
    messagebox.showerror("Error","cannot find 'resources' folder\nif you have it put it in (C:\\Surtr\\surtr\\resources) and restart your computer")
    sys.exit(1)
    
configfile = os.path.join(resource_path,"surtrconfig.conf")
taskfile = os.path.join(resource_path, "updates", "tasksbot.json")
tasklogs = os.path.join(resource_path, "logs", "surtr_tasks.log")


def settings(index):
  try:
    if os.path.exists(configfile) and os.path.isfile(configfile):
      try:
        with open(configfile, "r") as f:
          for i in f:
            if index in i:
              ans = i.split("=")
              return " ".join(ans[1:]).strip()
        # If we get here, setting was not found
        messagebox.showerror("Error","Configuration setting '"+index+"' not found in surtrconfig.conf")
        os._exit(10000)
      except (IOError, OSError) as e:
        logger.error(f"Error reading config file: {e}")
        return ""
    else:
        messagebox.showerror("Error","cannot find 'surtrconfig.conf' file in resources folder")
        os._exit(10000)
  except Exception as e:
      logger.error(f"Unexpected error in settings: {e}")
      return ""

# ────────────────────────────────────────────────
# Configuration - Edit this line to show/hide shell
# ────────────────────────────────────────────────
SHOW_SHELL = False          # ← Change to True if you want the shell window visible



TASKS_FILE = taskfile
LOG_FILE   = tasklogs

# Read setting from config file
if settings("showShellWhenRunningTask") == "yes":
    SHOW_SHELL = True
elif settings("showShellWhenRunningTask") == "no":
    SHOW_SHELL = False


# ────────────────────────────────────────────────
# Logging (file only - no console spam)
# ────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8")]
)
logger = logging.getLogger("SurtrTaskRunner")

logger.info(f"Starting Surtr Task Runner (shell window visible = {SHOW_SHELL})")

if not os.path.exists(taskfile):
    logger.error("Cannot find 'tasksbot.json' file in updates folder")
    sys.exit(1)
# ────────────────────────────────────────────────
# Load / Save tasks
# ────────────────────────────────────────────────
def load_tasks():
    if os.path.exists(TASKS_FILE):
        try:
            with open(TASKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load tasks file: {e}")
            return {}
    return {}

def save_tasks(tasks):
    try:
        with open(TASKS_FILE, "w", encoding="utf-8") as f:
            json.dump(tasks, f, indent=2)
    except Exception as e:
        logger.error(f"Failed to save tasks file: {e}")


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

# ────────────────────────────────────────────────
# Execute one task
# ────────────────────────────────────────────────
def execute_task(name, command):
    shortentext = shorten(command) # used only to preview long commands in short format do not use this for anything else
    logger.info(f"Running task '{name}': {shortentext}")

    try:
        # Hide window unless SHOW_SHELL is True
        creationflags = subprocess.CREATE_NEW_CONSOLE # ← This line forces a NEW cmd window
        commandlist = text_to_list(command)
        if not SHOW_SHELL:
            creationflags = subprocess.CREATE_NO_WINDOW
        
        cwd = os.path.dirname(os.path.abspath(__file__))
        
        if SHOW_SHELL:
            # Show output directly in shell window - don't capture it
            process = subprocess.Popen(
                ["surtr.exe"] + commandlist,
                cwd=cwd,
                creationflags=creationflags  
            )
            try:
                returncode = process.wait(timeout=300)
                logger.info(f"Task '{name}' completed (exit code {returncode})")
            except subprocess.TimeoutExpired:
                process.kill()
                logger.error(f"Task '{name}' timed out after 300 seconds")
                return
        else:
            # Capture output silently
            result = subprocess.run(
                ["surtr.exe"] + commandlist,
                capture_output=True,
                text=True,
                creationflags=creationflags,
                cwd=cwd,
                timeout=300  # 5-minute safety timeout
            )
            returncode = result.returncode
            stdout_data = result.stdout
           
            if returncode == 0:
                logger.info(f"Task '{name}' completed successfully")
                if stdout_data:
                    logger.debug(f"stdout: {stdout_data.strip()}")
                else:
                    logger.debug("No output from task")
            else:
                logger.error(f"Task '{name}' failed (exit code {returncode})")
                if stdout_data:
                    logger.error(f"stdout: {stdout_data.strip()}")
                else:
                    logger.error("No output from task")
                
    except subprocess.TimeoutExpired:
        logger.error(f"Task '{name}' timed out after 300 seconds")
    except FileNotFoundError:
        logger.error(f"surtr executable not found - cannot run task '{name}'")
    except Exception as e:
        logger.exception(f"Unexpected error in task '{name}': {e}")

# ────────────────────────────────────────────────
# Main loop
# ────────────────────────────────────────────────
def main():
    while True:
        now = datetime.now()
        tasks = load_tasks()

        updated = False
        for name, task in tasks.items():
            next_run_str = task.get("next_run")
            if not next_run_str:
                continue
            try:
                next_run = datetime.fromisoformat(next_run_str)
            except ValueError:
                logger.warning(f"Invalid next_run format for task '{name}' - skipping")
                continue

            if now >= next_run:
                cmd = task.get("command")
                if cmd:
                    execute_task(name, cmd)

                # Update scheduling with validation
                interval_sec = task.get("interval_seconds", 0)
                try:
                    interval_sec = float(interval_sec)
                    if interval_sec > 0:
                        task["last_run"] = now.isoformat()
                        task["next_run"] = (now + timedelta(seconds=interval_sec)).isoformat()
                        updated = True
                except (ValueError, TypeError):
                    logger.warning(f"Invalid interval_seconds for task '{name}': {interval_sec} - task will not reschedule")
                    continue

        if updated:
            save_tasks(tasks)

        time.sleep(1)  # Check every second

if __name__ == "__main__":
    main()