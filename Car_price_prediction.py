import pandas as pd
import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from pathlib import Path
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score

# 1. Load data
df = pd.read_csv(Path.home() / "Downloads" / "Car details v3.csv")

# 2. Prepare data
df["brand"] = df["name"].str.split().str[0]
df["model"] = df["name"].str.split(n=1).str[1]
df["mileage"] = pd.to_numeric(
    df["mileage"].astype(str).str.extract(r"(\d+\.?\d*)")[0],
    errors="coerce"
)

features = [
    "brand", "model", "fuel", "transmission", "owner",
    "year", "km_driven", "mileage"
]

df = df.dropna(subset=features + ["selling_price"])
df = df.drop_duplicates()
df = df[df["selling_price"] > 0]

X = df[features]
y = df["selling_price"]

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Preprocessing
categorical = ["brand", "model", "fuel", "transmission", "owner"]
numeric = ["year", "km_driven", "mileage"]

preprocessing = ColumnTransformer([
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
    ("num", "passthrough", numeric)
])

# 5. Model + hyperparameter tuning
pipeline = Pipeline([
    ("prep", preprocessing),
    ("rf", RandomForestRegressor(random_state=42, n_jobs=-1))
])

search = RandomizedSearchCV(
    pipeline,
    {
        "rf__n_estimators": [100, 150, 200],
        "rf__max_depth": [None, 20, 30],
        "rf__min_samples_leaf": [1, 2, 4]
    },
    n_iter=5, cv=3,
    scoring="neg_mean_absolute_error",
    random_state=42, n_jobs=1
)

search.fit(X_train, y_train)
model = search.best_estimator_

# 6. Evaluate
predictions = model.predict(X_test)

print("Best parameters:", search.best_params_)
print("MAE:", round(mean_absolute_error(y_test, predictions), 2))
print("R2 score:", round(r2_score(y_test, predictions), 4))

# 7. Save model and frontend options
data = {
    "version": 2,
    "model": model,
    "brand_models": df.groupby("brand")["model"].apply(
        lambda x: sorted(x.unique().tolist())
    ).to_dict(),
    "fuel_options": sorted(df["fuel"].unique().tolist()),
    "transmission_options": sorted(df["transmission"].unique().tolist()),
    "owner_options": sorted(df["owner"].unique().tolist()),
    "mileage_default": float(df["mileage"].median()),
    "mileage_max": float(df["mileage"].max())
}

joblib.dump(data, Path(__file__).with_name("car_price_model.pkl"))

# 8. Save graph
plt.scatter(y_test, predictions, alpha=0.5)
plt.xlabel("Actual Price")
plt.ylabel("Predicted Price")
plt.title("Actual vs Predicted Car Prices")
plt.tight_layout()
plt.savefig(Path(__file__).with_name("car_price_predictions.png"))
plt.close()

print("Model saved! Training completed.")
