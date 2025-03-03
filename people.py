from typing import Dict, List
from datetime import datetime
import re

class IDGenerator:
    _id_counters = {
        'PAT': 0,  
        'DOC': 0,  
        'NUR': 0,  
        'ADM': 0   
    }
    
    @classmethod
    def generate_id(cls, person_type: str) -> str:
        """
        Generate a unique ID based on person type.
        Format: [TYPE]-[YEAR]-[SEQUENCE]
        """
        prefix = person_type[:3].upper()
        
        if prefix in cls._id_counters:
            cls._id_counters[prefix] += 1
        else:
            cls._id_counters[prefix] = 1
            
        year = datetime.now().year
        
        return f"{prefix}-{year}-{cls._id_counters[prefix]:04d}"

class Person(IDGenerator):
    def __init__(self, name: str, age: int, gender: str, contact_info: Dict) -> None:
        self._name: str = name
        self._age: int = age
        self._gender: str = gender
        self._contact_info: Dict = contact_info
        self._id = None
    
    def get_name(self) -> str:
        return self._name
    def get_age(self) -> int:
        return self._age
    def get_gender(self) -> str:
        return self._gender
    def get_contact_info(self) -> Dict:
        return self._contact_info
    def get_id(self) -> str:
        return self._id
    
    def set_name(self, name) -> None:
        self._name = name
    def set_age(self, age) -> None:
        self._age = age if age >= 0 else ValueError('Age not valid')
    def set_gender(self, gender) -> None:
        self._gender = gender
    def set_contact_info(self, contact_info) -> None:
        self._contact_info = contact_info

class Patient(Person):
    def __init__(self, name, age, gender, contact_info, assigned_doctor=None, medical_history=None):
        super().__init__(name, age, gender, contact_info)
        self._id = self.generate_id("PAT")
        self._medical_history: Dict = medical_history or {}
        self._assigned_doctor = assigned_doctor
    
    def view_medical_history(self) -> None:
        print(self._medical_history)
    
    def book_appointment(self, day, doctor) -> None:
        return self._medical_history.update((day, doctor))
    
    def get_patient_info(self) -> tuple[str, int, str]:
        return (self.get_name(), self.get_age(), self.get_id())

class Doctor(Person):
    def __init__(self, name, age, gender, contact_info, specialization=None, available_slots=None, patients_list=None):
        super().__init__(name, age, gender, contact_info)
        self._id = self.generate_id("DOC")
        self._specialization = specialization
        self._available_slots = available_slots or []
        self._patients_list = patients_list or []
    
    def diagnose_patient(self, patient):
        diagnose = ()
        return patient._medical_history((datetime.now(), self.get_name(), diagnose))
    
    def prescribe_medication(self, patient, medication):
        return (self.get_name(), patient.get_name(), medication)
    
    def view_patient_records(self, patient):
        return patient.view_medical_history()

class Nurse(Person):
    def __init__(self, name, age, gender, contact_info, assigned_ward=None, patients_assigned=None):
        super().__init__(name, age, gender, contact_info)
        self._id = self.generate_id("NUR")
        self._assigned_ward = assigned_ward
        self._patients_assigned: List = patients_assigned or []
    
    def assist_doctor(self, doctor):
        return (self.get_name(), doctor.get_name(), datetime.now())
    
    def record_vitals(self, vitals:List):
        return vitals
    
    def update_patient_statues(self, patient):
        statues = []
        return statues

class Administrator(Person):
    def __init__(self, name, age, gender, contact_info):
        super().__init__(name, age, gender, contact_info)
        self._id = self.generate_id("ADM")
# iam testing braah
#contact_info = {"phone": "123-456-7890", "email": "john@example.com"}
#patient1 = Patient("John Doe", 35, "Male", contact_info)
#print(f"Patient ID: {patient1.get_id()}")  

#doctor1 = Doctor("Jane Smith", 40, "Female", {"phone": "123-555-9876"}, "Cardiology")
#print(f"Doctor ID: {doctor1.get_id()}")  

nurse1 = Nurse("Mark Johnson", 28, "Male", {"phone": "555-1234"}, "Emergency")
print(f"Nurse ID: {nurse1.get_id()}")  
