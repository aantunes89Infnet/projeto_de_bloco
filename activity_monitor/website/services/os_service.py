import os
import random

import psutil
from psutil import AccessDenied


class OsService:
    def __init__(self, psutil):
        self._dirs_info = os.listdir()
        self._files = []
        self._files_info_dict = dict()
        self._dirs = []
        self._psutil = psutil
        self._processDict = dict()

        self.isFile()
        self.setFilesInfos()
        self.listProcess()

    def isFile(self):
        for element in self._dirs_info:
            if os.path.isfile(element):
                self._files.append(element)
            else:
                self._dirs.append(element)

    def setFilesInfos(self):
        for file in self._files:
            self._files_info_dict[file] = os.stat(file).st_size / 1000

    def getDirs(self):
        return self._dirs

    def getFilesInfos(self):
        return self._files_info_dict.items()

    def listProcess(self):
        pids = self._psutil.pids()
        for n in range(10):
            try:
                process = psutil.Process(random.choice(pids)).as_dict()
                self._processDict[process['name']] = process
            except AccessDenied:
                pass

    def getProcessWith(self, attr):
        new_dict = dict()
        for k, v in self._processDict.items():
            new_dict[k] = v[attr]
        return new_dict
