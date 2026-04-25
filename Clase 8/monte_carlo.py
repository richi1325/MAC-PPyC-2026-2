import multiprocessing
import random

def monte_carlo(tareas):
    punto_en_circulo = 0
    for _ in range(tareas):
        x = random.random() * 2 - 1
        y = random.random() * 2 - 1
        if (x ** 2 + y ** 2) <= 1:
            punto_en_circulo += 1
    return punto_en_circulo

if __name__ == '__main__':
    ITERACIONES = 300_000_000
    nucleos = multiprocessing.cpu_count()
    tareas_por_nucleo = ITERACIONES // nucleos
    tareas_totales = [tareas_por_nucleo] * nucleos 
    with multiprocessing.Pool(processes=nucleos) as pool:
        resultado = pool.map(monte_carlo, tareas_totales)
    print(4 * sum(resultado) / ITERACIONES)