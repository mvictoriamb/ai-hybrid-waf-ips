import os

def bloquear_ip_iptables(ip_maliciosa, tipo_ataque):
    print(f"[🛡️ IPS ACTIVO] {tipo_ataque} detectado desde {ip_maliciosa}. Bloqueando IP...")
    
    # Comando de Linux para tirar a la basura todo el tráfico de esa IP
    comando = f"iptables -A INPUT -s {ip_maliciosa} -j DROP"
    os.system(comando)
    
    print(f"[+] IP {ip_maliciosa} bloqueada con éxito en el Firewall.")
