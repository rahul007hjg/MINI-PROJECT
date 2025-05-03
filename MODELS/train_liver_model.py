import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
import pickle

# Load the dataset (adjust path and delimiter if necessary)
df = pd.read_csv("liver_disease.csv")  # assuming comma-separated

# Preprocess data:
# Use the correct column names. In your CSV, the gender column is "Gender".
df["Gender"] = df["Gender"].apply(lambda x: 1 if x.strip().lower() == "male" else 0)

# (Optional) Rename columns if needed; e.g., if there's a spelling mistake:
df = df.rename(columns={"Total_Protiens": "Total_Proteins"})

# Define the features based on your CSV columns
features = [
    "Age", 
    "Gender", 
    "Total_Bilirubin", 
    "Direct_Bilirubin", 
    "Alkaline_Phosphotase", 
    "Alamine_Aminotransferase", 
    "Aspartate_Aminotransferase", 
    "Total_Proteins", 
    "Albumin", 
    "Albumin_and_Globulin_Ratio"
]

X = df[features]
y = df["Dataset"]  # Adjust if your target column name is different

# Impute missing values in X using the median of each column
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(X)

# Train the logistic regression model using the imputed data
model = LogisticRegression(max_iter=1000)
model.fit(X_imputed, y)

# Save the trained model to a pickle file
with open("liver_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Liver disease model trained and saved as liver_model.pkl")
