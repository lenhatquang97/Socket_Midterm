from tkinter import *
from tkinter import ttk
import threading
import socket
from time import sleep
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll
class Kill(Frame):
    def __init__(self,master,conn:socket.socket,function='KILL'):
        Frame.__init__(self, master)
        self.master = master
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
        self.conn.send(("KILL " + self.pid.get()).encode())
        sleep(5)
        data = self.conn.recv(8)
        if data == 'TRUE':
            self.conn.send('SHWPRC'.encode())
            with self.conn:
                while True:
                    data = self.conn.recv(1024)
                    if not data:
                        break
                    print(data.decode(), end='')
            print("")
        else:
            print("Failed to kill process.")
        pass
class Start(Kill):
    def __init__(self, master, conn,function):
        super().__init__(master, conn, function=function)
    def sendProcess(self):
        self.conn.send(("START " + self.pid.get()).encode())
        sleep(5)
        data = self.conn.recv(8)
        if data == 'TRUE':
            self.conn.send('SHWPRC'.encode())
            with self.conn:
                while True:
                    data = self.conn.recv(1024)
                    if not data:
                        break
                    print(data.decode(), end='')
            print("")
        else:
            print("Failed to start process.")
        pass
class Process(Frame):
    def __init__(self,master, conn:socket.socket):
        Frame.__init__(self, master)
        self.master = Toplevel(master)
        self.master.resizable(FALSE, FALSE)
        self.conn = conn
    
        killButton = ttk.Button(self.master, text='Kill',command=self.eventKillProcess)
        killButton.place(x=5,y=5,height=60)

        watchButton = ttk.Button(self.master, text='Watch',command=self.eventWatchProcess)
        watchButton.place(x=130,y=5,height=60)

        startButton = ttk.Button(self.master, text='Start',command=self.eventStartProcess)
        startButton.place(x=380,y=5,height=60)
        #file status

    def loadProcess(self):
        self.master.wm_title("Process")
        self.master.geometry('510x300')
        self.master.mainloop()
    def eventKillProcess(self):
        ins=Kill(Toplevel(),self.conn)
        ins.load()
    def eventWatchProcess(self):
        self.conn.send("SHWPRC")
    def eventStartProcess(self):
        ins=Start(Toplevel(),self.conn,'START')
        ins.load('Start')
