import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 1. Configuración de rutas
RUTA_DATOS_WEB = "data/csic_database.csv" 
RUTA_MODELO_WAF = "brain/waf_model.pkl"

def cargar_y_limpiar_datos(ruta):
    print("[*] Cargando dataset CSIC 2010 para el WAF (Solo columnas útiles)...")
    columnas_deseadas = ['URL', 'content', 'classification']
    
    try:
        df = pd.read_csv(ruta, usecols=columnas_deseadas)
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo en {ruta}. Asegúrate de haberlo descargado en la carpeta data.")

    print(f"[*] Datos cargados: {df.shape[0]} filas totales.")
    
    # 🔍 MODO DETECTIVE: Ver qué palabras exactas usa el CSV
    valores_unicos = df['classification'].unique()
    print(f"[*] Etiquetas reales encontradas en tu archivo: {valores_unicos}")
    
    # --- LIMPIEZA CRÍTICA PARA EL WAF ---
    print("[*] Limpiando datos y extrayendo payloads...")
    
    df['URL'] = df['URL'].fillna('')
    df['content'] = df['content'].fillna('')
    
    X = df['URL'] + " " + df['content']
    
    # Traducción a prueba de balas: Detecta si dice 'anomalous', o si ya es un '1'
    y = df['classification'].apply(lambda x: 1 if str(x).strip().lower() in ['anomalous', '1', '1.0'] else 0)
    
    # 🛡️ Control de seguridad antes de entrenar
    total_normales = sum(y == 0)
    total_ataques = sum(y == 1)
    print(f"[*] Balance tras la limpieza: {total_normales} Normales | {total_ataques} Ataques Web")
    
    if total_ataques == 0:
        raise ValueError("¡ALERTA! No se ha detectado ningún ataque en los datos. Revisa la columna 'classification'.")
        
    return X, y

def entrenar_waf():
    # 2. Cargar datos
    X, y = cargar_y_limpiar_datos(RUTA_DATOS_WEB)
    
    print("[*] Dividiendo datos para entrenamiento y prueba (80% - 20%)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 3. Configurar el "Cerebro" (Pipeline: TF-IDF + Random Forest)
    # n_estimators=100 para igualar la precisión del modelo de red.
    # n_jobs=-1 usa todos los núcleos de tu procesador.
    print("[*] Entrenando el modelo WAF (Esto puede tardar unos minutos)...")
    modelo_waf = Pipeline([
        ('vectorizador', TfidfVectorizer(max_features=5000, analyzer='char_wb', ngram_range=(1, 4))),
        ('clasificador', RandomForestClassifier(n_estimators=100, class_weight='balanced', n_jobs=-1, random_state=42))
    ])
    
    modelo_waf.fit(X_train, y_train)
    
    # 4. Evaluar el rendimiento del modelo
    print("\n[*] Entrenamiento completado. Evaluando precisión con datos desconocidos:")
    predicciones = modelo_waf.predict(X_test)
    target_names = ['Normal (0)', 'Ataque Web (1)']
    print(classification_report(y_test, predicciones, target_names=target_names))
    
    # 5. Guardar el modelo en disco
    print(f"\n[*] Guardando el cerebro entrenado en: {RUTA_MODELO_WAF}")
    joblib.dump(modelo_waf, RUTA_MODELO_WAF)
    print("[+] ¡Proceso completado con éxito! Tienes tu modelo WAF listo para defender.")

# Arrancar el script
if __name__ == "__main__":
    entrenar_waf()