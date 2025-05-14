# GUIA DE IMPLEMENTACIÓN - FIREWALL

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

Ingresa al cmd y ubícate  dentro de la carpeta o lugar donde quieras que quede guardado el firewall, y ejecuta este comando.
`git clone https://github.com/sofia0281/Firewall.git`

### 2. Configura un entorno virtual

Ingresa a la terminal y ubícate dentro de Firewall

Debe quedar algo así:

C:tu_ruta\de\archivo\Firewall >>

1. Crea el entorno virtual

```bash
python -m venv venv
```

1. Activa el entorno virtual
- Windows

```bash
.\venv\Scripts\activate
```

- Linux

```bash
source venv/bin/activate
```

Sabrás que se **activó** correctamente porque vas a ver esto al lado de tu ruta

![image.png](attachment:ea86f391-305b-4bd1-a704-4b65bf55e8ec:image.png)

### 3. Instala las dependencias del proyecto

Una vez activado el entorno, podrás instalar los paquetes necesario sin problemas, recuerda que debe estar el entorno activado:

- Instalar individualmente

```bash
pip install nombre_del_paquete
```

- Instalar todo

```bash
pip install . 
```

Si las librerías siguen apareciendo como no instaladas, cierra y abre de nuevo el visual studio.

### 4. Corre el proyecto

1. Ingresa a la carpeta src

```bash
cd src
```

1. Ejecuta el firewall

```bash
python firewall.py
```

Esto es lo que deberás ver en tu terminal:

![image.png](attachment:ad3f238d-b98e-459c-bc8f-e4d498b3e8ed:image.png)

Opción 1: Ejecutar firewall con las configuraciones del .env

Opción 2: Puedes decirle al programa si quieres “habilitar” paquetes ICMP o no, y tambien puesdes ingresar ips permitidas o no escribir nada para ejecutar las del .env

Notas: 

1. Cada vez que cambies algo en el .env cierra la terminal e ingresa de nuevo al entorno virtual
2. No cambies la configuración de la variable: STRICT_MODE del .env
3. Siempre ejecuta dentro del venv

Realizado por:
Jancarlo Gallón
Sofia Soto Parra