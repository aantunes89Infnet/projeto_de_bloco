import psutil


class MemoryService:

    def __init__(self):
        self._memory = None

    def setMemoryInfo(self):
        self._memory = psutil.virtual_memory()

    def getMemoryInfo(self):
        if self._memory is None:
            self.setMemoryInfo()
        in_use_percent = (self._memory.used / self._memory.total) * 100
        return round(in_use_percent, 2)
