import os
import time
import urllib.request
import zipfile
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.colors import LogNorm

# ==========================================
# 1. DESCARGA DEL SHAPEFILE DE ZONAS
# ==========================================
def obtener_shapefile_zonas():
    os.makedirs('taxi_zones', exist_ok=True)
    shapefile_path = 'taxi_zones/taxi_zones.shp'
    
    if not os.path.exists(shapefile_path):
        print("📥 Descargando Shapefile de zonas de Nueva York...")
        url = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip"
        zip_path = "taxi_zones/taxi_zones.zip"
        urllib.request.urlretrieve(url, zip_path)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall('./')
        print("✅ Zonas descargadas y extraídas.")
    
    # Cargamos el shapefile con geopandas
    gdf_zonas = gpd.read_file(shapefile_path)
    # Convertimos al sistema de coordenadas compatible con mapas web (Mercator)
    gdf_zonas = gdf_zonas.to_crs(epsg=3857)
    return gdf_zonas

# ==========================================
# 2. RENDERIZADO DEL MAPA DE COROPLETAS
# ==========================================
def guardar_mapa_coropleta(gdf_hora, hora, vmax):
    fig, ax = plt.subplots(figsize=(12, 12), dpi=120)
    
    # Dibujamos las zonas de taxi coloreadas por la columna 'trip_count'
    # missing_kwds hace que las zonas sin viajes sean transparentes o negras
    gdf_hora.plot(
        column='trip_count',
        ax=ax,
        cmap=plt.cm.hot,
        norm=LogNorm(vmin=1, vmax=vmax),
        alpha=0.8,
        edgecolor='black', # Bordes
        linewidth=0.3,
        missing_kwds={'color': 'none'} # Zonas con 0 viajes no se colorean
    )
    
    # Añadimos el mapa
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.DarkMatter, crs=gdf_hora.crs.to_string(), attribution=False)
    
    # Ajustamos el encuadre a la ciudad de Nueva York
    ax.set_xlim(-8250000, -8210000)
    ax.set_ylim(4960000, 4995000)
    ax.axis('off')
    
    # Título para saber qué hora estamos viendo
    plt.text(0.05, 0.95, f'Hora: {hora:02d}:00', transform=ax.transAxes, 
             fontsize=24, color='white', fontweight='bold', 
             bbox=dict(facecolor='black', alpha=0.5, edgecolor='none'))
    
    nombre_archivo = f"output/zonas_hora_{hora:02d}.png"
    plt.savefig(nombre_archivo, bbox_inches='tight', pad_inches=0, facecolor='black')
    plt.close(fig)
    print(f"Guardado mapa de zonas: {nombre_archivo}")

# ==========================================
# 3. PROCESAMIENTO PRINCIPAL
# ==========================================
if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    start_total = time.time()
    
    # 1. CARGA DE DATOS
    print("Cargando dataset de viajes...")
    df = pd.read_parquet("data/yellow_tripdata_2026-01.parquet")
    #df = pd.read_parquet("data/fhvhv_tripdata_2026-01.parquet-01.parquet")
    

    # 2. EXTRACCIÓN DE LA HORA
    print("Procesando fechas...")
    df['hour'] = df['tpep_pickup_datetime'].dt.hour
    
    # 3. AGRUPACIÓN POR HORA Y ZONA
    print("Contando viajes por zona y hora...")
    conteo_viajes = df.groupby(['hour', 'PULocationID']).size().reset_index(name='trip_count')
    
    # 4. CARGA DEL SHAPEFILE
    gdf_zonas = obtener_shapefile_zonas()
    
    # Calculamos un vmax global para que la escala de colores sea consistente en las 24 horas
    vmax_global = conteo_viajes['trip_count'].quantile(0.99)
    if vmax_global < 2: vmax_global = 10
    
    print("Generando mapas de calor por zonas...")
    start_render = time.time()
    
    # 5. RENDERIZADO ITERATIVO
    for hora in range(24):
        # Filtramos los datos de esa hora
        datos_hora = conteo_viajes[conteo_viajes['hour'] == hora]
        
        # Hacemos un "JOIN" entre los polígonos del mapa y nuestros conteos
        # (LocationID es la columna en el shapefile de Nueva York que equivale a PULocationID)
        gdf_hora = gdf_zonas.merge(datos_hora, left_on='LocationID', right_on='PULocationID', how='left')
        
        # Renderizamos a PNG
        guardar_mapa_coropleta(gdf_hora, hora, vmax_global)
        
    print(f"Tiempo de renderizado: {time.time() - start_render:.2f} segundos")
    print(f"⏱️ TIEMPO TOTAL: {time.time() - start_total:.2f} segundos")