import joblib
from scapy.all import sniff, IP, TCP, Raw
# Importamos tu escudo
from mitigator import bloquear_ip_iptables

print("[*] Despertando a la Inteligencia Artificial...")
# Cargamos el cerebro WAF que entrenaste en la Fase 1
try:
    modelo_waf = joblib.load("brain/waf_model.pkl")
    print("[+] Cerebro WAF cargado correctamente.")
except FileNotFoundError:
    print("[-] Error: No se encuentra el modelo en brain/waf_model.pkl")
    exit()

def analizar_y_decidir(paquete):
    # Solo analizamos si el paquete tiene capa de Red (IP), Transporte (TCP) y Datos puros (Raw)
    if IP in paquete and TCP in paquete and Raw in paquete:
        ip_origen = paquete[IP].src
        
        # Extraemos el texto del paquete y lo decodificamos
        try:
            payload = paquete[Raw].load.decode('utf-8', errors='ignore')
        except:
            payload = ""
            
        # Si hay texto, le preguntamos a la IA
        if payload:
            # El modelo espera una lista, por eso lo metemos en corchetes [payload]
            prediccion = modelo_waf.predict([payload])[0]
            
            if prediccion == 1:  # 1 significa Ataque Web en tu modelo
                print(f"\n[⚠️ ALERTA WAF] Texto malicioso detectado desde {ip_origen}!")
                print(f"[*] Fragmento del ataque: {payload[:60]}...") 
                
                # ¡Que caiga el martillo! Llamamos a iptables
                bloquear_ip_iptables(ip_origen, "Inyección/Ataque Web (Capa 7)")

def iniciar_ips():
    print("\n[*] 🛡️ AI-Hybrid-WAF-IPS Iniciado y Protegiendo la red...")
    print("[*] Presiona Ctrl+C para detener.")
    # Escuchamos la red y pasamos cada paquete a nuestra función
    sniff(prn=analizar_y_decidir, store=False)

if __name__ == "__main__":
    iniciar_ips()
