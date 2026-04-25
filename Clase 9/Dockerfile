# Imagen base ligera de Python
FROM python:3.11-slim

# Variables de entorno
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema (opcional pero útil)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

# Copiar archivo de requerimientos primero (mejora cache)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Exponer el puerto
EXPOSE 8000

# Comando para correr la app
# Cambia "main:app" si tu archivo o variable se llaman distinto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]