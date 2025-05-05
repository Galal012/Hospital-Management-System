CREATE TABLE 'Patient' (
    'patient_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'name' TEXT NOT NULL,
    'age' INTEGER CHECK('age' > 0),
    'gender' TEXT CHECK('gender' IN ('male', 'female')),
    'contact_info' TEXT NOT NULL,
    'security_info' TEXT NOT NULL,
    'diagnosis' TEXT,
    'prescribed_treatment' TEXT,
    'assigned_doctor' TEXT
);

CREATE TABLE 'Doctor' (
    'doctor_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'name' TEXT NOT NULL,
    'age' INTEGER CHECK('age' >= 18),
    'gender' TEXT CHECK('gender' IN ('male', 'female')),
    'contact_info' TEXT NOT NULL,
    'security_info' TEXT NOT NULL,
    'specialization' TEXT NOT NULL,
    'patient_list' TEXT
);

CREATE TABLE 'Administrator' (
    'admin_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'name' TEXT NOT NULL,
    'age' INTEGER CHECK('age' >= 18),
    'gender' TEXT CHECK('gender' IN ('male', 'female')),
    'contact_info' TEXT NOT NULL,
    'security_info' TEXT NOT NULL
);

CREATE TABLE 'Nurse' (
    'nurse_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'name' TEXT NOT NULL,
    'assigned_ward' INTEGER REFERENCES 'Ward'('room_id'),
    'contact_info' TEXT
);

CREATE TABLE 'Vitals' (
    'vital_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'patient_id' INTEGER NOT NULL REFERENCES 'Patient'('patient_id'),
    'nurse_id' INTEGER NOT NULL REFERENCES 'Nurse'('nurse_id'),
    'timestamp' DATETIME DEFAULT CURRENT_TIMESTAMP,
    'blood_pressure' TEXT,
    'heart_rate' INTEGER,
    'temperature' REAL
);

CREATE TABLE 'Appointment' (
    'appointment_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'patient_id' INTEGER NOT NULL REFERENCES 'Patient'('patient_id'),
    'doctor_id' INTEGER NOT NULL REFERENCES 'Doctor'('doctor_id'),
    'date' DATE NOT NULL,
    'time' TIME NOT NULL,
    'status' TEXT CHECK('status' IN ('scheduled', 'completed', 'cancelled')) DEFAULT 'scheduled'
);

CREATE TABLE 'Department' (
    'department_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' TEXT NOT NULL,
    'head_of_department' INTEGER REFERENCES 'Doctor'('doctor_id'),
    'services_offered' TEXT
);

CREATE TABLE 'Medicine' (
    'medicine_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' TEXT NOT NULL UNIQUE,
    'stock' INTEGER DEFAULT 0 CHECK('stock' >= 0),
    'expiry_date' DATE
);

CREATE TABLE 'Prescription' (
    'prescription_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'patient_id' INTEGER NOT NULL REFERENCES 'Patient'('patient_id'),
    'doctor_id' INTEGER NOT NULL REFERENCES 'Doctor'('doctor_id'),
    'medicine_id' INTEGER NOT NULL REFERENCES 'Medicine'('medicine_id'),
    'dosage' TEXT NOT NULL,
    'date_prescribed' DATE DEFAULT CURRENT_DATE
);

CREATE TABLE 'MedicalRecord' (
    'record_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'patient_id' INTEGER NOT NULL REFERENCES 'Patient'('patient_id'),
    'doctor_id' INTEGER NOT NULL REFERENCES 'Doctor'('doctor_id'),
    'diagnosis' TEXT NOT NULL,
    'prescribed_treatment' TEXT NOT NULL,
    'test_results' TEXT,
    'record_date' DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE 'Ward' (
    'room_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'type' TEXT CHECK(type IN ('ICU', 'general', 'private')) NOT NULL,
    'availability' BOOLEAN DEFAULT TRUE,
    'assigned_patient' INTEGER REFERENCES 'Patient'('patient_id')
);

CREATE TABLE 'Billing' (
    'bill_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'patient_id' INTEGER NOT NULL REFERENCES 'Patient'('patient_id'),
    'treatment_cost' REAL DEFAULT 0.0 CHECK('treatment_cost' >= 0),
    'medicine_cost' REAL DEFAULT 0.0 CHECK('medicine_cost' >= 0),
    'total_amount' REAL GENERATED ALWAYS AS ('treatment_cost' + 'medicine_cost') STORED,
    'payment_status' TEXT CHECK('payment_status' IN ('paid', 'unpaid')) DEFAULT 'unpaid',
    'date_issued' DATE DEFAULT CURRENT_DATE
);

-- Indexes for frequently queried fields
CREATE INDEX idx_patient_name ON Patient(name);
CREATE INDEX idx_doctor_specialization ON Doctor(specialization);
CREATE INDEX idx_appointment_date ON Appointment(date);
CREATE INDEX idx_medicine_stock ON Medicine(stock);

-- sqlite3 hospital.db < schema.sql