from tkinter import Tk, filedialog
from datetime import datetime

import os
import subprocess
import webbrowser

def runReport(Folder1, Folder2):
    #create folder for new report
    now = datetime.now()
    current_time = now.strftime("%Y%m%d_%H%M%S")
    
    folderName = "D:\\gitrep\\Reports\\Shell" + current_time
    os.mkdir(folderName)

    #create report parameters
    repExe = "D:\\ReportGenerator\\ReportGenerator_5.0.2\\net5.0\\ReportGenerator.exe "
    reports = '-reports:"{PATH1}\\coverage.xml;{PATH2}\\coverage.xml" '.format(PATH1=Folder1, PATH2=Folder2)
    targetdir = '-targetdir:"{PATH}" '.format(PATH=folderName)
    sourcedirs = '-sourcedirs:"D:\\gitrep\\iterorth"'
    
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
path1 = filedialog.askdirectory(title="Select first folder") # Returns opened path as str
path2 = filedialog.askdirectory(title="Select secons folder") # Returns opened path as str

runReport(path1, path2)

