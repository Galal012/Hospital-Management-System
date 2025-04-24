CREATE TABLE 'Patient' (
    'patient_id' INTEGER PRIMARY KEY,
    'name' TEXT NOT NULL,
    'age' INTEGER,
    'gender' TEXT,
    'medical_history' INTEGER REFERENCES 'MedicalRecord'('record_id'),
    'contact_info' TEXT,
    'assigned_doctor' INTEGER REFERENCES 'Doctor'('doctor_id')
);

CREATE TABLE 'Doctor' (
    'doctor_id' INTEGER PRIMARY KEY,
    'name' TEXT NOT NULL,
    'specialization' TEXT,
    'contact_info' TEXT,
    'department_id' INTEGER REFERENCES 'Department'('department_id')
);

CREATE TABLE 'Nurse' (
    'nurse_id' INTEGER PRIMARY KEY,
    'name' TEXT NOT NULL,
    'assigned_ward' INTEGER REFERENCES 'Ward'('room_id'),
    'contact_info' TEXT
);

-- Appointment System
CREATE TABLE 'Appointment' (
    'appointment_id' INTEGER PRIMARY KEY,
    'patient_id' INTEGER REFERENCES 'Patient'('patient_id'),
    'doctor_id' INTEGER REFERENCES 'Doctor'('doctor_id'),
    'date' DATE,
    'time' TIME,
    'status' TEXT CHECK(status IN ('scheduled', 'completed', 'cancelled'))
);

-- Department Structure
CREATE TABLE 'Department' (
    'department_id' INTEGER PRIMARY KEY,
    'name' TEXT NOT NULL,
    'head_of_department' INTEGER REFERENCES 'Doctor'('doctor_id'),
    'services_offered' TEXT
);

-- Pharmacy System
CREATE TABLE 'Medicine' (
    'medicine_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'name' TEXT NOT NULL,
    'stock' INTEGER DEFAULT 0
);

CREATE TABLE Prescription (
    'prescription_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'patient_id' INTEGER REFERENCES 'Patient'('patient_id'),
    'doctor_id' INTEGER REFERENCES 'Doctor'('doctor_id'),
    'medicine_id' INTEGER REFERENCES 'Medicine'('medicine_id'),
    'dosage' TEXT,
    'date_prescribed' DATE
);

-- Medical Records
CREATE TABLE 'MedicalRecord' (
    'record_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'patient_id' INTEGER REFERENCES 'Patient'('patient_id'),
    'doctor_id' INTEGER REFERENCES 'Doctor'('doctor_id'),
    'diagnosis' TEXT,
    'prescribed_treatment' TEXT,
    'test_results' TEXT,
    'record_date' DATE
);

-- Billing Syste
-- will use transactions later
CREATE TABLE 'Bill' (
    'bill_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'patient_id' INTEGER REFERENCES 'Patient'('patient_id'),
    'treatment_cost' REAL,
    'medicine_cost' REAL,
    'total_amount' REAL GENERATED ALWAYS AS (treatment_cost + medicine_cost) STORED,
    'payment_status' TEXT CHECK('payment_status' IN ('paid', 'unpaid'))
);

-- Ward Management
CREATE TABLE 'Ward' (
    'room_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'type' TEXT CHECK(type IN ('icu', 'general', 'private')),
    'availability' BOOLEAN DEFAULT 1,
    'assigned_patient' INTEGER REFERENCES 'Patient'('patient_id')
);

-- Administrator
CREATE TABLE 'Administrator' (
    'admin_id' INTEGER PRIMARY KEY,
    'name' TEXT NOT NULL,
    'role' TEXT NOT NULL,
    'contact_info' TEXT
);
