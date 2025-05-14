from handler import Handler
from dotenv import load_dotenv
from scapy.all import *
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

class ProtocolFilterHandler(Handler):
    def __init__(self):
        super().__init__()
        self.next_handler = None
        self.allowed_protocols = self._load_allowed_protocols()
        print(f"🔧 Protocolos permitidos: {', '.join(self.allowed_protocols)}")

    def _load_allowed_protocols(self):
        """Carga protocolos permitidos desde .env con valores por defecto"""
        protocols_str = os.getenv("allowed_protocols", "TCP,UDP,IP,Ethernet")
        return [proto.strip().upper() for proto in protocols_str.split(',') if proto.strip()]

    def set_next(self, handler):
        self.next_handler = handler

    def handler_request(self, packet):
        packet_protocols = self._get_protocol_stack(packet)
        forbidden_protos = self._identify_forbidden_protocols(packet_protocols)
        
        if not forbidden_protos:
            print(f"✅ Todos los protocolos permitidos: {packet_protocols}")
            if self.next_handler:
                return self.next_handler.handler_request(packet)
            return None
        else:
            for proto in forbidden_protos:
                print(f"🚫 Protocolo no permitido detectado: {proto}")
            print (f"Protocol Blocked (Forbidden: {', '.join(forbidden_protos)})")
            if self.next_handler:
                return self.next_handler.handler_request(packet)
            return None
            

    def _get_protocol_stack(self, packet):
        """Obtiene la pila completa de protocolos del paquete"""
        protocols = []
        current_layer = packet
        while current_layer:
            protocols.append(current_layer.name.upper())
            current_layer = current_layer.payload if hasattr(current_layer, 'payload') else None
        return protocols

    def _identify_forbidden_protocols(self, packet_protocols):
        """Identifica protocolos no permitidos en el paquete"""
        return [proto for proto in packet_protocols if proto not in self.allowed_protocols]