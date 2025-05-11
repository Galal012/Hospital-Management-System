import sqlite3
from typing import Optional


# Database connection singleton
class DatabaseConnection:
    _connection = None

    @staticmethod
    def get_db_connection():
        if DatabaseConnection._connection is None:
            DatabaseConnection._connection = sqlite3.connect('hospital.db')
            DatabaseConnection._connection.row_factory = sqlite3.Row
        return DatabaseConnection._connection

class DBHandler:
    @staticmethod
    def create_tables():
        conn = DatabaseConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
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
                ''')

        cursor.execute('''
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
                ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS 'Administrator' (
                'admin_id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'app_id' TEXT UNIQUE NOT NULL,
                'name' TEXT NOT NULL,
                'age' INTEGER,
                'gender' TEXT,
                'contact_info' TEXT NOT NULL,
                'security_info' TEXT NOT NULL
            );
                ''')

        cursor.execute('''
                CREATE TABLE IF NOT EXISTS 'MedicalRecord' (
                'record_id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'app_id' TEXT UNIQUE NOT NULL,
                'patient_id' TEXT NOT NULL,
                'doctor_id' TEXT NOT NULL,
                'diagnosis' TEXT NOT NULL,
                'prescribed_treatment' TEXT NOT NULL,
                'test_results' TEXT NOT NULL,
                'date' TEXT NOT NULL,
                'time' TEXT NOT NULL
            );
                ''')
        conn.commit()

    @staticmethod
    def get_db_id(table: str, app_id: str) -> Optional[int]:
        """Get database ID from application-generated ID"""
        conn = DatabaseConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT rowid FROM {table} WHERE app_id = ?', (app_id,))
        result = cursor.fetchone()
        return result[0] if result else None


    @staticmethod
    def insert_patient(patient: 'Patient'):
        conn = DatabaseConnection.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Patient (app_id, name, age, gender, contact_info, security_info,
                diagnosis, prescribed_treatment, assigned_doctor)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                patient.get_id(),
                patient.get_name(),
                patient.get_age(),
                patient.get_gender(),
                f"{patient.get_contact_info()["email"]},{patient.get_contact_info()["phone_number"]}",
                f"{patient.get_security_info()["email"]},{patient.get_security_info()["password"]}",
                patient.get_diagnosis(),
                patient.get_prescribed_treatment(),
                patient.get_assigned_doctor()
            ))
            conn.commit()
        finally:
            pass

    @staticmethod
    def insert_doctor(doctor: 'Doctor'):
        conn = DatabaseConnection.get_db_connection()
        try:
            patient_list = ""
            for p in doctor.get_patient_list():
                patient_list += f"{p.get_id()}:"
            patient_list = patient_list[:-1]

            cursor = conn.cursor()
            cursor.execute('''
                            INSERT INTO Doctor (app_id, name, age, gender, contact_info, security_info,
                            specialization, patient_list)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ''', (
                doctor.get_id(),
                doctor.get_name(),
                doctor.get_age(),
                doctor.get_gender(),
                f"{doctor.get_contact_info()["email"]},{doctor.get_contact_info()["phone_number"]}",
                f"{doctor.get_security_info()["email"]},{doctor.get_security_info()["password"]}",
                doctor.get_specialization(),
                patient_list
            ))
            conn.commit()
        finally:
            pass

    @staticmethod
    def insert_administrator(admin: 'Administrator'):
        conn = DatabaseConnection.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                            INSERT INTO Administrator (app_id, name, age, gender, contact_info, security_info)
                            VALUES (?, ?, ?, ?, ?, ?)
                        ''', (
                admin.get_id(),
                admin.get_name(),
                admin.get_age(),
                admin.get_gender(),
                f"{admin.get_contact_info()["email"]},{admin.get_contact_info()["phone_number"]}",
                f"{admin.get_security_info()["email"]},{admin.get_security_info()["password"]}"
            ))
            conn.commit()
        finally:
            pass

    @staticmethod
    def insert_medical_record(record, patient_id):
        conn = DatabaseConnection.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                                INSERT INTO MedicalRecord (app_id, patient_id, doctor_id, diagnosis,
                                prescribed_treatment, test_results, date, time)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (
                record.get_record_id(),
                record.get_patient().get_id(),
                record.get_doctor().get_id(),
                record.get_diagnosis(),
                record.get_prescribed_treatment(),
                record.get_test_results(),
                record.get_date(),
                record.get_time(),
            ))
            conn.commit()
        finally:
            pass

    @staticmethod
    def get_table(table):
        conn = DatabaseConnection.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table}')
        result = cursor.fetchall()
        return result