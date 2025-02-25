# -*- coding: utf-8 -*-
"""Copy of Store_Sales_Prediction_Machine_Learning_Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/184E8yRbI_E35JZWmpPX-iuYja1mvBnxE

Read Data from File to Pandas DataFrame
"""

!pip install pandas matplotlib seaborn xgboost scikit_learn

#Reading Input Dataset
import pandas as pd
data = pd.read_csv('/content/BigMart_Sales.csv')

#lets print first 5 lines of dataset
data.head()

data.info()

data.isnull().sum()

"""Replacing Missing Values with Mean and Mode."""

data['Item_Weight'].mean()

data['Item_Weight'] = data['Item_Weight'].fillna(data['Item_Weight'].mean())

data.isnull().sum()

outlet_size_mode = data.pivot_table(values='Outlet_Size', columns = 'Outlet_Type', aggfunc=(lambda x:x.mode()))

outlet_size_mode

missing_values_loc = data['Outlet_Size'].isnull()

missing_values_loc

data.loc[missing_values_loc,'Outlet_Size'] = data.loc[missing_values_loc,'Outlet_Type' ].apply(lambda x:outlet_size_mode[x])

data.isnull().sum()

data.describe()

"""Drawing Distribution (For Numeric Fields) and CountPlots(For Categorical Cols)"""

import matplotlib.pyplot as plt
import seaborn as sns

#Data Distribution for Item_Weight Col
plt.figure(figsize=(6,6))
sns.displot(data['Item_Weight'])
plt.show()

#Data Distribution for Item_Visibility Col
plt.figure(figsize=(6,6))
sns.displot(data['Item_Visibility'])
plt.show()

#Data Distribution for Item_MRP Col
plt.figure(figsize=(6,6))
sns.displot(data['Item_MRP'])
plt.show()

#Data Distribution for Item_Outlet_Sales Col
plt.figure(figsize=(6,6))
sns.displot(data['Item_Outlet_Sales'])
plt.show()

#CountPlot for Item_Outlet_Sales Col
plt.figure(figsize=(6,6))
sns.countplot(x = data['Outlet_Establishment_Year'], data=data)
plt.show()

"""

1.   List item
2.   List item

"""

data.head()

#CountPlot for Item_Outlet_Sales Col
plt.figure(figsize=(6,6))
sns.countplot(x = data['Item_Fat_Content'], data=data)
plt.show()

#CountPlot for Item_Outlet_Sales Col
plt.figure(figsize=(25,6))
sns.countplot(x = data['Item_Type'], data=data)
plt.show()

#CountPlot for Item_Outlet_Sales Col
plt.figure(figsize=(6,6))
sns.countplot(x = data['Outlet_Size'], data=data)
plt.show()

#CountPlot for Item_Outlet_Sales Col
plt.figure(figsize=(15,6))
sns.countplot(x = data['Outlet_Type'], data=data)
plt.show()

#CountPlot for Item_Outlet_Sales Col
plt.figure(figsize=(6,6))
sns.countplot(x = data['Outlet_Location_Type'], data=data)
plt.show()

data['Item_Fat_Content'].value_counts()

data.replace({'Item_Fat_Content':{'LF':'Low Fat', 'low fat':'Low Fat', 'reg':'Regular'}}, inplace=True)

data['Item_Fat_Content'].value_counts()

data.head()

from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()

data['Item_Identifier'] = encoder.fit_transform(data['Item_Identifier'])

data['Item_Fat_Content'] = encoder.fit_transform(data['Item_Fat_Content'])

data['Item_Type'] = encoder.fit_transform(data['Item_Type'])

data['Outlet_Identifier'] = encoder.fit_transform(data['Outlet_Identifier'])

data['Outlet_Size'] = encoder.fit_transform(data['Outlet_Size'])

data['Outlet_Location_Type'] = encoder.fit_transform(data['Outlet_Location_Type'])

data['Outlet_Type'] = encoder.fit_transform(data['Outlet_Type'])

data['Item_Fat_Content'].value_counts()

x = data.drop(columns='Item_Outlet_Sales')
y = data['Item_Outlet_Sales']

x

y

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

print(x.shape, x_train.shape, x_test.shape)

print(y.shape, y_train.shape, y_test.shape)

"""#Model Creation"""

from xgboost import XGBRegressor

model = XGBRegressor()

#training our model

model.fit(x_train, y_train)

from sklearn.metrics import r2_score

predictions_train = model.predict(x_train)

r2_score(predictions_train, y_train)

predictions_test = model.predict(x_test)

r2_score(predictions_test, y_test)

