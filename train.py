import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

np.random.seed(42)
n_samples = 2000

locality_data = {
    'Pune': {'Kothrud': 9500, 'Hinjewadi': 7500, 'Viman Nagar': 11000, 'Baner': 9000, 'Hadapsar': 6500},
    'Mumbai': {'Andheri': 18000, 'Bandra': 28000, 'Thane': 11000, 'Navi Mumbai': 9000, 'Borivali': 14000},
    'Bangalore': {'Koramangala': 12000, 'Whitefield': 8000, 'Indiranagar': 14000, 'Electronic City': 6000, 'HSR Layout': 10000},
    'Delhi': {'Dwarka': 9500, 'South Delhi': 16000, 'Noida': 6500, 'Gurgaon': 10500, 'Rohini': 7500}
}

cities = list(locality_data.keys())
sampled_cities = np.random.choice(cities, n_samples)
sampled_localities = [np.random.choice(list(locality_data[c].keys())) for c in sampled_cities]

property_types = ['Apartment', 'Villa', 'Independent House']
furnished_statuses = ['Unfurnished', 'Semi-Furnished', 'Fully Furnished']
property_ages = ['New Construction', '1-5 Years', '5-10 Years', '10+ Years']

data = {
    'city': sampled_cities,
    'locality': sampled_localities,
    'area_sqft': np.random.randint(400, 4000, n_samples),
    'bhk': np.random.choice([1, 2, 3, 4], n_samples),
    'balcony': np.random.choice(['Has Balcony', 'No Balcony'], n_samples),
    'property_type': np.random.choice(property_types, n_samples),
    'furnished_status': np.random.choice(furnished_statuses, n_samples),
    'property_age': np.random.choice(property_ages, n_samples),
    'amenities_score': np.random.randint(1, 10, n_samples)
}

df = pd.DataFrame(data)
df['base_rate'] = df.apply(lambda row: locality_data[row['city']][row['locality']], axis=1)

df['price_lakhs'] = (
    (df['area_sqft'] * df['base_rate']) / 100000 +
    (df['bhk'] * 8) +
    (df['amenities_score'] * 3) +
    np.random.normal(0, 5, n_samples)
).round(2)

X = df.drop(columns=['price_lakhs', 'base_rate'])
y = df['price_lakhs']

categorical_cols = ['city', 'locality', 'balcony', 'property_type', 'furnished_status', 'property_age']

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

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, 'model.pkl')
print("✅ Model Trained & Saved Successfully as model.pkl!")