import platform
import socket
import psutil
import subprocess
import os
import netifaces


class IpService:
    def __init__(self):
        self._psutil = psutil
        self._platform = platform.system()
        self._gateways = netifaces.gateways()
        self._socket = socket

    def getPlatform(self):
        return self._platform

    def getIpInfo(self):
        s = self._socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]

    def getHosts(self):
        base_ip = self._getSubNet()
        return self._verifyHosts(f"{base_ip}")

    def getNetMask(self):
        network = self._psutil.net_if_addrs()['en0']
        netmask = None
        for net in network:
            if net[2] is not None:
                netmask = net[2]
                break
        return netmask

    def getDefaultGateway(self):
        return self._gateways['default'][netifaces.AF_INET][0]

    def netDataByInterface(self):
        return self._psutil.net_io_counters()

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
