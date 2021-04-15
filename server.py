from tkinter import ttk
from tkinter import *
import threading
import socket

class Server(object):
    def main_form(self):
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
        self.connectButton = ttk.Button(self.mainframe, text='Open', command=self.threadConnect)
        self.connectButton.grid(column=1, row=1)
        self.root.mainloop()
        pass
    def threadConnect(self):
        con=threading.Thread(target=self.Connect)
        con.start()
    def Connect(self):
        port = 1025
        addr = socket.gethostbyname(socket.gethostname())
        print(addr, port)
        self.connectButton['text'] = 'Close'
        self.connectButton['command'] = self.Close
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((addr, port))
        s.listen()
        while True:
            self.conn, self.target_addr = s.accept()

    def Close(self):
        close_it=threading.Thread(self.root.destroy())
        close_it.start()
ins=Server()
mainz=threading.Thread(target=ins.main_form)
mainz.start()