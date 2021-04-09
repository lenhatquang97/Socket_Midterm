from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import socket

class Client(object):
    def __init__(self):
        """Creates the interface window"""
        self.root = Tk()
        self.root.title("Client")

        #mainframe
        self.mainframe = ttk.Frame(self.root, padding="20 20 100 100")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE, FALSE)

        #IP addr. input space
        self.ip_addr = StringVar()
        ip_addr_entry = ttk.Entry(self.mainframe, width=40, textvariable=self.ip_addr)
        ttk.Label(self.mainframe, text='IP Addr.').grid(column=1, row=1, sticky=(W,E))
        ip_addr_entry.grid(column=2,row=1,sticky=(W,E))
        
        #Connect button
        connectButton = ttk.Button(self.mainframe, text='Connect', command=self.connect)
        connectButton.grid(column=3, row=1, sticky=(E))

        #Functions
        ttk.Label(self.mainframe, text='Command').grid(column=1,row=2,sticky=(W,E))
        self.func = StringVar()
        funcEntry = ttk.Combobox(self.mainframe, textvariable=self.func, width=40)
        funcEntry['values'] = ("Show running processes", "Show running apps", "Shutdown", "Screen capture"
                                , "Keylogging", "Edit registries")
        funcEntry.state(["readonly"])
        funcEntry.grid(column=2, row=2, sticky=(S))

        #Confirmation button
        confButton = ttk.Button(self.mainframe, text='Go', command=None)
        confButton.grid(column=3, row=2, sticky=(E,S))

        for child in self.mainframe.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

        self.root.mainloop()
        pass
    connection = None
    #Connect to the server
    def connect(self):
        try:
            IP = self.ip_addr.get()
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((IP, 1025))
        except:
            messagebox.showerror(title='Connect error', message='An error occurred while trying to connect to the address' + 
                            self.ip_addr.get() + ".")
    

    def __del__(self):
        if type(self.connection) == socket.socket:
            self.connection.close()
            print("Connection closed")

#ins = Client()

