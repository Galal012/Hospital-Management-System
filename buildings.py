import curses
from curses import wrapper
from typing import Dict, List
import people as pp


class Building:
    __number_of_buildings: int = 0
    def __init__(self) :
        self._id: str = str()
        Building.__number_of_buildings += 1

    @staticmethod
    def get_number_of_buildings() -> int:
        return Building.__number_of_buildings

    def get_id(self) -> str:
        return self._id


class Department(Building):
    __number_of_departments: int = 0

    def __init__(self, name: str, services_offered: list) -> None:
        super().__init__()
        self._name: str = name
        self._services_offered = services_offered
        self._head_of_department = str()
        self._doctors_list = list()
        Department.__number_of_departments += 1
        self._id = pp.hc.helper_functions.generate_id("DEP", Department.get_number_of_departments())

    # Getter methods
    def get_name(self) -> str:
        return self._name
    def get_services_offered(self) -> List:
        return self._services_offered
    def get_head_of_department(self) -> str:
        return self._head_of_department
    def get_doctors_list(self) -> List:
        return self._doctors_list

    # Setter methods
    def set_department_name(self, name: str) -> None:
        self._name = name
    def set_head_of_department(self, head_of_department: str) -> None:
        self._head_of_department = head_of_department
    def add_doctor(self, doctor) -> None:
        self._doctors_list.append(doctor)
    def remove_doctor(self, win, doctor_id):
        idx = -1

        for i, doctor in enumerate(self._doctors_list):
            if doctor.get_id() == doctor_id:
                idx = i
                break

        if idx == -1:
            pp.hc.helper_functions.display_error(win, "Can't Find This Doctor")
            pp.tm.sleep(3)
        else:
            del self._doctors_list[idx]
            pp.hc.helper_functions.display_success_message(win, "Patient Removed Successfully")
            pp.tm.sleep(3)

    def view_doctors_list(self):
        pp.hc.helper_functions.display_page_heading("Doctors List Page")

        def run(stdscr):
            headings = ["Name", "Age", "Gender", "Specialization"]
            cols_width = [40, 6, 8, 30]
            data = list()
            for doctor in self._doctors_list:
                data.append([doctor.get_name(), doctor.get_age(), doctor.get_gender(), doctor.get_specialization()])
            pp.hc.helper_functions.display_table(
                stdscr,
                6,
                "Doctors List:",
                headings,
                data,
                cols_width
            )

        wrapper(run)

    def add_service(self, service: str) -> None:
        self._services_offered.append(service)

    @staticmethod
    def get_number_of_departments() -> int:
        return Department.__number_of_departments


class Pharmacy(Building):
    __number_of_pharmacies: int = 0

    def __init__(self, pharmacy_name, pharmacist_name) -> None:
        super().__init__()
        self._pharmacy_name =  pharmacy_name
        self._pharmacist_name = pharmacist_name
        self._available_medicines = dict()
        self._prescriptions_list = list()
        Pharmacy.__number_of_pharmacies += 1
        self._id = pp.hc.helper_functions.generate_id("PHR", Pharmacy.get_number_of_pharmacies())

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

    @staticmethod
    def get_number_of_pharmacies() -> int:
        return Pharmacy.__number_of_pharmacies


class Ward(Building):
    __number_of_wards: int = 0

    def __init__(self, room_type) -> None:
        super().__init__()
        self._room_type = room_type
        self._availability = True
        self._patient = None
        Ward.__number_of_wards += 1
        self._id = pp.hc.helper_functions.generate_id("WRD", Ward.get_number_of_wards())

    def assign_room(self, patient_name):
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

    @staticmethod
    def get_number_of_wards() -> int:
        return Ward.__number_of_wards

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