import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# 1. Generate Synthetic Indian Real Estate Dataset
np.random.seed(42)
n_samples = 1500

# भारतातील प्रमुख शहरे
locations = ['Mumbai', 'Pune', 'Bangalore', 'Delhi', 'Hyderabad', 'Chennai', 'Kolkata', 'Ahmedabad']
property_types = ['Apartment', 'Villa', 'Independent House', 'Studio']
furnished_statuses = ['Unfurnished', 'Semi-Furnished', 'Fully Furnished']
property_ages = ['New Construction', '1-5 Years', '5-10 Years', '10+ Years']

data = {
    'location': np.random.choice(locations, n_samples),
    'area_sqft': np.random.randint(400, 4000, n_samples),
    'bhk': np.random.choice([1, 2, 3, 4, 5], n_samples),
    'balcony': np.random.choice(['Has Balcony', 'No Balcony'], n_samples),
    'property_type': np.random.choice(property_types, n_samples),
    'furnished_status': np.random.choice(furnished_statuses, n_samples),
    'property_age': np.random.choice(property_ages, n_samples),
    'amenities_score': np.random.randint(1, 10, n_samples)
}

df = pd.DataFrame(data)

# Target Variable Calculation (Price in Lakhs ₹)
base_prices = {
    'Mumbai': 15000, 'Delhi': 11000, 'Bangalore': 9000, 'Pune': 7500,
    'Hyderabad': 7000, 'Chennai': 6500, 'Kolkata': 5500, 'Ahmedabad': 5000
}
df['base_rate'] = df['location'].map(base_prices)
df['price_lakhs'] = (
    (df['area_sqft'] * df['base_rate']) / 100000 +
    (df['bhk'] * 8) +
    (df['amenities_score'] * 3) +
    np.random.normal(0, 5, n_samples)
).round(2)

X = df.drop(columns=['price_lakhs', 'base_rate'])
y = df['price_lakhs']

# 2. Preprocessing & ML Pipeline Setup
categorical_cols = ['location', 'balcony', 'property_type', 'furnished_status', 'property_age']
numerical_cols = ['area_sqft', 'bhk', 'amenities_score']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'
)

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# 3. Train Model and Save Artifact
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, 'model.pkl')
print("✅ All-India Location Model Trained Successfully! Saved as model.pkl")