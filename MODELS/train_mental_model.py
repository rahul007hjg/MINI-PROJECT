import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
import pickle

# Load the dataset (assumes the CSV file is named "student_mental_health.csv")
df = pd.read_csv("student_mental_health.csv")

# Drop the Timestamp and "What is your course?" columns
df = df.drop(columns=["Timestamp", "What is your course?"], errors="ignore")

# Convert "Choose your gender" to binary: Male = 1, Female = 0
df["gender"] = df["Choose your gender"].apply(lambda x: 1 if x.strip().lower() == "male" else 0)

# Convert "Your current year of Study" to numeric by extracting the digit
df["year"] = df["Your current year of Study"].str.extract(r'(\d+)').astype(float)

# Map CGPA using provided ranges
cgpa_map = {
    "2.50 - 2.99": 0,
    "3.00 - 3.49": 1,
    "3.50 - 4.00": 2
}
df["cgpa_num"] = df["What is your CGPA?"].map(cgpa_map)

# Convert Marital status to binary (Yes = 1, No = 0)
df["marital"] = df["Marital status"].apply(lambda x: 1 if x.strip().lower() == "yes" else 0)

# Convert "Did you seek any specialist for a treatment?" to binary (Yes = 1, No = 0)
df["specialist"] = df["Did you seek any specialist for a treatment?"].apply(lambda x: 1 if x.strip().lower() == "yes" else 0)

# Define target: 1 if any of Depression, Anxiety, or Panic attack is Yes; else 0
def mental_target(row):
    symptoms = [row["Do you have Depression?"], row["Do you have Anxiety?"], row["Do you have Panic attack?"]]
    return 1 if any(str(symptom).strip().lower() == "yes" for symptom in symptoms) else 0

df["target"] = df.apply(mental_target, axis=1)

# Define features (all columns except the mental health symptom questions and target)
features = ["gender", "Age", "year", "cgpa_num", "marital", "specialist"]
X = df[features]
y = df["target"]

# Impute missing values using the median
imputer = SimpleImputer(strategy="median")
X_imputed = imputer.fit_transform(X)

# Train a logistic regression model
model = LogisticRegression(max_iter=1000)
model.fit(X_imputed, y)

# Save the trained model to a pickle file
with open("mental_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("Mental health model trained and saved as mental_model.pkl")
