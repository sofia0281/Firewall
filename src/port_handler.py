from handler import Handler
from dotenv import load_dotenv
from scapy.all import *
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Valor por defecto: lista vacía si ALLOWED_IPS no existe
allowed_ports_str = os.getenv("ALLOWED_PORTS", "")
allowed_ports = [int(p) for p in allowed_ports_str.split(',')] if allowed_ports_str else []

class PortFilterHandler(Handler):
    def __init__(self, allowed_ports):
        self.allowed_ports = [int(p) for p in allowed_ports]
        self.next_handler = None

    def set_next(self, handler):
        self.next_handler = handler

    def handler_request(self, packet):
        if packet.haslayer(TCP):
            port = packet[TCP].dport
        elif packet.haslayer(UDP):
            port = packet[UDP].dport
        else:
            return self.next_handler.handler_request(packet) if self.next_handler else None

        if port in self.allowed_ports:
            print(f"✅ Puerto {port} permitido")
            return self.next_handler.handler_request(packet) if self.next_handler else None
        else:
            print(f"🚫 Puerto {port} bloqueado")
            return "Port Blocked"

    def is_allowed_port(self, port):
        return port in self.allowed_ports
