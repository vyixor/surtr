# surtr_updater.py
import os
import threading
import time
import tempfile
import math
import platform
import subprocess
from urllib.parse import urlsplit, unquote
import sys
import requests
import customtkinter as ctk
import json
import datetime as dt
import updater
import ctypes
# check for resources folder first (only for windows)
if(os.path.exists(os.path.normpath("resources")) and os.path.isdir(os.path.normpath("resources"))):
    resource_path = os.path.normpath("resources")  
elif (os.path.exists(os.path.normpath("C:\\Surtr\\surtr\\resources")) and os.path.isdir(os.path.normpath("C:\\Surtr\\surtr\\resources"))):
    resource_path = os.path.normpath("C:\\Surtr\\surtr\\resources")
else:
    sys.exit(1)
    
    
updatefile = os.path.join(resource_path,"updates","updatecheck.json")


# ---------- CONFIGURE THIS ----------
UPDATE_URL = "https://example.com/surtr_v5_55_installer.exe"
# Optional: filename to save as (if None, inferred from URL)
CURRENT_VERSION = None
LATEST_VERSION = None
SAVE_AS = None
# ------------------------------------

ctk.set_appearance_mode("System")  # "Dark", "Light", or "System"
ctk.set_default_color_theme("blue")


def human_size(num_bytes: int) -> str:
    if num_bytes is None:
        return "Unknown"
    step = 1024.0
    if num_bytes < step:
        return f"{num_bytes} B"
    for unit in ("KB", "MB", "GB", "TB"):
        num_bytes /= step
        if abs(num_bytes) < step:
            return f"{num_bytes:.2f} {unit}"
    return f"{num_bytes:.2f} PB"


class UpdaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Surtr Updater")
        self.geometry("540x260")
        self.resizable(False, False)

        # State variables (thread-shared)
        self.total_bytes = None
        self.downloaded_bytes = 0
        self.start_time = None
        self.is_downloading = False
        self.error = None
        self.finished_success = False
        self.saved_path = None

        # Header / message
        header = ctk.CTkLabel(self, text="Surtr Update", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(pady=(18, 6))

        message_text = (
            "A new update is available.\n\n"
            f"Current version: {CURRENT_VERSION}    Latest version: {LATEST_VERSION}\n\n"
            "Would you like to download and install the update now?"
        )
        msg = ctk.CTkLabel(self, text=message_text, justify="center", wraplength=480)
        msg.pack(padx=20)

        # Progress components
        self.progress = ctk.CTkProgressBar(self, width=480)
        self.progress.set(0)
        self.progress.pack(pady=(12, 4))

        self.status_label = ctk.CTkLabel(self, text="Idle", anchor="w")
        self.status_label.pack(fill="x", padx=20)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=14, fill="x", padx=20)

        self.update_btn = ctk.CTkButton(btn_frame, text="Update now", command=self.on_update_now)
        self.update_btn.pack(side="left", expand=True, padx=(0, 8))

        self.notnow_btn = ctk.CTkButton(btn_frame, text="Not now", command=self.on_not_now)
        self.notnow_btn.pack(side="right", expand=True, padx=(8, 0))

        # Make sure polling runs for UI updates
        self.after(200, self._poll)

    def on_not_now(self):
        self.destroy()

    def on_update_now(self):
        if self.is_downloading:
            return
        # disable buttons
        self.update_btn.configure(state="disabled")
        self.notnow_btn.configure(state="disabled")
        self.is_downloading = True
        self.start_time = time.time()
        self.status_label.configure(text="Starting download...")
        thread = threading.Thread(target=self._download_thread, daemon=True)
        thread.start()

    def _download_thread(self):
        url = UPDATE_URL
        try:
            # Determine filename
            filename = SAVE_AS
            if not filename:
                path = urlsplit(url).path
                filename = os.path.basename(unquote(path)) or "surtr_update"
            # Save to temp dir (or current dir) - change as needed
            tmpdir = tempfile.gettempdir()
            dest_path = os.path.join(tmpdir, filename)
            # if exists, overwrite
            # Start request
            with requests.get(url, stream=True, timeout=15) as r:
                r.raise_for_status()
                total = r.headers.get("content-length")
                self.total_bytes = int(total) if total is not None else None
                self.downloaded_bytes = 0
                chunk_size = 8192
                # Write
                with open(dest_path, "wb") as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if not chunk:
                            continue
                        f.write(chunk)
                        self.downloaded_bytes += len(chunk)
                # finished
            self.saved_path = dest_path
            self.finished_success = True
            self.error = None
        except Exception as e:
            self.error = str(e)
            self.finished_success = False
        finally:
            self.is_downloading = False

    def _poll(self):
        # update progress UI using current state
        if self.is_downloading:
            # show progress if we have total
            if self.total_bytes:
                fraction = min(1.0, self.downloaded_bytes / float(self.total_bytes))
                self.progress.set(fraction)
                percent = fraction * 100.0
            else:
                # indeterminate-looking: slowly move progress
                cur = getattr(self, "_ind_val", 0.0)
                cur = (cur + 0.02) % 1.0
                self._ind_val = cur
                self.progress.set(cur)
                percent = None

            elapsed = max(1e-3, time.time() - (self.start_time or time.time()))
            speed = self.downloaded_bytes / elapsed
            speed_text = f"{human_size(int(speed))}/s"
            if self.total_bytes:
                self.status_label.configure(
                    text=f"Downloading: {human_size(self.downloaded_bytes)} / {human_size(self.total_bytes)} "
                         f"({percent:.1f}%) — {speed_text}"
                )
            else:
                self.status_label.configure(
                    text=f"Downloading: {human_size(self.downloaded_bytes)} — {speed_text}"
                )
        else:
            # not downloading
            if self.finished_success and self.saved_path:
                self.progress.set(1.0)
                self.status_label.configure(text=f"Downloaded\nLaunching installer...")
                # Launch installer/program now, then close GUI
                try:
                    self._launch_file(self.saved_path)
                    # small delay to let launch happen
                    self.after(800, self.destroy)
                except Exception as e:
                    self.status_label.configure(text=f"Failed to launch installer: {e}")
                    self.update_btn.configure(state="normal")
                    self.notnow_btn.configure(state="normal")
                # prevent re-entering this branch
                self.finished_success = False
                self.saved_path = None
            elif self.error:
                # show error and re-enable Not now to allow closing
                self.status_label.configure(text=f"Download failed: {self.error}")
                self.update_btn.configure(state="normal")
                self.notnow_btn.configure(state="normal")
                # reset error so it doesn't re-set constantly
                self.error = None
            else:
                # idle state
                pass

        # continue polling
        self.after(200, self._poll)

    def _launch_file(self, path):
        """
        Launch the downloaded file with administrator privileges on Windows.
        Other OSes just open it normally.
        """


        if not os.path.exists(path):
            raise FileNotFoundError(path)

        system = platform.system()
        if system == "Windows":
            try:
                # Use ShellExecuteEx to request admin privileges
                SHELLEXECUTEINFO = ctypes.Structure
                class SHELLEXECUTEINFO(ctypes.Structure):
                    _fields_ = [
                        ("cbSize", ctypes.c_ulong),
                        ("fMask", ctypes.c_ulong),
                        ("hwnd", ctypes.c_void_p),
                        ("lpVerb", ctypes.c_wchar_p),
                        ("lpFile", ctypes.c_wchar_p),
                        ("lpParameters", ctypes.c_wchar_p),
                        ("lpDirectory", ctypes.c_wchar_p),
                        ("nShow", ctypes.c_int),
                        ("hInstApp", ctypes.c_void_p),
                        ("lpIDList", ctypes.c_void_p),
                        ("lpClass", ctypes.c_wchar_p),
                        ("hkeyClass", ctypes.c_void_p),
                        ("dwHotKey", ctypes.c_ulong),
                        ("hIcon", ctypes.c_void_p),
                        ("hProcess", ctypes.c_void_p)
                    ]
                ShellExecuteEx = ctypes.windll.shell32.ShellExecuteExW
                SEE_MASK_NOCLOSEPROCESS = 0x00000040
                SW_SHOW = 5

                sei = SHELLEXECUTEINFO()
                sei.cbSize = ctypes.sizeof(SHELLEXECUTEINFO)
                sei.fMask = SEE_MASK_NOCLOSEPROCESS
                sei.hwnd = None
                sei.lpVerb = "runas"  # request administrator privileges
                sei.lpFile = path
                sei.lpParameters = None
                sei.lpDirectory = None
                sei.nShow = SW_SHOW

                if not ShellExecuteEx(ctypes.byref(sei)):
                    raise RuntimeError("Elevation (Run as Administrator) failed or was canceled.")
                return
            except Exception as e:
              try:
                os.startfile(path)  # type: ignore
                return
              except Exception:
                # fallback to subprocess
                subprocess.Popen([path], shell=True)
                return

        elif system == "Darwin":  # macOS
            subprocess.Popen(["open", path])
        else:  # Linux/Unix
            try:
                subprocess.Popen(["xdg-open", path])
            except Exception:
                os.chmod(path, 0o755)
                subprocess.Popen([path])




    
def showupdate(updateurl,currentversion,latestversion):
    global UPDATE_URL,CURRENT_VERSION,LATEST_VERSION
    
    try:
      UPDATE_URL = updateurl
      CURRENT_VERSION = currentversion
      LATEST_VERSION = latestversion
    
      app = UpdaterApp()
      app.mainloop()
    
      return latestversion
    except Exception as e:
      return currentversion
  
  
  
#updates
try:
 with open(updatefile,"r") as f:
    upte = f.read()
    uptejson = json.loads(upte)
    d = dt.datetime.now()
    #update check update for today
    currentdate = d.strftime('%d %B %Y')
    if uptejson["last_check"] != currentdate:
        uptejson["last_check"] = currentdate  
        #latestupdate = {"version":"4.99","downloadfile":"https://www.7-zip.org/a/7z2408-x64.exe"} # for only test 
        #free
        #latestupdate = updater.check_update('free')
        #pro
        latestupdate = updater.check_update('pro')
        
        
        #print(f" update = {latestupdate}")
        if not isinstance(latestupdate,dict):
            os._exit(3)
        if "downloadfile" not in latestupdate or latestupdate["downloadfile"] == "":
            os._exit(3)
        if "version" not in latestupdate or latestupdate["version"] == "":
            os._exit(3)
                
       
        #check if latest version is greater than installed version
        latestv = float(latestupdate["version"])
        currentv = float(uptejson["version"])
    
        if latestv > currentv:
              updateurl = latestupdate["downloadfile"]
              currentversion = uptejson["version"]
              latestversion = latestupdate["version"]
              newversion = showupdate(updateurl,currentversion,latestversion)
              if newversion:
                uptejson["version"] = newversion
              #lets save
              savit = json.dumps(uptejson,indent=4)
              fw = open(updatefile,"w")
              fw.write(savit)
              #lets save
except Exception as e:
    #print(f"Error: {e}")
    os._exit(7)             