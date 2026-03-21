import threading
import queue
import time

# Configuración masiva
NUM_ASIENTOS = 10000
NUM_VENDEDORES = 1000

# La Queue es inherentemente segura para hilos
asientos_disponibles = queue.Queue()
for i in range(NUM_ASIENTOS):
    asientos_disponibles.put(i)

asientos_ocupados = [None] * NUM_ASIENTOS
ventas_totales = 0
lock_contador = threading.Lock()

def vendedor_eficiente(id_vendedor):
    global ventas_totales
    while True:
        try:
            # Intentamos sacar un asiento de la cola sin bloquearnos para siempre
            asiento_id = asientos_disponibles.get_nowait()
            
            # Simulamos el trabajo de procesar el pago
            time.sleep(0.0001) 
            
            asientos_ocupados[asiento_id] = f"Vendedor-{id_vendedor}"
            
            with lock_contador:
                ventas_totales += 1
                
            asientos_disponibles.task_done()
        except queue.Empty:
            # Si la cola está vacía, el vendedor termina su turno
            break

start_time = time.time()

hilos = []
for i in range(NUM_VENDEDORES):
    t = threading.Thread(target=vendedor_eficiente, args=(i,))
    hilos.append(t)
    t.start()

for t in hilos:
    t.join()

end_time = time.time()

print(f"--- RESULTADOS OPTIMIZADOS ---")
print(asientos_ocupados)
print(f"Ventas totales: {ventas_totales}")
print(f"Asientos libres: {len([a for a in asientos_ocupados if a is None])}")
print(f"Tiempo total: {end_time - start_time:.2f} segundos")