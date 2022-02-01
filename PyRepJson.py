from tkinter import Tk, filedialog
from datetime import datetime
import json

import os
import subprocess
import webbrowser

def runReport(Folders):
    #create folder for new report
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    f = open ('PyRep.json')
    data = json.load (f)
    f.close()

    driveName = data['appDrive']
    folderName = driveName + data['repFolder'] + data['repPrefix'] + current_time
    os.mkdir(folderName)

    #create report parameters
    repExe = driveName + data['repExe']
    reports = '-reports:"'
    for folder in Folders:
        reports += folder + "\\coverage.xml;"
    reports +='" '
    targetdir = '-targetdir:"{PATH}" '.format(PATH=folderName)
    sourcedirs = '-sourcedirs:"' + driveName + data['sourcedirs'] + '"'
    
    #run the report
    cmd = repExe + reports + targetdir + sourcedirs
    print (cmd)
    subprocess.call(cmd)

    #show the report
    url = "file://" + folderName + '\\index.html'
    webbrowser.open(url)




# MAIN
root = Tk() # pointing root to Tk() to use it as Tk() in program.
root.withdraw() # Hides small tkinter window.
root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
folders = []
while True:
    path1 = filedialog.askdirectory(title="Select first folder") # Returns opened path as str
    if not path1:
        break
    folders.append(path1)

runReport(folders)

