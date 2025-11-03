"""
Interactive symptom checker with chat-like interface
"""
import pandas as pd
from model_utils import load_or_train_model, predict_from_symptoms, get_disease_precautions

def interactive_symptom_checker():
    """
    Interactive chat-like symptom checker
    Asks user about symptoms one by one with yes/no answers
    """
    print("\n" + "="*60)
    print(" " * 15 + "INTERACTIVE SYMPTOM CHECKER")
    print("="*60)
    print("\nI'll ask you about symptoms one by one.")
    print("Please answer with: 'yes' or 'y' for YES")
    print("                   'no' or 'n' for NO")
    print("                   'done' when you're finished\n")
    print("-"*60)
    
    # Load model
    print("Loading prediction model...")
    model, encoder_data = load_or_train_model()
    
    if model is None:
        print("Error: Could not load or train model!")
        return None, []
    
    # Get all available symptoms
    all_symptoms = encoder_data.get('columns', [])
    # Filter out numeric columns and get actual symptom names
    symptom_names = [s for s in all_symptoms if not s.replace('_', '').isdigit()]
    
    # Get unique symptom names (remove duplicates from one-hot encoding artifacts)
    unique_symptoms = []
    seen = set()
    for sym in symptom_names:
        if sym not in seen and sym.lower() != 'none':
            unique_symptoms.append(sym)
            seen.add(sym)
    
    # Limit to top symptoms for better UX (you can adjust this)
    symptoms_to_check = unique_symptoms[:50]  # Check first 50 symptoms
    
    user_symptoms = []
    confirmed_symptoms = []
    
    print(f"\nI'll ask you about {len(symptoms_to_check)} common symptoms.")
    print("You can stop anytime by typing 'done'\n")
    
    symptom_num = 0
    max_symptoms = len(symptoms_to_check)
    
    for i, symptom in enumerate(symptoms_to_check, 1):
        symptom_num = i
        
        # Format symptom name for display (clean it up)
        display_symptom = symptom.replace('_', ' ').title()
        
        print(f"[{i}/{max_symptoms}] Do you have: {display_symptom}?")
        response = input("Your answer (yes/no/done): ").strip().lower()
        
        if response in ['done', 'd', 'exit', 'quit', 'stop']:
            print(f"\n✓ Stopped at symptom {i}. You've answered {len(confirmed_symptoms)} symptoms.")
            break
        elif response in ['yes', 'y']:
            confirmed_symptoms.append(symptom)
            user_symptoms.append(symptom)
            print(f"  ✓ Marked: {display_symptom}\n")
        elif response in ['no', 'n']:
            print(f"  - Skipped: {display_symptom}\n")
        else:
            print("  ⚠ Invalid response. Please answer 'yes', 'no', or 'done'.\n")
            # Ask again for the same symptom
            i -= 1
            continue
        
        # If we have enough symptoms, we can optionally stop early
        # (You can remove this if you want to ask all questions)
        if len(confirmed_symptoms) >= 5:
            print(f"\nYou have {len(confirmed_symptoms)} symptoms so far.")
            continue_choice = input("Continue with more symptoms? (yes/no): ").strip().lower()
            if continue_choice in ['no', 'n']:
                break
    
    if not user_symptoms:
        print("\n⚠ No symptoms selected. Please consult a doctor for proper diagnosis.")
        return None, []
    
    # Make prediction
    print("\n" + "-"*60)
    print("Analyzing your symptoms...")
    print("-"*60)
    
    predicted_disease, confidence = predict_from_symptoms(model, encoder_data, user_symptoms)
    
    if predicted_disease:
        print(f"\n{'='*60}")
        print(" PREDICTION RESULT")
        print(f"{'='*60}")
        print(f"\nPredicted Disease: {predicted_disease}")
        print(f"Confidence Level: {confidence*100:.1f}%")
        print(f"\nSymptoms you reported: {len(user_symptoms)}")
        for i, sym in enumerate(user_symptoms, 1):
            print(f"  {i}. {sym.replace('_', ' ').title()}")
        
        # Get precautions
        precautions_df = get_disease_precautions()
        if not precautions_df.empty and 'Disease' in precautions_df.columns:
            disease_precautions = precautions_df[precautions_df['Disease'] == predicted_disease]
            if not disease_precautions.empty:
                print(f"\n{'='*60}")
                print(" RECOMMENDED PRECAUTIONS")
                print(f"{'='*60}")
                prec_row = disease_precautions.iloc[0]
                prec_cols = [col for col in precautions_df.columns if 'Precaution' in col]
                for col in prec_cols:
                    if pd.notna(prec_row[col]):
                        print(f"  • {prec_row[col]}")
        
        print(f"\n{'='*60}")
        print("⚠ IMPORTANT: This is an AI prediction, not a medical diagnosis.")
        print("Please consult with a qualified healthcare professional for proper diagnosis and treatment.")
        print(f"{'='*60}\n")
        
        return predicted_disease, user_symptoms
    else:
        print("\n⚠ Could not make a prediction. Please consult a doctor.")
        return None, user_symptoms

def simple_symptom_checker():
    """
    Simpler version - asks about most common symptoms interactively
    """
    print("\n" + "="*60)
    print(" " * 18 + "SYMPTOM CHECKER")
    print("="*60)
    
    # Load model
    model, encoder_data = load_or_train_model()
    if model is None:
        return None, []
    
    # Common symptoms to check (you can customize this list)
    common_symptoms = [
        "Fever", "Cough", "Headache", "Nausea", "Fatigue",
        "Muscle Pain", "Joint Pain", "Rash", "Itching",
        "Chest Pain", "Shortness of Breath", "Dizziness",
        "Abdominal Pain", "Diarrhea", "Vomiting"
    ]
    
    user_symptoms = []
    
    print("\nI'll ask you about common symptoms. Answer with 'yes' or 'no'.\n")
    
    for symptom in common_symptoms:
        response = input(f"Do you have {symptom}? (yes/no): ").strip().lower()
        if response in ['yes', 'y']:
            user_symptoms.append(symptom.lower().replace(' ', '_'))
            print(f"  ✓ Added: {symptom}\n")
        else:
            print(f"  - Skipped\n")
    
    if not user_symptoms:
        print("No symptoms reported.")
        return None, []
    
    # Make prediction
    predicted_disease, confidence = predict_from_symptoms(model, encoder_data, user_symptoms)
    
    if predicted_disease:
        print(f"\n{'='*60}")
        print(f"Predicted: {predicted_disease}")
        print(f"Confidence: {confidence*100:.1f}%")
        print(f"{'='*60}\n")
        return predicted_disease, user_symptoms
    
    return None, user_symptoms

