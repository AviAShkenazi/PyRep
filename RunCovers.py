from tkinter import Tk, filedialog
from datetime import datetime
import json

import os
import subprocess
import webbrowser
import logging

#create class to run the code coverage app
# then create report

#timer decorator
def timer(fn):
    from time import perf_counter

    def inner(self, *args, **kwargs):
        start_time = perf_counter()
        to_execute = fn(self, *args, **kwargs)
        end_time = perf_counter()
        execution_time = end_time - start_time
        totalTime = '{0} took {1:.8f}s to execute'.format(fn.__name__, execution_time)
        print(totalTime)
        self.LogToFile(totalTime)

        return to_execute

    return inner

class CodeCover:
    def __init__(self) -> None:
        f = open ('PyRep.json')
        self.jsonData = json.load (f)
        f.close()
        self.appsList = self.jsonData['apps']

    def LogToFile (self, message):
        """
        Put a message to a log file
        :param message: The message
        :return: None
        """
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        logger.info('Create Log file for ' + message)

    def CreataFolder(self):
        self.folders = []
        #create report folder
        now = datetime.now()
        current_time = now.strftime("%Y%m%d_%H%M%S")
        self.driveName = self.jsonData['repDrive']
        self.folderName = self.driveName + self.jsonData['repFolder'] + self.jsonData['repPrefix'] + current_time
        self.folders.append(self.folderName)

        os.mkdir(self.folderName)
        logging.basicConfig(filename=self.folderName+'.log', filemode='w')
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.basicConfig(level=logging.DEBUG)

    @timer
    def RunOpenCover (self, appData):
        """
        Run open cover application to gather code coverage information
        :param appData: from json file
        :return: None
        """
        localAppData = os.getenv('LOCALAPPDATA')
        appPath = appData['appDrive'] + appData['appPath']
        appName = appPath + appData['appNAme']
        self.LogToFile('Create Log file for ' + appName)
        
        cmd = localAppData + '\\Apps\\OpenCover\\OpenCover.Console.exe -target:"' + appName + '" -output:"' + \
              self.folderName + '\\coverage.xml" -register:user '
        print (cmd)
        subprocess.call(cmd)

    def CollectFolderNames(self):
        if self.jsonData['merge']:
            root = Tk() # pointing root to Tk() to use it as Tk() in program.
            root.withdraw() # Hides small tkinter window.
            root.attributes('-topmost', True) # Opened windows will be active. above all windows despite of selection.
            while True:
                path1 = filedialog.askdirectory(title="Select more folder") # Returns opened path as str
                if not path1:
                    break
                self.folders.append(path1)

    @timer
    def RunReport(self, appData):
        """
        Run the reporter app to create an HTML report acording to collected coverage data
        :param appData: reporter info from json file
        :return: None
        """
        repExe = self.driveName + self.jsonData['repExe']
        reports = '-reports:"'
        for folder in self.folders:
            reports += folder + "\\coverage.xml;"
        reports +='" '
        targetDir = '-targetdir:"{PATH}" '.format(PATH=self.folderName)
        sourceDirs = '-sourcedirs:"' + self.driveName + appData['sourcedirs'] + '"'

        cmd = repExe + reports + targetDir + sourceDirs
        print (cmd)
        subprocess.call(cmd)

    def ShowReport(self):
        url = "file://" + self.folderName + '\\index.html'
        print (url)
        webbrowser.open_new_tab(url)
        

    def Run(self):
        for app in self.appsList:
            if app['active'] == 0: continue
            self.CreataFolder ()
            self.RunOpenCover(app)
            self.CollectFolderNames()
            self.RunReport(app)
            self.ShowReport()

# MAIN
if __name__ == "__main__":
    code = CodeCover()
    code.Run()


