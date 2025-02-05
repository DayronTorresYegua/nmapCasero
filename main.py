import socket
import ipaddress
import subprocess
import sys
from datetime import datetime

def validar_ip(ip):
    """Verifica si la dirección IP tiene un formato válido."""
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def hacer_ping(ip):
    """Comprueba si la IP está activa en la red con un ping."""
    try:
        comando = ["ping", "-c", "1", ip] if sys.platform != "win32" else ["ping", "-n", "1", ip]
        resultado = subprocess.run(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return resultado.returncode == 0
    except Exception as e:
        print(f"Error al ejecutar ping: {e}")
        return False

def escanear_puertos(ip, puertos):
    """Escanea una lista de puertos en la IP dada."""
    print(f"\n[+] Escaneando {len(puertos)} puertos en {ip}...\n")
    abiertos = []
    inicio = datetime.now()

    for puerto in puertos:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((ip, puerto)) == 0:
                abiertos.append(puerto)
                print(f"[✔] Puerto {puerto} ABIERTO")

    fin = datetime.now()
    print(f"\n[✓] Escaneo completado en {fin - inicio} segundos.")
    if abiertos:
        print("\n[+] Puertos abiertos detectados:")
        print(", ".join(map(str, abiertos)))
    else:
        print("[!] No se encontraron puertos abiertos.")

def main():
    """Función principal del programa."""
    if len(sys.argv) < 2:
        print("Uso: python scanner.py <IP> [-c]")
        return

    ip = sys.argv[1]
    modo_rapido = "-c" in sys.argv

    if not validar_ip(ip):
        print("[!] Dirección IP no válida.")
        return

    print(f"[+] Comprobando disponibilidad de {ip}...")
    if not hacer_ping(ip):
        print("[!] La IP no responde al ping. Puede estar inactiva o bloquear ICMP.")
        return

    # Puertos más usados para el escaneo rápido
    puertos_comunes = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 3389, 8080]
    
    # Determinar qué puertos escanear
    puertos_a_escanear = puertos_comunes if modo_rapido else range(0, 65536)

    escanear_puertos(ip, puertos_a_escanear)

if __name__ == "__main__":
    main()
