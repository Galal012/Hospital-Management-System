from typing import Dict, List
from helper_classes import ID_Generator
from people import Doctor, Patient


class Building:
    __number_of_buildings: int = 0
    def __init__(self, build_type: str) :
        Building.__number_of_buildings += 1
        self._id: str = ID_Generator.generate_id(build_type, Building.get_number_of_buildings())
        return self._id
    @staticmethod
    def get_number_of_buildings() -> int:
        return Building.__number_of_buildings

    def get_id(self) -> str:
        return self._id


class Department(Building):
    def __init__(self, name: str, head_of_department: str) -> None:
        super().__init__("BLD/D")
        self._name: str = name
        self._head_of_department: str = head_of_department
        self._doctors_list = list()
        self._services_offered = list()

    # Getter methods
    def get_department_info(self) -> str:
        return f"Name: {self._name}\nHead of department: {self._head_of_department}"
    def get_doctors_list(self) -> List:
        return self._doctors_list
    def get_services_offered(self) -> List:
        return self._services_offered

    # Setter methods
    def set_department_name(self, name: str) -> None:
        self._name = name
    def set_head_of_department(self, head_of_department: str) -> None:
        self._head_of_department = head_of_department
    def add_doctor(self, doctor) -> None:
        self._doctors_list.append(doctor.get_name())
    def add_service(self, service: str) -> None:
        self._services_offered.append(service)


class Pharmacy(Building):
    def __init__(self ,pharmacist, available_medicines = None , prescriptions_list = None) -> None:
        self.available_medicines = dict()
        self.prescriptions_list = list()
        self.pharmacist = pharmacist
        self.id=super().__init__("BLD/PH")

    def dispense_medication(self, prescription):
        medicine_name = prescription.get("medicine_name")
        quantity = prescription.get("quantity")

        if medicine_name in self.available_medicines:
            if self.available_medicines[medicine_name] >= quantity:
                self.available_medicines[medicine_name] -= quantity
                self.prescriptions_list.append(prescription)
                print(f"Dispensed {quantity} units of {medicine_name}.")
            else:
                print(f"Insufficient stock for {medicine_name}. Available: {self.available_medicines[medicine_name]}")
        else:
            print(f"{medicine_name} is not available in the pharmacy.")
    def check_stock(self, medicine_name):
        return self.available_medicines.get(medicine_name, 0)
    def update_medicine_list(self, medicine_name: str, quantity:int) -> None:
        if medicine_name in self.available_medicines:
            self.available_medicines[medicine_name]+= quantity
        else:
            self.available_medicines[medicine_name] = quantity
        print(f"Updated {medicine_name} stock to {self.available_medicines[medicine_name]} units.")

    def __str__(self):
        """
        for better represntation
        """
        return (f"Pharmacist: {self.pharmacist}\n"
                f"Available Medicines: {self.available_medicines}\n"
                f"Prescriptions List: {self.prescriptions_list}")
class Ward(Building):
    def __init__(self, room_type, avilablitity=True, patient=None) -> None:
        self.id=super().__init__("BLD/WRM")
        valid_types = ["ICU", "general", "private"]
        if room_type not in valid_types:
            raise ValueError(f"Invalid room type. Must be one of: {valid_types}")
        self.room_type = room_type
        self.patient = patient
        self.avilablitity = avilablitity
    def assign_room(self, patient_name: Patient):
        if self.avilablitity:
            self.patient = patient_name.get_name()
            self.avilablitity = False
            print(f"Room {self.id} ({self.room_type}) assigned to {self.patient}.")
        else:
            print(f"Room {self.id} is already occupied by {self.patient}.")
    def discharge_patient(self):
        if not self.avilablitity:
            print(f"Patient {self.patient} discharged from Room {self.id}.")
            self.assigned_patient = None
            self.availability = True
        else:
            print(f"Room {self.id} is already available.")
    def check_availability(self):
        return self.avilablitity

# Testing department
# doctor1 = Doctor("Galal", 18, "Male", "Eys")
# administration_building = Department("Administration", doctor1.get_name())
# administration_building.add_doctor(doctor1)
# administration_building.add_service("Stamping papers")
# print(administration_building.get_department_info())
# print(administration_building.get_doctors_list())
# print(administration_building.get_services_offered())
# print(administration_building.get_id())
#testing pharmacy
#my_pharmacy = Pharmacy(pharmacist="John Doe")

#my_pharmacy.update_medicine_list("Paracetamol", 100)
#my_pharmacy.update_medicine_list("Ibuprofen", 50)
#
#print(f"Paracetamol stock: {my_pharmacy.check_stock('Paracetamol')}")
#
#prescription = {"medicine_name": "Paracetamol", "quantity": 10}
#my_pharmacy.dispense_medication(prescription)
#
#print(my_pharmacy)
#room1 = Ward( room_type="ICU")
#
#print(room1.check_availability()) 
#pa1 = Patient("zod", 3, "Male")
#room1.assign_room(pa1) 
#
#print(room1.check_availability()) 
#
#
#room1.discharge_patient()  
#
