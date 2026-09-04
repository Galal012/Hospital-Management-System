import pickle
import os
import people as pp
import buildings as bd

DATA_FILE = "hospital_state.pkl"

def save_app_state(persons: dict, buildings: dict, hc_module):
    """
    Serializes the current in-memory application state and internal class counters.
    """
    state = {
        "persons": persons,
        "buildings": buildings,
        "appointments": getattr(hc_module, 'appointments', []),
        "bills": getattr(hc_module, 'bills', []),
        # Save the exact state of all class counters
        "counters": {
            "patients": pp.Patient._Patient__number_of_patients,
            "doctors": pp.Doctor._Doctor__number_of_doctors,
            "nurses": pp.Nurse._Nurse__number_of_nurses,
            "admins": pp.Administrator._Administrator__number_of_administrator,
            "departments": bd.Department._Department__number_of_departments,
            "pharmacies": bd.Pharmacy._Pharmacy__number_of_pharmacies,
            "wards": bd.Ward._Ward__number_of_wards,
            "appointments": hc_module.Appointment._Appointment__number_of_appointments,
            "records": hc_module.MedicalRecord._MedicalRecord__number_of_records,
            "bills": hc_module.Billing._Billing__number_of_bills
        }
    }
    
    with open(DATA_FILE, "wb") as f:
        pickle.dump(state, f)


def load_app_state(persons: dict, buildings: dict, hc_module):
    """
    Deserializes the application state and restores internal class counters
    to prevent ID generation collisions.
    """
    if not os.path.exists(DATA_FILE):
        return  # No save file exists yet; start fresh.
        
    with open(DATA_FILE, "rb") as f:
        state = pickle.load(f)
        
    # Restore state by updating the existing dictionaries in place
    persons.update(state.get("persons", {}))
    buildings.update(state.get("buildings", {}))
    
    # Safely restore lists in place to maintain memory references
    if hasattr(hc_module, 'appointments'):
        hc_module.appointments.clear()
        hc_module.appointments.extend(state.get("appointments", []))
        
    if hasattr(hc_module, 'bills'):
        hc_module.bills.clear()
        hc_module.bills.extend(state.get("bills", []))

    # Restore the class-level counters so new IDs generate correctly
    counters = state.get("counters", {})
    if counters:
        pp.Patient._Patient__number_of_patients = counters.get("patients", 0)
        pp.Doctor._Doctor__number_of_doctors = counters.get("doctors", 0)
        pp.Nurse._Nurse__number_of_nurses = counters.get("nurses", 0)
        pp.Administrator._Administrator__number_of_administrator = counters.get("admins", 0)
        
        bd.Department._Department__number_of_departments = counters.get("departments", 0)
        bd.Pharmacy._Pharmacy__number_of_pharmacies = counters.get("pharmacies", 0)
        bd.Ward._Ward__number_of_wards = counters.get("wards", 0)
        
        hc_module.Appointment._Appointment__number_of_appointments = counters.get("appointments", 0)
        hc_module.MedicalRecord._MedicalRecord__number_of_records = counters.get("records", 0)
        hc_module.Billing._Billing__number_of_bills = counters.get("bills", 0)