from tkinter import *
#import tkinter, tkFileDialog
from tkinter.filedialog import askdirectory
from tkinter.colorchooser import *

#from PIL import ImageTk, Image
from PIL import Image
from imageprocess import imageprocess
import glob, os

def doNothing():
    print("do nothing")

class newFrame:
    inURL=""
    outURL=""
    color = (0,0,0)
    def __init__(self,master):
        frame = Frame(master)   
        frame.pack(fill="both", expand=1)
        
        
        self.inputFolderAddress = Entry(frame)
        self.outputFolderAddress = Entry(frame)
        
        self.inputFolderSelectButton = Button(frame, text = "set input images folder...", command = self.inputDirectory)       
        self.outputFolderSelectButton = Button(frame, text = "set output images folder...", command = self.outputDirectory)
        
        
        self.inputFolderAddress.grid(row=0,columnspan=3, padx=5, pady=2, sticky="ew")
        self.inputFolderSelectButton.grid(row=0, column = 3, padx=5, pady=2,  sticky="ew")
        self.outputFolderAddress.grid(row=1, columnspan=3, padx=5, pady=2,  sticky="ew")
        self.outputFolderSelectButton.grid(row=1, column = 3,padx=5, pady=2)
        
        
        self.widthLabel = Label(frame, text = "width")
        self.heightLabel = Label(frame, text = "height")
        
        self.width = Entry(frame)
        self.height = Entry(frame)
        
        self.widthLabel.grid(row=2, padx=5, pady=2, sticky="e")
        self.heightLabel.grid(row=3, padx=5, pady=2, sticky="e")
        
        self.width.grid(row=2, padx=5, pady=2,column = 1, sticky="w")
        self.height.grid(row=3, padx=5, pady=2,column =1, sticky="w")
        
        self.colorSelectButton = Button(frame, text = "select background color...", command = self.getColor)
        self.colorSelectButton.grid(row=5, padx=5, pady=2, sticky="w")

        self.colorbox = Canvas(frame, bg="white", height=30, width=20)
        self.colorbox.grid(row=6, padx=5, pady=10, sticky="ew")
        
        self.startButton = Button(frame, text = "Start", command = self.start, bg = "red")
        self.startButton.grid(row=7, padx=5, pady=10, columnspan=4, sticky="ew")
        
        self.status = Label(frame, text = "Progress 0%" , bd=1, relief = SUNKEN, anchor=W)
        self.status.grid(row=8, columnspan=4, padx=5, pady=10,sticky="ew")

        #frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        
        
    def printMessage(self):
        print("working")
        
        
    def inputDirectory(self):
        global inURL
        inURL=askdirectory()
        self.inputFolderAddress.delete(0, 'end')
        self.inputFolderAddress.insert(0,inURL)

        
    def outputDirectory(self):
        global outURL
        outURL=askdirectory()
        self.outputFolderAddress.delete(0, 'end')
        self.outputFolderAddress.insert(0,outURL)
    
    def buttonColor(self):
        self.colorSelectButton.config(bg=self.color)


    def getColor(self):
        global color
        color,hexV = askcolor()
        self.colorbox.configure(background=hexV)
        #self.color = askcolor() 
        #self.buttonColor()
        
    def start(self):
        global inURL
        global outURL
        height = int(self.height.get())
        width = int(self.width.get())
        print("Start processing......",height,width)
        
        for root, dirs, files in os.walk(inURL):
            total_file_count = len(files)
            shade = ""
            i=0
            count=0
            for file in files:
                if file.endswith(".jpg"):
                     imageprocess(height,width,10,inURL,outURL,file,color)
                     count=count+1
                     percentage = 100*count/total_file_count
                     while i< int(percentage*1.5) :
                         shade=shade+"|"
                         i=i+1
                     self.status.config(text=""+shade+str(int(percentage))+"%")
                

root = Tk()
root.title('Automatic Professional Portrait Creator')
root.geometry("500x400")
menu = Menu(root)
root.config(menu = menu)

fileMenu = Menu(menu)
menu.add_cascade(label = "File",menu = fileMenu)
fileMenu.add_command(label = "New", command = doNothing) #command = restart
fileMenu.add_command(label = "Exit", command = root.destroy)

editMenu = Menu(menu)
menu.add_cascade(label = "Edit",menu = editMenu)
editMenu.add_command(label = "Set width and height...",command = doNothing) # implement this

n = newFrame(root)
root.mainloop()
