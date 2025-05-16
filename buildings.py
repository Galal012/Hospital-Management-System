import curses
from abc import ABC, abstractmethod
from curses import wrapper
from typing import Dict, List
import people as pp


class Building(ABC):
    __number_of_buildings: int = 0
    def __init__(self) :
        self._id: str = str()
        Building.__number_of_buildings += 1

    @staticmethod
    def get_number_of_buildings() -> int:
        return Building.__number_of_buildings

    def get_id(self) -> str:
        return self._id

    @abstractmethod
    def view_information(self):
        pass


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

    def view_information(self):
        def run(stdscr):
            headings = ["Department Data"]
            cols_width = [30, 120]
            data = [
                ["ID", self.get_id()],
                ["Name", self.get_name()],
                ["Head of Department", self.get_head_of_department()],
                ["Services Offered", str(self.get_services_offered())[1:-1].replace("'", "")]
            ]
            pp.hc.helper_functions.display_table(
                stdscr,
                6,
                "Department Information:",
                headings,
                data,
                cols_width
            )

        wrapper(run)

    @staticmethod
    def get_number_of_departments() -> int:
        return Department.__number_of_departments


class Pharmacy(Building):
    __number_of_pharmacies: int = 0

    def __init__(self, pharmacy_name, pharmacist_name) -> None:
        super().__init__()
        self._pharmacy_name =  pharmacy_name
        self._pharmacist_name = pharmacist_name
        self._medicine_stock = dict()
        self._prescriptions_list = list()
        Pharmacy.__number_of_pharmacies += 1
        self._id = pp.hc.helper_functions.generate_id("PHR", Pharmacy.get_number_of_pharmacies())

    def get_pharmacy_name(self):
        return self._pharmacy_name
    def get_pharmacist_name(self):
        return self._pharmacist_name

    def add_medicine_stock(self, medicine_name: str, quantity:int) -> None:
        if medicine_name in self._medicine_stock:
            self._medicine_stock[medicine_name] += quantity
        else:
            self._medicine_stock[medicine_name] = quantity

    def check_stock(self, medicine_name):
        return self._medicine_stock.get(medicine_name, 0)

    def dispense_medication(self, prescription):
        for item in prescription:
            if self._medicine_stock.get(item[0], 0) < item[1]:
                return False

        for item in prescription:
            self._medicine_stock[item[0]] -= item[1]

        self._prescriptions_list.append(prescription)
        return True

    def view_stock(self):
        pp.hc.helper_functions.display_page_heading("View Stock Page")

        def run(stdscr):
            headings = ["Medicine Name", "Quantity"]
            cols_width = [20, 12]
            data = list()
            for item in self._medicine_stock:
                data.append([item, self._medicine_stock[item]])
            pp.hc.helper_functions.display_table(
                stdscr,
                6,
                "Current Stock:",
                headings,
                data,
                cols_width
            )

        wrapper(run)

    def view_information(self):
        def run(stdscr):
            headings = ["Pharmacy Data"]
            cols_width = [30, 60]
            data = [
                ["ID", self.get_id()],
                ["Pharmacy Name", self.get_pharmacy_name()],
                ["Pharmacist Name", self.get_pharmacist_name()],
            ]
            pp.hc.helper_functions.display_table(
                stdscr,
                6,
                "Pharmacy Information:",
                headings,
                data,
                cols_width
            )

        wrapper(run)

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

    def get_room_type(self):
        return self._room_type
    def check_availability(self):
        return self._availability

    def assign_room(self, patient):
        self._patient = patient
        self._availability = False

    def discharge_patient(self):
        self._patient = None
        self._availability = True


    def view_information(self):
        def run(stdscr):
            headings = ["Ward Data"]
            cols_width = [30, 60]
            patient_id, patient_name = None, None
            if self._patient:
                patient_id, patient_name = self._patient.get_id(), self._patient.get_name()
            data = [
                ["ID", self.get_id()],
                ["Room Type", self.get_room_type()],
                ["Availability", self.check_availability()],
                ["Assigned Patient ID", patient_id],
                ["Assigned Patient Name", patient_name]
            ]
            pp.hc.helper_functions.display_table(
                stdscr,
                6,
                "Ward Information:",
                headings,
                data,
                cols_width
            )

        wrapper(run)

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