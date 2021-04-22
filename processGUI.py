from tkinter import *
from tkinter import ttk
import threading
import socket
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll
class KeyloggerWindow(Frame):
    def __init__(self,master,ip,port_no):
        Frame.__init__(self, master)
        self.master=master
        self.master.resizable(FALSE, FALSE)
        self.ip=ip
        self.port_no=port_no
    
        hookButton = ttk.Button(self.master, text='Hook',command=self.manageEventHook)
        hookButton.place(x=5,y=5,height=60)

        unHookButton = ttk.Button(self.master, text='Unhook',command=self.eventUnhook)
        unHookButton.place(x=130,y=5,height=60)
        
        printButton = ttk.Button(self.master, text='Print',command=self.eventPrint)
        printButton.place(x=255,y=5,height=60)

        deleteButton = ttk.Button(self.master, text='Delete',command=self.eventDelete)
        deleteButton.place(x=380,y=5,height=60)
        #file status

        self.treeViewProcess=ttk.Treeview(self.master)
        self.treeViewProcess["columns"]=("one","two","three")
        


    def loadKeyLog(self):
        self.master.wm_title("Keylogger")
        self.master.geometry('510x250')
        self.master.mainloop()
    def manageEventHook(self):
        threading.Thread(target=self.eventHook).start()
    def eventHook(self):
        pass
    def eventUnhook(self):
        pass
    def eventPrint(self):
        pass 
    def eventDelete(self):
        pass
