import base64
import io
import random
import urllib
import matplotlib.pyplot as plt

import cpuinfo
import psutil
import time


class CpuService:

    def __init__(self):
        self._info = cpuinfo.get_cpu_info()
        self._psutil = psutil

    def getCpuList(self):
        return self._psutil.cpu_percent(interval=1, percpu=True)

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

    def getBits(self):
        return self._info['bits']

    def getFreq(self):
        return self._psutil.cpu_freq().current

    def getCpuUsage(self, times):
        cpu_list = self.setupCpuList()
        for n in range(times):
            cpu_info = self._psutil.cpu_percent(interval=0, percpu=True)
            for i, use in enumerate(cpu_info):
                cpu_list[i].append(use)
            time.sleep(0.5)
        return cpu_list

    def getGraphBuffer(self, times):
        cpu_list = self.getCpuUsage(times)
        buffer_list = list()
        for i, cpu in enumerate(cpu_list):
            ax = plt.subplot()
            ax.plot(range(times), cpu)
            ax.set(xlabel="Time", ylabel="Percentage of Use %", title=f"CPU: {i + 1}")

            fig = plt.gcf()
            buffer = io.BytesIO()
            fig.savefig(buffer, format='png')
            buffer.seek(0)
            buffer_string = base64.b64encode(buffer.read())
            buffer_list.append(urllib.parse.quote(buffer_string))

        return buffer_list

    def setupCpuList(self):
        cpu_count = self._psutil.cpu_count()
        cpu_list = list()
        for c in range(cpu_count):
            cpu_list.append(list())
        return cpu_list
