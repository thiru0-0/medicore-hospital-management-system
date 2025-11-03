import pandas as pd
import os
import sys

# Add src directory to Python path for imports (works when running as script)
src_dir = os.path.dirname(os.path.abspath(__file__))
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Also add parent directory to path for relative imports
parent_dir = os.path.dirname(src_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from patient import patient_menu
from doctor import doctor_menu
from admin import admin_menu

def main_menu():
    """Display the main menu and handle role selection"""
    while True:
        print("\n" + "="*50)
        print(" " * 10 + "Medicore - Hospital Management System")
        print("="*50)
        print("1. Patient Portal")
        print("2. Doctor Portal")
        print("3. Admin Portal")
        print("4. Exit")
        print("="*50)
        
        try:
            choice = input("Enter your choice: ").strip()
            
            if choice == '1':
                role = 'patient'
                user_id = login_user(role)
                if user_id:
                    patient_menu(user_id)
            elif choice == '2':
                role = 'doctor'
                user_id = login_user(role)
                if user_id:
                    doctor_menu(user_id)
            elif choice == '3':
                role = 'admin'
                user_id = login_user(role)
                if user_id:
                    admin_menu()
            elif choice == '4':
                print("Thank you for using Medicore!")
                break
            else:
                print("Invalid choice! Please try again.")
        except KeyboardInterrupt:
            print("\n\nExiting...")
            break
        except Exception as e:
            print(f"An error occurred: {e}")

def login_user(role):
    """Handle login for different roles (patient, doctor, admin)"""
    print("\n" + "-"*50)
    print(f" {role.upper()} PORTAL - LOGIN")
    print("-"*50)
    
    # Get CSV file path based on role
    csv_file = f"data/{role}s.csv"
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return None
    
    try:
        # Read the CSV file with explicit UTF-8 encoding
        df = pd.read_csv(csv_file, encoding='utf-8')
        
        # Get credentials from user
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        # Find user based on role
        if role == 'patient':
            user = df[(df['username'] == username) & (df['password'] == password)]
            user_id_col = 'patient_id'
        elif role == 'doctor':
            user = df[(df['username'] == username) & (df['password'] == password)]
            user_id_col = 'doctor_id'
        elif role == 'admin':
            user = df[(df['username'] == username) & (df['password'] == password)]
            user_id_col = 'admin_id'
        
        if not user.empty:
            user_id = user.iloc[0][user_id_col]
            print(f"\n✓ Login successful! Welcome, {username}")
            return user_id
        else:
            print("\n✗ Invalid username or password!")
            return None
            
    except Exception as e:
        print(f"Error during login: {e}")
        return None

if __name__ == "__main__":
    main_menu()
