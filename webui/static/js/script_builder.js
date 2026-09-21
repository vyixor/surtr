
if(sessionStorage.getItem("screenbot4environmentsessionrunning") !== null){
        document.body.innerHTML="<p> Your new session creation hasn't been completed click <a href='/yourenv'>here</a> to continue your session creation </p>"
}
     
// Command definitions
const commands = {
    
    screenShot: [
        { name: "Full Screen", syntax: "screenShot {filename}", fields: [{ label: "Filename", type: "text", id: "filename" }] },
        { name: "Region", syntax: "screenShot {left} {top} {width} {height} {filename}", 
          fields: [
              { label: "Left", type: "number", id: "left" },
              { label: "Top", type: "number", id: "top" },
              { label: "Width", type: "number", id: "width" },
              { label: "Height", type: "number", id: "height" },
              { label: "Filename", type: "text", id: "filename" }
          ] },
        { name: "Mouse Area", syntax: "screenShot mouse {width} {height} {filename}", 
          fields: [
              { label: "Width", type: "number", id: "width" },
              { label: "Height", type: "number", id: "height" },
              { label: "Filename", type: "text", id: "filename" }
          ] }
    ],

    //new
    screenShotMonitor: [
        { name: "Full Screen", syntax: "screenShotMonitor {monitorindex} {filename}", 
          fields: [
              { label: "Monitor Index", type: "number", id: "monitorindex" },
              { label: "Filename", type: "text", id: "filename" }
          ] },
        { name: "Region", syntax: "screenShotMonitor {monitorindex} {left} {top} {width} {height} {filename}", 
          fields: [
              { label: "Monitor Index", type: "number", id: "monitorindex" },
              { label: "Left", type: "number", id: "left" },
              { label: "Top", type: "number", id: "top" },
              { label: "Width", type: "number", id: "width" },
              { label: "Height", type: "number", id: "height" },
              { label: "Filename", type: "text", id: "filename" }
          ] },
        { name: "Mouse Area", syntax: "screenShotMonitor {monitorindex} mouse {width} {height} {filename}", 
          fields: [
              { label: "Monitor Index", type: "number", id: "monitorindex" },
              { label: "Width", type: "number", id: "width" },
              { label: "Height", type: "number", id: "height" },
              { label: "Filename", type: "text", id: "filename" }
          ] }
    ],
    
    //new
    comment: [
          { name: "Add a comment", 
         syntax: "~~{texts}", 
          fields: [
              { label: "type your text", type: "text",id: "texts"},
          ] 
        },
    ],
    //new
    mouse: [
        //move
         { name: "Simple Move", 
         syntax: "mouse move {x} {y} {speed}", 
          fields: [
              { label: "x", type: "number", id: "x" },
              { label: "y", type: "number", id: "y" },
              { label: "speed", type: "number", id: "speed" }
          ] 
        }, 

        { name: "move To Image", 
         syntax: "mouse move {filename} {speed}", 
          fields: [
              { label: "image file", type: "text", id: "filename" },
              { label: "speed", type: "number", id: "speed" }
          ] 
        },


        //drag
         { name: "Simple Drag", 
         syntax: "mouse drag {x} {y} {speed}", 
          fields: [
              { label: "x", type: "number", id: "x" },
              { label: "y", type: "number", id: "y" },
              { label: "speed", type: "number", id: "speed" }
          ] 
        },
        
        
        { name: "Drag To Image", 
         syntax: "mouse drag {filename} {speed}", 
          fields: [
              { label: "image file", type: "text", id: "filename" },
              { label: "speed", type: "number", id: "speed" }
          ] 
        },

        { name: "Drag From Image To Image", 
         syntax: "mouse drag {filename} {filename2} {speed}", 
          fields: [
              { label: "image file", type: "text", id: "filename" },
              { label: "image file2", type: "text", id: "filename2" },
              { label: "speed", type: "number", id: "speed" }
          ] 
        },

        //click
         { name: "Click", 
         syntax: "mouse click", 
          fields: [
              { label: "(optional leave blank)", type: "text"},
          ] 
        },
        
        { name: "Click Position", 
         syntax: "mouse click {x} {y}", 
          fields: [
              { label: "x", type: "number", id: "x" },
              { label: "y", type: "number", id: "y" },
          ] 
        },


        { name: "Click Image On Screen", 
         syntax: "mouse click {filename}", 
          fields: [
              { label: "image file", type: "text", id: "filename" },
          ] 
        },
        
        //double click

         { name: "Double Click", 
         syntax: "mouse doubleClick", 
          fields: [
              { label: "(optional leave blank)", type: "text"},
          ] 
        },


        { name: "Double Click Position", 
         syntax: "mouse doubleClick {x} {y} {interval}", 
          fields: [
              { label: "x", type: "number", id: "x" },
              { label: "y", type: "number", id: "y" },
              { label: "interval (optional)", type: "number", id: "interval" },
          ] 
        },

        { name: "Double Click Image On Screen", 
         syntax: "mouse doubleClick {filename}", 
          fields: [
              { label: "image file", type: "text", id: "filename" },
          ] 
        },


        //tripple click
         { name: "Triple Click", 
         syntax: "mouse tripleClick", 
          fields: [
              { label: "(optional leave blank)", type: "text"},
          ] 
        },

        
        { name: "Triple Click Position", 
         syntax: "mouse tripleClick {x} {y} {interval}", 
          fields: [
              { label: "x", type: "number", id: "x" },
              { label: "y", type: "number", id: "y" },
              { label: "interval (optional)", type: "number", id: "interval" },
          ] 
        },

        { name: "Triple Click Image On Screen", 
         syntax: "mouse tripleClick {filename}", 
          fields: [
              { label: "image file", type: "text", id: "filename" },
          ] 
        },
        
        //right click
         { name: "Right Click", 
         syntax: "mouse rightClick", 
          fields: [
              { label: "(optional leave blank)", type: "text"},
          ] 
        },

        { name: "Right Click Position", 
         syntax: "mouse rightClick {x} {y} {interval}", 
          fields: [
              { label: "x", type: "number", id: "x" },
              { label: "y", type: "number", id: "y" },
              { label: "interval (optional)", type: "number", id: "interval" },
          ] 
        },

        { name: "Right Click Image On Screen", 
         syntax: "mouse rightClick {filename}", 
          fields: [
              { label: "image file", type: "text", id: "filename" },
          ] 
        },

        //scroll
         { name: "Mouse Scroll", 
         syntax: "mouse scroll {units}", 
          fields: [
              { label: "number of units", type: "number",id:"units"},
          ] 
        },
        
         { name: "Mouse Scroll Horizontally", 
         syntax: "mouse scrollH {units}", 
          fields: [
              { label: "number of units", type: "number", id: "units"},
          ] 
        },
         { name: "Mouse Scroll Vertically", 
         syntax: "mouse scrollV {units}", 
          fields: [
              { label: "number of units", type: "number",id: "units"},
          ] 
        },
    ],
    
     //new
   keyboard: [
         { name: "Keyboard Type", 
         syntax: "keyBoard type {speed}", 
          fields: [
              { label: "Typing Speed", type: "number",id:"speed"},
          ] 
        },
        
         { name: "Keyboard Hold, Release, Press", 
         syntax: "keyBoard {option} {key}", 
          fields: [
              { label: "Options (hold,release,press)", type: "text", id: "option"},
              { label: "key", type: "text", id: "key"},
          ] 
        },
    ],


      //new
   if_else: [
         { name: "if", 
         syntax: "if {command} {logicals} {condition} ?run {exec}", 
          fields: [
              { label: "type your command", type: "text",id:"command"},
              { label: "use logical operators (?equ,?nequ,?cntn,?grtn,?lstn)", type: "text",id:"logicals"},
              { label: "condition to match", type: "text",id:"condition"},
              { label: "command to run if condition matches", type: "text",id:"exec"},
          ] 
        },
        
         { name: "if not", 
         syntax: "if not {command} {logicals} {condition} ?run {exec}", 
          fields: [
              { label: "type your command", type: "text",id:"command"},
              { label: "use logical operators (?equ,?nequ,?cntn,?grtn,?lstn)", type: "text",id:"logicals"},
              { label: "condition to match", type: "text",id:"condition"},
              { label: "command to run if condition matches", type: "text",id:"exec"},
          ] 
        },
       
        { name: "if ?else", 
         syntax: "if {command} {logicals} {condition} ?run {exec} ?else {exec2}", 
          fields: [
              { label: "type your command", type: "text",id:"command"},
              { label: "use logical operators (?equ,?nequ,?cntn,?grtn,?lstn)", type: "text",id:"logicals"},
              { label: "condition to match", type: "text",id:"condition"},
              { label: "command to run if condition match", type: "text",id:"exec"},
              { label: "command to run if condition did not match", type: "text",id:"exec2"},
          ] 
        },
       
        { name: "if not ?else", 
         syntax: "if not {command} {logicals} {condition} ?run {exec} ?else {exec2}", 
          fields: [
              { label: "type your command", type: "text",id:"command"},
              { label: "use logical operators (?equ,?nequ,?cntn,?grtn,?lstn)", type: "text",id:"logicals"},
              { label: "condition to match", type: "text",id:"condition"},
              { label: "command to run if condition match", type: "text",id:"exec"},
              { label: "command to run if condition did not match", type: "text",id:"exec2"},
          ] 
        },

    ],

   //new
   createlabel: [
         { name: "new label", 
         syntax: "{labelname}:", 
          fields: [
              { label: "type a new label name", type: "text",id:"labelname"},
          ] 
        },

        { name: "new transparent label", 
         syntax: "_{labelname}:", 
          fields: [
              { label: "type a new label name", type: "text",id:"labelname"},
          ] 
        },
    ],


   //new
   run: [
        { name: "run labelname", 
         syntax: "run {label}:", 
          fields: [
              { label: "label name", type: "text",id:"label"},
          ] 
        },
        
        { name: "run .as script", 
         syntax: "run {script}", 
          fields: [
              { label: "script path and name (use double slash for path seperator example path\\\\folder\\\\script.as", type: "text", id: "script"},
          ] 
        },

        { name: "run external script label", 
         syntax: "run {script} {label}:", 
          fields: [
              { label: "script path and name (use double slash for path seperator example path\\\\folder\\\\script.as", type: "text", id: "script"},
              { label: "label name", type: "text",id:"label"},
          ] 
        },
        
    ],
  
   //new
   seeimage: [
         { name: "see an image on screen", 
         syntax: "seeImage {imagepath}", 
          fields: [
              { label: "type the image path make sure it is saved in the computer", type: "text",id:"imagepath"},
          ] 
        },
    ],
 
  //new
   wait: [
         { name: "wait some seconds", 
         syntax: "wait {sec}", 
          fields: [
              { label: "seconds", type: "number",id:"sec"},
          ] 
        },
    ],

  //new
   speech: [
         { name: "voices", 
         syntax: "voices", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
         { name: "say", 
         syntax: "say voice-{index} {speed} {texts}", 
          fields: [
              { label: "voice index", type: "number",id:"index"},
              { label: "speed (use : to add volume)", type: "text",id:"speed"},
              { label: "what to say", type: "text",id:"texts"},
          ] 
        },
        { name: "talk (async)", 
         syntax: "talk voice-{index} {speed} {texts}", 
          fields: [
              { label: "voice index", type: "number",id:"index"},
              { label: "speed (use : to add volume)", type: "text",id:"speed"},
              { label: "what to say", type: "text",id:"texts"},
          ] 
        },
    ],

  //new
   addvariable: [
         { name: "set a variable", 
         syntax: "set  {{"+"{variablename}"+"}}  {value}", 
          fields: [
              { label: "variable name", type: "text",id:"variablename"},
              { label: "value", type: "text",id:"value"},
          ] 
        },
    ],

   //new
   msg: [
         { name: "display an alert", 
         syntax: "msg {texts}", 
          fields: [
              { label: "write something to show", type: "text",id:"texts"},
          ] 
        },
    ],

  //new
   confirm: [
         { name: "display an alert", 
         syntax: "msg {texts}", 
          fields: [
              { label: "write something to show", type: "text",id:"texts"},
          ] 
        },
    ],

    //new
   userinput: [
         { name: "prompt for input", 
         syntax: "userInput {texts}", 
          fields: [
              { label: "write something to show", type: "text",id:"texts"},
          ] 
        },
    ],

     //new
   readimage: [
         { name: "read an return texts in an image", 
         syntax: "readImage {imagepath} {option} {lang}", 
          fields: [
              { label: "imagepath", type: "text",id:"imagepath"},
              { label: "options (useBlackWhite,useGray)", type: "text",id:"option"},
              { label: "language", type: "text",id:"lang"},
          ] 
        },
    ],

    //new
   readscreen: [
         { name: "read an return texts on the screen", 
         syntax: "readScreen {lang}", 
          fields: [
              { label: "language", type: "text",id:"lang"},
          ] 
        },
    ],

   //new
   wordocr: [
         { name: "Move to word", 
         syntax: "moveToWord {option} {speed} {lang} {word}", 
          fields: [
              { label: "option (one,all)", type: "text",id:"option"},
              { label: "speed", type: "text",id:"speed"},
              { label: "language", type: "text",id:"lang"},
              { label: "word", type: "text",id:"word"},
          ] 
        },

        { name: "click word", 
         syntax: "clickWord {option} {lang} {word}", 
          fields: [
              { label: "option (one,all)", type: "text",id:"option"},
              { label: "language", type: "text",id:"lang"},
              { label: "word", type: "text",id:"word"},
          ] 
        },

        { name: "double click word", 
         syntax: "doubleClickWord {option} {lang} {word}", 
          fields: [
              { label: "option (one,all)", type: "text",id:"option"},
              { label: "language", type: "text",id:"lang"},
              { label: "word", type: "text",id:"word"},
          ] 
        },

        { name: "triple click word", 
         syntax: "tripleClickWord {option} {lang} {word}", 
          fields: [
              { label: "option (one,all)", type: "text",id:"option"},
              { label: "language", type: "text",id:"lang"},
              { label: "word", type: "text",id:"word"},
          ] 
        },


    ],

   //new
   textocr: [
         { name: "Move to text", 
         syntax: "moveToText {option} {speed} {lang} {texts}", 
          fields: [
              { label: "option (one,all)", type: "text",id:"option"},
              { label: "speed", type: "text",id:"speed"},
              { label: "language", type: "text",id:"lang"},
              { label: "texts", type: "text",id:"texts"},
          ] 
        },

        { name: "click text", 
         syntax: "clickText {option} {lang} {texts}", 
          fields: [
              { label: "option (one,all)", type: "text",id:"option"},
              { label: "language", type: "text",id:"lang"},
              { label: "texts", type: "text",id:"texts"},
          ] 
        },

        { name: "double click text", 
         syntax: "doubleClickText {option} {lang} {texts}", 
          fields: [
              { label: "option (one,all)", type: "text",id:"option"},
              { label: "language", type: "text",id:"lang"},
              { label: "texts", type: "text",id:"texts"},
          ] 
        },

        { name: "triple click text", 
         syntax: "tripleClickText {option} {lang} {texts}", 
          fields: [
              { label: "option (one,all)", type: "text",id:"option"},
              { label: "language", type: "text",id:"lang"},
              { label: "texts", type: "text",id:"texts"},
          ] 
        },


    ],

    //new
   runcmd: [
         { name: "run windows command", 
         syntax: "runCmd {command}", 
          fields: [
              { label: "type your command", type: "text",id:"command"},
          ] 
        },
        { name: "run windows command with live", 
         syntax: "runCmd live:yes {command}", 
          fields: [
              { label: "type your command", type: "text",id:"command"},
          ] 
        },
    ],

     //new
   repeat: [
         { name: "repeat command n times", 
         syntax: "repeat {n} {command}", 
          fields: [
              { label: "type the number of times to run", type: "number",id:"n"},
              { label: "type your command", type: "text",id:"command"},
          ] 
        },
    ],
   
      //new
   screensize: [
         { name: "screen width", 
         syntax: "screenWidth", 
          fields: [
              { label: "(leave blank)", type: "text",},
          ] 
        },
         { name: "screen height", 
         syntax: "screenHeigth", 
          fields: [
              { label: "(leave blank)", type: "text",},
          ] 
        },
    
    ],

       //new
   mouseposition: [
         { name: "mouse position", 
         syntax: "mousePosition", 
          fields: [
              { label: "(leave blank)", type: "text",},
          ] 
        },
         { name: "mouse x position", 
         syntax: "mousePositionX", 
          fields: [
              { label: "(leave blank)", type: "text",},
          ] 
        },
         { name: "mouse y position", 
         syntax: "mousePositionY", 
          fields: [
              { label: "(leave blank)", type: "text",},
          ] 
        },
    
    ],

      //new
   files: [
         { name: "file exists", 
         syntax: "fileman fileExist {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },
        { name: "read a file", 
         syntax: "fileman readFile {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "write to file", 
         syntax: "fileman writeFile {name} {content}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
              { label: "what you want to write", type: "text",id:"content"}
          ] 
        },
        { name: "append to file", 
         syntax: "fileman appendFile {name} {content}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
              { label: "what you want to write", type: "text",id:"content"}
          ] 
        },

        { name: "delete a file or folder", 
         syntax: "fileman deleteFile {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "delete a file or folder (no errors)", 
         syntax: "fileman deleteFile {name} -noerror", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "open file", 
         syntax: "fileman startFile {name} {arguments}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
              { label: "arguments (optional)", type: "text",id:"arguments"},
          ] 
        },

        { name: "is file", 
         syntax: "fileman isFile {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "is directory", 
         syntax: "fileman isDir {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "show content of a directory", 
         syntax: "fileman listContent {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "get file extension", 
         syntax: "fileman getType {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },


        { name: "get file size", 
         syntax: "fileman getSize {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "create directory", 
         syntax: "fileman newDir {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "show absolute path", 
         syntax: "fileman absolutePath {name}", 
          fields: [
              { label: "enter path", type: "text",id:"name"},
          ] 
        },

        { name: "file copy", 
         syntax: "fileman copy {from} {to}", 
          fields: [
              { label: "copy from", type: "text",id:"from"},
              { label: "copy to", type: "text",id:"to"},
          ] 
        },

        { name: "file move", 
         syntax: "fileman move {from} {to}", 
          fields: [
              { label: "move from", type: "text",id:"from"},
              { label: "move to", type: "text",id:"to"},
          ] 
        },


    ],

      //new
   window: [
         { name: "list all open windows", 
         syntax: "windowList", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
        { name: "focus a window", 
         syntax: "focusWindow {name}", 
          fields: [
              { label: "type the name of the window", type: "text",id:"name"},
          ] 
        },
        { name: "get focused window name", 
         syntax: "focusedWindow", 
          fields: [
              { label: "(leave blank)", type: "text",id:"name"},
          ] 
        },
         { name: "minimize a window", 
         syntax: "minimizeWindow {name}", 
          fields: [
              { label: "type the name of the window", type: "text",id:"name"},
          ] 
        },
         { name: "maximize a window", 
         syntax: "maximizeWindow {name}", 
          fields: [
              { label: "type the name of the window", type: "text",id:"name"},
          ] 
        },
         { name: "close a window", 
         syntax: "closeWindow {name}", 
          fields: [
              { label: "type the name of the window", type: "text",id:"name"},
          ] 
        },

         { name: "Resize and reposition a window", 
         syntax: "resetWindow {name} {x} {y} {width} {height}", 
          fields: [
              { label: "type the name of the window", type: "text",id:"name"},
              { label: "x", type: "number",id:"x"},
              { label: "y", type: "number",id:"y"},
              { label: "width", type: "number",id:"width"},
              { label: "height", type: "number",id:"height"},
          ] 
        },
        
         { name: "Find a window containing the word", 
         syntax: "inWindowTitle {word}", 
          fields: [
              { label: "type the word to find", type: "text",id:"word"},
          ] 
        },

         { name: "get window properties", 
         syntax: "getWindow{option} {name}", 
          fields: [
              { label: "option (X,Y,Width,Height) Note: options are case-sensitive", type: "text",id:"option"},
              { label: "window name", type: "text",id:"name"},
          ] 
        },

    ],

      //new
   clipboard: [
         { name: "copy to clipboard", 
         syntax: "clipboardCopy {texts}", 
          fields: [
              { label: "your text", type: "text",id:"texts"},
          ] 
        },
        { name: "paste clipboard content", 
         syntax: "clipboardPaste", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
    ],

   //new
   watchdog: [
         { name: "watch file", 
         syntax: "watchFile {name}", 
          fields: [
              { label: "filename", type: "text",id:"name"},
          ] 
        },
        { name: "watch folder", 
         syntax: "WatchFolder {name}", 
          fields: [
              { label: "foldername", type: "text",id:"name"},
          ] 
        },
        { name: "show changes on watched file/folder", 
         syntax: "WatchStatus {name}", 
          fields: [
              { label: "(optional) watched file name", type: "text",id:"name"},
          ] 
        },
        { name: "stop watching file/folder", 
         syntax: "stopWatching {name}", 
          fields: [
              { label: "watched file name", type: "text",id:"name"},
          ] 
        },
        { name: "number of changes detected", 
         syntax: "changeDetected {name}", 
          fields: [
              { label: "(optional) watched file name", type: "text",id:"name"},
          ] 
        },
        { name: "List monitored files/folders", 
         syntax: "filesWatched", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
        { name: "Restore a watched file to its initial state", 
         syntax: "restoreFile {name}", 
          fields: [
              { label: "watched file name", type: "text",id:"name"},
          ] 
        },
    ],

       //new
   timer: [
         { name: "start a timer", 
         syntax: "timerStart", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
        { name: "stop a timer", 
         syntax: "timerStop", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
        { name: "Get elapsed time (in seconds)", 
         syntax: "timer", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
       
    ],

      //new
   pixel: [
         { name: "get pixel color", 
         syntax: "pixelColor {x} {y} hex:{opt}", 
          fields: [
              { label: "x", type: "number",id:"x"},
              { label: "y", type: "number",id:"y"},
              { label: "use hex format (yes or no)", type: "text",id:"opt"},
          ] 
        },
        { name: "wait for pixel color", 
         syntax: "waitPixelColor {x} {y} {hex} {timeout}", 
          fields: [
              { label: "x", type: "number",id:"x"},
              { label: "y", type: "number",id:"y"},
              { label: "color to wait for in hex format", type: "text",id:"hex"},
              { label: "timeout (n)", type: "number",id:"timeout"},
          ] 
        },
        { name: "get pixel colors in a region", 
         syntax: "getPixelColorRegion {x} {y} {width} {height}", 
          fields: [
              { label: "x", type: "number",id:"x"},
              { label: "y", type: "number",id:"y"},
              { label: "width", type: "number",id:"width"},
              { label: "height", type: "number",id:"height"},
          ] 
        },
        { name: "colors exists in a region", 
         syntax: "colorExistsInRegion {x} {y} {width} {height} {hexes}", 
          fields: [
              { label: "x", type: "number",id:"x"},
              { label: "y", type: "number",id:"y"},
              { label: "width", type: "number",id:"width"},
              { label: "height", type: "number",id:"height"},
              { label: "your hex,use space to seperate multiple hex", type: "text",id:"hexes"},
          ] 
        },
        { name: "similar colors exists in a region ", 
         syntax: "colorExistsInRegionSimilar {x} {y} {width} {height} {tolerance} {hexes}", 
          fields: [
              { label: "x", type: "number",id:"x"},
              { label: "y", type: "number",id:"y"},
              { label: "width", type: "number",id:"width"},
              { label: "height", type: "number",id:"height"},
              { label: "tolerance (n)", type: "number",id:"tolerance"},
              { label: "your hex,use space to seperate multiple hex", type: "text",id:"hexes"},
          ] 
        },

        { name: "colors exists in an image", 
         syntax: "colorExistsInImage {image} {hexes}", 
          fields: [
              { label: "imagepath", type:"text",id:"image"},
              { label: "your hex,use space to seperate multiple hex", type: "text",id:"hexes"},
          ] 
        },
        { name: "similar colors exists in an image", 
         syntax: "colorExistsInImageSimilar {image} {tolerance} {hexes}", 
          fields: [
              { label: "imagepath", type:"text",id:"image"},
              { label: "tolerance (n)", type: "number",id:"tolerance"},
              { label: "your hex,use space to seperate multiple hex", type: "text",id:"hexes"},
          ] 
        },
        { name: "Get raw pixel data in RGB", 
         syntax: "toPixel {image}", 
          fields: [
              { label: "imagepath", type:"text",id:"image"},
          ] 
        },
        { name: "Get raw pixel data in hex", 
         syntax: "toHex {image}", 
          fields: [
              { label: "imagepath", type:"text",id:"image"},
          ] 
        },
        
    ],

      //new
   getenv: [
         { name: "Get OS name and version", 
         syntax: "getEnv os", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
         { name: "Get current username", 
         syntax: "getEnv user", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
         { name: "Get CPU usage percentage", 
         syntax: "getEnv cpuUsage", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
         { name: "Get available RAM", 
         syntax: "getEnv ramFree", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
         { name: "Get total RAM", 
         syntax: "getEnv ramTotal", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
         { name: "Get disk free space", 
         syntax: "getEnv diskFree {drive}", 
          fields: [
              { label: "type the drive letter example c:", type: "text",id:"drive"},
          ] 
        },
         { name: "Get disk total space", 
         syntax: "getEnv diskTotal {drive}", 
          fields: [
              { label: "type the drive letter example c:", type: "text",id:"drive"},
          ] 
        },
         { name: "Get system hostname", 
         syntax: "getEnv hostname", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
    ],

      //new
   commandregister: [
         { name: "register a new command", 
         syntax: "registerCommand {name} run {script}", 
          fields: [
              { label: "name of your new command", type: "text",id:"name"},
              { label: "external .as script", type: "text",id:"{script}"},
          ] 
        },

        { name: "show registered commands", 
         syntax: "registeredCommand", 
          fields: [
               { label: "leave blank", type: "text"},
          ] 
        },

        { name: "remove a registered command", 
         syntax: "removeCommand {name}", 
          fields: [
               { label: "name of the registered command", type: "text",id:"name"},
          ] 
        },
    ],

    //new
   get: [
         { name: "Run a command and store its result", 
         syntax: "get {{"+"{variablename}"+"}}  {command}", 
          fields: [
              { label: "variable name", type: "text",id:"variablename"},
              { label: "command to run", type: "text",id:"command"},
          ] 
        },
    ],

    //new
    textlower: [
         { name: "Convert text to lower case", 
         syntax: "textLower {texts}", 
          fields: [
              { label: "Enter text", type: "text",id:"texts"},
          ] 
        },
    ],

    //new
    textupper: [
         { name: "Convert text to upper case", 
         syntax: "textUpper {texts}", 
          fields: [
              { label: "Enter text", type: "text",id:"texts"},
          ] 
        },
    ],


    //new
    textstartwith: [
         { name: "text starts with a specific text", 
         syntax: "textStartWith {start} {texts}", 
          fields: [
              { label: "Starts with", type: "text",id:"start"},
              { label: "Enter text", type: "text",id:"texts"},
          ] 
        },
    ],

    //new
    textendwith: [
         { name: "text ends with a specific text", 
         syntax: "textEndWith {end} {texts}", 
          fields: [
              { label: "Ends with", type: "text",id:"end"},
              { label: "Enter text", type: "text",id:"texts"},
          ] 
        },
    ],


    //new
    texthas: [
         { name: "text has a specific text", 
         syntax: "textHas {hs} {texts}", 
          fields: [
              { label: "Has", type: "text",id:"hs"},
              { label: "Enter text", type: "text",id:"texts"},
          ] 
        },
    ],

    //new
    tobase: [
         { name: "convert to base64", 
         syntax: "toBase64 {texts}", 
          fields: [
              { label: "Enter text", type: "text",id:"texts"},
          ] 
        },
    ],


     //new
    empty: [
         { name: "Check if a variable is empty", 
         syntax: "empty {texts}", 
          fields: [
              { label: "Enter empty text or variable name", type: "text",id:"texts"},
          ] 
        },
    ],


     //new
    decodebase: [
         { name: "decode base64", 
         syntax: "decodeBase64 {bstext}", 
          fields: [
              { label: "Enter text", type: "text",id:"bstext"},
          ] 
        },
    ],

    //new
   resetenvironment: [
         { name: "Reset environment for a clean start", 
         syntax: "resetEnvironment", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
    ],
    
    //new
    getvalue: [
          { name: "hold the value of a variable for use with if", 
         syntax: "getValue {variablename}", 
          fields: [
              { label: "variable name", type: "text",id:"variablename"},
          ] 
        },
    ],

    //new
    stopscript: [
          { name: "stop a running script", 
         syntax: "stop", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
          { name: "stop a running script", 
         syntax: "stopScript", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
    ],

    //new
    security: [
          { name: "change screenbot4 password", 
         syntax: "setSecurityPassword {password}", 
          fields: [
              { label: "variable name", type: "text",id:"password"},
          ] 
        },
        { name: "activate security mode", 
         syntax: "activateSecurity", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
        { name: "disactivate security mode", 
         syntax: "disactivateSecurity", 
          fields: [
              { label: "(leave blank)", type: "text"},
          ] 
        },
        { name: "guest user", 
         syntax: "guestUser {opt}", 
          fields: [
              { label: "options(on/off)", type: "text",id:"opt"},
          ] 
        },


    ],

       //new
   textonscreen: [
         { name: "iterate on texts", 
         syntax: "textOnScreen {lang} {texts} {command}", 
          fields: [
              { label: "language", type: "text",id:"lang"},
              { label: "text to find", type: "text",id:"texts"},
              { label: "command to run", type: "text",id:"command"},
          ] 
        },
    ],

    //new
    emit: [
          { name: "print text", 
         syntax: "emit {texts}", 
          fields: [
              { label: "enter text", type: "text",id:"texts"},
          ] 
        },
    ],

    //new
    JSON: [
          { name: "create json", 
         syntax: "json {name} {value}", 
          fields: [
              { label: "json name", type: "text",id:"name"},
              { label: "json syntax", type: "text",id:"value"},
          ] 
        },

        { name: "get json", 
         syntax: "json {name}", 
          fields: [
              { label: "existing json name", type: "text",id:"name"},
          ] 
        },

        { name: "parse to json format", 
         syntax: "parseJson {texts}", 
          fields: [
              { label: "json syntax", type: "text",id:"texts"},
          ] 
        },
       
        { name: "delete json", 
         syntax: "jsonDelete {key}", 
          fields: [
              { label: "json key or name", type: "text",id:"key"},
          ] 
        },

        { name: "save json", 
         syntax: "jsonSave {name} {file} {indent}", 
          fields: [
              { label: "json name", type: "text",id:"name"},
              { label: "save to", type: "text",id:"file"},
              { label: "indent(optional)", type: "number",id:"indent"},
          ] 
        },

        { name: "get json length", 
         syntax: "lenJson {name}", 
          fields: [
              { label: "json name or key", type: "text",id:"name"},
          ] 
        },


    ],
    
    //new
    recorder: [
          { name: "start recording", 
         syntax: "startRecorder {file}", 
          fields: [
              { label: "save to (optional)", type: "text",id:"file"},
          ] 
        },

        { name: "stop recording", 
         syntax: "stopRecorder", 
          fields: [
              { label: "leave blank(optional)", type: "text"},
          ] 
        },
    ],

    //new
    replace: [
          { name: "replace text with specific text", 
         syntax: "replace {text1} {text2} {fulltext}", 
          fields: [
              { label: "replace this", type: "text",id:"text1"},
              { label: "replace with", type: "text",id:"text2"},
              { label: "text", type: "text",id:"fulltext"},
          ] 
        },
    ],

    //new
    random: [
        { name: "generate random text", 
         syntax: "random", 
          fields: [
              { label: "leave blank (optional)", type: "text"},
          ] 
        },

        { name: "generate random with specific length", 
         syntax: "random len:{lent}", 
          fields: [
              { label: "random length", type: "number",id:"{lent}"},
          ] 
        },

        { name: "generate random form text with specific length", 
         syntax: "random len:{lent} {texts}", 
          fields: [
              { label: "random length", type: "number",id:"{lent}"},
              { label: "text", type: "text",id:"{texts}"},
          ] 

        },

        { name: "generate random form texts with specific length", 
         syntax: "random len:{lent} {texts}", 
          fields: [
              { label: "random length", type: "number",id:"{lent}"},
              { label: "text", type: "text",id:"{texts}"},
          ] 

        },

        { name: "generate random form texts", 
         syntax: "random {texts}", 
          fields: [
              { label: "text", type: "text",id:"{texts}"},
          ] 

        },

    ],

    //new
   splitrun: [
         { name: "split by word", 
         syntax: "splitRun '{texts}' ?run {command}", 
          fields: [
              { label: "text to split", type: "text",id:"texts"},
              { label: "command to run on each text,type {{item}} on the position you want each splitted text to appear on your command", type: "text",id:"command"},
          ] 
        },
        { name: "split using a custom token", 
         syntax: "splitRun ?token '{token}' {texts} ?run {command}", 
          fields: [
              { label: "your custom token", type: "text",id:"token"},
              { label: "text to split", type: "text",id:"texts"},
              { label: "command to run on each text,type {{item}} on the position you want each splitted text to appear on your command", type: "text",id:"command"},
          ] 
        },
        { name: "split by each line in a file", 
         syntax: "splitRun {filename} ?run {command}", 
          fields: [
              { label: "file to split", type: "text",id:"filename"},
              { label: "command to run on each text,type {{item}} on the position you want each splitted text to appear on your command", type: "text",id:"command"},
          ] 
        },
    ],
    
    //new
    integer: [
          { name: "change command results to integers", 
         syntax: "integer {command}", 
          fields: [
              { label: "command,make sure command returns numbers", type: "text",id:"command"},
          ] 
        },
    ],

    //new
    exit: [
          { name: "exit label", 
         syntax: "exit {texts}", 
          fields: [
              { label: "exit text (optional)", type: "text",id:"texts"},
          ] 
        },
    ],







//command ends here
};

// Current command being edited
let currentCommand = null;
let selectedOption = null;

// Initialize modal and buttons
document.addEventListener("DOMContentLoaded", () => {
    const modal = document.getElementById("commandModal");
    const closeBtn = document.getElementsByClassName("close")[0];
    const commandButtons = document.getElementsByClassName("command-btn");

    // Open modal when command button is clicked
    Array.from(commandButtons).forEach(btn => {
        btn.addEventListener("click", () => {
            const command = btn.getAttribute("data-command");
            currentCommand = command;
            openModal(command);
        });
    });

    // Close modal
    closeBtn.addEventListener("click", () => {
        modal.style.display = "none";
    });

    // Close modal when clicking outside
    window.addEventListener("click", (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });
});

// Open modal and populate options
function openModal(command) {
    const modal = document.getElementById("commandModal");
    const modalTitle = document.getElementById("modalTitle");
    const modalOptions = document.getElementById("modalOptions");

    modalTitle.textContent = `Select ${command} Options`;
    modalOptions.innerHTML = "";

    // Create dropdown for command variants
    const select = document.createElement("select");
    select.id = "commandVariant";
    commands[command].forEach((option, index) => {
        const opt = document.createElement("option");
        opt.value = index;
        opt.textContent = option.name;
        select.appendChild(opt);
    });

    const optionGroup = document.createElement("div");
    optionGroup.className = "option-group";
    optionGroup.innerHTML = `<label>Command Variant</label>`;
    optionGroup.appendChild(select);
    modalOptions.appendChild(optionGroup);

    // Populate fields when variant is selected
    select.addEventListener("change", () => {
        selectedOption = commands[command][select.value];
        populateFields(modalOptions, selectedOption);
    });

    // Initialize with first option
    selectedOption = commands[command][0];
    populateFields(modalOptions, selectedOption);

    modal.style.display = "flex";
}

// Populate input fields for selected command variant
function populateFields(container, option) {
    // Remove existing fields (except variant dropdown)
    while (container.children.length > 1) {
        container.removeChild(container.lastChild);
    }

    // Create input fields
    option.fields.forEach(field => {
        const group = document.createElement("div");
        group.className = "option-group";
        group.innerHTML = `<label>${field.label}</label>`;
        const input = document.createElement("input");
        input.type = field.type;
        input.id = field.id;
        input.required = true;
        group.appendChild(input);
        container.appendChild(group);
    });
}

// Insert command into textarea
function insertCommand() {
    if (!selectedOption) return;

    const values = {};
    selectedOption.fields.forEach(field => {
        const input = document.getElementById(field.id);
        values[field.id] = input.value;
    });

    let commandText = selectedOption.syntax;
    for (const key in values) {
        //for space in parameters
        if (values[key].includes(" ")){
           values[key] =  `"${values[key]}"`
        }
        commandText = commandText.replace(`{${key}}`, values[key]);

         

    }

    const textarea = document.getElementById("scriptArea");
    textarea.value += (textarea.value ? "\n" : "") + commandText;
    document.getElementById("commandModal").style.display = "none";
}

// Save script to computer
function saveScript() {
    const textarea = document.getElementById("scriptArea");
    const content = textarea.value;
    var scriptname = ""
    if (!content) {
        alert("Script is empty!");
        return;
    }
    if (sessionStorage.getItem("screenbot4scriptname") === null){
      scriptname = prompt("New file name");
      sessionStorage.setItem("screenbot4scriptname",scriptname);
      const blob = new Blob([content], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = scriptname;
      a.click();
      URL.revokeObjectURL(url);
    }else{
      scriptname = sessionStorage.getItem("screenbot4scriptname");
      const blob = new Blob([content], { type: "text/plain" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = scriptname;
      a.click();
    URL.revokeObjectURL(url);
    }
}






async function runScript() {
    const textarea = document.getElementById("scriptArea");
    const shell = document.getElementById("shellarea");
    const output = document.getElementById("responds");
    const closeBtn2 = document.getElementsByClassName("close")[1];
    const content = textarea.value;
    if (!content) {
        alert("Script is empty!");
        return;
    }

    try {
        sessionStorage.setItem("screenbot4lastscript", content);
        shell.style.display = "flex";
        output.textContent = "running...";
        const res = await fetch("/script_builder", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ script: content })
        });
        

        output.textContent = "";
        //FOR JSON RESPONSE RETURNED BY SERVER
        const contentType = res.headers.get('content-type') || '';
        // if server returned JSON, parse it and show
        if (contentType.includes('application/json')) {
        try {
            const j = await res.json();
            output.textContent = j.message ?? JSON.stringify(j);
        } catch (err) {
            output.textContent = 'Failed to parse JSON response';
        }
        output.scrollTop = output.scrollHeight;
        return;
       }

       // If body is null (some servers), just read text() as fallback
      if (!res.body) {
        const text = await res.text();
        output.textContent = text;
        output.scrollTop = output.scrollHeight;
        return;
      }

        // Streaming path: read chunks from the ReadableStream
        const reader = res.body.getReader();
        const decoder = new TextDecoder();

       while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const chunk = decoder.decode(value, { stream: true });
        output.innerText += chunk;
        output.scrollTop = output.scrollHeight; // auto-scroll to bottom
       }
    } catch (error) {
        alert("Error running script: " + error.message);
    }




    // Close modal2
    closeBtn2.addEventListener("click", () => {
        shell.style.display = "none";
    });

}

function loadScript(){
    fupload = document.getElementById("fileinput");
    fupload.click();
}

function addinput(){
    const field1 = document.getElementById("clifield")
    const xhttp = new XMLHttpRequest();
    xhttp.open("POST", "/addline", true);
    formdta = new FormData()
    formdta.append("line",field1.value)
    xhttp.send(formdta);

}


fileInput = document.getElementById("fileinput")
const textArea = document.getElementById("scriptArea");
fileInput.addEventListener("change", function () {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (event) {
                    
                    sessionStorage.setItem("screenbot4scriptname",file.name);
                    sessionStorage.setItem("screenbot4lastscript", event.target.result);
                    
                    textArea.value = event.target.result;
                };
                reader.readAsText(file);
            }
        });


  
function loadlastscript(){
    if (sessionStorage.getItem("screenbot4lastscript") !== null){
      var openlastscript = sessionStorage.getItem("screenbot4lastscript");
      const textArea = document.getElementById("scriptArea");
      textArea.value = openlastscript;
    }
}

loadlastscript()

