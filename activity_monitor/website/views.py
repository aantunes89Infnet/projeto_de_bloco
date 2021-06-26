from django.http import HttpResponse
from django.template import loader
from .services.cpu import CpuService
from .services.memory import MemoryService
from .services.disc import DiscService
from .services.ip import IpService

import psutil

cpu_service = CpuService(psutil)
memory_service = MemoryService()
disc_service = DiscService(psutil)
ip_service = IpService(psutil)


def index(request):
    cpu = round(psutil.cpu_percent(), 2)

    template = loader.get_template('index.html')

    context = {
        'memory': memory_service.getMemoryInfo(),
        'cpu': cpu_service.getPercent(),
        'disc': disc_service.getDiscPercentage(),
        'ip': ip_service.getIpInfo(),
    }
    return HttpResponse(template.render(context, request))


def cpu_info(request):
    context = {
        'cpu_list': cpu_service.getPercent(),
        'cpu_brand': cpu_service.getBrand(),
        'cpu_arch': cpu_service.getArch()
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

# TODO: Adicionar informação de nome/modelo da CPU (brand)
# TODO: Adicionar informação do tipo da arquitetura (arch);
# TODO: Adicionar informação da palavra do processador (bits);
# TODO: Adicionar informação sobre a frequência total e frequência de uso da CPU;
# TODO: Adicionar informação do número total de núcleos (núcleo físico) e threads (núcleo lógico).
