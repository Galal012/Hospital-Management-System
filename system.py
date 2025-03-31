import people as pp

current_user = None


class HospitalManagementSystem:
    @staticmethod
    def display_starting_page() -> None:
        print(75*"-")
        print(f"{15*" "}*** Welcome to Hospital Management System *** {15*" "}")
        print(75*"-")

        pp.hc.helper_functions.display_date_time()
        print(2*"\n", end="")

        pp.hc.helper_functions.print_options(["Login", "Registration", "Exit"])


    @staticmethod
    def display_login_page() -> None:
        print("Log In:")
        pp.hc.helper_functions.print_options(["Admin", "Doctor", "Nurse", "Patient", "Go Back"])


    @staticmethod
    def login_user(users: str) -> bool:
        global current_user

        email = input("Email: ")
        password = input("Password: ")

        if users not in pp.persons:
            pp.hc.helper_functions.print_error("Invalid Credentials Please Try again")
            print(3 * "\n", end="")
            return False

        for user in pp.persons[users]:
            security_info = user.get_security_info()
            if security_info["email"] == email and security_info["password"] == password:
                current_user = user
                pp.hc.helper_functions.print_success_message("Successful Log In")
                print(3 * "\n", end="")
                return True

        print()
        pp.hc.helper_functions.print_error("Invalid Credentials Please Try again")
        print(3 * "\n", end="")
        return False


    @staticmethod
    def display_user_interface(options: list):
        global current_user

        pp.hc.helper_functions.print_welcome_message(current_user.get_name())
        print()
        pp.hc.helper_functions.print_options(options)


    @staticmethod
    def display_registration_page() -> None:
        print("Register:")
        pp.hc.helper_functions.print_options(["Admin", "Doctor", "Nurse", "Patient", "Go Back"])


    @staticmethod
    def register_admin():
        name = input("Full Name: ")
        age = pp.hc.helper_functions.take_int(1, 120, "Age")
        gender = input("Gender(Male/Female): ")
        email = input("Email: ")
        password = input("Password: ")
        phone_number = input("Phone Number: ")

        admin = pp.Administrator(name, age, gender)
        admin.add_contact_info("email", email)
        admin.add_contact_info("phone_number", phone_number)
        admin.add_security_info("id", admin.get_id())
        admin.add_security_info("email", email)
        admin.add_security_info("password", password)

        return admin


    @staticmethod
    def register_doctor():
        name = input("Full Name: ")
        age = pp.hc.helper_functions.take_int(1, 120, "Age")
        gender = input("Gender(Male/Female): ")
        specialization = input("Specialization: ")
        email = input("Email: ")
        password = input("Password: ")
        phone_number = input("Phone Number: ")

        doctor = pp.Doctor(name, age, gender, specialization)
        doctor.add_contact_info("email", email)
        doctor.add_contact_info("phone_number", phone_number)
        doctor.add_security_info("id", doctor.get_id())
        doctor.add_security_info("email", email)
        doctor.add_security_info("password", password)

        return doctor


    @staticmethod
    def register_nurse():
        name = input("Full Name: ")
        age = pp.hc.helper_functions.take_int(1, 120, "Age")
        gender = input("Gender(Male/Female): ")
        email = input("Email: ")
        password = input("Password: ")
        phone_number = input("Phone Number: ")

        nurse = pp.Nurse(name, age, gender)
        nurse.add_contact_info("email", email)
        nurse.add_contact_info("phone_number", phone_number)
        nurse.add_security_info("id", nurse.get_id())
        nurse.add_security_info("email", email)
        nurse.add_security_info("password", password)

        return nurse


    @staticmethod
    def register_patient():
        name = input("Full Name: ")
        age = pp.hc.helper_functions.take_int(1, 120, "Age")
        gender = input("Gender(Male/Female): ")
        email = input("Email: ")
        password = input("Password: ")
        phone_number = input("Phone Number: ")

        patient = pp.Patient(name, age, gender)
        patient.add_contact_info("email", email)
        patient.add_contact_info("phone_number", phone_number)
        patient.add_security_info("id", patient.get_id())
        patient.add_security_info("email", email)
        patient.add_security_info("password", password)

        return patient