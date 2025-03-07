from typing import Dict, List
from helper_classes import ID_Generator
from people import Doctor


class Building:
    __number_of_buildings: int = 0
    def __init__(self) -> None:
        Building.__number_of_buildings += 1
        self._id: str = ID_Generator.generate_id("BLD", Building.get_number_of_buildings())

    @staticmethod
    def get_number_of_buildings() -> int:
        return Building.__number_of_buildings

    def get_id(self) -> str:
        return self._id


class Department(Building):
    def __init__(self, name: str, head_of_department: str) -> None:
        super().__init__()
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
    ...


class Ward(Building):
    ...


# Testing
# doctor1 = Doctor("Galal", 18, "Male", "Eys")
# administration_building = Department("Administration", doctor1.get_name())
# administration_building.add_doctor(doctor1)
# administration_building.add_service("Stamping papers")
# print(administration_building.get_department_info())
# print(administration_building.get_doctors_list())
# print(administration_building.get_services_offered())
# print(administration_building.get_id())
