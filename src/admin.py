import pandas as pd
import os
import re
from datetime import datetime

def admin_menu():
    """Display admin menu and handle admin operations"""
    while True:
        print("\n" + "-"*50)
        print(" ADMIN MENU")
        print("-"*50)
        print("1. Add Doctor")
        print("2. Generate Reports")
        print("3. Generate Data Profile")
        print("4. Logout")
        print("-"*50)
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                add_doctor()
            elif choice == '2':
                generate_reports()
            elif choice == '3':
                generate_data_profile()
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

def add_doctor():
    """Allow admin to add a new doctor to the system"""
    print("\n" + "-"*50)
    print(" ADD NEW DOCTOR")
    print("-"*50)
    
    try:
        doctors_df = pd.read_csv("data/doctors.csv", encoding='utf-8')
        
        # Generate next consecutive doctor ID
        max_num = 0
        
        # Extract numbers from existing doctor IDs (e.g., DOC001 -> 1, DOC006 -> 6)
        for existing_id in doctors_df['doctor_id'].values:
            # Extract numeric part from ID (e.g., "DOC006" -> "006" -> 6)
            match = re.search(r'\d+', str(existing_id))
            if match:
                num = int(match.group())
                if num > max_num:
                    max_num = num
        
        # Generate next ID
        next_num = max_num + 1
        doctor_id = f"DOC{next_num:03d}"  # Format as DOC001, DOC002, etc.
        
        # Display generated doctor ID
        print(f"\nGenerated Doctor ID: {doctor_id}")
        print("-"*50)
        print("\nEnter doctor details:")
        
        # Get new doctor details
        name = input("Name: ").strip()
        specialization = input("Specialization: ").strip()
        availability = input("Availability (e.g., Mon-Fri 10AM-4PM): ").strip()
        contact = input("Contact: ").strip()
        email = input("Email: ").strip()
        username = input("Username: ").strip()
        
        # Check if username already exists
        if username in doctors_df['username'].values:
            print(f"Error: Username {username} already exists!")
            return
        
        password = input("Password: ").strip()
        
        # Create new doctor record
        new_doctor = {
            'doctor_id': doctor_id,
            'username': username,
            'password': password,
            'name': name,
            'specialization': specialization,
            'availability': availability,
            'contact': contact,
            'email': email
        }
        
        # Add to dataframe
        doctors_df = pd.concat([doctors_df, pd.DataFrame([new_doctor])], ignore_index=True)
        doctors_df.to_csv("data/doctors.csv", index=False, encoding='utf-8')
        
        print(f"\n✓ Doctor added successfully!")
        print(f"  Doctor ID: {doctor_id}")
        print(f"  Name: {name}")
        print(f"  Specialization: {specialization}")
        
    except Exception as e:
        print(f"Error adding doctor: {e}")

def generate_reports():
    """Generate various reports for the hospital"""
    print("\n" + "-"*50)
    print(" GENERATE REPORTS")
    print("-"*50)
    
    try:
        print("\nSelect report type:")
        print("1. Appointment Summary")
        print("2. Doctor Performance")
        print("3. Patient Statistics")
        print("4. All Reports")
        
        choice = input("\nEnter your choice: ").strip()
        
        reports_dir = "analysis"
        if not os.path.exists(reports_dir):
            os.makedirs(reports_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if choice == '1' or choice == '4':
            # Appointment Summary
            if os.path.exists("data/appointments.csv"):
                appointments_df = pd.read_csv("data/appointments.csv", encoding='utf-8')
                
                report = f"\n{'='*60}\n"
                report += f" APPOINTMENT SUMMARY REPORT\n"
                report += f" Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
                report += f"{'='*60}\n\n"
                
                report += f"Total Appointments: {len(appointments_df)}\n"
                report += f"Scheduled: {len(appointments_df[appointments_df['status'] == 'Scheduled'])}\n"
                report += f"Completed: {len(appointments_df[appointments_df['status'] == 'Completed'])}\n\n"
                
                if not appointments_df.empty:
                    report += f"Appointments by Doctor:\n"
                    report += f"{'-'*60}\n"
                    doctor_counts = appointments_df['doctor_id'].value_counts()
                    for doctor_id, count in doctor_counts.items():
                        report += f"{doctor_id}: {count} appointments\n"
                
                print(report)
                
                # Save to file
                report_file = f"{reports_dir}/appointment_summary_{timestamp}.txt"
                with open(report_file, 'w') as f:
                    f.write(report)
                print(f"Report saved to: {report_file}\n")
            else:
                print("No appointment data available.")
        
        if choice == '2' or choice == '4':
            # Doctor Performance
            doctors_df = pd.read_csv("data/doctors.csv", encoding='utf-8')
            
            report = f"\n{'='*60}\n"
            report += f" DOCTOR PERFORMANCE REPORT\n"
            report += f" Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += f"{'='*60}\n\n"
            
            if os.path.exists("data/appointments.csv"):
                appointments_df = pd.read_csv("data/appointments.csv", encoding='utf-8')
                
                for _, doctor in doctors_df.iterrows():
                    doctor_appts = appointments_df[appointments_df['doctor_id'] == doctor['doctor_id']]
                    completed = doctor_appts[doctor_appts['status'] == 'Completed']
                    
                    report += f"Doctor: {doctor['name']}\n"
                    report += f"  Specialization: {doctor['specialization']}\n"
                    report += f"  Total Appointments: {len(doctor_appts)}\n"
                    report += f"  Completed: {len(completed)}\n"
                    report += f"{'-'*60}\n"
            else:
                report += "No appointment data available.\n"
            
            print(report)
            
            # Save to file
            report_file = f"{reports_dir}/doctor_performance_{timestamp}.txt"
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {report_file}\n")
        
        if choice == '3' or choice == '4':
            # Patient Statistics
            patients_df = pd.read_csv("data/patients.csv", encoding='utf-8')
            
            report = f"\n{'='*60}\n"
            report += f" PATIENT STATISTICS REPORT\n"
            report += f" Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            report += f"{'='*60}\n\n"
            
            report += f"Total Patients: {len(patients_df)}\n"
            report += f"Gender Distribution:\n"
            gender_counts = patients_df['gender'].value_counts()
            for gender, count in gender_counts.items():
                report += f"  {gender}: {count}\n"
            
            report += f"\nAge Statistics:\n"
            report += f"  Average Age: {patients_df['age'].mean():.1f}\n"
            report += f"  Min Age: {patients_df['age'].min()}\n"
            report += f"  Max Age: {patients_df['age'].max()}\n"
            
            if os.path.exists("data/appointments.csv"):
                appointments_df = pd.read_csv("data/appointments.csv", encoding='utf-8')
                unique_patients = appointments_df['patient_id'].nunique()
                report += f"\nPatients with Appointments: {unique_patients}\n"
            
            print(report)
            
            # Save to file
            report_file = f"{reports_dir}/patient_statistics_{timestamp}.txt"
            with open(report_file, 'w') as f:
                f.write(report)
            print(f"Report saved to: {report_file}\n")
        
        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice!")
            
    except Exception as e:
        print(f"Error generating reports: {e}")

def generate_data_profile():
    """Generate data profile/statistics for all datasets"""
    print("\n" + "-"*50)
    print(" GENERATE DATA PROFILE")
    print("-"*50)
    
    try:
        profile_dir = "analysis"
        if not os.path.exists(profile_dir):
            os.makedirs(profile_dir)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        profile_file = f"{profile_dir}/data_profile_{timestamp}.txt"
        
        profile = f"\n{'='*70}\n"
        profile += f" DATA PROFILE REPORT\n"
        profile += f" Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        profile += f"{'='*70}\n\n"
        
        # Doctors Profile
        if os.path.exists("data/doctors.csv"):
            doctors_df = pd.read_csv("data/doctors.csv", encoding='utf-8')
            profile += f"DOCTORS DATASET\n"
            profile += f"{'-'*70}\n"
            profile += f"Total Records: {len(doctors_df)}\n"
            profile += f"Columns: {', '.join(doctors_df.columns.tolist())}\n"
            profile += f"Specializations: {', '.join(doctors_df['specialization'].unique())}\n"
            profile += f"\n{doctors_df.describe().to_string() if not doctors_df.select_dtypes(include=['number']).empty else 'No numeric columns'}\n\n"
        
        # Patients Profile
        if os.path.exists("data/patients.csv"):
            patients_df = pd.read_csv("data/patients.csv", encoding='utf-8')
            profile += f"PATIENTS DATASET\n"
            profile += f"{'-'*70}\n"
            profile += f"Total Records: {len(patients_df)}\n"
            profile += f"Columns: {', '.join(patients_df.columns.tolist())}\n"
            profile += f"Age Range: {patients_df['age'].min()} - {patients_df['age'].max()} years\n"
            profile += f"Gender Distribution: {patients_df['gender'].value_counts().to_dict()}\n"
            profile += f"\n{patients_df.describe().to_string()}\n\n"
        
        # Admins Profile
        if os.path.exists("data/admins.csv"):
            admins_df = pd.read_csv("data/admins.csv", encoding='utf-8')
            profile += f"ADMINS DATASET\n"
            profile += f"{'-'*70}\n"
            profile += f"Total Records: {len(admins_df)}\n"
            profile += f"Columns: {', '.join(admins_df.columns.tolist())}\n\n"
        
        # Appointments Profile
        if os.path.exists("data/appointments.csv"):
            appointments_df = pd.read_csv("data/appointments.csv", encoding='utf-8')
            profile += f"APPOINTMENTS DATASET\n"
            profile += f"{'-'*70}\n"
            profile += f"Total Records: {len(appointments_df)}\n"
            profile += f"Columns: {', '.join(appointments_df.columns.tolist())}\n"
            profile += f"Status Distribution: {appointments_df['status'].value_counts().to_dict()}\n\n"
        else:
            profile += f"APPOINTMENTS DATASET\n"
            profile += f"{'-'*70}\n"
            profile += f"No appointment records yet.\n\n"
        
        # Disease Predictions Profile
        if os.path.exists("data/disease_predictions.csv"):
            predictions_df = pd.read_csv("data/disease_predictions.csv", encoding='utf-8')
            profile += f"DISEASE PREDICTIONS DATASET\n"
            profile += f"{'-'*70}\n"
            profile += f"Total Records: {len(predictions_df)}\n"
            profile += f"Columns: {', '.join(predictions_df.columns.tolist())}\n\n"
        
        print(profile)
        
        # Save to file
        with open(profile_file, 'w') as f:
            f.write(profile)
        print(f"Data profile saved to: {profile_file}\n")
        
    except Exception as e:
        print(f"Error generating data profile: {e}")

