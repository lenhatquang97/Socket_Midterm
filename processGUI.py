from tkinter import *
from tkinter import ttk
import threading
import socket
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll
class Process(Frame):
    def __init__(self,master,ip,port_no):
        Frame.__init__(self, master)
        self.master=master
        self.master.resizable(FALSE, FALSE)
        self.ip=ip
        self.port_no=port_no
    
        killButton = ttk.Button(self.master, text='Kill',command=self.eventKillProcess)
        killButton.place(x=5,y=5,height=60)

        watchButton = ttk.Button(self.master, text='Watch',command=self.eventWatchProcess)
        watchButton.place(x=130,y=5,height=60)
        
        deleteButton = ttk.Button(self.master, text='Delete',command=self.eventDeleteProcess)
        deleteButton.place(x=255,y=5,height=60)

        startButton = ttk.Button(self.master, text='Start',command=self.eventStartProcess)
        startButton.place(x=380,y=5,height=60)
        #file status

        self.treeViewProcess=ttk.Treeview(self.master)
        s = ttk.Style()
        s.configure('Treeview', rowheight=30)
        
        self.treeViewProcess["columns"]=("one","two")
        self.treeViewProcess.column("#0",width=165,anchor=CENTER)
        self.treeViewProcess.column("one",width=165,anchor=CENTER)
        self.treeViewProcess.column("two",width=165,anchor=CENTER)
        self.treeViewProcess.heading("#0",text='Name Process')
        self.treeViewProcess.heading("one",text='ID Process')
        self.treeViewProcess.heading("two",text='Count Threads')

        #Mau
        self.treeViewProcess.insert("",'end',text='notepad.exe',values=("1234",'12'))

        self.treeViewProcess.place(x=5, y=80,height=200)

        


    def loadKeyLog(self):
        self.master.wm_title("Process")
        self.master.geometry('510x300')
        self.master.mainloop()
    def eventKillProcess(self):
        pass
    def eventWatchProcess(self):
        pass
    def eventDeleteProcess(self):
        pass 
    def eventStartProcess(self):
        pass
ins = Process(Tk(),'192.168.137.1',1025)
ins.loadKeyLog()