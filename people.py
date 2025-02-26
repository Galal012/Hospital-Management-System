from typing import Dict

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
        self._medical_history: Dict = medical_history
        self._assigned_doctor = assigned_doctor
    def view_medical_history(self) -> None:
        print(self._medical_history)
    
    def book_appointment(self, day, doctor) -> None:
        return self._medical_history.update((day, doctor))

    def get_patient_info(self) -> tuple[str, int, int]:
        return (self.get_name(), self.get_age(), self.get_id())

class Doctor(Person):
    ...

class Nurse(Person):
    ...

class Administrator(Person):
    ...