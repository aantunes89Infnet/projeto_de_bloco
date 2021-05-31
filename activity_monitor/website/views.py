from django.http import HttpResponse
from django.template import loader
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
    ip_address = dic_interfaces['en0'][0].address

    template = loader.get_template('index.html')

    context = {
        'memory': memory_percentage(memory),
        'cpu': cpu,
        'disk': disk_percent,
        'ip': ip_address,
    }
    return HttpResponse(template.render(context, request))
