import time
import random
import requests
import threading
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, text

semaforo = threading.Semaphore(8)
dic = {}

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
                    dic[symbol] = precio
                else:
                    precio = "Privado"
                break
            else:
                continue
        print(f"La accion {symbol} cuesta: {precio}")
        print(dic)

#conexion con base de datos
user = "postgres"
password = "supersecret"
host = "localhost"
port = "5432"
database = "postgres"
#funcion conexion
def get_connection(user, password, host, port, database):
    return create_engine(
        url="postgresql+psycopg2://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )

#funcion insert
def insertdic(symbol, price):
    with get_connection(user, password, host, port, database).connect() as connection:
        insertdata = connection.execute(text(f"INSERT INTO inversiones(SYMBOL, PRICE, REGISTER_DATE) VALUES ('{symbol}', {price}, NOW())"))
        connection.commit()


if __name__ == "__main__":
    with open("Clase 3 y 4/data/lista_sp500.txt", "r") as f:
        lista_symbolos = eval(f.read())[:4]
    threads = []
    for symbol in lista_symbolos:
        threads.append(
            threading.Thread(target=obtener_precio_stock, args=(symbol,))
        )
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    thread_insert = []
    for value in dic.items():
        thread_insert.append(
            threading.Thread(target=insertdic, args=value)
        )
    for thread in thread_insert:
        thread.start()

    for thread in thread_insert:
        thread.join()