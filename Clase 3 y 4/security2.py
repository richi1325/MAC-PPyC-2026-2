import socket
import threading
import queue

resultados_escaneo = {} 
cola_trabajos = queue.Queue()

def trabajador():
    while not cola_trabajos.empty():
        try:
            # Saca un trabajo (host y puerto) de la cola
            host, puerto = cola_trabajos.get_nowait()
        except queue.Empty:
            break
            
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((host, puerto)) == 0:
                resultados_escaneo[host].append(puerto)
                print(f"[ABIERTO] {host} - Puerto {puerto}")

        cola_trabajos.task_done()

hosts = [
    "scanme.nmap.org", 
    "testphp.vulnweb.com",
    "example.com",
]

puertos_a_escanear = range(1, 9000)

print("Iniciando escaneo masivo con threading puro y Queue...\n")

for host in hosts:
    resultados_escaneo[host] = []

for host in hosts:
    for puerto in puertos_a_escanear:
        cola_trabajos.put((host, puerto))

# 4. Creamos y arrancamos SOLO 100 hilos
hilos = []
for _ in range(100):
    t = threading.Thread(target=trabajador)
    t.start()
    hilos.append(t)

cola_trabajos.join()


for host, puertos in resultados_escaneo.items():
    puertos_ordenados = sorted(puertos)
    if puertos_ordenados:
        print(f"🌐 {host}: Puertos abiertos {puertos_ordenados}")
    else:
        print(f"🌐 {host}: Ningún puerto abierto encontrado en el rango.")