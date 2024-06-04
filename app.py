from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split
import os

app = Flask(__name__)

# Load dataset
dataset = pd.read_csv(os.path.join(os.getcwd(), "daily_csv.csv"))

# Data preprocessing
dataset['year'] = pd.DatetimeIndex(dataset['Date']).year
dataset['month'] = pd.DatetimeIndex(dataset['Date']).month
dataset['day'] = pd.DatetimeIndex(dataset['Date']).day
dataset.drop('Date', axis=1, inplace=True)
dataset['Price'].fillna(dataset['Price'].mean(), inplace=True)

x = dataset.iloc[:, 1:4].values  # inputs
y = dataset.iloc[:, 0:1].values  # output price only

# Splitting the dataset 
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

# Model training
dtr = DecisionTreeRegressor()
dtr.fit(x_train, y_train)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json(force=True)
    day = int(data['day'])
    month = int(data['month'])
    year = int(data['year'])
    prediction = dtr.predict([[year, month, day]])
    return jsonify({'price': prediction[0]})

if __name__ == '__main__':
    app.run(debug=True)
