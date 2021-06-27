import random

from django.http import HttpResponse
from django.template import loader
from psutil import AccessDenied

from .services.cpu import CpuService
from .services.memory import MemoryService
from .services.disc import DiscService
from .services.ip import IpService
from .services.os_service import OsService

import psutil

cpu_service = CpuService(psutil)
memory_service = MemoryService(psutil)
disc_service = DiscService(psutil)
ip_service = IpService(psutil)
os_service = OsService(psutil)


def index(request):
    template = loader.get_template('index.html')
    context = {
        'memory': memory_service.getMemoryInfo(),
        'cpu': cpu_service.getPercent(),
        'disc': disc_service.getDiscPercentage(),
        'ip': ip_service.getIpInfo(),

        'dirs': os_service.getDirs(),
        'files': os_service.getFilesInfos(),

        'listOfProcess': os_service.getProcessWith('pid'),
    }
    return HttpResponse(template.render(context, request))


def cpu_info(request):
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
        "ip_info": ip_service.getIpInfo()
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