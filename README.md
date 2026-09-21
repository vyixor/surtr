# Surtr ⚔️🔥

**Reliable Windows Automation — Image & OCR Powered**

### Surtr — Reliable Windows Automation When Other Tools Fail

[![GitHub stars](https://img.shields.io/github/stars/vyixor/surtr?style=social)](https://github.com/vyixor/surtr/stargazers)
[![GitHub release](https://img.shields.io/github/v/release/vyixor/surtr)](https://github.com/vyixor/surtr/releases)
[![Downloads](https://img.shields.io/github/downloads/vyixor/surtr/total)](https://github.com/vyixor/surtr/releases)
[![License](https://img.shields.io/github/license/vyixor/surtr)](LICENSE)

> **Just keep building.**

Many automation tools rely on fixed coordinates or fragile selectors. Scripts break when windows move, applications update, or screen resolutions change.

**Surtr** is a free, open-source Windows automation tool built to keep working when simpler automation approaches fail.

Instead of relying only on fixed coordinates or brittle selectors, Surtr can **look at the screen like a human** using image detection and OCR to find and interact with buttons, text, icons, forms, and other visual elements.

![Surtr in action — clicking button by image even after resize](assets/surtr-image-click-demo.gif)

*Image-based automation can survive window movement, resizing, and different screen layouts.*

---

# Why Surtr?

* Works when coordinate-based macros fail
* Built-in macro recorder turns actions into reusable scripts
* Image-based automation and OCR
* Powerful downloader and scraping tools
* Advanced OCR for screenshots, receipts, invoices, and documents
* **SurtrUI** desktop IDE with visual script building
* **WebUI** for browser-based remote control
* Task Bot scheduler for unattended recurring jobs
* Built-in JSON processing
* Extensive scripting capabilities
* Runs locally with no cloud dependency
* No subscriptions
* No ads
* Open source

Surtr was built over months of experimentation, debugging, redesigning, and adding features. It is still evolving, but the core idea remains simple:

> **Build automation that doesn't fall apart the moment the screen changes.**

---

# Quick Start

## For normal users

Download the latest release:

**[Download the latest Surtr release](https://github.com/vyixor/surtr/releases/latest)**

Install Surtr and open Command Prompt:

```bat
surtr --version
```

Launch the desktop IDE:

```bat
surtrui
```

or launch `surtrui.exe` from the installation directory.

To launch WebUI:

```bat
webuilauncher
```

Then open:

```text
http://127.0.0.1:4444
```

> **Important:** If you use WebUI, change the default password immediately.

---

# Developer Setup — Run Surtr From Source

Want to explore the source code, modify Surtr, build your own commands, or contribute?

You're welcome here.

The source version of Surtr is intended for **Windows**.

## Recommended Python version

The recommended Python version for the current source tree is:

```text
Python 3.11.9
```

Using the recommended version helps avoid compatibility problems with some of Surtr's Windows-specific dependencies.

Check your Python version:

```bat
python --version
```

Expected:

```text
Python 3.11.9
```

## 1. Clone the repository

```bat
git clone https://github.com/vyixor/surtr.git
cd surtr
```

## 2. Create a virtual environment

Recommended:

```bat
python -m venv .venv
```

Activate it on Windows:

```bat
.venv\Scripts\activate
```

Your terminal should now show something similar to:

```text
(.venv)
```

## 3. Install dependencies

Install everything from the included requirements file:

```bat
python -m pip install -r requirements.txt
```

If `pip` is outdated:

```bat
python -m pip install --upgrade pip
```

Then install the requirements again:

```bat
python -m pip install -r requirements.txt
```

---

# OCR Setup — Tesseract

Surtr's OCR functionality uses **Tesseract OCR**.

You have two ways to make Tesseract available.

## Option 1 — Install Tesseract normally

Install Tesseract OCR on Windows using a suitable Tesseract distribution.

After installation, make sure `tesseract.exe` is available to Surtr.

Then test it from Command Prompt:

```bat
tesseract --version
```

If Windows recognizes the command, Surtr should normally be able to find it.

---

## Option 2 — Use Surtr's local OCR directory

If Tesseract is installed but Surtr cannot detect it automatically, you can place Tesseract directly inside Surtr's OCR resources directory.

Use:

```text
resources\OcR
```

The important file is:

```text
resources\OcR\tesseract.exe
```

Copy the required Tesseract files into that directory so that `tesseract.exe` is directly available there.

Your directory should look approximately like:

```text
surtr/
│
├── resources/
│   └── OcR/
│       ├── tesseract.exe
│       └── ...
│
├── autoscreen.py
├── requirements.txt
└── ...
```

This local fallback is useful when Surtr cannot detect a system-wide Tesseract installation.

### If OCR is not working

Check that this file exists:

```text
resources\OcR\tesseract.exe
```

Then try running Tesseract manually:

```bat
resources\OcR\tesseract.exe --version
```

If that works, Surtr should be able to use the local copy.

---

# Run Surtr From Source

Once Python, the dependencies, and Tesseract are ready:

```bat
python autoscreen.py
```

If everything is installed correctly, Surtr should start normally.

That's it.

You can then explore the source, modify commands, create your own automation logic, and experiment with the framework.

---

# Developer Quick Setup

For experienced developers, the entire setup is essentially:

```bat
git clone https://github.com/vyixor/surtr.git
cd surtr

python -m venv .venv
.venv\Scripts\activate

python -m pip install -r requirements.txt

python autoscreen.py
```

If OCR fails:

```text
Make sure resources\OcR\tesseract.exe exists.
```

---

# How Surtr Works

Surtr runs as a lightweight CLI automation engine, but its real strength comes from combining automation with visual understanding.

### Image Detection

Commands such as:

```text
seeImage
moveToWord
textOnScreen
```

can search the screen for images or text and return coordinates, status values, or matches.

### OCR Engine

Commands such as:

```text
imageReader
readScreen
```

can extract text from screenshots and other images.

### Surtr Scripting

Surtr provides its own scripting syntax with support for:

* Variables
* Conditions
* Loops
* Labels
* External scripts
* Multi-line blocks
* JSON operations
* Error handling
* Task automation

Example:

```text
if {{input}} ?cntn bad ?run stop
```

### SurtrUI

SurtrUI provides a native desktop interface with:

* Script Builder
* Syntax highlighting
* Command tools
* Terminal
* Task Bot
* Script management

### WebUI

The WebUI provides browser-based access to Surtr, including:

* Live desktop streaming
* File browser
* Terminal
* Script Builder
* Remote automation control

Everything is designed to run locally.

---

# Power Feature #1 — Fetcher

Fetcher is Surtr's built-in downloading and web-fetching system.

It supports:

* Parallel segmented downloads
* Retries
* Backoff
* Batch downloads
* HTML parsing
* JSON parsing
* Data extraction
* Local HTML parsing

## Single download

```bat
fetcher -fetch-download ^
-url https://example.com/linux.iso ^
-saveto linux.iso ^
-split-download 8 ^
-chunk-size 4096 ^
-retries 10 ^
-backoff-factor 1.5 ^
-show-progress
```

## Batch downloads

Create `downloads.json`:

```json
[
  {
    "url": "https://site.com/file1.zip",
    "save_as": "dl1.zip",
    "split_download": 6
  },
  {
    "url": "https://site.com/video.mp4",
    "save_as": "movie.mp4",
    "split_download": 12
  }
]
```

Run:

```bat
fetcher -fetch-download-json downloads.json -max-worker 10
```

This allows multiple downloads to run concurrently while each download can also use segmented transfers.

## Web scraping

Fetch → parse → extract:

```bat
fetcher -fetch "[{\"url\":\"https://news.com/article\",\"parser\":\"bs4\",\"select\":\"div\"}]"
```

### BS4 vs SBS4

**BS4**

Full BeautifulSoup parsing.

Useful for:

* Complex selectors
* Classes
* Nested structures
* Local HTML files
* Raw HTML content

Example:

```text
-select "div.article > p:first-child"
```

**SBS4**

Strict web parser.

Accepts:

```text
http://
https://
```

Example:

```text
-select "p"
```

## Scrape a local HTML file

```bat
fetcher -fetch "[{\"url\":\"C:\\path\\myfile.html\",\"parser\":\"bs4\",\"select\":\"div\"}]"
```

---

# Power Feature #2 — imageReader

Surtr includes an OCR system for extracting text from:

* Screenshots
* Receipts
* Invoices
* Documents
* Images
* Live desktop captures

## Basic OCR

```text
imageReader -image receipt.png -lang eng
```

## Improve difficult scans

```text
imageReader -image scan.jpg -transform bw -min-conf 65 -psm 6
```

## Preserve document layout

```text
imageReader -image invoice.png -char-width 9 -line-height 22 -save invoice.txt
```

## Silent OCR + save

```text
imageReader -image screenshot.png -hide-output -save result.txt
```

## OCR a live screen

```text
screenShot temp.png ++ imageReader -image temp.png -lang eng
```

---

# Power Feature #3 — SurtrUI

Launch:

```bat
surtrui
```

or open `surtrUi.exe`.

SurtrUI includes three major areas:

### Script Builder

Visually create and edit Surtr scripts with syntax highlighting and command helpers.

### Terminal

Run Surtr commands interactively and inspect output immediately.

### Surtr Task Bot

Schedule automation such as:

* Every few minutes
* Hourly
* Daily
* Weekly
* Custom recurring jobs

---

# Surtr In Action

<div align="center">
  <img src="assets/ide.png" width="48%" alt="SurtrUI Script Builder view">
  <img src="assets/taskbot.png" width="48%" alt="Surtr Task Bot view">
  <img src="assets/terminal.png" width="48%" alt="Surtr Terminal view">
</div>

---

# Power Feature #4 — WebUI

Launch:

```bat
webuilauncher
```

Then open:

```text
http://127.0.0.1:4444
```

<div align="center">
  <img src="assets/webuisettings0.png" width="48%" alt="Surtr WebUI Settings">
  <img src="assets/webuisettings1.png" width="48%" alt="Surtr WebUI Settings">
  <img src="assets/webuiclidashboard.png" width="48%" alt="Surtr WebUI CLI dashboard">
</div>

### What you get

**Live Desktop Stream**

Watch Surtr automate the desktop in real time.

**File Browser**

Browse and download files remotely.

**Terminal**

Execute commands through the browser.

**Script Builder**

Build and run Surtr scripts without leaving the browser.

<div align="center">
  <img src="assets/webuilogin.png" width="48%" alt="Surtr WebUI Login">
  <img src="assets/dashboard.png" width="48%" alt="Surtr WebUI Dashboard">
  <img src="assets/webscriptbuilder.png" width="48%" alt="Surtr WebUI Script Builder">
</div>

> **Security:** Change the default WebUI password immediately after setup.

---

# Surtr Macro Recorder

One of Surtr's most useful features is the built-in **Macro Recorder**.

It watches your mouse and keyboard actions and converts them into a Surtr `.as` script.

## Record a macro

Open SurtrUI or run:

```text
startRecorder mymacro.as
```

You can also specify a recording duration:

```text
startRecorder mymacro.as 60
```

Perform your normal actions:

* Click buttons
* Type text
* Move windows
* Scroll
* Navigate applications
* Perform repetitive workflows

Stop recording:

```text
stopRecorder
```

Surtr creates:

```text
mymacro.as
```

Run it with:

```bat
surtr run mymacro.as
```

![Replay recorded script](assets/macro-recorder-demo.gif)

## Tips for better recordings

* Keep actions deliberate
* Avoid unnecessarily fast clicks
* Save clean reference images when visual matching is required
* Open recorded scripts in SurtrUI and refine them
* Add conditions, loops, and variables
* Combine recordings with Task Bot
* Test your automation after changing window size or layout

Record once.

Improve the script.

Schedule it.

Let Surtr do the repetitive work.

---

# Security Notes

Surtr is a powerful automation tool because it can interact with your Windows environment.

That power should be used responsibly.

### WebUI

Change the default password via the WebUI configuration tools.

Use a strong password and configure the maximum number of users appropriately.

### Guest mode

Enable guest restrictions when appropriate:

```text
guestUser on
```

### Security password

```text
setSecurityPassword strongpass
activateSecurity
```

### Error handling

Use:

```text
set {{onerror}} mylabel:
```

to provide controlled failure handling.

### Validate inputs

Example:

```text
if {{input}} ?cntn bad ?run stop
```

### Best practices

* Test scripts before scheduling them
* Be careful when executing shell commands
* Avoid running untrusted scripts
* Review automation code before running it
* Keep Surtr updated
* Use strong WebUI credentials
* Restrict remote access when it is not needed

---

# Quick Examples

## Auto-click a save button

```text
while not seeImage save-btn.png ?run wait 2
mouse click
```

## Read a price from a screenshot

```text
screenShot price.png ++ imageReader -image price.png -lang eng -save price.txt
```

## Schedule a daily backup

Example Task Bot command:

```text
fileman copy C:\Data D:\Backup
```

Schedule:

```text
Every day at 23:00
```

---

# Surtr JSON

Surtr includes built-in JSON commands for creating, reading, modifying, appending, saving, deleting, and querying JSON data directly from automation scripts.

JSON is stored in memory during a session and remains available across runs only when saved to a file.

## JSON path syntax

Keys are wrapped in square brackets:

```text
[key]
```

Numeric array indexes remain plain:

```text
.0
.1
.2
```

Example:

```text
config.[theme]
config.[users].0.[name]
```

## JSON commands

| Command                           | Purpose            | Example                                   |
| --------------------------------- | ------------------ | ----------------------------------------- |
| `json <name> <json>`              | Create/update JSON | `json config {"theme":"dark"}`            |
| `json <name>`                     | Print entire JSON  | `json config`                             |
| `json <name>.[key]`               | Read a value       | `json config.[theme]`                     |
| `json <name>.[key] <value>`       | Set a value        | `json config.[theme] light`               |
| `jsonAppend <path> <value>`       | Append data        | `jsonAppend config.[favorites] "SurtrUI"` |
| `jsonSave <name> <file> [indent]` | Save JSON          | `jsonSave config settings.json 2`         |
| `jsonDelete <path>`               | Delete a value     | `jsonDelete config.[theme]`               |
| `lenJson <path>`                  | Get length         | `lenJson config.[favorites]`              |
| `jsonParse <json>`                | Parse JSON         | `jsonParse {"key":"value"}`               |

## Example

```text
json config '{"theme":"dark","favorites":["Task Bot"]}'

json config

json config.[theme] light

jsonAppend config.[favorites] "SurtrUI"

jsonDelete config.[theme]

jsonDelete config.[favorites].0

jsonSave config myconfig.json 2
```

## Fetch API data and parse JSON

```text
get {{data}} fetcher -fetch '[{"url":"https://myapisite.com","parser":"json"}]' -headers '{"User-Agent":"Mozilla/5.0","Accept":"application/json"}' -getdata

jsonParse {{data}}

json users {{data}}

json users.[0].[name]

lenJson users
```

---

# Surtr Configuration

Surtr can be customized through its configuration file.

Typical location:

```text
C:\Surtr\surtr\surtrconfig.conf
```

or the equivalent location in your installation directory.

The configuration file can be opened with any text editor.

## Example configuration

```ini
allowExternalScriptLabels=yes

autoBackupFileOnWatch=yes

trayIcon=yes

showSafeModeWarnings=yes

surtrPath=C:\\Surtr\\surtr

webuiSurtrWaitTimeout=120

useWebuiDefaultSurtrTheme=yes

useSurtrTheme=no

surtrUiOutput=shell

keepOutputShellOpen=no

showShellWhenRunningTask=yes
```

### Popular customizations

**Keep command windows open**

```ini
keepOutputShellOpen=yes
```

**Run Task Bot jobs silently**

```ini
showShellWhenRunningTask=no
```

**Use the built-in WebUI theme**

```ini
useWebuiDefaultSurtrTheme=yes
```

**Hide the system tray icon**

```ini
trayIcon=no
```

Restart Surtr after configuration changes.

Always keep a backup of your configuration file before making major changes.

---

# Troubleshooting

## Surtr does not start from source

Confirm that you are using the recommended Python version:

```bat
python --version
```

Recommended:

```text
Python 3.11.9
```

Then reinstall dependencies:

```bat
python -m pip install -r requirements.txt
```

## OCR is not working

Check:

```text
resources\OcR\tesseract.exe
```

or verify the system installation:

```bat
tesseract --version
```

If Windows cannot find `tesseract`, install it or place the Tesseract files in:

```text
resources\OcR
```

## A dependency is missing

Run:

```bat
python -m pip install -r requirements.txt
```

If you are using a virtual environment, make sure it is activated first.

## Surtr works from the installer but not from source

Make sure you have:

1. Python 3.11.9
2. All requirements installed
3. Tesseract configured
4. The project files in their expected locations
5. The virtual environment activated

Then run:

```bat
python autoscreen.py
```

---

# Project Philosophy

Surtr started with a simple problem:

**Automation should not break just because a window moved.**

From that idea, it grew into a much larger automation framework combining:

* Visual recognition
* OCR
* Automation scripting
* GUI tooling
* Remote browser control
* Task scheduling
* Downloading
* Web fetching
* JSON processing
* Macro recording

It is not meant to replace every automation framework.

It is meant to be another option — especially when traditional automation starts becoming fragile.

---

# Open Source

Surtr is **free and open source**.

The source code is available so developers can:

* Study how it works
* Modify it
* Build new features
* Create custom commands
* Improve existing systems
* Report bugs
* Submit fixes
* Experiment with the framework

The project is still evolving, and you may encounter bugs or unfinished areas. That's part of the journey.

If you find something broken, please open an issue with:

* What you were trying to do
* What you expected
* What actually happened
* Your Python version
* Your Windows version
* Relevant error output
* Steps to reproduce the problem

Good bug reports make Surtr better for everyone.

---

# Contributing

Pull requests, ideas, bug reports, and improvements are welcome.

Before submitting a large change, opening an issue to discuss the idea can save time for everyone.

When contributing:

* Keep changes focused
* Avoid unnecessary dependencies
* Preserve Windows compatibility
* Test automation features before submitting
* Document new commands and features
* Keep security in mind

---

# Download

### Latest Release

**[Download Surtr](https://github.com/vyixor/surtr/releases/latest)**

No ads.

No subscriptions.

No cloud dependency.

Just Windows automation.

---

# Documentation

Full documentation:

**[Surtr Documentation](http://screenbot.cu.ma/docs.php)**

You can also run:

```text
define
```

inside Surtr to explore available commands and functionality.

---

# Support the Project

Surtr is free and open-source.

Development takes time, testing, debugging, and a ridiculous amount of coffee. ☕🔥

If Surtr saves you time, helps automate something annoying, or simply makes your workflow better, consider supporting the project.

Every bit of support helps keep development moving.

---

<div align="center">

### Surtr ⚔️🔥

**Just keep building.**

Made with 🔥 by Victor James

[GitHub](https://github.com/vyixor/surtr) · [Issues](https://github.com/vyixor/surtr/issues) · [Releases](https://github.com/vyixor/surtr/releases)

⭐ **Star the repository if Surtr helps you.**

</div>
