import time
import multiprocessing

INITIAL_NUMBER = 33
STOP_NUMBER = 126
SUPERSECRET_PASSWORD = "s^42F~}3q&-"

def buscar_password(nombre_proceso):
    for intento in generate_passwords(nombre_proceso):
        if intento == SUPERSECRET_PASSWORD:
            print("Contraseña encontrada:", intento)
    print("Termino proceso:", nombre_proceso)


def generate_passwords(tamano, posicion=0, salto=1):
    base = STOP_NUMBER - INITIAL_NUMBER + 1  # 94
    total = base ** tamano

    for indice in range(posicion, total, salto):
        n = indice
        chars = [None] * tamano

        for i in range(tamano - 1, -1, -1):
            residuo = n % base
            chars[i] = chr(INITIAL_NUMBER + residuo)
            n //= base

        yield "".join(chars)

if __name__ == "__main__":
    start = time.time()
    PASSWORD_LENGTH = 12
    procesos = []
    
    for i in range(PASSWORD_LENGTH):
        p = multiprocessing.Process(
            target=buscar_password,
            args = (i + 1,)
        )
        procesos.append(p)
    
    for proceso in procesos:
        proceso.start()
    
    for proceso in procesos:
        proceso.join()
    
    print("Tiempo final", time.time()-start)