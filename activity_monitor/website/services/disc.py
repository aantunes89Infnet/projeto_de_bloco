import psutil


class DiscService:
    def __init__(self):
        self._psutil = psutil
        self._disc_percentage = None

    def setDiscInfo(self):
        disc = self._psutil.disk_usage('.')
        self._disc_percentage = round(disc.percent, 2)

    def getDiscPercentage(self):
        if self._disc_percentage is None:
            self.setDiscInfo()
        return self._disc_percentage
