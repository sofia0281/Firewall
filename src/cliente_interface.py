import sys
import os
from firewall import setup_firewall
import socket 
from scapy.all import sniff, IP, ICMP, TCP, UDP
class FirewallCLI:
    def __init__(self):
        self.firewall = None
        self.config = None
        self.running = False

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def show_menu(self):
        self.clear_screen()
        print("🔥 Firewall de Control de Acceso - Menú Principal")
        print("\n1. Iniciar firewall")
        print("2. Configurar parámetros manualmente(Habilitar ICMP e ingresar ips manualmente)")
        print("3. Ver configuración actual")
        print("4. Salir")
        
        choice = input("\nSeleccione una opción: ")
        return choice

    def manual_config(self):
        self.clear_screen()
        print("⚙️ Configuración Manual")
        
        # ICMP
        icmp = input("¿Permitir ICMP? (s/n): ").lower() == 's'
        
        # IPs permitidas
        print("\nIngrese IPs permitidas (separadas por coma):")
        ips = input("(Dejar vacío para usar .env): ").strip()
        allowed_ips = [ip.strip() for ip in ips.split(',')] if ips else None
        
        # Guardar configuración temporal
        os.environ['ICMP_ALLOWED'] = str(icmp)
        if allowed_ips:
            os.environ['ALLOWED_IPS'] = ','.join(allowed_ips)

        if self.firewall and hasattr(self.firewall.first_handler, 'update_config'):
            self.firewall.first_handler.update_config(
                icmp_allowed=icmp,
                allowed_ips=allowed_ips if allowed_ips else None
            )
        
        input("\nConfiguración guardada. Presione Enter para continuar...")
    def start_firewall(self):
        try:
            self.firewall, self.config = setup_firewall()
            
            # Configurar verbosidad (nivel de detalle de lo mostrado en la terminal)
            current_handler = self.firewall.first_handler
            while current_handler:
                if hasattr(current_handler, 'set_verbose'):
                    current_handler.set_verbose(True)
                current_handler = getattr(current_handler, '_next_handler', None)
            
            print("\n🛡️ Firewall iniciado con configuración:")
            print(f"  - ICMP: {'PERMITIDO' if self.config['icmp_allowed'] else 'BLOQUEADO'}")
            print(f"  - IPs permitidas: {self.config['allowed_ips']}")
            # print(f"  - Modo verbose: {'ACTIVADO' if verbose else 'DESACTIVADO'}")
            print("\nPresione Ctrl+C para detener...")
            
            self.running = True
            sniff(
                prn=self.packet_callback,
                filter=f"ip and dst host {socket.gethostbyname(socket.gethostname())}",
                store=0,
                iface="Wi-Fi"
            )
        except KeyboardInterrupt:
            self.running = False
            print("\nFirewall detenido.")
            input("Presione Enter para continuar...")

    def packet_callback(self, packet):
        if packet.haslayer(IP):
            # Inicio de la cadena de handlers
            result = self.firewall.process(packet)
    def run(self):
        while True:
            choice = self.show_menu()
            
            if choice == '1':
                self.start_firewall()
            elif choice == '2':
                self.manual_config()
            elif choice == '3':
                self.show_current_config()
            elif choice == '4':
                print("\nSaliendo del firewall...")
                sys.exit(0)
            else:
                input("Opción inválida. Presione Enter para continuar...")

    def show_current_config(self):
        self.clear_screen()
        print("📋 Configuración Actual")
        if self.config:
            print(f"\n- ICMP permitido: {self.config['icmp_allowed']}")
            print(f"- IPs permitidas: {self.config['allowed_ips']}")
        else:
            print("\nInicia el firewall o configura parámetros manuales.")
        input("\nPresione Enter para volver al menú...")

if __name__ == "__main__":
    cli = FirewallCLI()
    cli.run()