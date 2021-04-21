from tkinter import ttk
from tkinter import *
import threading
import socket
import os
import pyautogui
import registry
from winreg import *
import keyboard #pip install keyboard

mp={
    'HKEY_CLASSES_ROOT':HKEY_CLASSES_ROOT,
    'HKEY_CURRENT_CONFIG':HKEY_CURRENT_CONFIG,
    'HKEY_CURRENT_USER':HKEY_CURRENT_USER,
    'HKEY_USERS':HKEY_USERS,
    'HKEY_LOCAL_MACHINE':HKEY_LOCAL_MACHINE
}
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
            print(data)
            if not data:
                break
            self.magicFunction(data)
    #Ham nay nhan lenh tu client
    def magicFunction(self,Str):
        if Str.decode()=='Hello':
            print('Hello')
        elif Str.decode().find('SHUTDOWN')!=-1:
            #Commands the server to shut down
            try:
                a = Str.decode().split()
                cmd = Str.decode()
                if len(a) == 2:
                    cmd='shutdown -s -t ' + a[1]
                else:
                    cmd='shutdown -s'
                os.system(cmd)
            except Exception as e:
                self.conn.send("Invalid command: " + str(e))
        elif Str.decode() == 'CAPSCR':
            print(Str.decode())
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
        elif Str.decode() == 'SHWPRC':
            print(Str.decode())
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
        elif Str.decode().find('GETVALUE')!=-1:
            print(Str.decode())
            arr = Str.decode().split(' ')
            brr = arr[1].split('\\',1)
            self.conn.send(str(registry.getValue(mp[brr[0]],brr[1],arr[2])).encode())
        elif Str.decode().find('DELETEVALUE')!=-1:
            print(Str.decode())
            arr = Str.decode().split(' ')
            brr = arr[1].split('\\',1)
            if registry.deleteValue(mp[brr[0]],brr[1],arr[2]):
                self.conn.send('Thao tác thành công'.encode())
            else:
                self.conn.send('Không thành công'.encode())
        elif Str.decode().find('CREATEKEY')!=-1:
            print(Str.decode())
            arr = Str.decode().split(' ')
            if registry.createKey(arr[1])==True:
                self.conn.send('Thao tác thành công'.encode())
            else:
                self.conn.send('Không thành công'.encode())
        elif Str.decode().find('DELETEKEY')!=-1:
            print(Str.decode())
            arr = Str.decode().split(' ')
            if registry.deleteKey(arr[1])==True:
                self.conn.send('Thao tác thành công'.encode())
            else:
                self.conn.send('Không thành công'.encode())
        elif Str.decode().find('SETVALUE')!=-1:
            print(Str.decode())
            arr = Str.decode().split('%')
            brr = arr[1].split('\\',1)
            try:
                if registry.setValue(mp[brr[0]],brr[1],arr[2],arr[3],arr[4]) == True:
                    self.conn.send('Thao tác thành công'.encode())
                else:
                    self.conn.send('Không thành công'.encode())
            except:
                self.conn.send('Không thành công'.encode())
        elif Str.decode() == 'KEYLOG':
            self.startKeylogging()    
        else:
            f_bin=open('testing.reg','wb+')
            f_bin.write(Str)
            f_bin.close()
            if len(Str)<1024:
                registry.importRegistry(filepath=r'E:\Python\Socket_Midterm\testing.reg')
                

    #ATTRIBUTES AND METHODS SPECIFICALLY FOR KEYLOGGING:
    __interval = 20
    __log = ''
    __noch = 0
    def __callback(self, event):
        name = event.name
        if len(name) > 1:
                if name == 'space':
                    name = ' '
                elif name == 'enter':
                    name = '[ENTER]\n'
                elif name == 'decimal':
                    name = '.'
                else:
                    name = name.replace(" ", "_")
                    name = f"[{name.upper()}]"
        self.__log += name
    def __report(self):
        if self.__log:
            self.conn.send(self.__log[self.__noch:].encode())
            self.__noch = len(self.__log)
        timer = threading.Timer(interval=self.__interval, function=self.__report)
        timer.daemon = True
        timer.start()
    def startKeylogging(self):
        keyboard.on_release(self.__callback)
        self.__report()
        keyboard.wait()
    ##################################################################################
    def Close(self):
        s.close()
        close_it=threading.Thread(target=self.root.destroy)
        close_it.start()
ins=Server()
mainz=threading.Thread(target=ins.main_form)
mainz.start()
