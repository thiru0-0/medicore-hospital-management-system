import pandas as pd
import os
from datetime import datetime
from symptom_checker import interactive_symptom_checker

def patient_menu(patient_id):
    """Display patient menu and handle patient operations"""
    while True:
        print("\n" + "-"*50)
        print(" PATIENT MENU")
        print("-"*50)
        print("1. Book Appointment")
        print("2. Predict Disease")
        print("3. View Appointment History")
        print("4. Logout")
        print("-"*50)
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                book_appointment(patient_id)
            elif choice == '2':
                predict_disease(patient_id)
            elif choice == '3':
                view_appointment_history(patient_id)
            elif choice == '4':
                print("Logging out...")
                break
            else:
                print("Invalid choice! Please try again.")
        except KeyboardInterrupt:
            print("\n\nLogging out...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def book_appointment(patient_id):
    """Allow patient to book an appointment with a doctor"""
    print("\n" + "-"*50)
    print(" BOOK APPOINTMENT")
    print("-"*50)
    
    try:
        # Read doctors data
        doctors_df = pd.read_csv("data/doctors.csv", encoding='utf-8')
        
        # Display available doctors
        print("\nAvailable Doctors:")
        print("-"*50)
        for idx, doctor in doctors_df.iterrows():
            print(f"{idx + 1}. {doctor['name']} - {doctor['specialization']}")
            print(f"   Availability: {doctor['availability']}")
            print(f"   Contact: {doctor['contact']}")
        
        # Get doctor selection
        doctor_choice = input("\nEnter doctor number (or 'q' to cancel): ").strip()
        if doctor_choice.lower() == 'q':
            return
        
        doctor_idx = int(doctor_choice) - 1
        if 0 <= doctor_idx < len(doctors_df):
            selected_doctor = doctors_df.iloc[doctor_idx]
            doctor_id = selected_doctor['doctor_id']
            
            # Get appointment details
            print(f"\nBooking appointment with {selected_doctor['name']}")
            date = input("Enter appointment date (YYYY-MM-DD): ").strip()
            time = input("Enter appointment time (HH:MM): ").strip()
            reason = input("Enter reason for appointment: ").strip()
            
            # Create or append to appointments file
            appointment_data = {
                'appointment_id': f"APT{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'patient_id': patient_id,
                'doctor_id': doctor_id,
                'doctor_name': selected_doctor['name'],
                'specialization': selected_doctor['specialization'],
                'date': date,
                'time': time,
                'reason': reason,
                'status': 'Scheduled',
                'diagnosis': '',
                'prescription': ''
            }
            
            appointments_file = "data/appointments.csv"
            if os.path.exists(appointments_file):
                appointments_df = pd.read_csv(appointments_file, encoding='utf-8')
            else:
                appointments_df = pd.DataFrame()
            
            appointments_df = pd.concat([appointments_df, pd.DataFrame([appointment_data])], ignore_index=True)
            appointments_df.to_csv(appointments_file, index=False, encoding='utf-8')
            
            print(f"\n✓ Appointment booked successfully!")
            print(f"  Appointment ID: {appointment_data['appointment_id']}")
            print(f"  Doctor: {selected_doctor['name']}")
            print(f"  Date: {date} at {time}")
        else:
            print("Invalid doctor selection!")
            
    except Exception as e:
        print(f"Error booking appointment: {e}")

def predict_disease(patient_id):
    """Interactive AI-powered disease prediction based on symptoms"""
    print("\n" + "-"*50)
    print(" DISEASE PREDICTION (AI-POWERED)")
    print("-"*50)
    
    try:
        # Get patient info
        patients_df = pd.read_csv("data/patients.csv", encoding='utf-8')
        patient = patients_df[patients_df['patient_id'] == patient_id].iloc[0]
        
        print(f"\nPatient: {patient['name']}")
        print(f"Age: {patient['age']}, Gender: {patient['gender']}")
        print("\n" + "-"*50)
        
        # Ask user if they want interactive or quick mode
        print("\nChoose prediction mode:")
        print("1. Interactive Chat (Recommended - I'll ask you about symptoms one by one)")
        print("2. Quick Mode (Enter symptoms as comma-separated list)")
        
        mode_choice = input("\nEnter your choice (1/2): ").strip()
        
        predicted_disease = None
        user_symptoms = []
        
        if mode_choice == '1':
            # Interactive chat mode
            predicted_disease, user_symptoms = interactive_symptom_checker()
        else:
            # Quick mode - fallback to simple input
            print("\nEnter your symptoms (separated by commas):")
            symptoms_input = input("Symptoms: ").strip().lower()
            
            if not symptoms_input:
                print("No symptoms entered!")
                return
            
            # Convert to list and use basic prediction
            symptom_list = [s.strip().replace(' ', '_') for s in symptoms_input.split(',')]
            user_symptoms = symptom_list
            
            # Try to use ML model if available
            try:
                from model_utils import load_or_train_model, predict_from_symptoms, get_disease_precautions
                
                model, encoder_data = load_or_train_model()
                if model:
                    predicted_disease, confidence = predict_from_symptoms(model, encoder_data, user_symptoms)
                    
                    if predicted_disease:
                        print(f"\n{'='*60}")
                        print(" PREDICTION RESULT")
                        print(f"{'='*60}")
                        print(f"\nPredicted Disease: {predicted_disease}")
                        print(f"Confidence Level: {confidence*100:.1f}%")
                        
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
            except Exception as e:
                print(f"\n⚠ Model prediction unavailable: {e}")
                print("Showing basic suggestions...")
                predicted_disease = "Consultation Recommended"
        
        # Save prediction record
        if predicted_disease or user_symptoms:
            prediction_file = "data/disease_predictions.csv"
            symptoms_str = ', '.join(user_symptoms) if user_symptoms else 'Not specified'
            
            prediction_data = {
                'prediction_id': f"PRED{datetime.now().strftime('%Y%m%d%H%M%S')}",
                'patient_id': patient_id,
                'symptoms': symptoms_str,
                'predicted_disease': predicted_disease if predicted_disease else 'Not predicted',
                'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            if os.path.exists(prediction_file):
                pred_df = pd.read_csv(prediction_file, encoding='utf-8')
            else:
                pred_df = pd.DataFrame()
            
            pred_df = pd.concat([pred_df, pd.DataFrame([prediction_data])], ignore_index=True)
            pred_df.to_csv(prediction_file, index=False, encoding='utf-8')
            
            print(f"\n✓ Prediction saved to your medical records.")
        
        print(f"\n{'='*60}")
        print("⚠ IMPORTANT REMINDER:")
        print("This is an AI prediction tool, not a substitute for medical diagnosis.")
        print("Always consult with a qualified healthcare professional.")
        print(f"{'='*60}\n")
        
    except Exception as e:
        print(f"Error in disease prediction: {e}")

def view_appointment_history(patient_id):
    """Display patient's appointment history"""
    print("\n" + "-"*50)
    print(" APPOINTMENT HISTORY")
    print("-"*50)
    
    try:
        appointments_file = "data/appointments.csv"
        if not os.path.exists(appointments_file):
            print("No appointments found.")
            return
        
        appointments_df = pd.read_csv(appointments_file, encoding='utf-8')
        patient_appointments = appointments_df[appointments_df['patient_id'] == patient_id]
        
        if patient_appointments.empty:
            print("No appointment history found.")
            return
        
        print(f"\nTotal Appointments: {len(patient_appointments)}")
        print("-"*50)
        
        for idx, appointment in patient_appointments.iterrows():
            print(f"\nAppointment {idx + 1}:")
            print(f"  ID: {appointment['appointment_id']}")
            print(f"  Doctor: {appointment.get('doctor_name', 'N/A')}")
            print(f"  Specialization: {appointment.get('specialization', 'N/A')}")
            print(f"  Date: {appointment['date']}")
            print(f"  Time: {appointment['time']}")
            print(f"  Reason: {appointment.get('reason', 'N/A')}")
            print(f"  Status: {appointment.get('status', 'N/A')}")
            if appointment.get('diagnosis'):
                print(f"  Diagnosis: {appointment['diagnosis']}")
            if appointment.get('prescription'):
                print(f"  Prescription: {appointment['prescription']}")
            print("-"*50)
            
    except Exception as e:
        print(f"Error viewing appointment history: {e}")
