https://www.kaggle.com/datasets/gallo33henrique/sentinel-2-satellite-imagery

# 🚀 Salvando a "GeoRisk AI"

## 🏢 La Startup

Ustedes acaban de ser contratados como el equipo de Ingeniería de Datos de **GeoRisk AI**, una startup *InsurTech* (tecnología de seguros) especializada en pólizas paramétricas contra desastres climáticos.

A diferencia de las aseguradoras tradicionales que envían peritos humanos a revisar un cultivo después de un desastre (lo cual toma meses y millones de dólares), GeoRisk AI paga automáticamente a los agricultores y municipios basándose en **datos satelitales casi en tiempo real**.

## 🚨 El Problema de Negocio

El modelo de negocio depende de procesar imágenes del satélite Sentinel-2 todos los días para monitorear el estado de las tierras aseguradas.

* **Si detectamos sequía extrema** (caída abrupta del NDVI/EVI), pagamos al agricultor.
* **Si detectamos inundaciones** (picos masivos de NDWI en zonas donde no había agua), pagamos a las comunidades.
* **Si detectamos incendios forestales** (picos en el NBR), liberamos fondos de emergencia.
* **Si detectamos expansión urbana no declarada** (crecimiento del NDBI sobre zonas agrícolas), ajustamos las primas de riesgo.

**La crisis:**
Nuestro prototipo en Python secuencial funcionaba perfecto cuando solo teníamos 100 clientes. Pero acabamos de cerrar un contrato para monitorear toda Europa (representado por las 27,000 imágenes del dataset de hoy).

Nuestro servidor actual **tarda 14 horas en procesar un solo día de imágenes**. Esto es inaceptable: para cuando terminamos de calcular el riesgo, el mercado ya cerró y nuestros clientes exigen alertas tempranas. Los inversores de la Ronda A amenazan con retirar los fondos si no podemos escalar la plataforma.

---

## 🎯 El Objetivo del Proyecto

Deberán procesar **todas las imágenes `.tif**` del dataset proporcionado y extraer información vital calculando Índices Espectrales.

**Requerimientos principales:**

1. **Calcular al menos 3 Índices Espectrales** (a elegir de la lista provista abajo) por cada imagen.
2. **Procesamiento Paralelo Total:** Su solución debe paralelizar tanto la lectura de los archivos desde el disco (I/O) como el cálculo matemático de los píxeles (CPU).
3. **Guardar los resultados:** Por cada imagen original, deben generar y guardar el resultado de los índices calculados (pueden ser como nuevas matrices, imágenes en blanco y negro, o combinarlos en una imagen RGB de "falso color").

**Restricción Tecnológica (Stack Libre):**
Tienen un código base de arranque, pero son libres de usar la arquitectura paralela que prefieran (Hilos, Procesos, Compilación JIT). **La única regla estricta es:** No pueden usar funciones de alto nivel que calculen estos índices por ustedes. Las matemáticas píxel por píxel deben ser programadas y optimizadas por su equipo.

---

## 🧮 Los Índices Espectrales (Elijan al menos 3)

Las fórmulas matemáticas operan sobre bandas específicas del satélite Sentinel-2.

* **Banda 2:** Azul (Blue)
* **Banda 3:** Verde (Green)
* **Banda 4:** Rojo (Red)
* **Banda 8:** Infrarrojo Cercano (NIR)
* **Banda 11:** Infrarrojo de Onda Corta 1 (SWIR 1)
* **Banda 12:** Infrarrojo de Onda Corta 2 (SWIR 2)

### 1. NDVI (Índice de Diferencia Normalizada de Vegetación)

Detecta la salud y densidad de la flora. Valores altos indican vegetación densa.


$$NDVI = \frac{NIR - Red}{NIR + Red}$$

### 2. NDWI (Índice de Diferencia Normalizada de Agua)

Resalta los cuerpos de agua suprimiendo el suelo y la vegetación.


$$NDWI = \frac{Green - NIR}{Green + NIR}$$

### 3. NDBI (Índice de Diferencia Normalizada de Áreas Construidas)

Diferencia el asfalto y el concreto (ciudades/carreteras) de los entornos naturales.


$$NDBI = \frac{SWIR1 - NIR}{SWIR1 + NIR}$$

### 4. NBR (Índice de Área Quemada Normalizada)

Usado para detectar cicatrices de incendios forestales y estimar la severidad del fuego.


$$NBR = \frac{NIR - SWIR2}{NIR + SWIR2}$$

### 5. EVI (Índice de Vegetación Mejorado)

Una versión avanzada del NDVI que corrige las distorsiones atmosféricas.


$$EVI = 2.5 \times \frac{NIR - Red}{NIR + 6 \times Red - 7.5 \times Blue + 1}$$

---

## 🛠️ Hints y Tips (¡LEAN ESTO!)

Trabajar con datos científicos crudos tiene trampas que destruirán su programa si no tienen cuidado. Aquí están las claves para manipular las bandas correctamente:

### 1. El Factor de Escala (La trampa de los 16 bits)

Los píxeles en los archivos `.tif` de Sentinel-2 **no van de 0 a 255**. Son enteros sin signo de 16 bits (`uint16`) que representan reflectancia multiplicada por 10,000.

* **La Regla:** Antes de aplicar cualquier fórmula matemática, **DEBEN dividir el valor del píxel entre 10,000.0** para convertirlo a un porcentaje real de reflectancia (de `0.0` a `1.0`).

### 2. Peligro de Underflow y Overflow

Si restan píxeles manteniendo el tipo de dato `uint16` (ejemplo: `2000 - 3000`), el resultado no será negativo, dará la vuelta a `64536`.

* **Solución:** Conviertan sus datos a valores de coma flotante (`float`) **durante** el cálculo.

### 3. División por Cero

El espacio es oscuro y los bordes de los satélites también. Habrá píxeles con valor `0` absoluto. Si su denominador en la fórmula `(Ej: NIR + Red)` da cero, su programa arrojará errores `NaN` (Not a Number) o colapsará.

* **Solución:** Incluyan validaciones dentro de su lógica iterativa para asignar `0.0` si el denominador es `0`.

### 4. Recorte de anomalías (Clipping)

Ocasionalmente, reflejos muy fuertes (techos metálicos, nubes) causarán que el valor crudo exceda los 10,000 (reflectancia > 1.0). Si es necesario, recorten los valores para que el máximo sea `1.0`.

---

¡Buena suerte, y que sus núcleos de procesamiento estén al 100%!