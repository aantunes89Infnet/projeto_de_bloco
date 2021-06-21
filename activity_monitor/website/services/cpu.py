import psutil


class CpuService:

    @staticmethod
    def getPercent():
        return psutil.cpu_percent(interval=1, percpu=True)

    @staticmethod
    def getCount():
        return psutil.cpu_count(logical=True)
