# -*- coding: utf-8 -*-
"""Store Sales Prediction - Fixed Version with Debugging"""

import sys
import pandas as pd

# Check if matplotlib is installed before importing
try:
    import matplotlib.pyplot as plt
    import seaborn as sns
    matplotlib_available = True
except ModuleNotFoundError:
    print("Warning: matplotlib not found. Visualization will be skipped.")
    matplotlib_available = False

import altair as alt  # Streamlit alternative
import streamlit as st

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import r2_score
from xgboost import XGBRegressor

# Load Data
data = pd.read_csv('BigMart_Sales.csv')
st.write("Data Loaded Successfully!")

# Check for missing values
data.isnull().sum()

# Fill missing values in 'Item_Weight' with mean
data['Item_Weight'].fillna(data['Item_Weight'].mean(), inplace=True)

# Fill missing values in 'Outlet_Size' with mode based on 'Outlet_Type'
outlet_size_mode = data.groupby('Outlet_Type')['Outlet_Size'].apply(lambda x: x.mode()[0] if not x.mode().empty else 'Medium')
data.loc[data['Outlet_Size'].isnull(), 'Outlet_Size'] = data['Outlet_Type'].map(outlet_size_mode)

# Confirm missing values handled
data.isnull().sum()
st.write("Missing values handled successfully!")

# Visualizing numeric distributions (Only if matplotlib is available)
numeric_cols = ['Item_Weight', 'Item_Visibility', 'Item_MRP', 'Item_Outlet_Sales']
if matplotlib_available:
    for col in numeric_cols:
        plt.figure(figsize=(6,6))
        sns.histplot(data[col], kde=True)
        plt.title(f'Distribution of {col}')
        plt.show()
else:
    st.line_chart(data[numeric_cols])

# Standardizing 'Item_Fat_Content' categories
data.replace({'Item_Fat_Content': {'LF': 'Low Fat', 'low fat': 'Low Fat', 'reg': 'Regular'}}, inplace=True)

# Encoding categorical variables
encoder = LabelEncoder()
categorical_features = ['Item_Identifier', 'Item_Fat_Content', 'Item_Type', 
                        'Outlet_Identifier', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']

for feature in categorical_features:
    data[feature] = encoder.fit_transform(data[feature])

# Splitting data into features and target
X = data.drop(columns='Item_Outlet_Sales')
y = data['Item_Outlet_Sales']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model training
model = XGBRegressor()
model.fit(X_train, y_train)

# Model evaluation
train_predictions = model.predict(X_train)
test_predictions = model.predict(X_test)

train_r2 = r2_score(y_train, train_predictions)
test_r2 = r2_score(y_test, test_predictions)

st.write(f"Train R² Score: {train_r2:.4f}")
st.write(f"Test R² Score: {test_r2:.4f}")
