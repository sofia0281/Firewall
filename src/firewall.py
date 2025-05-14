from IP_Handler import IPFilterHandler
from port_handler import PortFilterHandler 
from protocol_handler import ProtocolFilterHandler
from loggin_handler import LoggingHandler
from icmp_handler import ICMPFilterHandler
from state_handler import StatefulHandler
from network_block import block_ip 
from scapy.all import *
from dotenv import load_dotenv
import os
import socket
from threading import Thread

class Firewall:
    def __init__(self):
        self.first_handler = None
    
    def set_first_handler(self, handler):
        self.first_handler = handler

    def process(self, packet):
        if self.first_handler:
            result = self.first_handler.handler_request(packet)
            if result is None or result == "Logged and processed":
                return "Packet allowed by all filters"
            return result
        return "No handlers configured"

    # Mover setup_firewall FUERA de la clase Firewall
def setup_firewall():
    """Configura e inicializa el firewall con la cadena completa de handlers"""
    # 1. Cargar configuración desde .env
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if not os.path.exists(env_path):
        raise FileNotFoundError(f"No se encontró el archivo .env en {env_path}")
    
    load_dotenv(env_path)
    print(f"✅ Configuración cargada desde: {env_path}")

    # 2. Procesar configuración con valores por defecto
    config = {
        'allowed_ips': [ip.strip() for ip in os.getenv("ALLOWED_IPS", "192.168.1.1").split(',') if ip.strip()],
        'allowed_ports': [int(p.strip()) for p in os.getenv("ALLOWED_PORTS", "80,443,53").split(',') if p.strip()],
        'icmp_allowed': os.getenv("ICMP_ALLOWED", "True").lower() == "true",
        'strict_mode': os.getenv("STRICT_MODE", "True").lower() == "true"
    }

    print("\n🔧 Configuración activa:")
    print(f"  - IPs permitidas: {config['allowed_ips']}")
    print(f"  - Puertos permitidos: {config['allowed_ports']}")
    print(f"  - ICMP permitido: {'SI' if config['icmp_allowed'] else 'NO'}")
    print(f"  - Modo estricto: {'ACTIVADO' if config['strict_mode'] else 'DESACTIVADO'}")

    # 3. Crear instancias de handlers (orden de procesamiento recomendado)
    handlers = {
        'ip': IPFilterHandler(config['allowed_ips']),
        'icmp': ICMPFilterHandler(),
        'stateful': StatefulHandler(timeout=300),  # 5 minutos timeout
        'protocol': ProtocolFilterHandler(),
        'port': PortFilterHandler(config['allowed_ports']),
        'log': LoggingHandler()
    }

    # 4. Configurar cadena de responsabilidad
    # Cargar IPs permitidas en el handler ICMP (usamos las mismas que para IP)
    handlers['icmp'].update_config(
        icmp_allowed=config['icmp_allowed'],
        strict_mode=config['strict_mode'],
        allowed_ips=config['allowed_ips']
    )
    
    # Establecer cadena: IP → ICMP → Stateful → Protocol → Port → Log
    chain_order = ['ip', 'icmp', 'stateful', 'protocol', 'port', 'log']
    for i in range(len(chain_order)-1):
        current = chain_order[i]
        next_handler = chain_order[i+1]
        handlers[current].set_next(handlers[next_handler])

    # 5. Inicializar firewall
    firewall = Firewall()
    firewall.set_first_handler(handlers['ip'])

    return firewall, config

def run_cli():
    # Importación local para romper el ciclo de imports
    from cliente_interface import FirewallCLI
    cli = FirewallCLI()
    cli.run()

if __name__ == "__main__":
    run_cli()