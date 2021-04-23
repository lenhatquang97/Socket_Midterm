from tkinter import *
from tkinter import ttk
import threading
import socket
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll
class Kill(Frame):
    def __init__(self,master,conn:socket.socket,function='KILL'):
        Frame.__init__(self, master)
        self.master=master
        self.pid = StringVar()
        self.master.resizable(FALSE, FALSE)

        self.conn=conn
        self.entryInput = ttk.Entry(self.master,width=30,textvariable=self.pid)
        self.entryInput.place(x=5,y=5)

        clickButton = ttk.Button(self.master, text=function,command=self.sendProcess)
        clickButton.place(x=320,y=5,height=35)
    def load(self,name='Kill'):
        self.master.wm_title(name)
        self.master.geometry('450x50')
        self.master.mainloop()
    def sendProcess(self):
        pass
class Start(Kill):
    def __init__(self, master, conn,function):
        super().__init__(master, conn, function=function)
class Process(Frame):
    def __init__(self,master, conn:socket.socket):
        Frame.__init__(self, master)
        self.master=master
        self.master.resizable(FALSE, FALSE)
        self.conn = conn
    
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

        



    def loadProcess(self):
        self.master.wm_title("Process")
        self.master.geometry('510x300')
        self.master.mainloop()
    def eventKillProcess(self):
        ins=Kill(Toplevel(),self.conn)
        ins.load()
    def eventWatchProcess(self):
        pass
    def eventDeleteProcess(self):
        pass 
    def eventStartProcess(self):
        ins=Start(Toplevel(),self.conn,'START')
        ins.load('Start')
ins = Process(Tk(),conn=socket.socket)
ins.loadProcess()