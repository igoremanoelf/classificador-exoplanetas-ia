
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import numpy as np

def train_advanced_exoplanet_model():
    """
    Enhanced function to train a high-performance model.
    Uses more features, a Gradient Boosting model, and data scaling.
    """
    print("Starting the advanced training process...")

    # 1. Load Data
    url = "https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table=cumulative&select=*&format=csv"
    try:
        df = pd.read_csv(url)
        print("KOI data downloaded successfully.")
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    # 2. Feature Engineering and Preprocessing
    features = [
        'koi_period',
        'koi_duration',
        'koi_depth',
        'koi_prad',
        'koi_teq',
        'koi_insol',
        'koi_steff',
        'koi_slogg',
        'koi_srad',
        'koi_impact',
        'koi_model_snr', # Correct column name for Signal-to-Noise Ratio
        'koi_fpflag_nt',
        'koi_fpflag_ss',
        'koi_fpflag_co',
        'koi_fpflag_ec',
    ]
    target = 'koi_disposition'
    
    df_filtered = df[features + [target]]
    
    df_clean = df_filtered.dropna()
    df_clean = df_clean[df_clean[target].isin(['CONFIRMED', 'CANDIDATE', 'FALSE POSITIVE'])]
    print(f"Dataset reduced to {df_clean.shape[0]} samples after cleaning.")

    le = LabelEncoder()
    df_clean['target_encoded'] = le.fit_transform(df_clean[target])
    class_names = le.classes_
    print(f"Encoded classes: {list(zip(le.transform(class_names), class_names))}")

    X = df_clean[features]
    y = df_clean['target_encoded']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    print(f"Data split into {len(X_train)} for training and {len(X_test)} for testing.")

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("Features standardized with StandardScaler.")

    print("Training the GradientBoostingClassifier model...")
    model = GradientBoostingClassifier(n_estimators=200, learning_rate=0.1, max_depth=5, random_state=42)
    model.fit(X_train_scaled, y_train)
    print("Training complete.")

    y_pred = model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nFINAL MODEL ACCURACY: {accuracy:.4f}")
    print("\nFinal Classification Report:")
    print(classification_report(y_test, y_pred, target_names=class_names))

    joblib.dump(model, 'exoplanet_model.pkl')
    joblib.dump(le, 'label_encoder.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(features, 'model_features.pkl')
    print("\nModel, Label Encoder, Scaler, and feature list saved successfully!")

if __name__ == '__main__':
    train_advanced_exoplanet_model()
