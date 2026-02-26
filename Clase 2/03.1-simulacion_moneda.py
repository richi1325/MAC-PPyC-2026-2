import time
import threading
from scipy.stats import bernoulli

resultados = []

def generar_lanzamiento_moneda():
    global resultados
    resultados.append(int(bernoulli.rvs(0.5, size=1)[0]))

if __name__ == "__main__":
    start = time.time()
    threads = []
    n = 100_000
    for lanzamiento in range(n):
        threads.append(
            threading.Thread(
                target=generar_lanzamiento_moneda
            )
        )
    
    for thread in threads:
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end = time.time()
    conteo = 0
    for lanzamiento in resultados:
        if lanzamiento == 1:
            conteo += 1
    print(f"Cara: {conteo/n}, Cruz: {1 - conteo/n}")
    print(f"Tiempo final {end - start}")