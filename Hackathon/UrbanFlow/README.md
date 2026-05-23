https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

# 🚕 Salvando a "UrbanFlow AI"

## 🏢 La Startup

Ustedes acaban de ser contratados como el equipo de Ingeniería de Datos de **UrbanFlow AI**, una startup de *AdTech* (Tecnología Publicitaria). Nuestro modelo de negocio es vender espacios publicitarios dinámicos en pantallas digitales (billboards) distribuidas por toda la ciudad de Nueva York.

Para cobrar tarifas premium a marcas globales, prometemos publicidad basada en el flujo real y predictivo de la ciudad. Para predecir estos flujos con precisión, necesitamos entrenar nuestro modelo con **toda la historia de movilidad de Nueva York de los últimos dos años (2024 y 2025)**.

## 🚨 El Problema de Negocio

Hasta ahora, nuestro prototipo (el código base que se les entregó) funciona bien para procesar un solo mes de Taxis Amarillos.

**La crisis:**
Los ejecutivos han firmado una carta de intención con Coca-Cola, pero exigen ver los mapas de calor agregados y el análisis de flujo de **toda la ciudad usando todas las plataformas de transporte** (Yellow, Green y For-Hire Vehicles como Uber/Lyft) de 2024 y 2025.

Esto significa descargar, leer y procesar **72 archivos Parquet masivos** que en conjunto suman aproximadamente **600 millones de viajes**.
El código actual lee los datos cargándolos directamente a la memoria RAM. Si intentamos esto con el histórico completo, los servidores de la empresa explotan por *Out of Memory (OOM)*. Tenemos 3 horas y media para entregar los mapas de calor consolidados de estos dos años.

---

## 🎯 El Objetivo del Proyecto

Deberán reescribir y optimizar la tubería de datos (*Data Pipeline*) para que sea capaz de devorar años de historia sin colapsar, utilizando procesamiento paralelo y gestión inteligente de memoria.

**Requerimientos principales:**

1. **Escalabilidad Masiva:** Procesar los años 2024 y 2025 de los datasets `Yellow`, `Green`, y `High Volume FHV` (Uber/Lyft).
2. **Estandarización de Esquemas:** Los tres tipos de vehículos tienen nombres de columnas diferentes para las fechas y las zonas. Deberán limpiar y homologar los datos antes de procesarlos.
3. **Agrupación Global y Renderizado:** Generar mapas de calor (coropletas) que muestren el comportamiento promedio de la ciudad por hora, consolidando los 600 millones de viajes en un solo gran modelo visual.

**Restricción Tecnológica (Stack Libre):**
Tienen un código base que genera los mapas, pero son libres de cambiar la forma en que se leen y procesan los datos. Pueden usar procesamiento por lotes (*Chunking*), librerías de paralelismo (Multiprocessing), o *DataFrames* perezosos (*Lazy Evaluation*).

---

## 🛠️ Hints y Tips (¡LEAN ESTO!)

Trabajar con **600 millones de filas** cambiará su forma de programar para siempre. Aquí están las claves para sobrevivir:

### 1. El Asesino de RAM (Out of Memory)

`pd.read_parquet()` carga todo el archivo en la RAM. Un mes de Uber pesa más de 1 GB en disco, pero al descomprimirse en RAM puede ocupar 4 GB. Multipliquen eso por 24 meses y su computadora morirá.

* **Solución:** Investiguen cómo leer archivos Parquet por partes (filtrando solo las columnas que necesitan desde el disco) o usen herramientas diseñadas para datos más grandes que la memoria.

### 2. El Caos de los Esquemas (Data Cleaning)

No asuman que los datos son iguales.

* **Yellow Taxi:** Usa `tpep_pickup_datetime`
* **Green Taxi:** Usa `lpep_pickup_datetime`
* **Uber/Lyft (FHVHV):** Usa `pickup_datetime`
Su programa debe ser lo suficientemente inteligente para detectar qué archivo está leyendo y normalizar las columnas antes de intentar agruparlas.

### 3. Divide y Vencerás (Map-Reduce)

No intenten hacer un `groupby` de 600 millones de filas al mismo tiempo.

* **Estrategia:** Lean un archivo $\rightarrow$ Extraigan la hora $\rightarrow$ Cuenten los viajes por zona/hora (Reduciendo millones de filas a unas pocas cientos) $\rightarrow$ Guarden ese pequeño resumen $\rightarrow$ Liberen la memoria $\rightarrow$ Pasen al siguiente archivo. Al final, solo suman los resúmenes.

---

¡Buena suerte, y que sus pipelines de datos fluyan más rápido que el tráfico de Manhattan en hora pico!