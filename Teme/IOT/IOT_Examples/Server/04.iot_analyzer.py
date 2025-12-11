import pandas as pd
import numpy as np
import sqlite3
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import warnings

warnings.filterwarnings('ignore') # Ascunde avertismentele Scikit-learn

DB_FILE = "iot_data.db"
TABLE_NAME = "senzori_temperatura"

def load_data():
    """Încarcă datele din baza de date SQLite în Pandas DataFrame."""
    try:
        conn = sqlite3.connect(DB_FILE)
        df = pd.read_sql(f"SELECT * FROM {TABLE_NAME}", conn)
        conn.close()
        
        # Pregătirea datelor (obligatoriu)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['temperatura'] = pd.to_numeric(df['temperatura'])
        df = df.set_index('timestamp').sort_index()
        
        if df.empty:
            print("Eroare: Baza de date nu conține date.")
            return None
        return df
    except Exception as e:
        print(f"Eroare la încărcarea datelor: {e}")
        return None

def descriptive_analytics(df):
    ## 1. ANALIZA DESCRIPTIVĂ (Ce s-a întâmplat?)
    print("\n" + "="*70)
    print("1. ANALIZA DESCRIPTIVĂ (TENDINȚE ȘI STATISTICI)")
    print("="*70)
    
    print(f"Număr total de citiri: {len(df)}")
    print("\nStatistici Sumare:\n", df['temperatura'].describe().to_string())
    print(f"\nTemperatura medie pe oră: {df['temperatura'].resample('H').mean().mean():.2f} °C")


def diagnostic_analytics(df):
    ## 2. ANALIZA DIAGNOSTICĂ (De ce s-a întâmplat?)
    print("\n" + "="*70)
    print("2. ANALIZA DIAGNOSTICĂ (IDENTIFICARE ANOMALII)")
    print("="*70)
    
    # Calcularea IQR (Intervalul Intercuartilic) pentru a detecta valori aberante (outliers)
    Q1 = df['temperatura'].quantile(0.25)
    Q3 = df['temperatura'].quantile(0.75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    anomalies = df[(df['temperatura'] < lower_bound) | (df['temperatura'] > upper_bound)]
    
    if not anomalies.empty:
        print(f"Au fost detectate {len(anomalies)} citiri anormale (Outliers):")
        print(anomalies)
        print(f"\nMotiv posibil: Schimbări bruște (> {1.5 * IQR:.2f}°C) indică o posibilă defecțiune a senzorului sau intervenție externă (ex: deschiderea unei uși/ferestre).")
    else:
        print("Nu au fost detectate anomalii majore bazate pe IQR.")


def predictive_analytics(df):
    ## 3. ANALIZA PREDICTIVĂ (Ce se va întâmpla?)
    print("\n" + "="*70)
    print("3. ANALIZA PREDICTIVĂ (PREZICEREA TEMPERATURII)")
    print("="*70)
    
    if len(df) < 5:
        print("Necesită mai multe date pentru a antrena un model predictiv.")
        return

    # Feature Engineering (Lagging)
    df['T_minus_1'] = df['temperatura'].shift(1)
    df.dropna(inplace=True)

    X = df[['T_minus_1']] # Caracteristica: Temperatura în pasul anterior
    y = df['temperatura'] # Ținta: Temperatura curentă

    # Împărțirea (Train/Test) - shuffle=False pentru serii temporale
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    # Model: Regresie Liniară
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Prezicere și Evaluare
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    print(f"Model antrenat pentru a prezice temperatura viitoare (pe baza celei anterioare).")
    print(f"Acuratețe (R² Score): {r2:.4f}")
    print(f"Eroare Medie Absolută (MAE): {mae:.2f} °C")

    # Demonstrarea unei predicții viitoare (pe ultimul punct de date disponibil)
    last_temp = df['temperatura'].iloc[-1]
    next_temp_prediction = model.predict(np.array([[last_temp]]))[0]
    print(f"\nPe baza ultimei citiri de {last_temp:.2f}°C, predicția pentru următoarea citire este: {next_temp_prediction:.2f}°C")


def prescriptive_analytics(df):
    ## 4. ANALIZA PRESCRIPTIVĂ (Ce ar trebui să facem?)
    print("\n" + "="*70)
    print("4. ANALIZA PRESCRIPTIVĂ (RECOMANDĂRI AUTOMATE)")
    print("="*70)
    
    # Simulează logică de control/recomandare bazată pe reguli:
    current_temp = df['temperatura'].iloc[-1]
    
    TEMP_OPTIMA = 24.0
    PRAG_MAX = 25.5
    PRAG_MIN = 22.0
    
    if current_temp > PRAG_MAX:
        # Recomandare bazată pe logică
        recomandare = f"Temperatura ({current_temp:.2f}°C) depășește pragul maxim ({PRAG_MAX}°C). Acționează: Pornește sistemul de răcire sau ajustează termostatul."
        risc = "RIDICAT"
    elif current_temp < PRAG_MIN:
        recomandare = f"Temperatura ({current_temp:.2f}°C) este sub pragul minim ({PRAG_MIN}°C). Acționează: Pornește sistemul de încălzire."
        risc = "MODERAT"
    else:
        recomandare = f"Temperatura ({current_temp:.2f}°C) se încadrează în intervalul optim ({PRAG_MIN}°C - {PRAG_MAX}°C). Nu este necesară intervenția."
        risc = "SCĂZUT"
        
    print(f"Temperatura Curentă: {current_temp:.2f}°C")
    print(f"Nivel de Risc: {risc}")
    print(f"RECOMANDARE: {recomandare}")


# --- Rulare Principală ---
if __name__ == "__main__":
    data_frame = load_data()
    
    if data_frame is not None:
        descriptive_analytics(data_frame)
        diagnostic_analytics(data_frame)
        predictive_analytics(data_frame)
        prescriptive_analytics(data_frame)