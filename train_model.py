# train_model.py

import pandas as pd
import joblib
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

print("--- Iniciando script de treinamento do modelo ---")

# --- Configuração de Caminhos ---
DATA_PATH = Path("data/kepler_data.csv")
MODEL_DIR = Path("saved_model")
MODEL_PATH = MODEL_DIR / "model.joblib"
MODEL_DIR.mkdir(exist_ok=True) # Cria a pasta saved_model se não existir

# --- Carregamento e Limpeza ---
print(f"Carregando dataset de {DATA_PATH}...")
df = pd.read_csv(DATA_PATH, comment="#")
df.columns = df.columns.str.strip()

print("Limpando dados... Removendo colunas com mais de 40% de valores ausentes.")
# Primeiro, remova colunas que são muito vazias
limiar_na = 0.4
missing_ratio = df.isna().mean()
cols_validas = missing_ratio[missing_ratio < limiar_na].index
df = df[cols_validas].copy()

# Agora, remova as poucas linhas restantes que ainda têm valores ausentes
print("Removendo linhas com valores ausentes restantes...")
df.dropna(inplace=True)

print(f"Dataset limpo! Formato final: {df.shape}")

# --- Preparação dos Dados ---
print("Preparando dados para treinamento...")
X = df.select_dtypes(include='number')
y = df['koi_disposition']
TRAINING_COLUMNS = X.columns.tolist()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# --- Criação e Treinamento do Pipeline ---
print("Treinando o modelo RandomForestClassifier...")
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)

# --- Avaliação ---
accuracy = pipeline.score(X_test, y_test)
print(f"Acurácia do modelo no conjunto de teste: {accuracy:.4f}")

# --- Salvando o Modelo e as Colunas ---
print(f"Salvando o pipeline treinado em {MODEL_PATH}...")
joblib.dump({"model": pipeline, "columns": TRAINING_COLUMNS}, MODEL_PATH)

print("--- Script de treinamento concluído com sucesso! ---")