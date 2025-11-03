import pandas as pd
import os
from datetime import datetime

def doctor_menu(doctor_id):
    """Display doctor menu and handle doctor operations"""
    while True:
        print("\n" + "-"*50)
        print(" DOCTOR MENU")
        print("-"*50)
        print("1. View Patient List")
        print("2. Add Diagnosis")
        print("3. Logout")
        print("-"*50)
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                view_patient_list(doctor_id)
            elif choice == '2':
                add_diagnosis(doctor_id)
            elif choice == '3':
                print("Logging out...")
                break
            else:
                print("Invalid choice! Please try again.")
        except KeyboardInterrupt:
            print("\n\nLogging out...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def view_patient_list(doctor_id):
    """Display list of patients assigned to the doctor"""
    print("\n" + "-"*50)
    print(" PATIENT LIST")
    print("-"*50)
    
    try:
        # Get doctor info
        doctors_df = pd.read_csv("data/doctors.csv", encoding='utf-8')
        doctor = doctors_df[doctors_df['doctor_id'] == doctor_id].iloc[0]
        print(f"Doctor: {doctor['name']} - {doctor['specialization']}")
        
        # Read appointments
        appointments_file = "data/appointments.csv"
        if not os.path.exists(appointments_file):
            print("\nNo appointments found.")
            return
        
        appointments_df = pd.read_csv(appointments_file, encoding='utf-8')
        doctor_appointments = appointments_df[appointments_df['doctor_id'] == doctor_id]
        
        if doctor_appointments.empty:
            print("\nNo patients assigned yet.")
            return
        
        # Get unique patients
        patients_df = pd.read_csv("data/patients.csv", encoding='utf-8')
        unique_patient_ids = doctor_appointments['patient_id'].unique()
        
        print(f"\nTotal Patients: {len(unique_patient_ids)}")
        print("-"*50)
        
        for patient_id in unique_patient_ids:
            patient = patients_df[patients_df['patient_id'] == patient_id].iloc[0]
            patient_appts = doctor_appointments[doctor_appointments['patient_id'] == patient_id]
            
            print(f"\nPatient ID: {patient_id}")
            print(f"  Name: {patient['name']}")
            print(f"  Age: {patient['age']}, Gender: {patient['gender']}")
            print(f"  Contact: {patient['contact']}")
            print(f"  Email: {patient['email']}")
            print(f"  Total Appointments: {len(patient_appts)}")
            
            # Show upcoming appointments
            upcoming = patient_appts[patient_appts['status'] == 'Scheduled']
            if not upcoming.empty:
                print(f"  Upcoming Appointments: {len(upcoming)}")
                for _, apt in upcoming.iterrows():
                    print(f"    - {apt['date']} at {apt['time']} (Reason: {apt.get('reason', 'N/A')})")
            
            print("-"*50)
            
    except Exception as e:
        print(f"Error viewing patient list: {e}")

def add_diagnosis(doctor_id):
    """Allow doctor to add diagnosis and prescription for a patient"""
    print("\n" + "-"*50)
    print(" ADD DIAGNOSIS")
    print("-"*50)
    
    try:
        # Get doctor info
        doctors_df = pd.read_csv("data/doctors.csv", encoding='utf-8')
        doctor = doctors_df[doctors_df['doctor_id'] == doctor_id].iloc[0]
        
        # Read appointments
        appointments_file = "data/appointments.csv"
        if not os.path.exists(appointments_file):
            print("No appointments found.")
            return
        
        appointments_df = pd.read_csv(appointments_file, encoding='utf-8')
        doctor_appointments = appointments_df[appointments_df['doctor_id'] == doctor_id]
        
        # Show scheduled appointments
        scheduled = doctor_appointments[doctor_appointments['status'] == 'Scheduled']
        
        if scheduled.empty:
            print("No scheduled appointments found.")
            return
        
        print("\nScheduled Appointments:")
        print("-"*50)
        patients_df = pd.read_csv("data/patients.csv", encoding='utf-8')
        for num, (idx, apt) in enumerate(scheduled.iterrows(), 1):
            patient_id = apt['patient_id']
            patient = patients_df[patients_df['patient_id'] == patient_id].iloc[0]
            
            print(f"{num}. Patient: {patient['name']} ({patient_id})")
            print(f"   Date: {apt['date']} at {apt['time']}")
            print(f"   Reason: {apt.get('reason', 'N/A')}")
            print(f"   Appointment ID: {apt['appointment_id']}")
        
        # Get appointment selection
        apt_choice = input("\nEnter appointment number (or 'q' to cancel): ").strip()
        if apt_choice.lower() == 'q':
            return
        
        try:
            apt_idx = list(scheduled.index)[int(apt_choice) - 1]
            selected_apt = scheduled.loc[apt_idx]
            
            # Get diagnosis details
            print(f"\nAdding diagnosis for Appointment ID: {selected_apt['appointment_id']}")
            diagnosis = input("Enter diagnosis: ").strip()
            prescription = input("Enter prescription: ").strip()
            
            # Update appointment
            appointments_df.loc[appointments_df['appointment_id'] == selected_apt['appointment_id'], 'diagnosis'] = diagnosis
            appointments_df.loc[appointments_df['appointment_id'] == selected_apt['appointment_id'], 'prescription'] = prescription
            appointments_df.loc[appointments_df['appointment_id'] == selected_apt['appointment_id'], 'status'] = 'Completed'
            
            # Save updated appointments
            appointments_df.to_csv(appointments_file, index=False, encoding='utf-8')
            
            print(f"\n✓ Diagnosis added successfully!")
            print(f"  Diagnosis: {diagnosis}")
            print(f"  Prescription: {prescription}")
            
        except (ValueError, IndexError):
            print("Invalid appointment selection!")
            
    except Exception as e:
        print(f"Error adding diagnosis: {e}")

