from flask import Flask, request, jsonify
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import os

app = Flask(__name__)

# Global variables to store dataset and model
dataset = None
model = None

@app.route('/upload', methods=['POST'])
def upload():
    global dataset
    file = request.files['file']
    if file.filename.endswith('.csv'):
        dataset = pd.read_csv(file)
        return jsonify({'message': 'File uploaded successfully!'})
    else:
        return jsonify({'message': 'Invalid file format. Please upload a CSV file.'}), 400

@app.route('/preprocess', methods=['POST'])
def preprocess():
    global dataset
    if dataset is None:
        return jsonify({'message': 'No dataset uploaded.'}), 400

    # Handle missing values
    missing_values = request.json['missingValues']
    if missing_values == 'mean':
        dataset.fillna(dataset.mean(), inplace=True)
    elif missing_values == 'median':
        dataset.fillna(dataset.median(), inplace=True)
    elif missing_values == 'mode':
        dataset.fillna(dataset.mode().iloc[0], inplace=True)

    return jsonify({'message': 'Data preprocessed successfully!'})

@app.route('/train', methods=['POST'])
def train():
    global dataset, model
    if dataset is None:
        return jsonify({'message': 'No dataset uploaded.'}), 400

    # Train a simple Random Forest model
    X = dataset.iloc[:, :-1]
    y = dataset.iloc[:, -1]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    return jsonify({'accuracy': accuracy, 'message': 'Model trained successfully!'})

if __name__ == '__main__':
    app.run(debug=True)
    