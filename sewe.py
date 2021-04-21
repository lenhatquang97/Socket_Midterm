
# Import module
import wmi
  
# Initializing the wmi constructor
f = wmi.WMI()
  
flag = 0
  
# Iterating through all the running processes
for process in f.Win32_Process():
    print(process.Name)
  