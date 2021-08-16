from django.http import HttpResponse
from django.template import loader
from psutil import AccessDenied

from .services.cpu import CpuService
from .services.memory import MemoryService
from .services.disc import DiscService
from .services.ip import IpService
from .services.os_service import OsService

import psutil

import sched
import time
import threading

cpu_service = CpuService(psutil)
memory_service = MemoryService(psutil)
disc_service = DiscService(psutil)
ip_service = IpService(psutil)
os_service = OsService(psutil)


def print_time(cb):
    time.sleep(2)
    print("EVENTO", time.ctime())
    print(f"FREQUENCIA: {psutil.cpu_freq()[0]}")
    return cb


def index(request):
    scheduler = sched.scheduler(time.time, time.sleep)
    template = loader.get_template('index.html')

    print("EVENTO AGORA", time.ctime())

    context = {
        'memory': memory_service.getMemoryInfo(),
        'cpu': cpu_service.getPercent(),
        'disc': disc_service.getDiscPercentage(),
        'ip': ip_service.getIpInfo(),

        'dirs': scheduler.enterabs(2, 1, print_time(os_service.getDirs), ())[2],
        'files': scheduler.enterabs(4, 2, print_time(os_service.getFilesInfos), ())[2],

        'listOfProcess': os_service.getProcessWith('pid'),
    }

    print('CHAMADAS ESCALONADAS DA FUNÇÃO:', time.ctime())
    scheduler.run()
    return HttpResponse(template.render(context, request))


def cpu_info(request):
    threading.Thread
    context = {
        'cpu_list': cpu_service.getCpuList(),
        'cpu_brand': cpu_service.getBrand(),
        'cpu_arch': cpu_service.getArch(),
        'cpu_bits': cpu_service.getBits(),
        'cpu_freq': cpu_service.getFreq(),
    }
    template = loader.get_template('cpu-info.html')
    return HttpResponse(template.render(context, request))


def memory_info(request):
    context = {
        'memory_info': memory_service.getMemoryInfo()
    }
    template = loader.get_template('memory-info.html')
    return HttpResponse(template.render(context, request))


def disc_info(request):
    context = {
        "disc_percentage": disc_service.getDiscPercentage()
    }
    template = loader.get_template('disc-info.html')
    return HttpResponse(template.render(context, request))


def ip_info(request):
    context = {
        # "ip_info": ip_service.getIpInfo()
        "ip_info": ""
    }
    template = loader.get_template('ip-info.html')
    return HttpResponse(template.render(context, request))


def process():
    plist = psutil.get_process_list()
    plist = sorted(plist, key=lambda i: i.name)
    for i in plist:
        try:
            return i.name, i.get_cpu_percent()
        except AccessDenied:
            return "'%s' Process is not allowing us to view the CPU Usage!" % i.name
