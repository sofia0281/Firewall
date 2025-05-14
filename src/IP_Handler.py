from handler import Handler
from scapy.all import *
import socket

class IPFilterHandler(Handler):
    def __init__(self, allowed_ips):
        super().__init__()
        self.allowed_ips = allowed_ips or []
        self.verbose = True
        print("🛡️ Filtro de IPs configurado")
        print(f"Handler {self.__class__.__name__} inicializado")

    def set_verbose(self, verbose):
        self.verbose = verbose

    def handler_request(self, packet):
        if not packet.haslayer(IP):
            # Si no es IP, pasa al siguiente handler
            if self._next_handler:
                return self._next_handler.handler_request(packet)
            return None
            
        src_ip = packet[IP].src
        
        if src_ip in self.allowed_ips:
            if self.verbose:
                print(f"🟢 IP Autorizada: {src_ip}")
        else:
            print(f"⚠️ IP No Permitida detectada: {src_ip} (continuando análisis de paquete...)")
        
        # Pasa el paquete al siguiente handler INDEPENDIENTEMENTE del resultado
        if self._next_handler:
            return self._next_handler.handler_request(packet)
        return None