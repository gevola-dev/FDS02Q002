from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.tree import DecisionTreeClassifier

ROOT = Path(__file__).resolve().parent.parent

# 1. Caricamento dati
df = pd.read_csv(ROOT / "datasets" / "Churn_yn_missing_data.csv")

# 2. Target e feature
#   - Churn: 'y'/'n' -> 1/0
df["Churn"] = df["Churn"].map({"y": 1, "n": 0})
df = df.dropna(subset=["Churn"])

y = df["Churn"]
X = df.drop(columns=["Churn"])

# 3. Gestione missing values nelle feature
#   - numeriche: median
#   - categoriche: valore più frequente
numeric_cols = X.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

# 4. Preprocessori
numeric_transformer = Pipeline(
    [("imputer", SimpleImputer(strategy="median"))]
)
categorical_transformer = Pipeline(
    [
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ]
)

preprocess = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_cols),
        ("cat", categorical_transformer, categorical_cols),
    ]
)

# 5. Modello Decision Tree
tree_clf = DecisionTreeClassifier(
    criterion="gini",      # in linea con Gini/Entropy delle slide
    max_depth=None,        # puoi limitare la profondità per evitare overfitting
    random_state=42
)

# 6. Pipeline completa: preprocessing + modello
clf = Pipeline(
    steps=[
        ("preprocess", preprocess),
        ("model", tree_clf),
    ]
)

# 7. Train/test split (70/30)
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.3,
    random_state=42,
    stratify=y  # mantiene proporzioni di classi
)

# 8. Training
clf.fit(X_train, y_train)

# 9. Valutazione: training error e test error (in forma di accuracy)
y_train_pred = clf.predict(X_train)
y_test_pred = clf.predict(X_test)

train_accuracy = accuracy_score(y_train, y_train_pred)
test_accuracy = accuracy_score(y_test, y_test_pred)

print(f"Training accuracy: {train_accuracy:.3f}")
print(f"Test accuracy:     {test_accuracy:.3f}")
print("\nClassification report (test):")
print(classification_report(y_test, y_test_pred))