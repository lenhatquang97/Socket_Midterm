from shutdown import *
def shutDown(str):
    x = str.replace('SHUTDOWN','')
    if x == '':
        x='0'
    shutdown(time=int(x,base=10),force=False,warning_off=False)