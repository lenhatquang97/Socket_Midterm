from tkinter import *
from tkinter import ttk
import threading
import socket
from time import sleep
from typing_extensions import final
# pip install pillow
from PIL import Image, ImageTk
from pyautogui import scroll
import re
class Kill(Frame):
    def __init__(self,master,IP,port_no,function='KILL'):
        Frame.__init__(self, master)
        self.master = Toplevel(master)
        self.pid = StringVar()
        self.master.resizable(FALSE, FALSE)
        self.IP=IP
        self.port_no=port_no
        self.entryInput = ttk.Entry(self.master,width=30,textvariable=self.pid)
        if function=='START':
            self.entryInput.insert(0,'ProcessName')
        elif function=='KILL':
            self.entryInput.insert(0,'PID')
        self.entryInput.place(x=5,y=5)

        clickButton = ttk.Button(self.master, text=function,command=self.sendProcess)
        clickButton.place(x=320,y=5,height=35)
    def load(self,name='Kill'):
        self.master.wm_title(name)
        self.master.geometry('450x50')
        self.master.mainloop()
        try:
            self.master.destroy()
        except:
            print('No error')
    def sendProcess(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.IP, self.port_no))
            self.conn.send(("KILL " + self.pid.get()).encode())
            data = self.conn.recv(8)
            if data.decode() == 'TRUE':
                global PID_Deleted
                PID_Deleted=self.pid.get()
                self.master.quit()
        except:
            print("Failed to kill process.")
class Start(Kill):
    def __init__(self, master,IP,port_no,function):
        super().__init__(master,IP,port_no, function=function)
    def sendProcess(self):
        try:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.conn.connect((self.IP, self.port_no))
            self.conn.send(("START " + self.pid.get()).encode())
            data = self.conn.recv(8)
            if data.decode() == 'TRUE':
                self.master.quit()
            else: 
                print("Failed to start process.")
        except:
            pass
class Process(Frame):
    def __init__(self,master, IP, port_no):
        Frame.__init__(self, master)
        self.master = Toplevel(master)
        self.master.resizable(FALSE, FALSE)
        self.IP=IP
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
        self.treeViewProcess.heading("#0",text='Process Name')
        self.treeViewProcess.heading("one",text='Process ID')
        self.treeViewProcess.heading("two",text='Threads Count')

        #Mau
        #for i in range(0,10,1):
            #self.treeViewProcess.insert("",'end',text='notepad.exe',values=("1234",str(i)))

        self.treeViewProcess.place(x=5, y=80,height=200)

    def loadProcess(self):
        self.master.wm_title("Process")
        self.master.geometry('510x300')
        self.master.mainloop()
    def eventKillProcess(self):
        ins=Kill(self.master,self.IP,self.port_no)
        ins.load()
        self.deleteInTreeView(str(PID_Deleted))
    def eventDeleteProcess(self):
        selected_items = self.treeViewProcess.get_children()
        for child in selected_items:
            self.treeViewProcess.delete(child)
    def eventWatchProcess(self):
        self.eventDeleteProcess()
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect((self.IP, self.port_no))
        self.conn.send("SHWPRC".encode())
        final_result=[]
        csv_str=''
        while True:
            data = self.conn.recv(1024)
            if not data:
                break
            if data.decode().find('STOPRIGHTNOW')!=-1:
                break
            csv_str+=data.decode()
        final_result=csv_str.split(',')
        for i in range(0,len(final_result)//3,1):
            print(final_result[3*i],' ',final_result[3*i+1],' ',final_result[3*i+2])
            self.treeViewProcess.insert("",'end',text=final_result[3*i],values=(final_result[3*i+1],final_result[3*i+2]))
    def eventStartProcess(self):
        ins=Start(self.master,self.IP,self.port_no,'START')
        ins.load('Start')
    def deleteInTreeView(self,PID):
        selected_items = self.treeViewProcess.get_children()
        for child in selected_items:
            if str(self.treeViewProcess.item(child)['values'][0]) == PID:
                self.treeViewProcess.delete(child)