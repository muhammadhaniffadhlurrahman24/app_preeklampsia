import os
import numpy as np
import pandas as pd

from sklearn.model_selection import StratifiedKFold, cross_validate, cross_val_predict
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

import joblib

# =======================
# 1. KONFIGURASI
# =======================

CSV_PATH = "ALL_FINAL.csv"   # nama file dataset kamu
TARGET_COL = "Label"
N_SPLITS = 10                   # 10-fold CV

# =======================
# 2. LOAD & BERSIHKAN DATA
# =======================

# separator ; karena CSV-mu pakai ;
# decimal="." karena angka pakai titik
df = pd.read_csv(CSV_PATH, sep=";", decimal=".")

# bersihkan spasi di awal/akhir nama kolom (jaga-jaga)
df.columns = df.columns.str.strip()

print("Kolom di CSV:")
print(df.columns.tolist())
print()

if TARGET_COL not in df.columns:
    raise ValueError(f"Kolom target '{TARGET_COL}' tidak ditemukan di CSV.")

X = df.drop(columns=[TARGET_COL])
y = df[TARGET_COL]

# opsional tapi bagus: bersihkan spasi di nilai string (SMP , dll)
for col in X.select_dtypes(include=["object"]).columns:
    X[col] = X[col].astype(str).str.strip()

print(f"Jumlah baris (total data): {df.shape[0]}")
print(f"Jumlah kolom fitur      : {X.shape[1]}")
print("\nDistribusi kelas:")
print(y.value_counts())
print()

# =======================
# 3. DEFINISI FITUR
# =======================

numeric_features_all = [
    "Umur (Tahun)",
    "Pernikahan Ke",
    "BB Sebelum Hamil (Kg)",
    "TB (Cm)",
    "Indeks Massa Tubuh (IMT)",
    "Lingkar Lengan Atas (Cm)",
    "TD Sistolik I",
    "TD Diastolik I",
    "MAP (mmHg)",
    "Hb (gr/dl)",
]

categorical_features_all = [
    "Kabupaten/Kota",
    "Pendidikan",
    "Pekerjaan",
    "Status Nikah",
    "Paritas",
    "Hamil Pasangan Baru",
    "Jarak Anak >10 tahun",
    "Bayi Tabung",
    "Gemelli",
    "Perokok",
    "Hamil Direncanakan",
    "Riwayat Keluarga Preeklampsia",
    "Riwayat Preeklampsia",
    "Hipertensi Kronis",
    "Diabetes Melitus",
    "Riwayat Penyakit Ginjal",
    "Penyakit Autoimune",
    "APS",
    "Hipertensi Keluarga",
    "Riwayat Penyakit Ginjal Keluarga",
    "Riwayat Penyakit Jantung Keluarga",
]

numeric_features = [c for c in numeric_features_all if c in X.columns]
categorical_features = [c for c in categorical_features_all if c in X.columns]

missing_num = [c for c in numeric_features_all if c not in X.columns]
missing_cat = [c for c in categorical_features_all if c not in X.columns]

if missing_num or missing_cat:
    print("PERINGATAN: Ada kolom yang tidak ditemukan di CSV:")
    if missing_num:
        print("  - Numeric hilang   :", missing_num)
    if missing_cat:
        print("  - Categorical hilang:", missing_cat)
    print()

print("Fitur numerik yang dipakai   :", numeric_features)
print("Fitur kategorikal yang dipakai:", categorical_features)
print()

# =======================
# 4. PREPROCESSOR & MODEL
# =======================

numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="median")),
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore")),
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
    ]
)

rf_clf = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
)

model = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("clf", rf_clf),
])

# =======================
# 5. 10-FOLD STRATIFIED CV
# =======================

cv = StratifiedKFold(
    n_splits=N_SPLITS,
    shuffle=True,
    random_state=42,
)

scoring = {
    "accuracy": "accuracy",
    "precision_macro": "precision_macro",
    "recall_macro": "recall_macro",
    "f1_macro": "f1_macro",
}

print(f"=== {N_SPLITS}-fold Stratified Cross Validation ===\n")

cv_results = cross_validate(
    model,
    X,
    y,
    cv=cv,
    scoring=scoring,
    return_train_score=False,
)

print("Accuracy per fold       :", cv_results["test_accuracy"])
print("Mean accuracy           :", cv_results["test_accuracy"].mean())
print("Std accuracy            :", cv_results["test_accuracy"].std())
print()

print("Mean precision (macro)  :", cv_results["test_precision_macro"].mean())
print("Mean recall (macro)     :", cv_results["test_recall_macro"].mean())
print("Mean F1-score (macro)   :", cv_results["test_f1_macro"].mean())
print()

# =======================
# 6. CONFUSION MATRIX dari CV
# =======================

print("=== Confusion Matrix (gabungan semua fold) ===")

y_pred_cv = cross_val_predict(model, X, y, cv=cv)

labels = sorted(y.unique())  # ['NonPreeklampsia', 'Preeklampsia']
cm = confusion_matrix(y, y_pred_cv, labels=labels)

print("Labels (urutan baris/kolom):", labels)
print(cm)
print()

print("=== Classification Report (berdasarkan prediksi CV) ===")
print(classification_report(y, y_pred_cv, labels=labels))

# =======================
# 7. TRAIN FINAL MODEL DI SELURUH DATA
# =======================

print("\n=== Train model final di seluruh data ===")
model.fit(X, y)
print("Selesai train model final.\n")

# =======================
# 8. SIMPAN MODEL
# =======================

os.makedirs("ml_models", exist_ok=True)
MODEL_PATH = os.path.join("rf_preeclampsia.joblib")
joblib.dump(model, MODEL_PATH)
print(f"Model disimpan ke: {MODEL_PATH}")