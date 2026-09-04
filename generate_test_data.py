import people as pp
import buildings as bd
import helper_classes as hc
import data_manager

def generate_data():
    print("Generating fake hospital data...")

    # --- 1. Create People ---
    
    # Admin
    admin = pp.Administrator("Alice Boss", 45, "female")
    admin.add_contact_info("email", "admin@hospital.com")
    admin.add_security_info("email", "admin@hospital.com")
    admin.add_security_info("password", "password123")
    pp.persons.setdefault("admins", []).append(admin)

    # Doctors
    doc1 = pp.Doctor("Dr. Bob Smith", 50, "male", "Cardiology")
    doc1.add_contact_info("email", "doc1@hospital.com")
    doc1.add_security_info("email", "doc1@hospital.com")
    doc1.add_security_info("password", "password123")
    pp.persons.setdefault("doctors", []).append(doc1)

    doc2 = pp.Doctor("Dr. Clara Jones", 38, "female", "Neurology")
    doc2.add_contact_info("email", "doc2@hospital.com")
    doc2.add_security_info("email", "doc2@hospital.com")
    doc2.add_security_info("password", "password123")
    pp.persons.setdefault("doctors", []).append(doc2)

    # Nurses
    nurse1 = pp.Nurse("Nancy Joy", 28, "female")
    nurse1.add_contact_info("email", "nurse@hospital.com")
    nurse1.add_security_info("email", "nurse@hospital.com")
    nurse1.add_security_info("password", "password123")
    pp.persons.setdefault("nurses", []).append(nurse1)

    # Patients
    pat1 = pp.Patient("John Doe", 25, "male")
    pat1.add_contact_info("email", "patient1@hospital.com")
    pat1.add_security_info("email", "patient1@hospital.com")
    pat1.add_security_info("password", "password123")
    pat1.set_diagnosis("Mild Flu")
    pp.persons.setdefault("patients", []).append(pat1)

    pat2 = pp.Patient("Jane Roe", 30, "female")
    pat2.add_contact_info("email", "patient2@hospital.com")
    pat2.add_security_info("email", "patient2@hospital.com")
    pat2.add_security_info("password", "password123")
    pp.persons.setdefault("patients", []).append(pat2)

    # --- 2. Create Buildings ---

    # Departments
    dep1 = bd.Department("Cardiology", ["ECG", "Echocardiogram", "Heart Surgery"])
    dep1.set_head_of_department("Dr. Bob Smith")
    dep1.add_doctor(doc1)
    pp.buildings.setdefault("departments", []).append(dep1)

    # Pharmacy
    pharm = bd.Pharmacy("Main Hospital Pharmacy", "Pharma Pete")
    pharm.add_medicine_stock("paracetamol", 500)
    pharm.add_medicine_stock("amoxicillin", 150)
    pharm.add_medicine_stock("ibuprofen", 300)
    pp.buildings.setdefault("pharmacies", []).append(pharm)

    # Wards
    ward1 = bd.Ward("ICU")
    ward1.assign_room(pat1) # Assign John Doe to ICU
    pp.buildings.setdefault("wards", []).append(ward1)

    ward2 = bd.Ward("General")
    pp.buildings.setdefault("wards", []).append(ward2)

    # --- 3. Save it all to the pickle file ---
    data_manager.save_app_state(pp.persons, pp.buildings, hc)
    print("Test data successfully generated and saved to hospital_state.pkl!")

if __name__ == "__main__":
    generate_data()