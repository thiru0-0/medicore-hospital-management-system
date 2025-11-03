# 🏥 Medicore - Hospital Management System

A comprehensive menu-driven Hospital Management System built with Python, featuring role-based access control for patients, doctors, and administrators. The system provides appointment management, patient records, diagnosis tracking, and administrative tools with AI-powered disease prediction capabilities (under development).

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Login Credentials](#login-credentials)
- [Features Breakdown](#features-breakdown)
- [Development Status](#development-status)
- [Contributing](#contributing)
- [License](#license)

---

## ✨ Features

### 👤 **Patient Portal**
- 🔐 Secure login system
- 📅 **Book Appointments** - Schedule appointments with available doctors
- 🤖 **Disease Prediction** - AI-powered symptom checker for disease prediction *(Under Development)*
- 📜 **View Appointment History** - Access all past and upcoming appointments with diagnosis and prescriptions

### 👨‍⚕️ **Doctor Portal**
- 🔐 Secure login system
- 👥 **View Patient List** - See all patients assigned to you with their appointment details
- 📝 **Add Diagnosis** - Add diagnosis and prescription for patient appointments
- ✅ **Manage Appointments** - Update appointment status (Scheduled → Completed)

### 👨‍💼 **Admin Portal**
- 🔐 Secure login system
- ➕ **Add Doctors** - Register new doctors to the system (auto-generates doctor IDs)
- 📊 **Generate Reports** - Create comprehensive reports:
  - Appointment Summary
  - Doctor Performance Analysis
  - Patient Statistics
- 📈 **Generate Data Profile** - Comprehensive data profiling and statistics for all datasets

---

## 🛠️ Tech Stack

### Core Technologies
- **Python 3.13+** - Programming language
- **Pandas** - Data manipulation and CSV operations
- **NumPy** - Numerical computing

### Machine Learning & Data Science
- **scikit-learn** - Machine learning library for disease prediction
  - RandomForestClassifier for disease prediction
  - Model training and evaluation utilities
- **Matplotlib** - Data visualization (for analysis notebooks)
- **Seaborn** - Statistical data visualization (for analysis notebooks)

### Data Storage
- **CSV Files** - Flat file database for:
  - User credentials (patients, doctors, admins)
  - Appointments
  - Disease predictions
  - Disease symptoms dataset
  - Disease precautions dataset

### Development Tools
- **Jupyter Notebook** - Data analysis and model development
- **Standard Library Modules**:
  - `os` - File operations
  - `datetime` - Date and time handling
  - `re` - Regular expressions for data processing
  - `pickle` - Model serialization
  - `sys` - System-specific parameters

---

## 📁 Project Structure

```
Hospital_Management_System/
│
├── src/                          # Source code directory
│   ├── main.py                  # Main entry point and login system
│   ├── patient.py               # Patient portal functions
│   ├── doctor.py                # Doctor portal functions
│   ├── admin.py                 # Admin portal functions
│   ├── model_utils.py           # ML model utilities (loading, training)
│   └── symptom_checker.py       # Interactive symptom checker
│
├── data/                         # Data files directory
│   ├── patients.csv             # Patient credentials and information
│   ├── doctors.csv              # Doctor credentials and information
│   ├── admins.csv               # Admin credentials and information
│   ├── appointments.csv         # Appointment records
│   ├── disease_predictions.csv  # Disease prediction history
│   ├── DiseaseAndSymptoms.csv   # Disease symptoms dataset
│   └── Disease precaution.csv   # Disease precautions dataset
│
├── analysis/                     # Analysis and ML model development
│   ├── Symptoms_Prediction_&_Precautions.ipynb  # ML model notebook
│   └── save_model.py            # Script to train and save ML model
│
├── README.md                     # Project documentation (this file)
└── requirements.txt              # Python dependencies (to be created)

```

---

## 🚀 Installation

### Prerequisites
- Python 3.13 or higher
- pip (Python package manager)

### Step 1: Clone or Download the Project
```bash
cd /path/to/your/projects
# Download or clone the project directory
```

### Step 2: Install Dependencies
```bash
# Navigate to project directory
cd Hospital_Management_System

# Install required packages
pip install pandas numpy scikit-learn matplotlib seaborn
```

Or install from requirements.txt (if available):
```bash
pip install -r requirements.txt
```

### Step 3: Verify Installation
```bash
python -c "import pandas, numpy, sklearn; print('All packages installed successfully!')"
```

---

## 💻 Usage

### Running the Application

1. **Navigate to project directory:**
   ```bash
   cd Hospital_Management_System
   ```

2. **Run the main application:**
   ```bash
   python src/main.py
   ```
   Or:
   ```bash
   python3 src/main.py
   ```

3. **Follow the menu prompts:**
   - Select your portal (Patient/Doctor/Admin)
   - Enter your credentials
   - Access your respective menu

### First Time Setup

1. **Train the ML Model (Optional - for disease prediction):**
   ```bash
   cd analysis
   python save_model.py
   ```
   This will create:
   - `data/disease_prediction_model.pkl` - Trained model
   - `data/symptom_encoder.pkl` - Encoder information

2. **Start using the system:**
   ```bash
   python src/main.py
   ```

---

## 🔐 Login Credentials

### Patient Portal
| Username | Password | Patient ID |
|----------|----------|------------|
| `john_doe` | `pat123` | PAT001 |
| `priya_98` | `pat456` | PAT002 |
| `arun_v` | `pat789` | PAT003 |

### Doctor Portal
| Username | Password | Doctor ID |
|----------|----------|-----------|
| `drraj` | `doc123` | DOC001 |
| `drsneha` | `doc456` | DOC002 |
| `drarun` | `doc789` | DOC003 |

### Admin Portal
| Username | Password | Admin ID |
|----------|----------|----------|
| `admin1` | `admin123` | ADM001 |
| `superadmin` | `super123` | ADM002 |

---

## 📖 Features Breakdown

### Patient Portal Features

#### 1. Book Appointment
- View all available doctors with their specializations
- Select a doctor
- Choose appointment date and time
- Provide reason for appointment
- Appointment is saved with status "Scheduled"
- Auto-generates unique appointment ID

#### 2. Predict Disease *(Under Development)*
- **Interactive Chat Mode**: AI asks about symptoms one by one
- **Quick Mode**: Enter symptoms all at once
- Uses trained RandomForestClassifier model
- Provides disease prediction with confidence score
- Displays recommended precautions
- Saves prediction history

#### 3. View Appointment History
- View all appointments (past and upcoming)
- See doctor details, date, time, reason
- View diagnosis and prescriptions (if completed)
- Check appointment status

### Doctor Portal Features

#### 1. View Patient List
- See all patients assigned to you
- View patient details (name, age, gender, contact)
- See appointment count per patient
- View upcoming scheduled appointments
- Filter by appointment status

#### 2. Add Diagnosis
- View all scheduled appointments
- Select an appointment to diagnose
- Enter diagnosis details
- Enter prescription
- Update appointment status to "Completed"

### Admin Portal Features

#### 1. Add Doctor
- Auto-generates consecutive doctor IDs (DOC001, DOC002, ...)
- Validates doctor ID and username uniqueness
- Add doctor details:
  - Doctor ID (auto-generated)
  - Username and password
  - Name, specialization
  - Availability schedule
  - Contact information

#### 2. Generate Reports
- **Appointment Summary**:
  - Total appointments
  - Scheduled vs Completed counts
  - Appointments by doctor
- **Doctor Performance**:
  - Appointments per doctor
  - Completion rates
- **Patient Statistics**:
  - Total patients
  - Gender distribution
  - Age statistics
  - Patients with appointments

#### 3. Generate Data Profile
- Comprehensive statistics for all datasets
- Column information
- Data quality metrics
- Distribution analysis
- Saves to `analysis/` directory

---

## 🔄 Development Status

### ✅ Completed Features
- ✅ User authentication (Patient, Doctor, Admin)
- ✅ Appointment booking system
- ✅ Appointment history viewing
- ✅ Doctor-patient management
- ✅ Diagnosis and prescription system
- ✅ Admin doctor registration
- ✅ Report generation
- ✅ Data profiling
- ✅ ML model training infrastructure
- ✅ Interactive symptom checker interface

### 🚧 Under Development

#### Disease Prediction Module
- ⏳ **AI-Powered Disease Prediction** - Currently in development
  - Model training and evaluation completed
  - Integration with patient portal in progress
  - Interactive symptom checker interface ready
  - Full prediction pipeline coming soon

**Status**: The disease prediction feature is currently being refined and will be fully functional in the next update. The ML model is trained and ready, but the integration with the patient portal requires additional testing and optimization.

### 🔮 Future Enhancements
- [ ] Appointment cancellation
- [ ] Appointment rescheduling
- [ ] Patient profile updates
- [ ] Email notifications
- [ ] Database integration (SQLite/PostgreSQL)
- [ ] Web interface
- [ ] API development
- [ ] Mobile app support

---

## 📊 System Workflow

```
Main Menu
    │
    ├── Patient Portal
    │   ├── Login
    │   ├── Book Appointment
    │   ├── Predict Disease (Under Development)
    │   └── View History
    │
    ├── Doctor Portal
    │   ├── Login
    │   ├── View Patients
    │   └── Add Diagnosis
    │
    └── Admin Portal
        ├── Login
        ├── Add Doctor
        ├── Generate Reports
        └── Data Profile
```

---

## 🔧 Technical Details

### Data Management
- **CSV-based storage** - All data stored in CSV files
- **UTF-8 encoding** - Proper handling of special characters
- **Automatic ID generation** - Sequential IDs for doctors
- **Data validation** - Prevents duplicate entries

### Security
- **Password-based authentication** - Username/password login
- **Role-based access control** - Different portals for different roles
- **Session management** - User sessions maintained during usage

### Machine Learning
- **Model**: RandomForestClassifier
- **Training**: Jupyter notebook with data preprocessing
- **Features**: One-hot encoded symptoms
- **Accuracy**: High accuracy on training data
- **Storage**: Pickle format (.pkl files)

---

## 🐛 Troubleshooting

### Common Issues

1. **ModuleNotFoundError for sklearn**
   ```bash
   pip install scikit-learn
   ```

2. **CSV file encoding errors**
   - All CSV operations use UTF-8 encoding
   - Check if files are saved in UTF-8 format

3. **Import errors**
   - Make sure you're running from the project root directory
   - Check that `src/` directory is in Python path

4. **Model not found**
   - Run `analysis/save_model.py` to train and save the model
   - Ensure model files are in `data/` directory

---

## 🤝 Contributing

Contributions are welcome! Please feel free to:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📝 License

This project is open source and available for educational purposes.

---

## 👤 Author

**Medicore Development Team**

---

## 📞 Support

For issues, questions, or suggestions:
- Check the troubleshooting section
- Review the code documentation
- Open an issue on the repository

---

## 🙏 Acknowledgments

- scikit-learn community for ML tools
- Pandas team for data manipulation libraries
- Python community for excellent documentation

---

**Note**: This is an educational project demonstrating CRUD operations, menu-driven interfaces, and ML integration in a hospital management context. Always consult healthcare professionals for medical advice.

---

**Made with ❤️ for Healthcare Management**

