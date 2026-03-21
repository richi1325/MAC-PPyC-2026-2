import time
import multiprocessing

SUPER_SECRET_PASSWORD=1

def buscar_password(inicio, fin):
    for intento in range(inicio, fin):
        if intento == SUPER_SECRET_PASSWORD:
            print("Contraseña encontrada:", intento)

if __name__ == "__main__":
    start = time.time()
    PASSWORD_LENGTH = 100_000_000
    # Fragmentar el espacio de busqueda
    num_procesos = multiprocessing.cpu_count()
    rango = PASSWORD_LENGTH // num_procesos
    procesos = []
    
    for i in range(num_procesos):
        p = multiprocessing.Process(
            target=buscar_password,
            args = (i * rango, (i+1)*rango)
        )
        procesos.append(p)
    
    for proceso in procesos:
        proceso.start()
    
    for proceso in procesos:
        proceso.join()
    
    print("Tiempo final", time.time()-start)