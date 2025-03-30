from people import *

class HospitalManagementSystem:
    @staticmethod
    def display_date_time():
        date = f"Date: {str(datetime.now().date())}"
        time = f"Time: {str(datetime.now().time())[0:8]}"

        print(f"{date}{(75 - len(date) - len(time)) * " "}{time}")


    @staticmethod
    def print_options(options:list) -> None:
        print(30 * "-")
        for i, option in enumerate(options):
            item = f"{i + 1}. {option}"
            print(" ---  ", end="")
            print(item, end="")
            print(f"{(30 - 6 - len(item) - 4) * " "}----")
        print(30 * "-")


    @staticmethod
    def print_error(error:str) -> None:
        print(f"!! ERROR: {error} !!")


    @staticmethod
    def print_success_message(message:str) -> None:
        print(f"\n##### {message} #####\n")


    @staticmethod
    def take_int(start:int, end:int, type:str) -> int:
        try:
            option = int(input(f"{type}: "))
            while option < start or option > end:
                HospitalManagementSystem.print_error(f"Enter a Valid {type}")
                option = int(input(f"{type}: "))
        except ValueError:
            HospitalManagementSystem.print_error(f"Enter a Valid {type}")
            return HospitalManagementSystem.take_int(start, end, type)
        else:
            return option


    @staticmethod
    def display_starting_page() -> None:
        print(75*"-")
        print(f"{15*" "}*** Welcome to Hospital Management System *** {15*" "}")
        print(75*"-")

        HospitalManagementSystem.display_date_time()
        print(2*"\n", end="")

        HospitalManagementSystem.print_options(["Login", "Registration", "Exit"])


    @staticmethod
    def display_login_page() -> None:
        print("login")


    @staticmethod
    def display_registration_page() -> None:
        print("Register As:")
        HospitalManagementSystem.print_options(["Admin", "Doctor", "Nurse", "Patient"])


    @staticmethod
    def register_admin():
        name = input("Full Name: ")
        age = HospitalManagementSystem.take_int(1, 120, "Age")
        gender = input("Gender(Male/Female): ")
        email = input("Email: ")
        password = input("Password: ")
        phone_number = input("Phone Number: ")

        admin = Administrator(name, age, gender)
        admin.add_contact_info("email", email)
        admin.add_contact_info("phone_number", phone_number)
        admin.add_security_info("id", admin.get_id())
        admin.add_security_info("email", email)
        admin.add_security_info("password", password)

        return admin