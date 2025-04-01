import system as ss

def start_system() -> None:
    ss.HospitalManagementSystem.display_starting_page()

    option = ss.pp.hc.helper_functions.take_int(1, 3, "Option")
    match option:
        case 1:
            print(2 * "\n", end="")
            ss.HospitalManagementSystem.display_login_page()
            option = ss.pp.hc.helper_functions.take_int(1, 5, "Option")
            print()
            match option:
                case 1:
                    def admin_interface() -> None:
                        if ss.current_user is None:
                            is_logged = ss.HospitalManagementSystem.login_user("admins")
                            if not is_logged:
                                start_system()

                        ss.HospitalManagementSystem.display_user_interface([
                            "Add Doctor",
                            "Remove Doctor",
                            "Manage Hospital Operations",
                            "Log Out"
                        ])
                        option = ss.pp.hc.helper_functions.take_int(1, 4, "Option")
                        print()
                        match option:
                            case 1:
                                ss.current_user.add_doctor()
                                admin_interface()

                            case 2:
                                doctor_id = input("Doctor ID: ")
                                ss.current_user.remove_doctor(doctor_id)
                                admin_interface()

                            case 3:
                                ss.current_user.manage_hospital_operations()
                                admin_interface()

                            case 4:
                                ss.current_user = None
                                ss.pp.hc.helper_functions.print_success_message("Successful Log Out")
                                print(3 * "\n", end="")
                                start_system()

                    admin_interface()

                case 2:
                    def doctor_interface() -> None:
                        if ss.current_user is None:
                            is_logged = ss.HospitalManagementSystem.login_user("doctors")
                            if not is_logged:
                                start_system()

                        ss.HospitalManagementSystem.display_user_interface([
                            "Add Patient",
                            "Remove Patient",
                            "View Patients List",
                            "Diagnose Patient",
                            "Prescribe Medication",
                            "Add Patient Record",
                            "View Patient Records",
                            "Log Out"
                        ])
                        option = ss.pp.hc.helper_functions.take_int(1, 8, "Option")
                        print()
                        match option:
                            case 1:
                                patient_id = input("Patient ID: ")
                                if "patients" not in ss.pp.persons:
                                    print()
                                    ss.pp.hc.helper_functions.print_error("Can't Find This Patient")
                                    print(3 * "\n", end="")
                                    doctor_interface()
                                    return

                                for patient in ss.pp.persons["patients"]:
                                    if patient.get_id() == patient_id:
                                        ss.current_user.add_patient(patient)
                                        ss.pp.hc.helper_functions.print_success_message("Patient Added Successfully")
                                        print(3 * "\n", end="")
                                        doctor_interface()
                                        return

                                print()
                                ss.pp.hc.helper_functions.print_error("Can't Find This Patient")
                                print(3 * "\n", end="")
                                doctor_interface()

                            case 2:
                                patient_id = input("Patient ID: ")
                                ss.current_user.remove_patient(patient_id)
                                doctor_interface()

                            case 3:
                                ss.current_user.view_patients_list()
                                print(3 * "\n", end="")
                                doctor_interface()

                            case 4:
                                patient_id = input("Patient ID: ")
                                ss.current_user.diagnose_patient(patient_id)
                                doctor_interface()

                            case 5:
                                patient_id = input("Patient ID: ")
                                ss.current_user.prescribe_medication(patient_id)
                                doctor_interface()

                            case 6:
                                patient_id = input("Patient ID: ")
                                ss.current_user.add_patient_record(patient_id)
                                doctor_interface()

                            case 7:
                                patient_id = input("Patient ID: ")
                                ss.current_user.view_patient_records(patient_id)
                                doctor_interface()

                            case 8:
                                ss.current_user = None
                                ss.pp.hc.helper_functions.print_success_message("Successful Log Out")
                                print(3 * "\n", end="")
                                start_system()

                    doctor_interface()




        case 2:
            print(2 * "\n", end="")
            ss.HospitalManagementSystem.display_registration_page()
            option = ss.pp.hc.helper_functions.take_int(1, 5, "Option")
            print()
            match option:
                case 1:
                    admin = ss.HospitalManagementSystem.register_admin()
                    if "admins" not in ss.pp.persons:
                        ss.pp.persons["admins"] = list()
                    ss.pp.persons["admins"].append(admin)
                    ss.pp.hc.helper_functions.print_success_message("Admin Registered Successfully")
                    print(3*"\n", end="")

                    start_system()

                case 2:
                    doctor = ss.HospitalManagementSystem.register_doctor()
                    if "doctors" not in ss.pp.persons:
                        ss.pp.persons["doctors"] = list()
                    ss.pp.persons["doctors"].append(doctor)
                    ss.pp.hc.helper_functions.print_success_message("Doctor Registered Successfully")
                    print(3*"\n", end="")

                    start_system()

                case 3:
                    nurse = ss.HospitalManagementSystem.register_nurse()
                    if "nurses" not in ss.pp.persons:
                        ss.pp.persons["nurses"] = list()
                    ss.pp.persons["nurses"].append(nurse)
                    ss.pp.hc.helper_functions.print_success_message("Nurse Registered Successfully")
                    print(3 * "\n", end="")

                    start_system()

                case 4:
                    patient = ss.HospitalManagementSystem.register_patient()
                    if "patients" not in ss.pp.persons:
                        ss.pp.persons["patients"] = list()
                    ss.pp.persons["patients"].append(patient)
                    ss.pp.hc.helper_functions.print_success_message("Patient Registered Successfully")
                    print(3 * "\n", end="")

                    start_system()

                case _:
                    start_system()

        case _:
            exit()


start_system()