import threading
import time

start = time.time()
asientos = [None] * 10000
ventas_totales = 0
# Creamos el candado
lock_teatro = threading.Lock()

def vender_tickets_seguro(id_vendedor):
    global ventas_totales
    
    for _ in range(20):
        for i in range(len(asientos)):
            # SECCIÓN CRÍTICA: Bloqueamos antes de leer/escribir
            with lock_teatro:
                if asientos[i] is None:
                    time.sleep(0.0001) # La latencia ya no afecta
                    asientos[i] = f"Vendedor-{id_vendedor}"
                    ventas_totales += 1
                    break 
            # El lock se libera automáticamente al salir del bloque 'with'

vendedores = []
for i in range(1000):
    t = threading.Thread(target=vender_tickets_seguro, args=(i,))
    vendedores.append(t)
    t.start()

for t in vendedores:
    t.join()

asientos_ocupados = len([a for a in asientos if a is not None])
print(asientos)
print(f"--- RESULTADOS CON LOCK ---")
print(f"Tickets vendidos según el contador: {ventas_totales}")
print(f"Asientos realmente ocupados: {asientos_ocupados}")
print(f"Diferencia: {ventas_totales - asientos_ocupados} (¡Perfecto!)")
print(f"Tiempo total de ejecución: {time.time() - start:.2f} segundos")