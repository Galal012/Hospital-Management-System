from people import *
from buildings import *
from helper_classes import Appointment
import sqlite3
from typing import Optional

# Database connection singleton
def get_db_connection():
    conn = sqlite3.connect('hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

class DBHandler:
    @staticmethod
    def get_db_id(table: str, app_id: str) -> Optional[int]:
        """Get database ID from application-generated ID"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT rowid FROM {table} WHERE app_id = ?', (app_id,))
        result = cursor.fetchone()
        conn.close()
        return result[0] if result else None


    @staticmethod
    def insert_patient(patient: 'Patient'):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Patient (app_id, name, age, gender, contact_info, assigned_doctor)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                patient.get_id(),
                patient.get_name(),
                patient.get_age(),
                patient.get_gender(),
                str(patient.get_contact_info()),
                DBHandler.get_db_id('Doctor', patient._assigned_doctor) if patient._assigned_doctor else None
            ))
            # Insert medical records
            for record in patient._medical_history:
                DBHandler.insert_medical_record(record)
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_doctor(doctor: 'Doctor'):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Doctor (app_id, name, specialization, contact_info, department_id)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                doctor.get_id(),
                doctor.get_name(),
                doctor._specialization,
                str(doctor.get_contact_info()),
                DBHandler.get_db_id('Department', doctor._department_id) if hasattr(doctor, '_department_id') else None
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_nurse(nurse: 'Nurse'):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Nurse (app_id, name, assigned_ward, contact_info)
                VALUES (?, ?, ?, ?)
            ''', (
                nurse.get_id(),
                nurse.get_name(),
                DBHandler.get_db_id('Ward', nurse._assigned_ward) if nurse._assigned_ward else None,
                str(nurse.get_contact_info())
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_administrator(admin: 'Administrator'):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Administrator (app_id, name, role, contact_info)
                VALUES (?, ?, ?, ?)
            ''', (
                admin.get_id(),
                admin.get_name(),
                'System Administrator',  # Default role
                str(admin.get_contact_info())
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_medical_record(record: 'MedicalRecord'):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO MedicalRecord (
                    app_id, patient_id, doctor_id, diagnosis, 
                    prescribed_treatment, test_results, record_date
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                record._id,
                DBHandler.get_db_id('Patient', record._patient.get_id()),
                DBHandler.get_db_id('Doctor', record._doctor.get_id()),
                record._diagnosis,
                record._prescribed_treatment,
                record._test_results,
                f"{record._date} {record._time}"
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_appointment(appointment: 'Appointment'):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Appointment (
                    app_id, patient_id, doctor_id, date, time, status
                ) VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                appointment._id,
                DBHandler.get_db_id('Patient', appointment._patient.get_id()),
                DBHandler.get_db_id('Doctor', appointment._doctor.get_id()),
                appointment._date.date().isoformat(),
                appointment._time.strftime("%H:%M"),
                appointment._status
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_ward(ward):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Ward (app_id, type, availability, assigned_patient)
                VALUES (?, ?, ?, ?)
            ''', (
                ward.id,
                ward.room_type,
                ward.avilablitity,
                DBHandler.get_db_id('Patient', ward.patient.get_id()) if ward.patient else None
            ))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_medicine(medicine: dict):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Medicine (name, stock)
                VALUES (?, ?)
            ''', (medicine['name'], medicine['stock']))
            conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_prescription(prescription: dict):
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO Prescription (
                    patient_id, doctor_id, medicine_id, dosage, date_prescribed
                ) VALUES (?, ?, ?, ?, ?)
            ''', (
                DBHandler.get_db_id('Patient', prescription['patient_id']),
                DBHandler.get_db_id('Doctor', prescription['doctor_id']),
                prescription['medicine_id'],
                prescription['dosage'],
                prescription['date_prescribed']
            ))
            conn.commit()
        finally:
            conn.close()