# main.py

import joblib
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

# 1. CONFIGURAÇÃO DA API E CORS
app = FastAPI(title="API de Classificador de Exoplanetas")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

# 2. CARREGAMENTO DO MODELO E DEFINIÇÕES GLOBAIS
MODEL_PATH = Path("saved_model/model.joblib")
model_data = None

@app.on_event("startup")
def load_model():
    global model_data
    model_data = joblib.load(MODEL_PATH)
    print("Modelo e colunas carregados com sucesso.")

# 3. MODELO DE DADOS PYDANTIC (COM CAMPOS OPCIONAIS)
class KeplerFeatures(BaseModel):
    koi_fpflag_nt: Optional[float] = None
    koi_fpflag_ss: Optional[float] = None
    koi_fpflag_co: Optional[float] = None
    koi_fpflag_ec: Optional[float] = None
    koi_period: Optional[float] = None
    koi_duration: Optional[float] = None
    koi_depth: Optional[float] = None
    koi_prad: Optional[float] = None
    koi_teq: Optional[float] = None
    koi_model_snr: Optional[float] = None

# 4. ENDPOINT DE PREDIÇÃO
@app.post("/predict")
def predict(features: KeplerFeatures):
    if not model_data:
        raise HTTPException(status_code=503, detail="Modelo não está carregado.")
    try:
        pipeline = model_data["model"]
        columns = model_data["columns"]
        
        # Lógica para garantir todas as features, preenchendo as ausentes com 0
        data_for_model = {col: 0.0 for col in columns}
        received_data = {k: v for k, v in features.dict().items() if v is not None}
        data_for_model.update(received_data)
        
        input_df = pd.DataFrame([data_for_model])[columns]
        
        prediction = pipeline.predict(input_df)[0]
        probabilities = pipeline.predict_proba(input_df)[0]
        class_probabilities = {str(cls): float(prob) for cls, prob in zip(pipeline.classes_, probabilities)}

        return {"predicted_class": str(prediction), "probabilities": class_probabilities}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a predição: {str(e)}")