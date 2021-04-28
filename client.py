from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import socket
import commander
import threading
from registerGUI import *
import keylogGUI
import processGUI
from time import sleep
class Client(object):
    def __init__(self):
        """Creates the interface window"""
        self.root = Tk()
        self.root.title("Client")

        #mainframe
        self.mainframe = ttk.Frame(self.root, padding="10 10 25 25")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE, FALSE)

        #IP addr. input space
        self.ip_addr = StringVar()
        ip_addr_entry = ttk.Entry(self.mainframe, width=40, textvariable=self.ip_addr)
        ttk.Label(self.mainframe, text='IP Addr.').grid(column=1, row=1, sticky=(W,E))
        ip_addr_entry.grid(column=1,row=2,sticky=(W,E))

        #Port input space
        self.port = StringVar()
        port_entry = ttk.Entry(self.mainframe, width=10, textvariable=self.port)
        ttk.Label(self.mainframe, text='Port').grid(column=2, row=1, sticky=(W,E))
        port_entry.grid(column=2, row=2, sticky=(W,E))
        
        #Connect button
        connectButton = ttk.Button(self.mainframe, text='Connect', command=self.Connect)
        connectButton.grid(column=3, row=2, sticky=(E))

        #Functions
        ttk.Label(self.mainframe, text='Command').grid(column=1,row=3,sticky=(W,E))
        self.func = StringVar()
        funcEntry = ttk.Combobox(self.mainframe, textvariable=self.func, width=40)
        funcEntry['values'] = ("Show running processes", "Show running apps", "Shutdown", "Screen capture"
                                , "Keylog", "Edit registries")
        funcEntry.state(["readonly"])
        funcEntry.grid(column=1, row=4, sticky=(S))

        #Confirmation button
        self.confButton = ttk.Button(self.mainframe, text='Go', command=self.act, state=DISABLED)
        self.confButton.grid(column=3, row=4, sticky=(E,S))

        subframe = ttk.Frame(self.root, padding='3 3 12 12')
        subframe.grid(row=1, column=0)

        self.State = ttk.Label(subframe, text='Not connected')
        self.State.grid(column=1, row=1)

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)
        pass
    connection = None
    #Connect to the server
    def Connect(self):
        try:
            self.IP = str(self.ip_addr.get())
            self.port_no = int(self.port.get())
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.IP, self.port_no))
            self.connection.send('Hello'.encode())


            self.State['text'] = "Connected to server: " + self.IP + ":" + str(self.port_no) + "."
            self.confButton['state'] = NORMAL
        except:
            messagebox.showerror(title='Connect error', message='An error occurred while trying to connect to the address ' + 
                            self.IP + ":" + str(self.port_no) + ".")
            self.confButton['state'] = DISABLED
            
        
    def act(self):
        func = self.func.get()
        if func == "Show running processes":
            self.command_ShowProcess()
        elif func == "Show running apps":
            self.command_ShowApps()
        elif func == "Shutdown":
            self.command_Shutdown()
        elif func == "Screen capture":
            self.command_CaptureScreen()
        elif func == "Keylog":
            self.command_Keylog()
        elif func == "Edit registries":
            self.command_RegEdit()

    
    def command_Shutdown(self):
        cmd = commander.ShutdownCMD(self.root)
        cmd.NewInstance()
        if cmd.isExcuted==False:
            cmd.command = 'Nope'
        else:
            cmd.command = 'SHUTDOWN'
        command = cmd.command + " " + cmd.delay_time.get()
        print(command)
        self.sendToServer(command)
        
        pass

    def command_CaptureScreen(self):
        cmd = 'CAPSCR'
        print(cmd)
        self.sendToServer(cmd)
        scrshot = open("capture.png", 'wb')
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as re:
            re.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
            re.bind((socket.gethostbyname(socket.gethostname()), 1025))
            re.listen(1)
            conn, addr = re.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    scrshot.write(data)
        scrshot.close()
        pass

    def command_ShowProcess(self):
        ins = processGUI.Process(self.root,self.IP,self.port_no)
        processThread=threading.Thread(target=ins.loadProcess())
        processThread.start()
    def command_RegEdit(self):
        regEdit = RegistryWindow(Toplevel(),self.IP,self.port_no)
        regeditThread = threading.Thread(target=regEdit.loadReg(res='750x500'))
        regeditThread.start()
    
    def command_Keylog(self):
        keyloggerGUI = keylogGUI.KeyloggerWindow(Toplevel(),self.IP,self.port_no)
        keylogThread = threading.Thread(target=keyloggerGUI.loadKeyLog())
        keylogThread.start()
       

    #Ham gui toi server
    def sendToServer(self,Str):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.IP, self.port_no))
        self.connection.send(Str.encode())
    
    def NewInstance(self):
        self.root.mainloop()
    def CloseConnection(self):
        if type(self.connection) == socket.socket:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.IP, self.port_no))
            self.connection.send(b"")
            self.connection.close()
            
ins = Client()
ins.NewInstance()
