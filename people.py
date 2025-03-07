from typing import Dict, List
from datetime import datetime
from helper_classes import ID_Generator


class Person:
    __number_of_persons: int = 0
    def __init__(self, name: str, age: int, gender: str) -> None:
        self._name: str = name
        self._age: int = age
        self._gender: str = gender
        self._contact_info = dict()
        self._id: str = str()
        Person.__number_of_persons += 1
    
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

    @staticmethod
    def get_number_of_persons() -> int:
        return Person.__number_of_persons
    
    def set_name(self, name: str) -> None:
        self._name = name
    def set_age(self, age: int) -> None:
        self._age = age if age >= 0 else ValueError('Age not valid')
    def set_gender(self, gender: str) -> None:
        self._gender = gender
    def add_contact_info(self, key: str, value: str) -> None:
        self._contact_info[key] = value

class Patient(Person):
    __number_of_patients: int = 0
    def __init__(self, name: str, age: int, gender: str):
        super().__init__(name, age, gender)
        Patient.__number_of_patients += 1
        self._id: str = ID_Generator.generate_id("PAT", Patient.get_number_of_patients())
        self._assigned_doctor = str()
        self._medical_history = list()

    @staticmethod
    def get_number_of_patients() -> int:
        return Patient.__number_of_patients

    def get_medical_history(self) -> List:
        return self._medical_history
    
    def book_appointment(self, doctor, date, time) -> None:
        self._assigned_doctor = doctor.get_id()
        ... # Waiting for appointment class
    
    def get_patient_info(self) -> tuple[str, int, str]:
        return self.get_name(), self.get_age(), self.get_id()

class Doctor(Person):
    __number_of_doctors: int = 0
    def __init__(self, name: str, age: int, gender: str, specialization: str) -> None:
        super().__init__(name, age, gender)
        Doctor.__number_of_doctors += 1
        self._id: str = ID_Generator.generate_id("DOC", Doctor.get_number_of_doctors())
        self._specialization: str = specialization
        self._available_slots = list()
        self._patients_list = list()

    @staticmethod
    def get_number_of_doctors() -> int:
        return Doctor.__number_of_doctors
    
    def diagnose_patient(self, patient):
        ...
    
    def prescribe_medication(self, patient, medication):
        return self.get_name(), patient.get_name(), medication
    
    def view_patient_records(self, patient):
        ...

class Nurse(Person):
    __number_of_nurses: int = 0
    def __init__(self, name: str, age: int, gender: str, assigned_ward):
        super().__init__(name, age, gender)
        Nurse.__number_of_nurses += 1
        self._id: str = ID_Generator.generate_id("NUR", Nurse.get_number_of_nurses())
        self._assigned_ward = assigned_ward
        self._patients_assigned = list()

    @staticmethod
    def get_number_of_nurses() -> int:
        return Nurse.__number_of_nurses

    def assign_patient(self, patien) -> None:
        self._patients_assigned.append(patien)

    def assist_doctor(self, doctor):
        return self.get_name(), doctor.get_name(), datetime.now()
    
    def record_vitals(self, vitals:List):
        return vitals
    
    def update_patient_statues(self, patient):
        statues = []
        return statues

class Administrator(Person):
    __number_of_administrator: int = 0
    def __init__(self, name: str, age: int, gender: str):
        super().__init__(name, age, gender)
        Administrator.__number_of_administrator += 1
        self._id: str = ID_Generator.generate_id("ADM", Administrator.get_number_of_administrators())

    @staticmethod
    def get_number_of_administrators() -> int:
        return Administrator.__number_of_administrator


# iam testing braah
# patient1 = Patient("John Doe", 35, "Male")
# print(f"Patient ID: {patient1.get_id()}")
#
# doctor1 = Doctor("Jane Smith", 40, "Female", "Cardiology")
# print(f"Doctor ID: {doctor1.get_id()}")
#
# nurse1 = Nurse("Mark Johnson", 28, "Male", "Emergency")
# print(f"Nurse ID: {nurse1.get_id()}")
