import platform
import socket
import psutil
import subprocess
import os


class IpService:
    def __init__(self):
        self._platform = platform.system()

    def getPlatform(self):
        return self._platform

    def getIpInfo(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def getIpv4Net(self):
        dic = psutil.net_if_addrs()
        netmasks = []
        for i in dic.values():
            if i[0].netmask is not None:
                netmasks.append(i[0].netmask)
        return netmasks[0]

    def getIpv4NetMask(self):
        return psutil.net_if_addrs()[0]

    def getHosts(self):
        base_ip = self._getSubNet()
        return self._verifyHosts(f"{base_ip}")

    # ----------------- PRIVATE ---------------------
    def _getPingCode(self, hostname):
        args = []
        if self._platform == "Windows":
            args = ["ping", "-n", "1", "-l", "1", "-w", "100", hostname]
        else:
            args = ['ping', '-c', '1', '-W', '1', hostname]

        return subprocess.call(args, stdout=open(os.devnull, 'w'), stderr=open(os.devnull, 'w'))

    def _verifyHosts(self, base_ip):
        valid_hosts = []
        return_codes = dict()
        for i in range(1, 21):

            return_codes[base_ip + '{0}'.format(i)] = self._getPingCode(base_ip + '{0}'.format(i))

            if i % 20 == 0:
                print(".", end="")
            if return_codes[base_ip + '{0}'.format(i)] == 0:
                valid_hosts.append(base_ip + '{0}'.format(i))

        return valid_hosts

    def _getSubNet(self):
        ip_string = self.getIpInfo()
        ip_lista = ip_string.split('.')
        return ".".join(ip_lista[0:3]) + '.'

# utilizar matplot lib pra gerar o grafico (etapa 8)
