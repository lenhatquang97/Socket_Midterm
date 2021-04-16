from tkinter import filedialog
from tkinter import *
from winreg import *
import os
import winreg
def read_file(filename):
    f = open(filename,'r')
    print(f.read())
    pass
#send registry to server (will be done)
def sendRegistry():
    pass
#import registry in server
def importRegistry(filepath):
    os.system('reg import '+filepath)
#Create key folder
def createKey(pathRegistry):
    os.system('reg add '+pathRegistry)
#delete key folder
def deleteKey(pathRegistry):
    os.system('reg delete '+pathRegistry+' /f')
#Read key
def readKey(default_value,reg_path):
    hive = ConnectRegistry(None, default_value)
    hosts_key = OpenKey(hive, reg_path, access=KEY_READ | KEY_WOW64_64KEY)
    num_of_values = QueryInfoKey(hosts_key)[1]
    for i in range(num_of_values):
        values = EnumValue(hosts_key, i)
        print(values)
#set value value entry from registry key
def setValue(default_value,reg_path,name,value):
    try:
        winreg.CreateKey(default_value, reg_path)
        registry_key = winreg.OpenKey(default_value, reg_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError:
        return False
#Get value entry from registry key
def getValue(default_value,reg_path,name):
    try:
        registry_key = winreg.OpenKey(default_value, reg_path, 0, winreg.KEY_READ)
        value, regtype = winreg.QueryValueEx(registry_key, name)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError:
        return None

readKey(default_value=HKEY_CURRENT_USER,reg_path='test')
setValue(default_value=HKEY_CURRENT_USER,reg_path='test',name='ten',value='nono')