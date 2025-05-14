Este proyecto ofrece funcionalidades básicas de firewall, implementado en Python, usando el patrón Chain of Responsibility. Su objetivo es analizar y monitorear el tráfico de red (paquetes TCP, UDP, ICMP…) aplicando reglas personalizables en cascada, como:

**Filtrado por IP:** Alerta si la IP de origen de un paquete si no está dentro de la lista de IPs permitidas

**Control de ICMP:** Permite “bloquear” o “permitir” paquetes de tipo ICMP

**Filtrado por protocolo y puerto:** Alerta cuando los paquetes entrantes utilizan un protocolo no permitido o ingresan por un puerto no autorizado

**Registro detallado:** Un mensaje al final del análisis del paquete.

## ¿Cómo funciona?

1. **Captura paquetes de red** usando la librería **`scapy` ,** la cual permite leer y analizar cada campo de un paquete (IP origen/destino, puertos, flags TCP, tipo ICMP, etc.).
2. **Pasa cada paquete por una cadena de "handlers"** (filtros), donde cada uno verifica una condición específica:
    
    **IP_handler → ICMP_handler → Stateful_handler → Protocol_handler → Port_handler**
    
3. **Informa  en tiempo real**: Imprime mensajes en consola que permiten al usuario visualizar las los informes de cada análisis

## Instalación

### 1. Descarga el proyecto

### 2. Configura un entorno virtual

Ingresa a la terminal y ve a la dirección de tu proyecto

```bash
cd ruta/del/proyecto
```

Crea el entorno virtual

```bash
python -m venv venv
```

Activa el entorno virtual

- Windows

```bash
.\venv\Scripts\activate
```

- Linux

```bash
source venv/bin/activate
```

Sabrás que se activó correctamente porque vas a ver esto al lado de tu ruta

![image.png](attachment:ea86f391-305b-4bd1-a704-4b65bf55e8ec:image.png)

### 3. Instala las dependencias del proyecto

Una vez activado el entorno, podrías instalar los paquetes necesario sin problemas:

- Instalar individualmente

```bash
pip install nombre_del_paquete
```

- Instalar todo

```bash
pip install . 
```

### 4. Corre el proyecto

1. Ingresa a la carpeta src

```bash
cd src
```

1. Ejecuta el firewall

```bash
python firewall.py
```