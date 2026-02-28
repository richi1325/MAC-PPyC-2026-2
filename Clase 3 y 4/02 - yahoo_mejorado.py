import time
import random
import requests
import threading
from bs4 import BeautifulSoup
import queue

cola_procesos = queue.Queue()

def obtener_precio_stock():
    while not cola_procesos.empty():
        try:
            symbol = cola_procesos.get_nowait()
        except queue.Empty:
            break
        URL = f"https://finance.yahoo.com/quote/{symbol}"

        headers = {
            "User-Agent": "MiProyecto/1.0"
        }
        
        while True:
            time.sleep(30 * random.random())
            response = requests.get(URL, headers=headers,)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                valor = soup.find("span", {"data-testid": "qsp-price"})
                if valor:
                    precio = valor.text.strip()
                else:
                    precio = "Privado"
                break
            else:
                continue
        print(f"La accion {symbol} cuesta: {precio}")
        cola_procesos.task_done()

if __name__ == "__main__":
    with open("Clase 3/data/lista_sp500.txt", "r") as f:
        lista_symbolos = eval(f.read())
    threads = []
    
    for symbol in lista_symbolos:
        cola_procesos.put((symbol,))
    
    for _ in range(8):
        t = threading.Thread(target = obtener_precio_stock)
        t.start()