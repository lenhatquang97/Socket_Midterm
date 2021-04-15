from tkinter import ttk
from tkinter import *

import socket

class Server(object):
    def __init__(self):
        """Creates the interface window"""
        self.root = Tk()
        self.root.title("Client")

        #mainframe
        self.mainframe = ttk.Frame(self.root, padding="100 100 250 250")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE, FALSE)

        #Open server button
        self.connectButton = ttk.Button(self.mainframe, text='Open', command=self.Connect)
        self.connectButton.grid(column=1, row=1)
        self.root.mainloop()
        pass
    def Connect(self):
        port = 1025
        addr = socket.gethostbyname(socket.gethostname())
        print(addr, port)

        self.connectButton['text'] = 'Close'
        self.connectButton['command'] = self.Close

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((addr, port))
            s.listen()
            self.conn, self.target_addr = s.accept()
            with self.conn:
                print('Connected by', self.target_addr)
                while True:
                    data = self.conn.recv(1024)
                    if not data:
                        break

    def Close(self):
        self.root.destroy()
                    
    