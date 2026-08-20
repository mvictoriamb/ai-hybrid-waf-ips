from scapy.all import sniff, IP, TCP, UDP

def analizar_paquete(paquete):
    # Solo nos interesan los paquetes que tengan capa IP (Internet Protocol)
    if IP in paquete:
        ip_origen = paquete[IP].src
        ip_destino = paquete[IP].dst
        
        # Identificar si es TCP o UDP para saber el puerto
        puerto = "Desconocido"
        if TCP in paquete:
            puerto = paquete[TCP].dport
        elif UDP in paquete:
            puerto = paquete[UDP].dport
            
        print(f"[*] Paquete interceptado: {ip_origen} -> {ip_destino} (Puerto {puerto})")

def iniciar_escucha(interfaz=None):
    print(f"[*] Iniciando el Core IPS... Escuchando tráfico de red.")
    print("[*] Presiona Ctrl+C para detener.")
    
    # sniff captura los paquetes y ejecuta 'analizar_paquete' por cada uno
    sniff(iface=interfaz, prn=analizar_paquete, store=False)

if __name__ == "__main__":
    iniciar_escucha()

