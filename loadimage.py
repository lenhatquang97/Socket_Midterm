from tkinter import *

# pip install pillow
from PIL import Image, ImageTk

class Window(Frame):
    def __init__(self,filepath, master=None):
        Frame.__init__(self, master)
        self.filepath=filepath
        self.master = master
        self.pack(side=TOP,fill=BOTH, expand=1)
        load = Image.open(self.filepath)
        render = ImageTk.PhotoImage(load)
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

def loadImg(imgpath):
    root = Toplevel()
    app = Window(imgpath,root)
    root.wm_title("Tkinter window")
    root.geometry("1366x768")
    root.mainloop()