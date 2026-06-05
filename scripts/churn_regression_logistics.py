from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parent.parent

# 1. Caricamento dati
df = pd.read_csv(ROOT / "datasets" / "Churn_yn_missing_data.csv")

# 2. Controlla le colonne disponibili
print(df.columns)

# 3. Imposta nome della colonna target (classe) e delle feature
#    Adatta il nome "Churn" al nome reale nel tuo CSV
target_col = "Churn"

# Se la classe è 'y'/'n' o 'yes'/'no', trasformiamola in 1/0
df[target_col] = df[target_col].map({
    'y': 1, 'n': 0,
    'Y': 1, 'N': 0,
    'yes': 1, 'no': 0,
    'Yes': 1, 'No': 0
})

# Opzionale: se alcune righe hanno classe mancante, toglile
df = df.dropna(subset=[target_col])

X = df.drop(columns=[target_col])
y = df[target_col]

# 4. Identifica colonne numeriche e categoriche
numeric_cols = X.select_dtypes(include=["number"]).columns.tolist()
categorical_cols = X.select_dtypes(include=["object", "bool"]).columns.tolist()

print("Numeric:", numeric_cols)
print("Categorical:", categorical_cols)

# 5. Preprocessing:
#    - numeriche: imputazione media
#    - categoriche: imputazione 'missing' + OneHotEncoder
numeric_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="mean"))
])

categorical_transformer = Pipeline(steps=[
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("onehot", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols)
    ]
)

# 6. Modello: Logistic Regression binaria
log_reg = LogisticRegression(max_iter=1000)

# 7. Costruisci la pipeline completa (preprocessing + modello)
clf = Pipeline(steps=[
    ("preprocess", preprocessor),
    ("model", log_reg)
])

# 8. Split train/test (es. 70%/30%)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y  # per mantenere la proporzione di classi
)

# 9. Addestramento
clf.fit(X_train, y_train)

# 10. Valutazione
y_pred = clf.predict(X_test)

print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification report:")
print(classification_report(y_test, y_pred))

# 11. Esempio di predizione su un singolo record (prendi una riga dal test set)
sample = X_test.iloc[[0]]
print("\nEsempio record:")
print(sample)

proba = clf.predict_proba(sample)
pred = clf.predict(sample)

print("\nProbabilità predette (P(Y=0), P(Y=1)):", proba)
print("Classe predetta:", pred)