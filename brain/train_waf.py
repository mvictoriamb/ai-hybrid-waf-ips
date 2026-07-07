import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import joblib

# 1. Configuración
# Asumimos columnas 'texto' y 'etiqueta'
RUTA_DATOS_WEB = "../data/DATOS_POR_BUSCAR.csv" 
RUTA_MODELO_WAF = "waf_model.pkl"

def entrenar_waf():
    print("[*] Cargando dataset de texto para el WAF...")
    # Asegúrate de poner los nombres de columnas correctos según el CSV que descargues
    df = pd.read_csv(RUTA_DATOS_WEB)
    
    # Limpieza básica
    df.dropna(inplace=True)
    X = df['texto']     # La columna con los comandos SQL o XSS
    y = df['etiqueta']  # 1 (Ataque) o 0 (Normal)

    print("[*] Dividiendo datos (80% - 20%)...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # 2. La Magia del Texto (Pipeline)
    # TfidfVectorizer convierte el texto en números.
    # RandomForest aprende de esos números.
    print("[*] Creando y entrenando el modelo NLP para el WAF...")
    modelo_waf = Pipeline([
        ('vectorizador', TfidfVectorizer(max_features=5000, analyzer='char_wb', ngram_range=(1, 4))),
        ('clasificador', RandomForestClassifier(n_estimators=50, class_weight='balanced', n_jobs=-1))
    ])

    modelo_waf.fit(X_train, y_train)

    # 3. Evaluación
    print("\n[*] Evaluando el cerebro WAF:")
    predicciones = modelo_waf.predict(X_test)
    print(classification_report(y_test, predicciones))

    # 4. Guardar
    joblib.dump(modelo_waf, RUTA_MODELO_WAF)
    print(f"[+] ¡Cerebro WAF guardado en {RUTA_MODELO_WAF}!")

if __name__ == "__main__":
    entrenar_waf()