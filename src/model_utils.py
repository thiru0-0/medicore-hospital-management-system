"""
Utility functions for disease prediction model
"""
import pandas as pd
import numpy as np
import pickle
import os

# Lazy import sklearn - only import when needed
try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    print("Warning: scikit-learn not available. Please install it with: pip install scikit-learn")

def get_all_symptoms():
    """Get list of all unique symptoms from the dataset"""
    try:
        symptoms_df = pd.read_csv("data/DiseaseAndSymptoms.csv", encoding='utf-8')
        
        # Get all symptom columns
        symptom_cols = [col for col in symptoms_df.columns if 'Symptom_' in col]
        
        # Get unique symptoms from all columns
        all_symptoms = set()
        for col in symptom_cols:
            unique_vals = symptoms_df[col].dropna().unique()
            all_symptoms.update(unique_vals)
        
        # Remove 'None' if present
        all_symptoms.discard('None')
        all_symptoms.discard('none')
        
        return sorted(list(all_symptoms))
    except Exception as e:
        print(f"Error loading symptoms: {e}")
        return []

def get_disease_precautions():
    """Get precautions for diseases"""
    try:
        precautions_df = pd.read_csv("data/Disease precaution.csv", encoding='utf-8')
        return precautions_df
    except Exception as e:
        print(f"Error loading precautions: {e}")
        return pd.DataFrame()

def load_or_train_model():
    """Load trained model if exists, otherwise train a new one"""
    if not SKLEARN_AVAILABLE:
        print("Error: scikit-learn is not installed. Please install it first.")
        print("Run: pip install scikit-learn")
        return None, None
    
    model_path = "data/disease_prediction_model.pkl"
    encoder_path = "data/symptom_encoder.pkl"
    
    # Check if model exists
    if os.path.exists(model_path) and os.path.exists(encoder_path):
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            with open(encoder_path, 'rb') as f:
                encoder_data = pickle.load(f)
            return model, encoder_data
        except Exception as e:
            print(f"Error loading model: {e}. Retraining...")
    
    # Train new model
    return train_and_save_model()

def train_and_save_model():
    """Train the disease prediction model and save it"""
    if not SKLEARN_AVAILABLE:
        print("Error: scikit-learn is not installed. Please install it first.")
        print("Run: pip install scikit-learn")
        return None, None
    
    try:
        # Load data
        symptoms_df = pd.read_csv("data/DiseaseAndSymptoms.csv", encoding='utf-8')
        
        # Handle missing values
        symptom_cols = [col for col in symptoms_df.columns if 'Symptom_' in col]
        symptoms_df[symptom_cols] = symptoms_df[symptom_cols].fillna('None')
        
        # Prepare features and target
        X = symptoms_df[symptom_cols]
        y = symptoms_df['Disease']
        
        # One-hot encode symptoms
        X_encoded = pd.get_dummies(X, prefix='', prefix_sep='')
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_encoded, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        model = RandomForestClassifier(random_state=42, n_estimators=100)
        model.fit(X_train, y_train)
        
        # Save model and encoder info
        model_path = "data/disease_prediction_model.pkl"
        encoder_path = "data/symptom_encoder.pkl"
        
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        
        # Save encoder info (column names)
        encoder_data = {
            'columns': X_encoded.columns.tolist(),
            'feature_names': X_encoded.columns.tolist()
        }
        
        with open(encoder_path, 'wb') as f:
            pickle.dump(encoder_data, f)
        
        print(f"Model trained and saved successfully!")
        print(f"Model accuracy: {model.score(X_test, y_test):.4f}")
        
        return model, encoder_data
        
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None

def predict_from_symptoms(model, encoder_data, user_symptoms):
    """
    Predict disease from user symptoms
    
    Args:
        model: Trained RandomForestClassifier
        encoder_data: Dictionary with encoder information
        user_symptoms: List of symptom names that user has
        
    Returns:
        Predicted disease name
    """
    try:
        # Get all feature columns
        feature_columns = encoder_data['columns']
        
        # Create input DataFrame with all zeros
        input_data = pd.DataFrame(0, index=[0], columns=feature_columns)
        
        # Set user symptoms to 1
        for symptom in user_symptoms:
            # Try exact match first
            if symptom in feature_columns:
                input_data[symptom] = 1
            else:
                # Try case-insensitive match
                symptom_lower = symptom.lower().strip()
                for col in feature_columns:
                    if col.lower().strip() == symptom_lower:
                        input_data[col] = 1
                        break
        
        # Make prediction
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]
        confidence = max(probabilities)
        
        return prediction, confidence
        
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None, 0.0

