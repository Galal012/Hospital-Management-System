from typing import Dict, List
from datetime import datetime
from helper_classes import *

class Person():
    def __init__(self, name: str, age: int, gender: str, contact_info: Dict, ID: int) -> None:
        self._name: str = name
        self._age: int = age
        self._gender: str = gender
        self._contact_info: Dict = contact_info
        self._id = ID
    
    #getter methods
    def get_name(self) -> str:
        return self._name
    def get_age(self) -> int:
        return self._age
    def get_gender(self) -> str:
        return self._gender
    def get_contact_info(self) -> Dict:
        return self._contact_info
    def get_id(self) -> int:
        return self._id

    #setter methods
    def set_name(self, name) -> None:
        self._name = name
    def set_age(self, age) -> None:
        self._age = age if age >= 0 else ValueError('Age not valid')
    def set_gender(self, gender) -> None:
        self._gender = gender
    def set_contact_info(self, contact_info) -> None:
        self._contact_info = contact_info
    def set_id(self, ID) -> None:
        self._id = ID

class Patient(Person):
    def __init__(self, name, age, gender, contact_info, ID, assigned_doctor, medical_history):
        super().__init__(name, age, gender, contact_info, ID)
        self._medical_history: Dict = medical_history #changed when medical_history class is finished
        self._assigned_doctor = assigned_doctor
    def view_medical_history(self) -> None:
        print(self._medical_history) #changed when medical_history class is finished
    
    def book_appointment(self, day, doctor) -> None:
        return self._medical_history.update((day, doctor)) #changed when appointment class is finished

    def get_patient_info(self) -> tuple[str, int, int]:
        return (self.get_name(), self.get_age(), self.get_id())

class Doctor(Person):
    def __init__(self, name, age, gender, contact_info, ID, specialization, available_slots, patients_list):
        super().__init__(name, age, gender, contact_info, ID)
        self._specialization = specialization
        self._available_slots = available_slots
        self._patients_list = patients_list
    #work in progress getter/setter methods
    ...
    
    def diagnose_patient(self, patient):
        diagnose = ()
        return patient._medical_history((datetime.now() ,self.get_name(), diagnose)) #changed when medical_history class is finished
    def prescribe_medication(self, patient,medication):
        return (self.get_name(), patient.get_name(), medication) #work in progress
    def view_patient_records(self, patient):
        return patient.view_medical_history() #work in progress
    
class Nurse(Person):
    def __init__(self, name, age, gender, contact_info, ID, assigned_ward, patients_assigned):
        super().__init__(name, age, gender, contact_info, ID)
        self._assigned_ward = assigned_ward
        self._patients_assigned: List = patients_assigned
    def assist_doctor(self, doctor):
        return (self.get_name(), doctor.get_name(), datetime.now())
    def record_vitals(self, vitals:List):
        return vitals #????
    def update_patient_statues(self, patient):
        statues = []
        #make statues attribute in patient
        return statues
        

class Administrator(Person):
    ...