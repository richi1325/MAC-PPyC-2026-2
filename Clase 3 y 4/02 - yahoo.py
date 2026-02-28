import time
import random
import requests
import threading
from bs4 import BeautifulSoup

semaforo = threading.Semaphore(8)

def obtener_precio_stock(symbol):
    with semaforo:
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

if __name__ == "__main__":
    with open("Clase 3/data/lista_sp500.txt", "r") as f:
        lista_symbolos = eval(f.read())
    threads = []
    for symbol in lista_symbolos:
        threads.append(
            threading.Thread(target=obtener_precio_stock, args=(symbol,))
        )
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()