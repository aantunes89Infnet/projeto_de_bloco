class IpService:
    def __init__(self, psutil):
        self._psutil = psutil
        self._ipInfo = None

    def setIpInfo(self):
        self._ipInfo = self._psutil.net_if_addrs()

    def getIpInfo(self):
        if self._ipInfo is None:
            self.setIpInfo()
        return self.addressHandlerBySO(self._ipInfo)

    def addressHandlerBySO(self, dic_interfaces):
        if dic_interfaces['en0'][0].address is not None:
            return dic_interfaces['en0'][0].address
        if dic_interfaces['Conexão Local* 1'][1].address is not None:
            return dic_interfaces['Conexão Local* 1'][1].address
        return "Não foi possível encontra o endereço de IP"
