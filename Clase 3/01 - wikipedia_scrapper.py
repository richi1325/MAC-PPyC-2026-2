import requests
from bs4 import BeautifulSoup

try:
    with open("Clase 3/data/wiki.html", "r", encoding="utf-8") as f:
        response = f.read()
    soup = BeautifulSoup(response, "html.parser")
    table = soup.find(id="constituents")
    symbols = []
    # Iterar las filas de la tabla en html, se usa [1:] para ignorar la primer fila (títulos de la tabla)
    for row in table.find_all("tr")[1:]:
        # Almacenar en la lista todos los symbols de la página de wiki, find solo devuelve la primer coincidencia
        symbols.append(row.find("td").text.strip())
    with open("Clase 3/data/lista_sp500.txt", "w") as f:
        f.write(str(symbols))
except:
    URL = "https://es.wikipedia.org/wiki/Anexo:Compa%C3%B1%C3%ADas_del_S%26P_500"
    headers = {
        "User-Agent": "MiProyectoSP500/1.0"
    }

    # requests permite hacer peticiones http
    response = requests.get(URL, headers=headers)
    # Un código 200 representa una petición exitosa
    if response.status_code == 200:
        # open permite r/w archivos en el sistema
        with open("Clase 3/data/wiki.html", "w", encoding="utf-8") as f:
            f.write(response.text)
    else:
        print("Error al consultar la página")
        print(response.text)