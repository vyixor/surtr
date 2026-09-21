import os
import sys
from tkinter import PhotoImage
from customtkinter import *
import customtkinter
import pyaudiowpatch as pyaudio
from tkinter import messagebox
import credloader

if(os.path.exists(os.path.normpath("resources")) and os.path.isdir(os.path.normpath("resources"))):
    resource_path = os.path.normpath("resources")  
elif (os.path.exists(os.path.normpath("C:\\Surtr\\surtr\\resources")) and os.path.isdir(os.path.normpath("C:\\Surtr\\surtr\\resources"))):
    resource_path = os.path.normpath("C:\\Surtr\\surtr\\resources")
else:
    messagebox.showerror("Error","cannot find 'resources' folder")  
    sys.exit(100)
    
    
crefile = os.path.join(resource_path,"process","cred","awpdfs.sts")   
  

#for settings
webuibyte = {"bytes":""}
setting = {}

def settingsparser():
 try:
     decrp = credloader.decrypt_file(input_path=crefile,save=False)
     webuibyte["bytes"] = decrp
     prse = webuibyte["bytes"].decode()
     f = prse.split("\n")
     for i in f:
        stp = i.strip()
        ans = stp.split("=")
        setting[ans[0]] = " ".join(ans[1:]).strip()
 except Exception as e:
      messagebox.showerror("Error","WEBUI CANNOT START, CONFIGURATION ERROR")
      sys.exit(100)
 
settingsparser() 

    
def settings(index):
    if index in setting:
          return setting[index]
    else:
      return ""
 
  

p = pyaudio.PyAudio()

try: 
  
   dialog = customtkinter.CTk()
   dialog.config(background="white")
   # i replaced customtkinter default icon file CustomTkinter_icon_Windows.ico in py python venv folder with my own icon file so 
   # i dont need to set a default icon here
   #dialog.iconbitmap('resources\\icons\\icon.ico') # to change taskbar icon
   dialog.title("Surtr webui settings")

   # Move the window
   dialog.geometry("620x600")
   
   dialog.resizable(width=False,height=True)
   dialog.grid_columnconfigure(0, weight=1)
   dialog.grid_rowconfigure(0, weight=1)
   inp = StringVar()
   inp2 = StringVar()
   inp3 = StringVar()
   
   
   res = StringVar()
   vidq = StringVar()
   usecursor = StringVar()
   useaudio = StringVar()
   usedefaudio = StringVar()
   audiolist = StringVar()
   usescreen = StringVar()
   usefile = StringVar()
   usescriptbuilder = StringVar()
   usecommand = StringVar()
   userecord = StringVar()
   blockedcommand = StringVar()
   blockedfolder = StringVar()
   
   optns = []
   def savecredientials():
       uname = inp.get()
       pswrd = inp2.get()
       permnt = inp3.get()
       
       if uname=="":
           errinfo.configure(state="normal")
           errinfo.delete(1.0, END)
           errinfo.insert(1.0,"Username cannot be empty") 
           errinfo.configure(state="disabled")
       elif pswrd == "": 
           errinfo.configure(state="normal") 
           errinfo.delete(1.0, END)
           errinfo.insert(1.0,"Password cannot be empty") 
           errinfo.configure(state="disabled")
           
       elif vidq.get() == "": 
           errinfo.configure(state="normal") 
           errinfo.delete(1.0, END)
           errinfo.insert(1.0,"Give a video quality 10 - 100") 
           errinfo.configure(state="disabled")
       
       elif "=" in uname or "=" in pswrd or "=" in vidq.get() or "=" in blockedcommand.get(): 
           errinfo.configure(state="normal") 
           errinfo.delete(1.0, END)
           errinfo.insert(1.0,"(=) not allowed in input fields") 
           errinfo.configure(state="disabled")
           
       elif  vidq.get().isnumeric() == False: 
           errinfo.configure(state="normal") 
           errinfo.delete(1.0, END)
           errinfo.insert(1.0,"Only numbers allowed in video quality") 
           errinfo.configure(state="disabled")
           
       elif int(vidq.get()) < 10 or int(vidq.get()) >  100: 
           errinfo.configure(state="normal") 
           errinfo.delete(1.0, END)
           errinfo.insert(1.0,"Video quality input expects 10 - 100") 
           errinfo.configure(state="disabled")
          
       else: 
        try: 
         button.configure(text="SAVING")
         
         optns.append(f"username={uname}")
         optns.append(f"password={pswrd}")
         optns.append(f"resolution={res.get()}")
         optns.append(f"framequality={vidq.get()}")
         
         #for cursors
         if usecursor.get() == "1" :
               optns.append("usecursor=yes")
         else:
           optns.append("usecursor=no")
          
         # for audio 
         if useaudio.get() == "1" :
               optns.append("useaudio=yes")
         else:
           optns.append("useaudio=no")
           
           
         #for using default audio
         
         if usedefaudio.get() == "1" :
               optns.append("defaultloopback=yes")
         else:
           optns.append("defaultloopback=no")
         
         au = audiolist.get().split(':')
         optns.append(f"chosenloopbackid={au[0]}")
         
         # for all permissions
         if usescreen.get() == "1" :
               optns.append("usescreen=yes")
         else:
           optns.append("usescreen=no")
         
         if usefile.get() == "1" :
               optns.append("usefile=yes")
         else:
           optns.append("usefile=no")
           
         if usescriptbuilder.get() == "1" :
               optns.append("usescriptbuilder=yes")
         else:
           optns.append("usescriptbuilder=no")  
           
         if usecommand.get() == "1" :
               optns.append("usecommand=yes")
         else:
           optns.append("usecommand=no")
          
         if userecord.get() == "1" :
               optns.append("userecord=yes")
         else:
           optns.append("userecord=no")
           
          
         optns.append(f"blockedcommand={blockedcommand.get()}")
         
         if ";" in blockedfolder.get() or not blockedfolder.get() == "":
           addit = True
           if ";" in blockedfolder.get():
             chk = blockedfolder.get().split(";") 
           else:
             addit = False
             messagebox.showerror("Error","Please always add >> ; << at the end of every folder path you add. \n This indicates the end of every directory path. \n Surtr webui will skip folders without (;) at the end of their path. \n Skipping blocked folders list.")
           if addit == True:   
             for i in chk:
                 if os.path.exists(i) and os.path.isdir(i):
                          if len(i) > 25:
                              button.configure(text="Scanning {i[:25]}...")
                          else:
                            button.configure(text="Scan ended.")
                 else:
                    if i == "":
                       continue                  
                    addit = False
                    messagebox.showerror("Error",f"{i} does not exist or is not a folder. \n Skipping blocked folders list.")
                    break
                 button.configure(text="Scan ended.")
           if addit == True:
             optns.append(f"blockedfolder={blockedfolder.get()}")
         #save parameters
         if permnt == "1" :
           optns.append("permanent=yes")
         else:
           optns.append("permanent=no")
      
         credloader.encrypt_file("\n".join(optns),crefile,text=True)
         button.configure(text="SAVED") 
         
        except Exception as e:
         button.configure(text="Something went wrong")
         messagebox.showerror("Error",f"Error, {e}")
         
       
       
       set_appearance_mode("dark")
    
   set_appearance_mode("dark")                     # forces dark mode
   set_default_color_theme("dark-blue")            # any built-in theme works as base
    
   # SURTR COLOR OVERRIDE – works 100% on all current versions
   customtkinter.set_widget_scaling(1.0)
   customtkinter.CTkEntry.appearance_mode = "dark"
   customtkinter.CTkCheckBox.appearance_mode = "dark"
   customtkinter.CTkButton.appearance_mode = "dark"
   customtkinter.CTkTextbox.appearance_mode = "dark"
   customtkinter.CTkRadioButton.appearance_mode = "dark"
   customtkinter.CTkOptionMenu.appearance_mode = "dark"
   
   #fgColor="white" 
   fgColor="#151617"
   #textColor="black"
   textColor="#f7f5f2"
   #fgButtonColor="black"   #(on buttons)
   fgButtonColor="#ff3b1f"
   #hoverSaveColor="grey"   #(SAVE button)
   hoverSaveColor="#ff8a3d"
   checkboxColor = "white"
   checkboxColor = "#151617"
   
   boss = customtkinter.CTkScrollableFrame(dialog,width=500,height=600)
   boss.grid(row=0, column=0, padx=10, pady=10, sticky="ew")   
   #for errors    
   errinfo = customtkinter.CTkTextbox(boss,width=400,height=20,fg_color=fgColor,text_color="red",font=customtkinter.CTkFont(family="Calibri",size=20))
   #errinfo.insert(1.0,"error seen")
   errinfo.configure(state="disabled")
   errinfo.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
   
   
   #for username
   info = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info.insert(1.0,"WEBUI Username")
   info.configure(state="disabled")
   info.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
   
   field = customtkinter.CTkEntry(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,textvariable=inp,font=customtkinter.CTkFont(family="Calibri",size=20))
   field.grid(row=3, column=0, padx=10, pady=10, sticky="ew")
   field.focus()
   
   field.insert(0,settings("username"))
 
 
   #for password
   info2 = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info2.insert(1.0,"WEBUI Password")
   info2.configure(state="disabled")
   info2.grid(row=4, column=0, padx=10, pady=10, sticky="ew")
   
   
   field2 = customtkinter.CTkEntry(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,textvariable=inp2,font=customtkinter.CTkFont(family="Calibri",size=20))
   field2.grid(row=5, column=0, padx=10, pady=10, sticky="ew")
   
   field2.insert(0,settings("password"))
   #for videos
   info3 = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info3.insert(1.0,"RESOLUTION")
   info3.configure(state="disabled")
   info3.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
   
   # screen resolutions
   
   
   field3 = customtkinter.CTkRadioButton(boss,width=400,height=50,fg_color=fgButtonColor,text_color=textColor,variable=res,text="smooth video (lower quality): 640x360 (16:9 aspect ratio)",value="640x360",font=customtkinter.CTkFont(family="Calibri",size=20))
   field3.grid(row=7, column=0, padx=10, pady=10, sticky="ew")
   
   
   field4 = customtkinter.CTkRadioButton(boss,width=400,height=50,fg_color=fgButtonColor,text_color=textColor,variable=res,text="smooth video (lower quality): 800x450 (16:9 aspect ratio)",value="800x450",font=customtkinter.CTkFont(family="Calibri",size=20))
   field4.grid(row=8, column=0, padx=10, pady=10, sticky="ew")
   
   field5 = customtkinter.CTkRadioButton(boss,width=400,height=50,fg_color=fgButtonColor,text_color=textColor,variable=res,text="good balance (standard definition): 960x540 (16:9 aspect ratio)",value="960x540",font=customtkinter.CTkFont(family="Calibri",size=20))
   field5.grid(row=9, column=0, padx=10, pady=10, sticky="ew")
   
   field6 = customtkinter.CTkRadioButton(boss,width=400,height=50,fg_color=fgButtonColor,text_color=textColor,variable=res,text="decent quality (HD Ready): 1280x720 (16:9 aspect ratio)",value="1280x720",font=customtkinter.CTkFont(family="Calibri",size=20))
   field6.grid(row=10, column=0, padx=10, pady=10, sticky="ew")
    
   field7 = customtkinter.CTkRadioButton(boss,width=400,height=50,fg_color=fgButtonColor,text_color=textColor,variable=res,text="No resolution (Use normal screensize)",value="normal",font=customtkinter.CTkFont(family="Calibri",size=20))
   field7.grid(row=11, column=0, padx=10, pady=10, sticky="ew")   
   
   if settings("resolution") == "640x360":
     field3.select()
   elif settings("resolution") == "800x450":
     field4.select()
   elif settings("resolution") == "960x540":
     field5.select()    
   elif settings("resolution") == "1280x720":
      field6.select()   
   elif settings("resolution") == "normal":
      field7.select()   
   #screen and cursors
   
   info7 = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info7.insert(1.0,"FRAME AND CURSOR")
   info7.configure(state="disabled")
   info7.grid(row=12, column=0, padx=10, pady=10, sticky="ew")
    
   info8 = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info8.insert(1.0,"Video Quality")
   info8.configure(state="disabled")
   info8.grid(row=13, column=0, padx=10, pady=10, sticky="ew")
   
   field9 = customtkinter.CTkEntry(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,textvariable=vidq,font=customtkinter.CTkFont(family="Calibri",size=20))
   field9.grid(row=14, column=0, padx=10, pady=10, sticky="ew")
   field9.insert(0,settings("framequality"))
   
   field10 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=usecursor,
                                      text="Include Cursor",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field10.grid(row=15, column=0,padx=10, pady=10, sticky="ew")
   
   if(settings("usecursor") == "yes"):
         field10.select()
  
  
  
  # for audios
  
   info9 = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info9.insert(1.0,"AUDIO CONFIGURATIONS")
   info9.configure(state="disabled")
   info9.grid(row=16, column=0, padx=10, pady=10, sticky="ew")
   
   field11 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=useaudio,
                                      text="Include Audio",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field11.grid(row=17, column=0,padx=10, pady=10, sticky="ew")
   
   if(settings("useaudio") == "yes"):
         field11.select()
         
   field19 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=usedefaudio,
                                      text="Use Default Loopback Audio",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field19.grid(row=18, column=0,padx=10, pady=10, sticky="ew")
   
   if(settings("defaultloopback") == "yes"):
         field19.select()
         
   audio_opts = []
   for i in range(p.get_device_count()):
      try:
        info = p.get_device_info_by_index(i)
        audio_opts.append(f"{info['index']}: {info['name']} (Input: {info['maxInputChannels']}, Output: {info['maxOutputChannels']})")
        
      except Exception as e_dev_info:
          audio_opts.append(f"  Could not get info for device index {i}: {e_dev_info}")
        
   field12 = customtkinter.CTkOptionMenu(boss,width=400,height=50,fg_color=fgColor,text_color=textColor, variable=audiolist,values=audio_opts,font=customtkinter.CTkFont(family="Calibri",size=20))
   field12.grid(row=19, column=0, padx=10, pady=10, sticky="ew")
  
   
  
  
  # FOR PERMISSIONS
   info12 = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info12.insert(1.0,"PERMISSIONS")
   info12.configure(state="disabled")
   info12.grid(row=20, column=0, padx=10, pady=10, sticky="ew")
  
  
   field12 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=usescreen,
                                      text="Allow Desktop Stream",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field12.grid(row=21, column=0,padx=10, pady=10, sticky="ew")
   
   if(settings("usescreen") == "yes"):
         field12.select()
         
   field13 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=usefile,
                                      text="Allow File Manager",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field13.grid(row=22, column=0,padx=10, pady=10, sticky="ew")
   
   if(settings("usefile") == "yes"):
         field13.select()
   
   field14 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=usescriptbuilder,
                                      text="Enable Script Builder",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field14.grid(row=23, column=0,padx=10, pady=10, sticky="ew")
   
   
   if(settings("usescriptbuilder") == "yes"):
         field14.select()
         
   field15 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=usecommand,
                                      text="Allow Commands",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field15.grid(row=24, column=0,padx=10, pady=10, sticky="ew")
   
   if(settings("usecommand") == "yes"):
         field15.select()
         
   field16 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=userecord,
                                      text="Allow Recording",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field16.grid(row=25, column=0,padx=10, pady=10, sticky="ew")
   
   if(settings("userecord") == "yes"):
         field16.select()
         
         
   info13 = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info13.insert(1.0,"Commands not allowed (space for multiple commands)")
   info13.configure(state="disabled")
   info13.grid(row=26, column=0, padx=10, pady=10, sticky="ew")
   
   field17 = customtkinter.CTkEntry(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,textvariable=blockedcommand,font=customtkinter.CTkFont(family="Calibri",size=20))
   field17.grid(row=27, column=0, padx=10, pady=10, sticky="ew")
   
   field17.insert(0,settings("blockedcommand"))
   
   info14 = customtkinter.CTkTextbox(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,font=customtkinter.CTkFont(family="Calibri",size=20))
   info14.insert(1.0,"Folders not allowed (add {;} at the end of each folder path)")
   info14.configure(state="disabled")
   info14.grid(row=28, column=0, padx=10, pady=10, sticky="ew")
   
   field18 = customtkinter.CTkEntry(boss,width=400,height=50,fg_color=fgColor,text_color=textColor,textvariable=blockedfolder,font=customtkinter.CTkFont(family="Calibri",size=20))
   field18.grid(row=29, column=0, padx=10, pady=10, sticky="ew")
   
   field18.insert(0,settings("blockedfolder"))
   
       #to save permanent or temporary
   field19 = customtkinter.CTkCheckBox(boss,
                                      width=20,
                                      height=20,
                                      fg_color=fgButtonColor,
                                      text_color=textColor,
                                      bg_color=checkboxColor,
                                      variable=inp3,
                                      text="Permanent(use always / only this session)",
                                      checkmark_color="white",
                                      font=customtkinter.CTkFont(family="Calibri",size=20))
   field19.grid(row=30, column=0,padx=10, pady=10, sticky="ew")

   

   if(settings("permanent") == "yes"):
         field19.select()
   
      
   button = customtkinter.CTkButton(boss, text="SAVE",hover_color=hoverSaveColor,corner_radius=10,fg_color=fgButtonColor,text_color="white",command=savecredientials,font=customtkinter.CTkFont(family="Calibri",size=20))
   button.grid(row=31, column=0, padx=20, pady=10, sticky="ew")
   
   dialog.mainloop()
   

       
       
except Exception as e:
    messagebox.showerror("Error",f"Err: {e}")
    sys.exit(100)
