import os
import glob
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 1. Configuración de rutas
RUTA_DATOS = "data/CIC-IDS2017/*.csv" 
RUTA_MODELO = "brain/web_network_model.pkl"

def cargar_y_limpiar_datos(ruta):
    archivos_csv = glob.glob(ruta)
    
    if not archivos_csv:
        raise FileNotFoundError("No se encontraron archivos CSV en la carpeta data.")

    print(f"[*] Se encontraron {len(archivos_csv)} archivos. Cargando...")
    
    # Leer y concatenar todos los CSV en un solo DataFrame gigante
    lista_dataframes = [pd.read_csv(archivo) for archivo in archivos_csv]
    df_completo = pd.concat(lista_dataframes, ignore_index=True)
    
    print(f"[*] Datos cargados: {df_completo.shape[0]} filas totales.")
    
    # --- LIMPIEZA CRÍTICA PARA CIC-IDS2017 ---
    print("[*] Limpiando datos...")
    
    # Quitar espacios en blanco de los nombres de las columnas
    df_completo.columns = df_completo.columns.str.strip()
    
    # Reemplazar valores infinitos por NaN y luego borrar todas las filas con NaN
    df_completo.replace([np.inf, -np.inf], np.nan, inplace=True)
    df_completo.dropna(inplace=True)
    
    df_completo = df_completo[~df_completo['Label'].str.contains('Web Attack', case=False, na=False)]
    
    # Separar las características (X) de la etiqueta/respuesta (y)
    y = df_completo['Label']
    
    # Para evitar errores con IPs o Fechas, nos quedamos SOLO con las columnas matemáticas (numéricas)
    X = df_completo.select_dtypes(include=[np.number])
    
    return X, y

def entrenar_modelo():
    # 2. Cargar datos
    X, y = cargar_y_limpiar_datos(RUTA_DATOS)
    
    print("[*] Dividiendo datos para entrenamiento y prueba (80% - 20%)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Configurar el "Cerebro" (Random Forest)
    # Para más precisión, 100 n_estimators.
    # n_jobs=-1 usa todos los núcleos de tu procesador.
    print("[*] Entrenando el modelo Random Forest (Esto puede tardar unos minutos)...")
    modelo = RandomForestClassifier(n_estimators=100, class_weight='balanced', n_jobs=-1, random_state=42)
    
    modelo.fit(X_train, y_train)
    
    # 4. Evaluar el rendimiento del modelo
    print("\n[*] Entrenamiento completado. Evaluando precisión con datos desconocidos:")
    predicciones = modelo.predict(X_test)
    print(classification_report(y_test, predicciones))
    
    # 5. Guardar el modelo en disco
    print(f"\n[*] Guardando el cerebro entrenado en: {RUTA_MODELO}")
    joblib.dump(modelo, RUTA_MODELO)
    print("[+] ¡Proceso completado con éxito! Tienes tu modelo listo para defender.")

# Arrancar el script
if __name__ == "__main__":
    entrenar_modelo()