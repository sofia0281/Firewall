
from scapy.all import *
from network_block import block_ip 
from handler import Handler  

class ICMPFilterHandler(Handler):
    def __init__(self):
        super().__init__()
        self.verbose = True  
        print(f"Handler {self.__class__.__name__} inicializado")
        # Cargar configuración inicial
        self.load_config()

    def load_config(self):
        """Carga configuración desde variables de entorno"""
        self.icmp_allowed = os.getenv("ICMP_ALLOWED", "False").lower() == "true"
        self.strict_mode = os.getenv("STRICT_MODE", "True").lower() == "true"
        self.allowed_ping_ips = [
            ip.strip() for ip in 
            os.getenv("ALLOWED_IPS", "").split(',') 
            if ip.strip()
        ]

    def update_config(self, icmp_allowed=None, strict_mode=None, allowed_ips=None):
        """Permite actualizar configuración desde la interfaz"""
        if icmp_allowed is not None:
            self.icmp_allowed = icmp_allowed
        if strict_mode is not None:
            self.strict_mode = strict_mode
        if allowed_ips is not None:
            self.allowed_ping_ips = allowed_ips
    
    def load_allowed_ips(self, ips):
        """Carga la lista de IPs permitidas para ICMP"""
        self.allowed_ping_ips = [ip.strip() for ip in ips if ip.strip()]
        if self.verbose:
            print(f"🔄 IPs permitidas para ICMP actualizadas: {self.allowed_ping_ips}")

    def handler_request(self, packet):
        # print(f"\n[DEBUG] Paquete recibido: {packet.summary()}")
        
        if packet.haslayer(ICMP):
            # print(f"[DEBUG] Capa ICMP detectada: {packet[ICMP].summary()}")
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            # print(f"[DEBUG] Origen: {src_ip} -> Destino: {dst_ip}")
                
            if dst_ip != socket.gethostbyname(socket.gethostname()):
                if self._next_handler:
                    return self._next_handler.handler_request(packet)
                return None
                    
            if not self.icmp_allowed:
                print(f"🛑 Intento de ingreso de un ICMP (la política global no lo autoriza )")
                # return "ICMP Blocked (global policy)"
                if self._next_handler:
                    return self._next_handler.handler_request(packet)
                return None
            if src_ip in self.allowed_ping_ips:
                if self.verbose:
                    print(f"🟢 Ping PERMITIDO desde {src_ip}")
                # Pasar al siguiente handler si el paquete fue permitido
                if self._next_handler:
                    return self._next_handler.handler_request(packet)
                return None
            else:
                print(f"🛑 ICMP Bloqueado: Política {'global' if not self.icmp_allowed else 'por IP'} | Origen: {src_ip}")
                if self.strict_mode:
                    block_ip(src_ip)
                if self._next_handler:
                    return self._next_handler.handler_request(packet)
                return None
        
        else:  # Para paquetes NO ICMP
            # print(f"[DEBUG] El paquete NO contiene capa ICMP. Capas: {packet.layers()}")
            # Pasar al siguiente handler
            if self._next_handler:
                return self._next_handler.handler_request(packet)
            return None