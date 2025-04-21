import curses
from curses import wrapper

import system as ss

def start_system() -> None:
    wrapper(ss.HospitalManagementSystem.display_starting_page)

    option1 = ss.pp.hc.helper_functions.display_get_options([
        "Log In",
        "Register",
        "Exit"
    ], "Select Option:")
    match option1:
        case 1:
            ss.pp.hc.helper_functions.display_page_heading("*** Log In Page ***")

            option2 = ss.pp.hc.helper_functions.display_get_options([
                "Admin",
                "Doctor",
                "Nurse",
                "Patient",
                "Go Back"
            ], "Log In As:")

            match option2:
                case 1:
                    def admin_interface() -> None:
                        if ss.current_user is None:
                            is_logged = ss.HospitalManagementSystem.login_user("admins")
                            if not is_logged:
                                start_system()

                        ss.pp.hc.helper_functions.display_page_heading("*** Admin Page ***")
                        option3 = ss.pp.hc.helper_functions.display_get_options([
                            "Add Doctor",
                            "Remove Doctor",
                            "Manage Hospital Operations",
                            "Log Out"
                        ], f"####  Welcome Back, {ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                ss.pp.hc.helper_functions.display_page_heading("*** Registration Page ***")
                                ss.current_user.add_doctor(ss.HospitalManagementSystem.register_user("doctor"))
                                admin_interface()

                            case 2:
                                ss.pp.hc.helper_functions.display_page_heading("*** Remove Doctor Page ***")
                                def run(stdscr):
                                    win, doctor_id = ss.pp.hc.helper_functions.take_person_id(stdscr, "Doctor")
                                    ss.current_user.remove_doctor(win, doctor_id)

                                wrapper(run)
                                admin_interface()

                            case 3:
                                ss.pp.hc.helper_functions.display_page_heading("*** Hospital Operations page ***")

                                def run(stdscr):
                                    rows, columns = stdscr.getmaxyx()
                                    win = curses.newwin(1, columns // 2, rows // 4 - 1, columns // 4 - 1)
                                    ss.current_user.manage_hospital_operations(win)

                                wrapper(run)
                                admin_interface()

                            case 4:
                                ss.current_user = None
                                start_system()

                    admin_interface()

                case 2:
                    def doctor_interface() -> None:
                        if ss.current_user is None:
                            is_logged = ss.HospitalManagementSystem.login_user("doctors")
                            if not is_logged:
                                start_system()

                        ss.pp.hc.helper_functions.display_page_heading("*** Doctor Page ***")
                        option3 = ss.pp.hc.helper_functions.display_get_options([
                            "Add Patient",
                            "Remove Patient",
                            "View Patients List",
                            "Diagnose Patient",
                            "Prescribe Medication",
                            "Add Patient Record",
                            "View Patient Records",
                            "Log Out"
                        ], f"####  Welcome Back, {ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                ss.pp.hc.helper_functions.display_page_heading("*** Add Patient Page ***")
                                def run(stdscr):
                                    win, patient_id = ss.pp.hc.helper_functions.take_person_id(stdscr, "Patient")

                                    if "patients" not in ss.pp.persons:
                                        ss.pp.hc.helper_functions.display_error(win, "Can't Find This Patient")
                                        ss.tm.sleep(3)
                                        doctor_interface()
                                        return

                                    for patient in ss.pp.persons["patients"]:
                                        if patient.get_id() == patient_id:
                                            ss.current_user.add_patient(patient)
                                            ss.pp.hc.helper_functions.display_success_message(
                                                win,
                                                "Patient Added Successfully"
                                            )
                                            ss.tm.sleep(3)
                                            doctor_interface()
                                            return

                                    ss.pp.hc.helper_functions.display_error(win, "Can't Find This Patient")
                                    ss.tm.sleep(3)
                                    doctor_interface()

                                wrapper(run)

                            case 2:
                                ss.pp.hc.helper_functions.display_page_heading("*** Remove Patient Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.pp.hc.helper_functions.take_person_id(stdscr, "Patient")
                                    ss.current_user.remove_patient(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 3:
                                ss.current_user.view_patients_list()
                                doctor_interface()

                            case 4:
                                ss.pp.hc.helper_functions.display_page_heading("*** Diagnose Patient Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.pp.hc.helper_functions.take_person_id(stdscr, "Patient")
                                    ss.current_user.diagnose_patient(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 5:
                                ss.pp.hc.helper_functions.display_page_heading("*** Prescribe Medication Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.pp.hc.helper_functions.take_person_id(stdscr, "Patient")
                                    ss.current_user.prescribe_medication(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 6:
                                ss.pp.hc.helper_functions.display_page_heading("*** Add Patient Record Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.pp.hc.helper_functions.take_person_id(stdscr, "Patient")
                                    ss.current_user.add_patient_record(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 7:
                                ss.pp.hc.helper_functions.display_page_heading("*** Patient Records Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.pp.hc.helper_functions.take_person_id(stdscr, "Patient")
                                    ss.current_user.view_patient_records(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 8:
                                ss.current_user = None
                                start_system()

                    doctor_interface()

                case _:
                    start_system()




        case 2:
            ss.pp.hc.helper_functions.display_page_heading("*** Registration Page ***")

            option2 = ss.pp.hc.helper_functions.display_get_options([
                "Admin",
                "Doctor",
                "Nurse",
                "Patient",
                "Go Back"
            ], "Register As:")

            match option2:
                case 1:
                    ss.pp.hc.helper_functions.display_page_heading("*** Admin Registration Page ***")
                    admin = ss.HospitalManagementSystem.register_user("admin")
                    if "admins" not in ss.pp.persons:
                        ss.pp.persons["admins"] = list()
                    ss.pp.persons["admins"].append(admin)

                    start_system()

                case 2:
                    ss.pp.hc.helper_functions.display_page_heading("*** Doctor Registration Page ***")
                    doctor = ss.HospitalManagementSystem.register_user("doctor")
                    if "doctors" not in ss.pp.persons:
                        ss.pp.persons["doctors"] = list()
                    ss.pp.persons["doctors"].append(doctor)

                    start_system()

                case 3:
                    ss.pp.hc.helper_functions.display_page_heading("*** Nurse Registration Page ***")
                    nurse = ss.HospitalManagementSystem.register_user("nurse")
                    if "nurses" not in ss.pp.persons:
                        ss.pp.persons["nurses"] = list()
                    ss.pp.persons["nurses"].append(nurse)

                    start_system()

                case 4:
                    ss.pp.hc.helper_functions.display_page_heading("*** Patient Registration Page ***")
                    patient = ss.HospitalManagementSystem.register_user("patient")
                    if "patients" not in ss.pp.persons:
                        ss.pp.persons["patients"] = list()
                    ss.pp.persons["patients"].append(patient)

                    start_system()

                case _:
                    start_system()

        case _:
            exit()


start_system()