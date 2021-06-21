from django.http import HttpResponse
from django.template import loader
from .services.cpu import CpuService

import psutil


def memory_percentage(memory):
    in_use_percent = (memory.used / memory.total) * 100
    print(in_use_percent)
    return round(in_use_percent, 2)


def index(request):
    disk = psutil.disk_usage('.')
    disk_percent = round(disk.percent, 2)
    memory = psutil.virtual_memory()
    cpu = round(psutil.cpu_percent(), 2)

    dic_interfaces = psutil.net_if_addrs()
    ip_address = get_ip(dic_interfaces)

    template = loader.get_template('index.html')

    context = {
        'memory': memory_percentage(memory),
        'cpu': cpu,
        'disk': disk_percent,
        'ip': ip_address,
    }
    return HttpResponse(template.render(context, request))


def get_ip(dic_interfaces):
    try:
        return dic_interfaces['en0'][0].address
    except:
        return dic_interfaces['Conexão Local* 1'][1].address


def process(request):
    cpu_list = CpuService.getPercent()

    context = {'cpu_list': cpu_list}
    template = loader.get_template('process.html')
    return HttpResponse(template.render(context, request))
