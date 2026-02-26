import time
import threading

acumulado = 10

def api(nombre: str, incremento: int) -> None:
    # ! Race Condition
    global acumulado
    print(f"Hilo {nombre} empezando a descargar ...")
    time.sleep(5)
    acumulado += incremento
    print(f"Hilo {nombre} terminó con incremento: {acumulado}")

if __name__ == "__main__":
    start = time.time()
    threads = []
    for number in range(20):
        threads.append(
            threading.Thread(target=api, args=(number,number))
        )

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    end = time.time()
    print(f"Tiempo total {end - start}")
