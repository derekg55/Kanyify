import subprocess
import os
import glob
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from pydub import AudioSegment

os.environ["TK_SILENCE_DEPRECATION"] = "1"

window = Tk()
window.title("Kanyify")
window.geometry("500x500")
fileName = "default"

def combine():
    audio1 = AudioSegment.from_file(str(os.getcwd()+"/stems/vocals.out.wav"))
    audio2 = AudioSegment.from_file(str(os.getcwd()+"/stems/accompaniment.wav"))
    mixed = audio1.overlay(audio2)
    mixed.export(fileName+".wav", format="wav")
    messagebox.showinfo("Done","Complete! Outputted to"+os.getcwd())
    
    
def nameFile(input):
   global fileName
   fileName = input
   combine()
   
def name():
    top = Toplevel(window)
    top.geometry("750x250")
    top.title("Name file")
    textVar = StringVar()
    entry = Entry(top, width= 25,textvariable = textVar)
    entry.pack()
    button= Button(top, text="Ok", command=lambda:[nameFile(textVar.get()),top.destroy()])
    button.pack()

def openFile():
    filetypes = [("Audio files","*.mp3 *.wav")]
    filepath = filedialog.askopenfilename(filetypes=filetypes)
    if(filepath!=""):
        stempath = os.getcwd()+"/stems"
        subprocess.call(["spleeter", "separate", "-o", stempath, "-f", "{instrument}.{codec}", filepath])
        messagebox.showinfo("Done","Finished stem splitting. Press okay to begin Kanyification. This may take a while. Outputted to "+os.getcwd())
        inpath = os.getcwd()+"/stems/vocals.wav"
        outpath = os.getcwd()+"/stems/vocals.out.wav"
        subprocess.call(["svc", "infer", "-o", outpath, "-m", "G_199200.pth", "-c", "config.json", "-fm", clicked.get(), inpath])
        messagebox.showinfo("Done","Finished Kanyification. Press okay to begin final output.")
        name()

label2 = Label(window, text="Choose an algorithm.\n(crepe-tiny ==> fast & low quality, crepe ==> slow & high quality)", wraplength=300, justify="center")
label2.pack()
options = ["crepe-tiny","crepe"]
clicked = StringVar()
clicked.set(options[0])
drop = OptionMenu(window, clicked, *options)
drop.pack(pady=20)
label1 = Label(window, text="Choose a file to Kanyify.")
label1.pack()
button = Button(text="Select a file", command=openFile)
button.pack()

window.mainloop()

