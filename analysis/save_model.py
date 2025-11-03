"""
Script to train and save the disease prediction model
Run this script from the notebook or as a standalone script
"""

import pandas as pd
import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def train_and_save_model():
    """Train the model and save it for use in the main application"""
    
    print("Loading data...")
    # Load data
    symptoms_df = pd.read_csv("../data/DiseaseAndSymptoms.csv", encoding='utf-8')
    
    print("Preprocessing data...")
    # Handle missing values
    symptom_cols = [col for col in symptoms_df.columns if 'Symptom_' in col]
    symptoms_df[symptom_cols] = symptoms_df[symptom_cols].fillna('None')
    
    # Prepare features and target
    X = symptoms_df[symptom_cols]
    y = symptoms_df['Disease']
    
    print("Encoding symptoms...")
    # One-hot encode symptoms
    X_encoded = pd.get_dummies(X, prefix='', prefix_sep='')
    
    print("Splitting data...")
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Test data shape: {X_test.shape}")
    
    print("Training RandomForest model...")
    # Train model
    model = RandomForestClassifier(random_state=42, n_estimators=100, max_depth=20)
    model.fit(X_train, y_train)
    
    # Evaluate
    accuracy = model.score(X_test, y_test)
    print(f"\nModel trained successfully!")
    print(f"Accuracy on test set: {accuracy*100:.2f}%")
    
    # Save model
    model_path = "../data/disease_prediction_model.pkl"
    encoder_path = "../data/symptom_encoder.pkl"
    
    print(f"\nSaving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    # Save encoder info (column names)
    encoder_data = {
        'columns': X_encoded.columns.tolist(),
        'feature_names': X_encoded.columns.tolist()
    }
    
    print(f"Saving encoder info to {encoder_path}...")
    with open(encoder_path, 'wb') as f:
        pickle.dump(encoder_data, f)
    
    print("\n✓ Model and encoder saved successfully!")
    print(f"  - Model: {model_path}")
    print(f"  - Encoder: {encoder_path}")
    
    return model, encoder_data

if __name__ == "__main__":
    train_and_save_model()

