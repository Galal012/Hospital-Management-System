from system import *

persons = dict()
buildings = dict()


def start_system() -> None:
    HospitalManagementSystem.display_starting_page()

    option = HospitalManagementSystem.take_int(1, 3, "Option")
    match option:
        case 1:
            HospitalManagementSystem.display_login_page()

        case 2:
            print(2 * "\n", end="")
            HospitalManagementSystem.display_registration_page()
            option = HospitalManagementSystem.take_int(1, 4, "Option")
            print()
            match option:
                case 1:
                    admin = HospitalManagementSystem.register_admin()
                    if "admins" not in persons:
                        persons["admins"] = list()
                    persons["admins"].append(admin)
                    HospitalManagementSystem.print_success_message("Admin Registered Successfully")

                    start_system()

        case _:
            exit()


start_system()