import time
import threading
from pynput import keyboard, mouse
from pynput.keyboard import Key, Listener as KeyboardListener
from pynput.mouse import Listener as MouseListener
from datetime import datetime 
import datetime as dt
import ctypes

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


last_event_time = time.time()
typed_chars = []
held_keys = set()
is_typing = False
typing_timer = None

last_mouse_click_time = 0
click_count = 0
drag_start = None
button_down = None

records = []

# Movement tracking
mouse_is_moving = False
move_start = None
last_mouse_pos = None
mouse_timer = None
MOVE_NOISE_THRESHOLD = 5  # pixels

def print_wait():
    global last_event_time
    now = time.time()
    delta = round(now - last_event_time, 3)
    if delta > 0:
        records.append(f"wait {delta}")
    last_event_time = now

allhotkeys = [
'enter','space','tab','esc',
'backspace','delete','up',
'down','left','right',
'shift','shiftleft','shiftright',
'ctrl','ctrlleft','ctrlright',
'alt','altleft','altright',
'win','winleft','winright',
 'pageup','pagedown',
'capslock','home','end',
'insert','printscreen',
 'volumeup','volumedown','volumemute'
]

def pyautogui_key(key):
    try:
        if isinstance(key, Key):
            mapping = {
                Key.enter: 'enter', Key.space: 'space', Key.tab: 'tab', Key.esc: 'esc',
                Key.backspace: 'backspace', Key.delete: 'delete', Key.up: 'up',
                Key.down: 'down', Key.left: 'left', Key.right: 'right',
                Key.shift: 'shift', Key.shift_l: 'shiftleft', Key.shift_r: 'shiftright',
                Key.ctrl: 'ctrl', Key.ctrl_l: 'ctrlleft', Key.ctrl_r: 'ctrlright',
                Key.alt: 'alt', Key.alt_l: 'altleft', Key.alt_r: 'altright',
                Key.cmd: 'win', Key.cmd_l: 'winleft', Key.cmd_r: 'winright',
                Key.page_up: 'pageup', Key.page_down: 'pagedown',
                Key.caps_lock: 'capslock', Key.home: 'home', Key.end: 'end',
                Key.insert: 'insert', Key.print_screen: 'printscreen',
                Key.media_volume_up: 'volumeup', Key.media_volume_down: 'volumedown',
                Key.media_volume_mute: 'volumemute'
            }
            return mapping.get(key, str(key).lower().replace("key.", ""))
        else:
            char = key.char
            if char and ord(char) < 32:  # Ignore non-printable control chars (e.g., ACK \x06, SOH \x01, DC1 \x11, ENQ \x05, NAK \x15, SI \x0F, DLE \x10, ESC \x1B, GS \x1D, DC3 \x13, EOT \x04, VT \x0B, FF \x0C, etc.)
                return None
            return char.lower()
    except:
        return None

def flush_typing():
    global typed_chars, is_typing, last_event_time
    if typed_chars:
        print_wait()  # Ensure wait before typing flush for accuracy
        records.append(f"keyBoard type {{{{kspeed}}}} {''.join(typed_chars)}")
        typed_chars.clear()
    is_typing = False
    
def start_typing_timer():
    global typing_timer
    if typing_timer and not typing_timer.finished.is_set():  # Safer check
        typing_timer.cancel()
    typing_timer = threading.Timer(1.0, flush_typing)
    typing_timer.start()

# ------------------ Keyboard ------------------

def on_press(key):
        global is_typing  # Added: Declare global for assignment below
        k = pyautogui_key(key)
        if not k:
            return
        # Only skip duplicates for special keys (len > 1), allow repeats for printables
        if len(k) > 1 and k in held_keys:
            return
        held_keys.add(k)

        if len(k) == 1 and k.isprintable():
            if not is_typing:
                print_wait()
            typed_chars.append(k)
            is_typing = True
            last_event_time = time.time()
            start_typing_timer()
        else:
            # Special key (including space, enter, arrows, modifiers, etc.)
            flush_typing()
            print_wait()
            #records.append(f"keyBoard press {k}")
            records.append(f"keyBoard hold {k}")
            # Note: Using "press" here for the down event. i can change it if i prefer "hold {k}" ,
            # simply replace "press" with "hold" in this line. The wait between "press" and "release" effectively
            # represents the hold duration.


def on_release(key):
        k = pyautogui_key(key)
        if not k or k not in held_keys:
            return
        held_keys.remove(k)
        if k not in allhotkeys:
            return  # No release for printable chars (handled via "type")

        if is_typing:
            flush_typing()  # Flush any pending type before release (ensures type happens while key is "held")

        print_wait()
        records.append(f"keyBoard release {k}")

# ------------------ Mouse ------------------

def on_click(x, y, button, pressed):
    global last_mouse_click_time, click_count, drag_start, button_down

    now = time.time()
    btn = str(button).split('.')[-1]

    if pressed:
        print_wait()
        button_down = btn
        drag_start = (x, y)
        if now - last_mouse_click_time < 0.4:
            click_count += 1
        else:
            click_count = 1
        last_mouse_click_time = now
    else:
        print_wait()  # Added: wait before release action (click/drag)
        if drag_start and (x, y) != drag_start:
            records.append(f"mouse  drag  {x} {y} {{{{speed}}}}")
        else:
            if btn == "left":
                if click_count == 1:
                    records.append(f"mouse click {x} {y}")
                elif click_count == 2:
                    records.append(f"mouse doubleClick {x} {y}")
                elif click_count >= 3:
                    records.append(f"mouse tripleClick {x} {y}")
            elif btn == "right":
                records.append(f"mouse rightClick {x} {y}")
        drag_start = None
        button_down = None

def flush_mouse_move():
    global move_start, last_mouse_pos, mouse_is_moving
    if move_start and last_mouse_pos:
        dx = abs(last_mouse_pos[0] - move_start[0])
        dy = abs(last_mouse_pos[1] - move_start[1])
        if dx >= MOVE_NOISE_THRESHOLD or dy >= MOVE_NOISE_THRESHOLD:
            print_wait()
            records.append(f"mouse move {last_mouse_pos[0]} {last_mouse_pos[1]} {{{{speed}}}}")
    move_start = None
    last_mouse_pos = None
    mouse_is_moving = False

def start_mouse_timer():
    global mouse_timer
    if mouse_timer and not mouse_timer.finished.is_set():
        mouse_timer.cancel()
    mouse_timer = threading.Timer(1.0, flush_mouse_move)
    mouse_timer.start()

def on_move(x, y):
    global move_start, last_mouse_pos, mouse_is_moving
    if not mouse_is_moving:
        move_start = (x, y)
        mouse_is_moving = True
    last_mouse_pos = (x, y)
    start_mouse_timer()

def on_scroll(x, y, dx, dy):
    print_wait()
    direction = "up" if dy > 0 else "down"
    amount = abs(dy)  # Use scroll amount, not y pos
    if direction == "up":
        records.append(f"mouse scroll {amount}")
    elif direction == "down":
        records.append(f"mouse scroll -{amount}")

# ------------------ Runner ------------------

ml = None
kl = None
filesave = None
isrecording = False
stoptime = None



def start_recording(file=None, stime=None):
    global ml, kl, filesave, isrecording, stoptime
    if file is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filesave = f"recorded_{timestamp}.as"
    else:
        filesave = file
    if ml or kl:
        raise Exception("Recording is active. Stop recording and try again.")
    
    if stime is not None:
            stoptime = float(stime)
            startstoptimer()
    print("Starting recorder please wait...")
    if stime is not None:
        print(f"Recorder will stop automatically after {stime} seconds.")
    ml = MouseListener(on_click=on_click, on_scroll=on_scroll, on_move=on_move)
    kl = KeyboardListener(on_press=on_press, on_release=on_release)
    ml.start()
    kl.start()
    isrecording = True
    print("Recorder started")


def stop_recording(silent=False):
    global ml, kl, filesave, last_event_time, typing_timer, is_typing,isrecording
    global last_mouse_click_time, click_count, drag_start, button_down
    global mouse_is_moving, move_start, last_mouse_pos, mouse_timer, MOVE_NOISE_THRESHOLD
    
    if isrecording == False:
        #raise Exception("Recorder is not currently active.")
        return
    
    # Flush pending events
    flush_typing()
    flush_mouse_move()
    
    # Cancel timers if running
    if typing_timer and not typing_timer.finished.is_set():
        typing_timer.cancel()
    if mouse_timer and not mouse_timer.finished.is_set():
        mouse_timer.cancel()
    
    if ml or kl:
        ml.stop()
        kl.stop()
        ml = None
        kl = None
        
        if filesave is not None:
            stime = show_time()
            d = dt.datetime.now()
            sdate = d.strftime("%d %B %Y")
            
            if silent == False:
                print(f"Saving to {filesave}")
                
            with open(filesave, "w") as opn:
                opn.write(f"~~ Recorded with Surtr recorder {sdate} {stime}\n")
                opn.write("set {{speed}} 2\n")
                opn.write("set {{kspeed}} 0.25\n")
                
                try:
                  #if the first wait time is too long cut it short
                  if records[0].startswith("wait"):
                      getnumber = records[0].split(" ")
                      if int(float(getnumber[1])) > 10:
                           opn.write("set {{startTime}} 5\n")
                           records.pop(0)
                           records.insert(0,"wait {{startTime}}")
                except:
                    pass
                
                for line in records:
                    opn.write(f"{line}\n")
                    
            if silent == False:
               print("saved")
    
    # Reset everything
    records.clear()
    held_keys.clear()
    typed_chars.clear()
    last_event_time = time.time()
    is_typing = False
    typing_timer = None
    isrecording = False
    
    last_mouse_click_time = 0
    click_count = 0
    drag_start = None
    button_down = None

    mouse_is_moving = False
    move_start = None
    last_mouse_pos = None
    mouse_timer = None
    stoptime = None
    MOVE_NOISE_THRESHOLD = 5  # pixels
    
    
def startstoptimer():
    global stoptime
    if stoptime is not None:
        threading.Timer(stoptime, stop_recording, kwargs={"silent": True}).start()