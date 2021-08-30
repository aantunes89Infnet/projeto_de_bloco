import psutil


class MemoryService:

    def __init__(self):
        self._memory = None
        self._psutil = psutil

    def setMemoryInfo(self):
        self._memory = self._psutil.virtual_memory()

    def getMemoryInfo(self):
        if self._memory is None:
            self.setMemoryInfo()
        in_use_percent = (self._memory.used / self._memory.total) * 100
        return round(in_use_percent, 2)
