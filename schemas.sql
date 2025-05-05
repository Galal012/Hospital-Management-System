CREATE TABLE IF NOT EXISTS 'Patient' (
    'patient_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'name' TEXT NOT NULL,
    'age' INTEGER,
    'gender' TEXT,
    'contact_info' TEXT NOT NULL,
    'security_info' TEXT NOT NULL,
    'diagnosis' TEXT,
    'prescribed_treatment' TEXT,
    'assigned_doctor' TEXT
);

CREATE TABLE IF NOT EXISTS 'Doctor' (
    'doctor_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'name' TEXT NOT NULL,
    'age' INTEGER,
    'gender' TEXT,
    'contact_info' TEXT NOT NULL,
    'security_info' TEXT NOT NULL,
    'specialization' TEXT NOT NULL,
    'patient_list' TEXT
);

CREATE TABLE IF NOT EXISTS 'Administrator' (
    'admin_id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'app_id' TEXT UNIQUE NOT NULL,
    'name' TEXT NOT NULL,
    'age' INTEGER,
    'gender' TEXT,
    'contact_info' TEXT NOT NULL,
    'security_info' TEXT NOT NULL
);