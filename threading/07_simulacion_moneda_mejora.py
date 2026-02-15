import time
import threading
from scipy.stats import bernoulli

conteo = 0

def generar_lanzamiento_moneda():
    global conteo 
    if int(bernoulli.rvs(0.5, size=1)[0]) == 1:
        conteo += 1

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
    print(f"Cara: {conteo/n}, Cruz: {1 - conteo/n}")
    print(f"Tiempo final {end - start}")