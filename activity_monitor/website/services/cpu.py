import random
import cpuinfo


class CpuService:

    def __init__(self, psutil):
        self._info = cpuinfo.get_cpu_info()
        self._psutil = psutil

    def getPercent(self):
        return self._psutil.cpu_percent(interval=1, percpu=True)[random.randint(0, 1)]

    def getCount(self):
        return self._psutil.cpu_count(logical=True)

    def getArch(self):
        return self._info['arch']

    def getBrand(self):
        try:
            if self._info['brand_raw'] is not None:
                return self._info['brand_raw']
            else:
                return self._info['brand']
        except:
            return "Não encontrado"



