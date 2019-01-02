from tkinter import *
from tkinter import ttk, messagebox
from tkinter.filedialog import askopenfilename, askdirectory
import configparser
import os.path
from pytube import YouTube
from pytube import Playlist
import subprocess


def createConfigfile():
    config = configparser.ConfigParser()
    config['DEFAULTS'] = {'SaveDirectory':''}
    with open('configuration.ini','w') as configfile:
        config.write(configfile)

def readConfigfile():
    if not os.path.isfile('configuration.ini'):
        createConfigfile()

    config = configparser.ConfigParser()
    config.read('configuration.ini')
    localdirectory = config['DEFAULTS']['SaveDirectory']
    return localdirectory

def saveConfigfile():
    localdirectoryname = myDirectoryName.get()
    config = configparser.ConfigParser()

    config['DEFAULTS'] = {'SaveDirectory':localdirectoryname}
    with open('configuration.ini','w') as configfile:
        config.write(configfile)

def selectFileDirectory():
    try:
        value = askdirectory()
        myDirectoryName.set(value)
    except ValueError:
        pass 

def downloadYoutubeVideo():
    myyoutubevideo = youtubelink.get()
    yt = YouTube(myyoutubevideo)
    stream = yt.streams.first()
    stream.download(myDirectoryName.get())
    saveConfigfile()
    messagebox.showinfo("Download erfolgreich", "Das Video wurde herunter geladen.")

def downloadYoutubeAudio():
    myyoutubevideo = youtubelink.get()
    yt = YouTube(myyoutubevideo)
    stream = yt.streams.first()
    stream.download(myDirectoryName.get())
    mp4 = '"'+myDirectoryName.get()+'/'+stream.default_filename+'"'
    mp3 = '"'+myDirectoryName.get()+'/'+yt.title+'.mp3'+'"'
    ffmpeg = ('ffmpeg -i %s ' % mp4 + mp3) 
    subprocess.run(ffmpeg)#, shell=True
    os.remove(myDirectoryName.get()+'/'+stream.default_filename)
    saveConfigfile()
    messagebox.showinfo("Download erfolgreich", "Das Audio wurde herunter geladen.")

root = Tk()
root.title("Youtube-Downloader")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

youtubelink = StringVar()
youtubeplaylistlink = StringVar()
myDirectoryName = StringVar()

tempdirectory = readConfigfile()
myDirectoryName.set(tempdirectory)


# Enter YoutubePlaylist
#Label
ttk.Label(mainframe,text="Youtube-Playlist-Link").grid(column=1, row=0,sticky=(W))
#Entry
YoutubePL_entry = ttk.Entry(mainframe, width = 20, textvariable = youtubeplaylistlink)
YoutubePL_entry.grid(column=2, row=0,sticky=(W,E))

#Download video button
ttk.Button(mainframe, text="Download Video", command=downloadYoutubeVideo).grid(column=3,row=0, sticky=(E,W))
#Download Audio button
ttk.Button(mainframe, text="Download Audio", command=downloadYoutubeAudio).grid(column=4,row=0, sticky=(E,W))


# Enter Videolink
#Label
ttk.Label(mainframe,text="Youtube-Link").grid(column=1, row=1,sticky=(W))
#Entry
Youtube_entry = ttk.Entry(mainframe, width = 20, textvariable = youtubelink)
Youtube_entry.grid(column=2, row=1,sticky=(W,E))

#Download video button
ttk.Button(mainframe, text="Download Video", command=downloadYoutubeVideo).grid(column=3,row=1, sticky=(E,W))
#Download Audio button
ttk.Button(mainframe, text="Download Audio", command=downloadYoutubeAudio).grid(column=4,row=1, sticky=(E,W))

#Select target directory
#Label
ttk.Label(mainframe,text="Ausgabeverzeichnis").grid(column=1, row=2,sticky=(W))
directoryname_entry = ttk.Entry(mainframe, width = 20, textvariable = myDirectoryName)
directoryname_entry.grid(column=2, row=2,sticky=(W,E))

#Verzeichnis auswählen
ttk.Button(mainframe, text="Verzeichnis auswählen", command=selectFileDirectory).grid(column=3, row=2, sticky=W)



root.mainloop()

