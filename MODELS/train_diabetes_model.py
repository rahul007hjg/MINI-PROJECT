import pandas as pd
from sklearn.linear_model import LogisticRegression
import pickle

# Load the dataset (ensure your CSV file uses ";" as delimiter)
df = pd.read_csv("diabetes_dataset.csv", delimiter=";")

# Preprocess the data:
# Convert gender to binary (Male=1, Female=0)
df["gender"] = df["gender"].apply(lambda x: 1 if x.strip().lower() == "male" else 0)

# Separate features and target
X = df.drop("class", axis=1)
y = df["class"]

# Train a simple logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Save the trained model to a pickle file
with open("diabetes_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Model trained and saved as diabetes_model.pkl")
