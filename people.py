from typing import Dict, List
import helper_classes as hc

persons = dict()
buildings = dict()


class Person:
    __number_of_persons: int = 0
    def __init__(self, name: str, age: int, gender: str) -> None:
        self._name: str = name
        self._age: int = age
        self._gender: str = gender
        self._contact_info = dict()
        self._security_info = dict()
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
    def get_security_info(self) -> Dict:
        return self._security_info
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
    def add_security_info(self, key: str, value: str) -> None:
        self._security_info[key] = value

class Patient(Person):
    __number_of_patients: int = 0
    def __init__(self, name: str, age: int, gender: str):
        super().__init__(name, age, gender)
        Patient.__number_of_patients += 1
        self._id: str = hc.helper_functions.generate_id("PAT", Patient.get_number_of_patients())
        self._diagnosis = str()
        self._assigned_doctor = str()
        self._medical_history = list()

    @staticmethod
    def get_number_of_patients() -> int:
        return Patient.__number_of_patients

    def get_diagnosis(self) -> str:
        return self._diagnosis

    def get_medical_history(self) -> List:
        return self._medical_history
    
    def book_appointment(self, doctor, date, time) -> None:
        self._assigned_doctor = doctor.get_id()
        ... # Waiting for appointment class

    def get_patient_info(self) -> tuple[str, int, str, str]:
        return self.get_name(), self.get_age(), self.get_id(), self.get_diagnosis()

    def set_diagnosis(self, diagnosis: str) -> None:
        self._diagnosis = diagnosis

    def set_assigned_doctor(self, doctor) -> None:
        self._assigned_doctor = doctor

    def __str__(self):
        output = f"|{self.get_name():^20}|{f"{self.get_age():03d}":^5}|{self.get_gender():^8}|{self.get_diagnosis():^15}|"
        return f"{output}\n-{20*"-"}|{5*"-"}|{8*"-"}|{15*"-"}-"

class Doctor(Person):
    __number_of_doctors: int = 0
    def __init__(self, name: str, age: int, gender: str, specialization: str) -> None:
        super().__init__(name, age, gender)
        Doctor.__number_of_doctors += 1
        self._id: str = hc.helper_functions.generate_id("DOC", Doctor.get_number_of_doctors())
        self._specialization: str = specialization
        self._available_slots = list()
        self._patients_list = list()

    @staticmethod
    def get_number_of_doctors() -> int:
        return Doctor.__number_of_doctors

    def add_patient(self, patient) -> None:
        self._patients_list.append(patient)
        patient.set_assigned_doctor(self.get_name())

    def remove_patient(self, patient_id) -> None:
        idx = -1

        for i, patient in enumerate(self._patients_list):
            if patient.get_id() == patient_id:
                idx = i
                break

        if idx == -1:
            print()
            hc.helper_functions.print_error("Can't Find This Patient")
            print(3 * "\n", end="")
        else:
            self._patients_list[idx].set_assigned_doctor(str())
            del self._patients_list[idx]
            hc.helper_functions.print_success_message("Patient Removed Successfully")
            print(3 * "\n", end="")

    def view_patients_list(self):
        header = f"|{"Name":^20}|{"Age":^5}|{"Gender":^8}|{"Diagnosis":^15}|"
        print(f"={20*"="}|{5*"="}|{8*"="}|{15*"="}=\n{header}\n={20*"="}|{5*"="}|{8*"="}|{15*"="}=")

        if len(self._patients_list) == 0:
            print(f"|{"NO PATIENTS YET!":^51}|\n{len(header)*"-"}")
        else:
            for patient in self._patients_list:
                print(patient)

    def diagnose_patient(self, patient):
        ...
    
    def prescribe_medication(self, patient, medication):
        return self.get_name(), patient.get_name(), medication
    
    def view_patient_records(self, patient):
        ...

class Nurse(Person):
    __number_of_nurses: int = 0
    def __init__(self, name: str, age: int, gender: str):
        super().__init__(name, age, gender)
        Nurse.__number_of_nurses += 1
        self._id: str = hc.helper_functions.generate_id("NUR", Nurse.get_number_of_nurses())
        self._assigned_ward = str()
        self._patients_assigned = list()

    @staticmethod
    def get_number_of_nurses() -> int:
        return Nurse.__number_of_nurses

    def assign_patient(self, patien) -> None:
        self._patients_assigned.append(patien)

    def assign_ward(self, ward) -> None:
        self._assigned_ward = ward

    def assist_doctor(self, doctor):
        return self.get_name(), doctor.get_name(), hc.datetime.now()
    
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
        self._id: str = hc.helper_functions.generate_id("ADM", Administrator.get_number_of_administrators())

    @staticmethod
    def get_number_of_administrators() -> int:
        return Administrator.__number_of_administrator

    @staticmethod
    def add_doctor() -> None:
        name = input("Full Name: ")
        age = hc.helper_functions.take_int(1, 120, "Age")
        gender = input("Gender(Male/Female): ")
        specialization = input("Specialization: ")
        email = input("Email: ")
        password = input("Password: ")
        phone_number = input("Phone Number: ")

        doctor = Doctor(name, age, gender, specialization)
        doctor.add_contact_info("email", email)
        doctor.add_contact_info("phone_number", phone_number)
        doctor.add_security_info("id", doctor.get_id())
        doctor.add_security_info("email", email)
        doctor.add_security_info("password", password)
        if "doctors" not in persons:
            persons["doctors"] = list()
        persons["doctors"].append(doctor)
        hc.helper_functions.print_success_message("Doctor Added Successfully")
        print(3 * "\n", end="")

    @staticmethod
    def remove_doctor(doctor_id) -> None:
        idx = -1
        if "doctors" not in persons:
            print()
            hc.helper_functions.print_error("Can't Find This Doctor")
            print(3 * "\n", end="")
            return

        for i, doctor in enumerate(persons["doctors"]):
            if doctor.get_id() == doctor_id:
                idx = i
                break

        if idx == -1:
            print()
            hc.helper_functions.print_error("Can't Find This Doctor")
            print(3 * "\n", end="")
        else:
            del persons["doctors"][idx]
            hc.helper_functions.print_success_message("Doctor Removed Successfully")
            print(3 * "\n", end="")

    def manage_hospital_operations(self) -> None:
        print(f"{self.get_name()} is managing hospital operations.")
        print(3 * "\n", end="")




# # # iam testing braah
# patient1 = Patient("Galal Mohamed ", 1, "Male")
# patient1.set_diagnosis("Malaria")
# print(patient1)
# print(f"Patient ID: {patient1.get_id()}")
# #
# doctor1 = Doctor("Jane Smith", 40, "Female", "Cardiology")
# doctor1.view_patients_list()
# print(f"Doctor ID: {doctor1.get_id()}")
#
# nurse1 = Nurse("Mark Johnson", 28, "Male", "Emergency")
# print(f"Nurse ID: {nurse1.get_id()}")
