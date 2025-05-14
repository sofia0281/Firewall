# network_block.py (nueva versión)
import os
import platform
import logging
from datetime import datetime

def block_ip(ip):
    system = platform.system()
    try:
        if system == "Windows":
            # Bloquear IP en Windows Firewall
            os.system(f"netsh advfirewall firewall add rule name=\"BLOCK {ip}\" dir=in action=block remoteip={ip}")
            action = f"IP {ip} bloqueada en Windows Firewall"
        elif system == "Linux":
            # Bloquear IP con iptables
            os.system(f"sudo iptables -A INPUT -s {ip} -j DROP")
            action = f"IP {ip} bloqueada con iptables"
        else:
            action = "Sistema operativo no soportado"
        
        logging.warning(f"""
        🚨 BLOQUEO ACTIVADO
        • IP bloqueada: {ip}
        • Acción: {action}
        • Tiempo: {datetime.now()}
        """)
        return True
    except Exception as e:
        logging.error(f"Error al bloquear IP: {str(e)}")
        return False