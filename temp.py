
# import module
import psutil
import subprocess
cmd = 'powershell "gps | where {$_.MainWindowTitle } | select Description,Id,@{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}'
proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
for line in proc.stdout:
    if not line.decode()[0].isspace():
        print(line.decode().rstrip())
'''
# check if chrome is open
print('Process  Application ID  thread_count')

for i in psutil.process_iter():
    print(str(i.name())+'  '+str(i.pid)+'  '+str(i.num_threads())+' '+str(i.status()))

'''