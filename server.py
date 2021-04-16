from tkinter import ttk
from tkinter import *
import threading
import socket
import os
import pyautogui

class Server(object):
    def main_form(self):
        """Creates the interface window"""
        self.root = Tk()
        self.root.title("Server")

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
        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        s.bind((addr, port))
        s.listen()
        while True:
            self.conn, self.target_addr = s.accept()
            data=self.conn.recv(1024)
            if not data:
                break
            self.magicFunction(data.decode())
    #Ham nay nhan lenh tu client
    def magicFunction(self,Str):
        if Str=='Hello':
            print('Hello')
        elif Str.find('SHUTDOWN')!=-1:
            #Commands the server to shut down
            try:
                a = Str.split()
                cmd = str
                if len(a) == 2:
                    cmd='shutdown -s -t ' + a[1]
                else:
                    cmd='shutdown -s'
                os.system(cmd)
            except Exception as e:
                self.conn.send("Invalid command: " + str(e))
        elif Str == 'CAPSCR':
            print(Str)
            #Commands the server to capture its screen and send the screenshot back to the client
            pyautogui.screenshot().save('scr.png')
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as u:
                u.connect((self.target_addr[0], 1026))
                with open('scr.png', 'rb') as send:
                    while True:
                        data = send.read(1024)
                        if not data:
                            break
                        u.sendall(data)
        elif Str == 'SHWPRC':
            print(Str)
            #Commands the server to send the file consisting of running processes
            os.system("tasklist>list.txt")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as u:
                u.connect((self.target_addr[0], 1026))
                with open('list.txt', 'r') as send:
                    while True:
                        data = send.read(1024)
                        if not data:
                            break
                        u.sendall(data.encode())

        else:
            print('Nope')
    def Close(self):
        s.close()
        close_it=threading.Thread(target=self.root.destroy)
        close_it.start()
ins=Server()
mainz=threading.Thread(target=ins.main_form)
mainz.start()
