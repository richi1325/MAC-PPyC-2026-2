import time 
import multiprocessing

def calcular(nombre: str) -> None:
    print(f"Proceso {nombre} empezando a calcular ...")
    resultado = sum(i*i for i in range (50_000_000))
    print(f"Proceso {nombre} finalizó ...")

if __name__ == "__main__":
    start = time.time()
    procesos = []
    for name in ["X", "Y", "Z", "A"]:
        procesos.append(
            multiprocessing.Process(target=calcular,args=(name,))
        )
    
    for process in procesos:
        process.start()
    
    for process in procesos:
        process.join()

    end = time.time()
    print(f"Tiempo total: {end - start}")