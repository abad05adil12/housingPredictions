import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, LabelEncoder
import pickle

df = pd.read_csv("data.csv")

le = LabelEncoder()
df["Location"] = le.fit_transform(df["Location"])

X = df[["Size_sqft", "Bedrooms", "House_Age", "Location"]]
y = df["Price_PKR"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

model = LinearRegression()
model.fit(X_scaled, y)

pickle.dump(model, open("house_model.pkl", "wb"))
pickle.dump(scaler, open("scaler.pkl", "wb"))
pickle.dump(le, open("location_encoder.pkl", "wb"))

print("✅ Model trained and saved successfully")
