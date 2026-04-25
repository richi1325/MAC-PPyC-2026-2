import socket
import threading

semaforo = threading.Semaphore(100)
resultados_escaneo = {} 

def escanear_puerto(host, puerto):
    with semaforo:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            # Si el puerto está abierto (código 0)
            if s.connect_ex((host, puerto)) == 0:
                resultados_escaneo[host].append(puerto)
                print(f"[ABIERTO] {host} - Puerto {puerto}")

hosts = [
    "scanme.nmap.org", 
    "testphp.vulnweb.com",
    "example.com",
]

puertos_a_escanear = range(1, 9000)
threads = []

for host in hosts:
    resultados_escaneo[host] = []
    
    for puerto in puertos_a_escanear:
        t = threading.Thread(target=escanear_puerto, args=(host, puerto))
        threads.append(t)
        t.start()

for t in threads: 
    t.join()

for host, puertos in resultados_escaneo.items():
    puertos_ordenados = sorted(puertos)
    if puertos_ordenados:
        print(f"🌐 {host}: Puertos abiertos {puertos_ordenados}")
    else:
        print(f"🌐 {host}: Ningún puerto abierto encontrado en el rango.")