import time
from scapy.all import IP, TCP, UDP, ICMP
from handler import Handler

class Connection:
    def __init__(self, src_ip, src_port, protocol):
        self.src_ip = src_ip
        self.src_port = src_port
        self.protocol = protocol
        self.state = 'NEW'
        self.first_seen = time.time()
        self.last_seen = time.time()
        self.packet_count = 1

    def update(self):
        self.last_seen = time.time()
        self.packet_count += 1
        if self.state == 'NEW':
            self.state = 'ESTABLISHED'

    def expire(self, timeout):
        return (time.time() - self.last_seen) > timeout

class StatefulHandler(Handler):
    def __init__(self, timeout=300):
        super().__init__()
        self.connection_table = {}
        self.timeout = timeout
        print(f"🛡️ StatefulHandler configurado (Timeout: {timeout}s)")

    def set_next(self, handler):
        self._next_handler = handler
        return self

    def handler_request(self, packet):
        if not packet.haslayer(IP):
            return super().handler_request(packet)

        src_ip = packet[IP].src
        protocol = None
        src_port = None

        # Identificar protocolo y puerto (si aplica)
        if packet.haslayer(TCP):
            protocol = 'TCP'
            src_port = packet[TCP].sport
        elif packet.haslayer(UDP):
            protocol = 'UDP'
            src_port = packet[UDP].sport
        elif packet.haslayer(ICMP):
            protocol = 'ICMP'
            src_port = 0  # ICMP no usa puertos

        if not protocol:
            return super().handler_request(packet)

        connection_id = (src_ip, src_port, protocol)

        # Limpieza de conexiones expiradas
        self._clean_expired_connections()

        # Manejo de la conexión
        if connection_id in self.connection_table:
            conn = self.connection_table[connection_id]
            conn.update()
            print(f"🔄 Conexión {protocol} existente: {src_ip}:{src_port} "
            f"(Paquetes: {conn.packet_count}, Estado: {conn.state})")
        else:
            self.connection_table[connection_id] = Connection(src_ip, src_port, protocol)
            print(f"🆕 Nueva conexión {protocol} detectada: {src_ip}:{src_port}")

        if self._next_handler:
            return self._next_handler.handler_request(packet)
        return None

    def _clean_expired_connections(self):
        expired = [cid for cid, conn in self.connection_table.items() 
                 if conn.expire(self.timeout)]
        
        if expired:
            print(f"♻️ Limpiando {len(expired)} conexiones expiradas:")
            for cid in expired:
                print(f"   - {cid[2]} {cid[0]}:{cid[1]}")
                del self.connection_table[cid]