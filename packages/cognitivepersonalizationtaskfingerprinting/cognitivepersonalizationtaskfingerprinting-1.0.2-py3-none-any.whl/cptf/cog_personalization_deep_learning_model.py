import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, Normalizer
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras_sequential_ascii import keras2ascii
import tensorflow as tf

def read_csv_file(file_path):
    """Read a CSV file and return the DataFrame."""
    return pd.read_csv(file_path, sep=';')

def fill_na_with_minus_one(data):
    """Fill NaN values in the DataFrame with -1."""
    return data.fillna(-1)

def split_data(data, target_variable, predictors):
    """Split data into predictors (X) and target variables (y)."""
    X = data[predictors].values
    y = data[target_variable].values
    return X, y

def standardize_data(X, y):
    """Standardize predictor and target variable data."""
    predictor_scaler = StandardScaler()
    target_var_scaler = StandardScaler()

    X_standardized = predictor_scaler.fit_transform(X)
    y_standardized = target_var_scaler.fit_transform(y)

    return X_standardized, y_standardized, predictor_scaler, target_var_scaler


def train_neural_network(X_train, y_train):
    """Train a neural network model. Based on the dataset provided, the following values must be adapted."""
    model = Sequential()
    # ... (your model architecture)

    # Defining the Input layer and FIRST hidden layer, both are same!
    model.add(Dense(units=256, input_dim=105, kernel_initializer='normal', activation='relu'))

    # Defining the Second layer of the model
    # after the first layer we don't have to specify input_dim as keras configure it automatically
    model.add(Dropout(0.15))
    model.add(Dense(units=128, kernel_initializer='normal', activation='tanh'))
    model.add(Dropout(0.15))
    model.add(Dense(units=64, kernel_initializer='normal', activation='tanh'))
    model.add(Dropout(0.15))
    model.add(Dense(units=32, kernel_initializer='normal', activation='tanh'))
    model.add(Dropout(0.15))
    model.add(Dense(units=16, kernel_initializer='normal', activation='tanh'))
    model.add(Dropout(0.15))
    model.add(Dense(units=8, kernel_initializer='normal', activation='tanh'))

    # The output neuron is a single fully connected node
    # Since we will be predicting a single number
    model.add(Dense(4, kernel_initializer='normal'))

    # Compiling the model
    model.compile(loss='mean_squared_error', optimizer='adam')

    model.fit(X_train, y_train, batch_size=20, epochs=700, verbose=1)

    return model
def save_model(model, file_path='model.h5'):
    """Save the trained model."""
    model.save(file_path)

def main():
    # User input for CSV file path
    csv_file_path = input("Enter the path to the CSV file: ")

    # Reading and preparing the dataset
    data = read_csv_file(csv_file_path)
    data = fill_na_with_minus_one(data)

    # User input for target variable names
    target_variable = input("Enter the target variable name(s) separated by commas: ").split(',')

    # User input for predictor variable names
    predictors = input("Enter the predictor variable name(s) separated by commas: ").split(',')

    X, y = split_data(data, target_variable, predictors)
    X_std, y_std, predictor_scaler, target_var_scaler = standardize_data(X, y)

    # Splitting the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X_std, y_std, test_size=0.3, random_state=42)

    # Normalizing the data
    norm = Normalizer()
    X_train = norm.fit_transform(X_train)
    X_test = norm.fit_transform(X_test)
    y_train = norm.fit_transform(y_train)
    y_test = norm.fit_transform(y_test)

    # ... (your training and evaluation logic)

    # Saving the model
    model = train_neural_network(X_train, y_train)
    save_model(model)

if __name__ == "__main__":
    main()