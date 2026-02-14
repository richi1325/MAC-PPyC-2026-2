import time 
import multiprocessing

def calcular(nombre: str) -> None:
    print(f"Proceso {nombre} empezando a calcular ...")
    resultado = sum(i*i for i in range (50_000_000))
    print(f"Proceso {nombre} finalizó ...")

if __name__ == "__main__":
    start = time.time()
    proceso1 = multiprocessing.Process(target=calcular,args=("X",))
    proceso2 = multiprocessing.Process(target=calcular,args=("Y",))

    proceso1.start()
    proceso2.start()

    proceso1.join()
    proceso2.join()
    end = time.time()
    print(f"Tiempo total: {end - start}")