import threading
import time

start = time.time()
# Recurso compartido: 10000 asientos (None = vacío)
asientos = [None] * 100
ventas_totales = 0

def vender_tickets(id_vendedor):
    global ventas_totales
    
    for _ in range(20): # Cada vendedor intenta vender 20 tickets
        for i in range(len(asientos)):
            if asientos[i] is None:
                time.sleep(0.0001) 
                
                asientos[i] = f"Vendedor-{id_vendedor}"
                ventas_totales += 1
                break

# Crear 1000 hilos (vendedores)
vendedores = []
for i in range(10):
    t = threading.Thread(target=vender_tickets, args=(i,))
    vendedores.append(t)
    t.start()

for t in vendedores:
    t.join()

# Resultados
asientos_ocupados = len([a for a in asientos if a is not None])
print(asientos)
print(f"--- RESULTADOS SIN LOCK ---")
print(f"Tickets vendidos según el contador: {ventas_totales}")
print(f"Asientos realmente ocupados en el teatro: {asientos_ocupados}")
print(f"Diferencia (Sobrevendido): {ventas_totales - asientos_ocupados}")
print(f"Tiempo total de ejecución: {time.time() - start:.2f} segundos")