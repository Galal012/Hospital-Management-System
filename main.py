import curses
from curses import wrapper

from pandas.io.clipboard import is_available

import system as ss

# conn = ss.bd.pp.hc.sqf.DatabaseConnection.get_db_connection()
# cursor = conn.cursor()
# cursor.execute("SELECT * FROM MedicalRecord;")
# result = cursor.fetchall()[0]
# print(result["test_results"])
# conn.commit()

ss.bd.pp.hc.sqf.DBHandler.create_tables()
ss.LoadFromDB.load_patients()
ss.LoadFromDB.load_doctors()
ss.LoadFromDB.load_admins()
ss.LoadFromDB.load_records()


def start_system() -> None:
    wrapper(ss.HospitalManagementSystem.display_starting_page)

    option1 = ss.bd.pp.hc.helper_functions.display_get_options([
        "Log In",
        "Register",
        "Buildings",
        "Exit"
    ], "Select Option:")
    match option1:
        case 1:
            ss.bd.pp.hc.helper_functions.display_page_heading("*** Log In Page ***")

            option2 = ss.bd.pp.hc.helper_functions.display_get_options([
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

                        ss.bd.pp.hc.helper_functions.display_page_heading("*** Admin Page ***")
                        option3 = ss.bd.pp.hc.helper_functions.display_get_options([
                            "Add Doctor",
                            "Remove Doctor",
                            "Manage Hospital Operations",
                            "Log Out"
                        ], f"####  Welcome Back, Mr. {ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Registration Page ***")
                                ss.current_user.add_doctor(ss.HospitalManagementSystem.register_user("doctor"))
                                admin_interface()

                            case 2:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Remove Doctor Page ***")
                                def run(stdscr):
                                    win, doctor_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Doctor ID:", "Doctor ID:")
                                    ss.current_user.remove_doctor(win, doctor_id)

                                wrapper(run)
                                admin_interface()

                            case 3:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Hospital Operations page ***")

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

                        ss.bd.pp.hc.helper_functions.display_page_heading("*** Doctor Page ***")
                        option3 = ss.bd.pp.hc.helper_functions.display_get_options([
                            "Add Patient",
                            "Remove Patient",
                            "View Patients List",
                            "Diagnose Patient",
                            "Prescribe Medication",
                            "Add Patient Record",
                            "View Patient Records",
                            "Log Out"
                        ], f"####  Welcome Back, Dr. {ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Add Patient Page ***")
                                def run(stdscr):
                                    win, patient_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Patient ID:", "Patient ID:")

                                    if "patients" not in ss.bd.pp.persons:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Patient")
                                        ss.tm.sleep(3)
                                        doctor_interface()
                                        return

                                    for patient in ss.bd.pp.persons["patients"]:
                                        if patient.get_id() == patient_id:
                                            ss.current_user.add_patient(patient)
                                            ss.bd.pp.hc.helper_functions.display_success_message(
                                                win,
                                                "Patient Added Successfully"
                                            )
                                            ss.tm.sleep(3)
                                            doctor_interface()
                                            return

                                    ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Patient")
                                    ss.tm.sleep(3)
                                    doctor_interface()

                                wrapper(run)

                            case 2:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Remove Patient Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Patient ID:", "Patient ID:")
                                    ss.current_user.remove_patient(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 3:
                                ss.current_user.view_patients_list()
                                doctor_interface()

                            case 4:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Diagnose Patient Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Patient ID:", "Patient ID:")
                                    ss.current_user.diagnose_patient(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 5:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Prescribe Medication Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Patient ID:", "Patient ID:")
                                    ss.current_user.prescribe_medication(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 6:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Add Patient Record Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Patient ID:", "Patient ID:")
                                    ss.current_user.add_patient_record(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 7:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Patient Records Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Patient ID:", "Patient ID:")
                                    ss.current_user.view_patient_records(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 8:
                                ss.current_user = None
                                start_system()

                    doctor_interface()

                case 3:
                    def nurse_interface() -> None:
                        if ss.current_user is None:
                            is_logged = ss.HospitalManagementSystem.login_user("nurses")
                            if not is_logged:
                                start_system()

                        title = "Mr. "
                        if ss.current_user.get_gender().lower() == "female":
                            title = "Mrs. "
                        ss.bd.pp.hc.helper_functions.display_page_heading("*** Nurse Page ***")
                        option3 = ss.bd.pp.hc.helper_functions.display_get_options([
                            "Update Patient Status",
                            "Assist Doctor",
                            "Manage Ward",
                            "Log Out"
                        ], f"####  Welcome Back, {title}{ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Update Patient Status Page ***")

                                def run(stdscr):
                                    win, patient_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Patient ID:", "Patient ID:")
                                    ss.current_user.update_patient_statues(win, patient_id)
                                    nurse_interface()

                                wrapper(run)

                            case 2:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Assist Doctor Page ***")

                                def run(stdscr):
                                    win, doctor_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Doctor ID:", "Doctor ID:")

                                    if "doctors" not in ss.bd.pp.persons:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Doctor")
                                        ss.tm.sleep(3)
                                        nurse_interface()
                                        return

                                    for doctor in ss.bd.pp.persons["doctors"]:
                                        if doctor.get_id() == doctor_id:
                                            ss.current_user.assist_doctor(doctor)
                                            ss.bd.pp.hc.helper_functions.display_success_message(
                                                win,
                                                "Doctor Assisted Successfully"
                                            )
                                            ss.tm.sleep(3)
                                            nurse_interface()
                                            return

                                    ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Doctor")
                                    ss.tm.sleep(3)
                                    nurse_interface()

                                wrapper(run)

                            case 3:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Manage Ward Page ***")

                                def run(stdscr):
                                    win, ward_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Ward ID:", "Ward ID:")

                                    if "wards" not in ss.bd.pp.buildings:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Ward")
                                        ss.tm.sleep(3)
                                        nurse_interface()
                                        return

                                    for ward in ss.bd.pp.buildings["wards"]:
                                        if ward.get_id() == ward_id:
                                            ss.current_user.assign_ward(ward)
                                            ss.bd.pp.hc.helper_functions.display_success_message(
                                                win,
                                                "Ward Managed Successfully"
                                            )
                                            ss.tm.sleep(3)
                                            nurse_interface()
                                            return

                                    ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Ward")
                                    ss.tm.sleep(3)
                                    nurse_interface()

                                wrapper(run)

                            case 4:
                                ss.current_user = None
                                start_system()

                    nurse_interface()

                case 4:
                    def patient_interface() -> None:
                        if ss.current_user is None:
                            is_logged = ss.HospitalManagementSystem.login_user("patients")
                            if not is_logged:
                                start_system()

                        title = "Mr. "
                        if ss.current_user.get_gender().lower() == "female":
                            title = "Mrs. "
                        ss.bd.pp.hc.helper_functions.display_page_heading("*** Patient Page ***")
                        option3 = ss.bd.pp.hc.helper_functions.display_get_options([
                            "Book Appointment",
                            "View Medical History",
                            "Display Patient Information",
                            "Log Out"
                        ], f"####  Welcome Back, {title}{ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Appointment Booking Page ***")
                                ss.current_user.book_appointment()
                                patient_interface()

                            case 2:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Patient Records Page ***")
                                ss.current_user.view_medical_history()
                                patient_interface()

                            case 3:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Patient Information Page ***")
                                def run(stdscr):
                                    headings = ["Patient Data"]
                                    cols_width = [30, 40]
                                    data = [
                                        ["ID", ss.current_user.get_id()],
                                        ["Name", ss.current_user.get_name()],
                                        ["Age", ss.current_user.get_age()],
                                        ["Gender", ss.current_user.get_gender()],
                                        ["Assigned Doctor", ss.current_user.get_assigned_doctor()],
                                        ["Diagnosis", ss.current_user.get_diagnosis()],
                                        ["Prescribed Treatment", ss.current_user.get_prescribed_treatment()]
                                    ]
                                    ss.bd.pp.hc.helper_functions.display_table(
                                        stdscr,
                                        6,
                                        "Patient Information:",
                                        headings,
                                        data,
                                        cols_width
                                    )

                                wrapper(run)
                                patient_interface()

                            case 4:
                                ss.current_user = None
                                start_system()

                    patient_interface()

                case _:
                    start_system()




        case 2:
            ss.bd.pp.hc.helper_functions.display_page_heading("*** Registration Page ***")

            option2 = ss.bd.pp.hc.helper_functions.display_get_options([
                "Admin",
                "Doctor",
                "Nurse",
                "Patient",
                "Go Back"
            ], "Register As:")

            match option2:
                case 1:
                    ss.bd.pp.hc.helper_functions.display_page_heading("*** Admin Registration Page ***")
                    admin = ss.HospitalManagementSystem.register_user("admin")
                    if "admins" not in ss.bd.pp.persons:
                        ss.bd.pp.persons["admins"] = list()
                    ss.bd.pp.persons["admins"].append(admin)
                    ss.bd.pp.hc.sqf.DBHandler.insert_administrator(admin)

                    start_system()

                case 2:
                    ss.bd.pp.hc.helper_functions.display_page_heading("*** Doctor Registration Page ***")
                    doctor = ss.HospitalManagementSystem.register_user("doctor")
                    if "doctors" not in ss.bd.pp.persons:
                        ss.bd.pp.persons["doctors"] = list()
                    ss.bd.pp.persons["doctors"].append(doctor)
                    ss.bd.pp.hc.sqf.DBHandler.insert_doctor(doctor)

                    start_system()

                case 3:
                    ss.bd.pp.hc.helper_functions.display_page_heading("*** Nurse Registration Page ***")
                    nurse = ss.HospitalManagementSystem.register_user("nurse")
                    if "nurses" not in ss.bd.pp.persons:
                        ss.bd.pp.persons["nurses"] = list()
                    ss.bd.pp.persons["nurses"].append(nurse)

                    start_system()

                case 4:
                    ss.bd.pp.hc.helper_functions.display_page_heading("*** Patient Registration Page ***")
                    patient = ss.HospitalManagementSystem.register_user("patient")
                    if "patients" not in ss.bd.pp.persons:
                        ss.bd.pp.persons["patients"] = list()
                    ss.bd.pp.persons["patients"].append(patient)
                    ss.bd.pp.hc.sqf.DBHandler.insert_patient(patient)

                    start_system()

                case _:
                    start_system()

        case 3:
            def buildings_interface():
                ss.bd.pp.hc.helper_functions.display_page_heading("*** Buildings Management Page ***")

                option2 = ss.bd.pp.hc.helper_functions.display_get_options([
                    "Add Building",
                    "Remove Building",
                    "Manage Building",
                    "Go Back"
                ], "Select Option:")

                match option2:
                    case 1:
                        ss.bd.pp.hc.helper_functions.display_page_heading("*** Add Building Page ***")

                        option3 = ss.bd.pp.hc.helper_functions.display_get_options([
                            "Department",
                            "Pharmacy",
                            "Ward",
                            "Go Back"
                        ], "Add:")

                        match option3:
                            case 1:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Add Department Page ***")
                                department = ss.HospitalManagementSystem.add_building("department")
                                if "departments" not in ss.bd.pp.buildings:
                                    ss.bd.pp.buildings["departments"] = list()
                                ss.bd.pp.buildings["departments"].append(department)

                                buildings_interface()

                            case 2:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Add Pharmacy Page ***")
                                pharmacy = ss.HospitalManagementSystem.add_building("pharmacy")
                                if "pharmacies" not in ss.bd.pp.buildings:
                                    ss.bd.pp.buildings["pharmacies"] = list()
                                ss.bd.pp.buildings["pharmacies"].append(pharmacy)

                                buildings_interface()

                            case 3:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Add Ward Page ***")
                                ward = ss.HospitalManagementSystem.add_building("ward")
                                if "wards" not in ss.bd.pp.buildings:
                                    ss.bd.pp.buildings["wards"] = list()
                                ss.bd.pp.buildings["wards"].append(ward)

                                buildings_interface()

                            case _:
                                buildings_interface()

                    case 2:
                        ss.bd.pp.hc.helper_functions.display_page_heading("*** Remove Building Page ***")

                        option3 = ss.bd.pp.hc.helper_functions.display_get_options([
                            "Department",
                            "Pharmacy",
                            "Ward",
                            "Go Back"
                        ], "Remove:")

                        match option3:
                            case 1:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Remove Department Page ***")

                                def run(stdscr):
                                    win, department_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Department ID:", "Department ID:")

                                    idx = -1
                                    if "departments" not in ss.bd.pp.buildings:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Department")
                                        ss.bd.pp.tm.sleep(3)
                                        buildings_interface()

                                    for i, dep in enumerate(ss.bd.pp.buildings["departments"]):
                                        if dep.get_id() == department_id:
                                            idx = i
                                            break

                                    if idx == -1:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Department")
                                    else:
                                        del ss.bd.pp.buildings["departments"][idx]
                                        ss.bd.pp.hc.helper_functions.display_success_message(win, "Department Removed Successfully")

                                    ss.bd.pp.tm.sleep(3)
                                    buildings_interface()

                                wrapper(run)

                            case 2:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Remove Pharmacy Page ***")

                                def run(stdscr):
                                    win, pharmacy_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Pharmacy ID:", "Pharmacy ID:")

                                    idx = -1
                                    if "pharmacies" not in ss.bd.pp.buildings:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Pharmacy")
                                        ss.bd.pp.tm.sleep(3)
                                        buildings_interface()

                                    for i, phr in enumerate(ss.bd.pp.buildings["pharmacies"]):
                                        if phr.get_id() == pharmacy_id:
                                            idx = i
                                            break

                                    if idx == -1:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Pharmacy")
                                    else:
                                        del ss.bd.pp.buildings["pharmacies"][idx]
                                        ss.bd.pp.hc.helper_functions.display_success_message(win, "Pharmacy Removed Successfully")

                                    ss.bd.pp.tm.sleep(3)
                                    buildings_interface()

                                wrapper(run)

                            case 3:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Remove Ward Page ***")

                                def run(stdscr):
                                    win, ward_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Ward ID:", "Ward ID:")

                                    idx = -1
                                    if "wards" not in ss.bd.pp.buildings:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Ward")
                                        ss.bd.pp.tm.sleep(3)
                                        buildings_interface()

                                    for i, wrd in enumerate(ss.bd.pp.buildings["wards"]):
                                        if wrd.get_id() == ward_id:
                                            idx = i
                                            break

                                    if idx == -1:
                                        ss.bd.pp.hc.helper_functions.display_error(win, "Can't Find This Ward")
                                    else:
                                        del ss.bd.pp.buildings["wards"][idx]
                                        ss.bd.pp.hc.helper_functions.display_success_message(win, "Ward Removed Successfully")

                                    ss.bd.pp.tm.sleep(3)
                                    buildings_interface()

                                wrapper(run)

                            case _:
                                buildings_interface()

                    case 3:
                        ss.bd.pp.hc.helper_functions.display_page_heading("*** Manage Building Page ***")

                        option3 = ss.bd.pp.hc.helper_functions.display_get_options([
                            "Department",
                            "Pharmacy",
                            "Ward",
                            "Go Back"
                        ], "Manage:")

                        match option3:
                            case 1:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Manage Department Page ***")

                                def run(stdscr):
                                    headings = ["NO.", "ID", "Name", "Services Offered"]
                                    cols_width = [5, 20, 15, 100]
                                    data = list()
                                    stop = True

                                    if "departments" in ss.bd.pp.buildings:
                                        stop = False
                                        for i, dep in enumerate(ss.bd.pp.buildings["departments"]):
                                            data.append([
                                                f"{i+1}.",
                                                dep.get_id(),
                                                dep.get_name(),
                                                str(dep.get_services_offered())[1:-1].replace("'",  "")
                                            ])

                                    ss.bd.pp.hc.helper_functions.display_table(
                                        stdscr,
                                        6,
                                        "Current Departments:",
                                        headings,
                                        data,
                                        cols_width,
                                        stop
                                    )

                                    if stop:
                                        buildings_interface()

                                    win, department_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr, "Enter Department ID:", "Department ID:", 2+len(data))

                                    depart = None

                                    for dep in ss.bd.pp.buildings["departments"]:
                                        if dep.get_id() == department_id:
                                            depart = dep
                                            break

                                    if depart is None:
                                        ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                   "Incorrect Department ID")
                                        ss.tm.sleep(3)
                                        buildings_interface()

                                    else:
                                        def manage_department():
                                            ss.bd.pp.hc.helper_functions.display_page_heading(
                                                "*** Manage Department Page ***")

                                            option4 = ss.bd.pp.hc.helper_functions.display_get_options([
                                                "Set Head of Department",
                                                "Add Doctor",
                                                "Remove Doctor",
                                                "View Doctors List",
                                                "Add Service",
                                                "View Department Information",
                                                "Go Back"
                                            ], "Select Option:")

                                            match option4:
                                                case 1:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Setting Head of Department Page ***")

                                                    def run(stdscr):
                                                        win, head_of_department = ss.bd.pp.hc.helper_functions.take_user_input(stdscr,
                                                                                                                    "Enter The Head of Department:",
                                                                                                                    "Head of Department Name:")

                                                        head_of_department = head_of_department.strip()
                                                        if not head_of_department or head_of_department == "":
                                                            ss.bd.pp.hc.helper_functions.display_error(win, "Enter a valid name")
                                                        else:
                                                            depart.set_head_of_department(head_of_department)
                                                            ss.bd.pp.hc.helper_functions.display_success_message(win, "Head of Department Set Successfully")

                                                        ss.bd.pp.tm.sleep(3)
                                                        manage_department()

                                                    wrapper(run)

                                                case 2:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Add Doctor Page ***")

                                                    def run(stdscr):
                                                        win, doctor_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr,
                                                                                                                       "Enter Doctor ID:",
                                                                                                                       "Doctor ID:")

                                                        if "doctors" not in ss.bd.pp.persons:
                                                            ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                       "Can't Find This Doctor")
                                                            ss.tm.sleep(3)
                                                            manage_department()
                                                            return

                                                        for doctor in ss.bd.pp.persons["doctors"]:
                                                            if doctor.get_id() == doctor_id:
                                                                depart.add_doctor(doctor)
                                                                ss.bd.pp.hc.helper_functions.display_success_message(
                                                                    win,
                                                                    "Doctor Added Successfully"
                                                                )
                                                                ss.tm.sleep(3)
                                                                manage_department()
                                                                return

                                                        ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                   "Can't Find This Doctor")
                                                        ss.tm.sleep(3)
                                                        manage_department()

                                                    wrapper(run)

                                                case 3:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Remove Doctor Page ***")

                                                    def run(stdscr):
                                                        win, doctor_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr,
                                                                                                                       "Enter Doctor ID:",
                                                                                                                       "Doctor ID:")
                                                        depart.remove_doctor(win, doctor_id)
                                                        manage_department()

                                                    wrapper(run)

                                                case 4:
                                                    depart.view_doctors_list()
                                                    manage_department()

                                                case 5:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Add Service Page ***")

                                                    def run(stdscr):
                                                        win, service = ss.bd.pp.hc.helper_functions.take_user_input(stdscr,
                                                                                                                      "Enter Service:",
                                                                                                                      "Service:")

                                                        service = service.strip()
                                                        if not service or service == "":
                                                            ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                       "Enter a valid service")
                                                        else:
                                                            depart.add_service(service)
                                                            ss.bd.pp.hc.helper_functions.display_success_message(win,
                                                                                                                 "Service Added Successfully")

                                                        ss.bd.pp.tm.sleep(3)
                                                        manage_department()

                                                    wrapper(run)

                                                case 6:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Department Information Page ***")

                                                    depart.view_information()
                                                    manage_department()

                                                case _:
                                                    buildings_interface()

                                        manage_department()

                                wrapper(run)

                            case 2:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Manage Pharmacy Page ***")

                                def run(stdscr):
                                    headings = ["NO.", "ID", "Pharmacy Name", "Pharmacist Name"]
                                    cols_width = [5, 15, 30, 40]
                                    data = list()
                                    stop = True

                                    if "pharmacies" in ss.bd.pp.buildings:
                                        stop = False
                                        for i, phr in enumerate(ss.bd.pp.buildings["pharmacies"]):
                                            data.append([
                                                f"{i + 1}.",
                                                phr.get_id(),
                                                phr.get_pharmacy_name(),
                                                phr.get_pharmacist_name(),
                                            ])

                                    ss.bd.pp.hc.helper_functions.display_table(
                                        stdscr,
                                        6,
                                        "Current Pharmacies:",
                                        headings,
                                        data,
                                        cols_width,
                                        stop
                                    )

                                    if stop:
                                        buildings_interface()

                                    win, pharmacy_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr,
                                                                                                      "Enter Pharmacy ID:",
                                                                                                      "Pharmacy ID:",
                                                                                                      2 + len(data))

                                    pharma = None

                                    for phr in ss.bd.pp.buildings["pharmacies"]:
                                        if phr.get_id() == pharmacy_id:
                                            pharma = phr
                                            break

                                    if pharma is None:
                                        ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                   "Incorrect Pharmacy ID")
                                        ss.tm.sleep(3)
                                        buildings_interface()

                                    else:
                                        def manage_pharmacy():
                                            ss.bd.pp.hc.helper_functions.display_page_heading(
                                                "*** Manage Pharmacy Page ***")

                                            option4 = ss.bd.pp.hc.helper_functions.display_get_options([
                                                "Add Medicine Stock",
                                                "Check Medicine Stock",
                                                "Dispense Prescription",
                                                "View Current Stock",
                                                "View Pharmacy Information",
                                                "Go Back"
                                            ], "Select Option:")

                                            match option4:
                                                case 1:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Adding Medicine Stock Page ***")

                                                    def run(stdscr):
                                                        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
                                                        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
                                                        red_and_black = curses.color_pair(2)
                                                        green_and_black = curses.color_pair(3)

                                                        rows, columns = stdscr.getmaxyx()

                                                        win = curses.newwin(rows // 2, columns // 2,
                                                                            rows // 4 - 1, columns // 4 - 1)
                                                        win_rows, win_columns = win.getmaxyx()
                                                        win.clear()

                                                        win.addstr(0, 0, "Enter Medicine Name and Quantity:",
                                                                   curses.A_BOLD | green_and_black)
                                                        win.addstr(1, 0, "---------------------------------",
                                                                   curses.A_BOLD | green_and_black)

                                                        curses.curs_set(1)

                                                        def get_medicine_name():
                                                            try:
                                                                win.addstr(3, 5,
                                                                           f"Medicine Name:{(win_columns - len("Medicine Name:") - 5) * " "}",
                                                                           curses.A_BOLD)
                                                                stdscr.move(rows // 4 + 2, columns // 4 + 26)
                                                                win.move(3, 27)
                                                                win.refresh()
                                                                val = ss.bd.pp.hc.helper_functions.take_str(stdscr,
                                                                                                         win).strip()
                                                                if not val or val == "":
                                                                    raise ValueError
                                                            except ValueError:
                                                                win.addstr(win_rows - 1, 0,
                                                                           "!!ERROR: Enter a valid medicine name!!",
                                                                           red_and_black)
                                                                win.refresh()
                                                                return get_medicine_name()
                                                            except Exception as e:
                                                                win.addstr(win_rows - 1, 0,
                                                                           f"!!UNEXPECTED ERROR: {e}!!",
                                                                           red_and_black)
                                                                win.refresh()
                                                                return get_medicine_name()
                                                            else:
                                                                win.addstr(win_rows - 1, 0,
                                                                           f"{(win_columns - 1) * " "}")
                                                                win.refresh()
                                                                return val
                                                        medicine_name = get_medicine_name()

                                                        def get_quantity():
                                                            try:
                                                                win.addstr(4, 5,
                                                                           f"Quantity:{(win_columns - len("Quantity:") - 5) * " "}",
                                                                           curses.A_BOLD)
                                                                stdscr.move(rows // 4 + 3, columns // 4 + 26)
                                                                win.move(4, 27)
                                                                win.refresh()
                                                                val = int(ss.bd.pp.hc.helper_functions.take_str(stdscr,
                                                                                                             win).strip())
                                                                if val <= 0:
                                                                    raise ValueError
                                                            except ValueError:
                                                                win.addstr(win_rows - 1, 0,
                                                                           "!!ERROR: Enter a valid quantity!!",
                                                                           red_and_black)
                                                                win.refresh()
                                                                return get_quantity()
                                                            except Exception as e:
                                                                win.addstr(win_rows - 1, 0,
                                                                           f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                                                                win.refresh()
                                                                return get_quantity()
                                                            else:
                                                                win.addstr(win_rows - 1, 0,
                                                                           f"{(win_columns - 1) * " "}")
                                                                win.refresh()
                                                                return val
                                                        quantity = get_quantity()

                                                        ss.bd.pp.hc.helper_functions.display_success_message(win,
                                                                                                          "Medicine Stock Added Successfully")
                                                        ss.tm.sleep(3)

                                                        pharma.add_medicine_stock(medicine_name.lower(), quantity)
                                                        manage_pharmacy()

                                                    wrapper(run)

                                                case 2:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Check Medicine Stock Page ***")

                                                    def run(stdscr):
                                                        win, medicine_name = ss.bd.pp.hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter Medicine Name:",
                                                            "Medicine Name:")

                                                        medicine_name = medicine_name.strip().lower()
                                                        if not medicine_name or medicine_name == "":
                                                            ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                       "Enter a valid medicine name")
                                                        else:
                                                            quantity = pharma.check_stock(medicine_name)
                                                            if not quantity:
                                                                ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                           f"{medicine_name} is out of stock!")
                                                            else:
                                                                ss.bd.pp.hc.helper_functions.display_success_message(win,
                                                                                                                 f"{medicine_name.capitalize()} is available in stock – {quantity} units.")

                                                        ss.bd.pp.tm.sleep(3)
                                                        manage_pharmacy()

                                                    wrapper(run)

                                                case 3:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Dispense Prescription Page ***")

                                                    def run(stdscr):
                                                        win, prescription = ss.bd.pp.hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter Prescription (Formatted [Name:Quantity,Name:Quantity,...])",
                                                            "Prescription:")

                                                        prescription = prescription.strip()
                                                        if not prescription or prescription == "":
                                                            ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                       "Enter a valid Prescription")
                                                        else:
                                                            prescription = prescription.split(",")
                                                            for i in range(len(prescription)):
                                                                prescription[i] = prescription[i].split(":")
                                                                prescription[i][0] = prescription[i][0].lower()
                                                                prescription[i][1] = int(prescription[i][1])

                                                            can_dispense = pharma.dispense_medication(prescription)
                                                            if not can_dispense:
                                                                ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                           "Some items in the prescription are out of stock")
                                                            else:
                                                                ss.bd.pp.hc.helper_functions.display_success_message(
                                                                    win,
                                                                    "Prescription Dispensed Successfully")


                                                        ss.bd.pp.tm.sleep(3)
                                                        manage_pharmacy()

                                                    wrapper(run)

                                                case 4:
                                                    pharma.view_stock()
                                                    manage_pharmacy()

                                                case 5:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Pharmacy Information Page ***")

                                                    pharma.view_information()
                                                    manage_pharmacy()

                                                case _:
                                                    buildings_interface()

                                        manage_pharmacy()

                                wrapper(run)

                            case 3:
                                ss.bd.pp.hc.helper_functions.display_page_heading("*** Manage Ward Page ***")

                                def run(stdscr):
                                    headings = ["NO.", "ID", "Room Type", "Availability"]
                                    cols_width = [5, 15, 15, 20]
                                    data = list()
                                    stop = True

                                    if "wards" in ss.bd.pp.buildings:
                                        stop = False
                                        for i, wd in enumerate(ss.bd.pp.buildings["wards"]):
                                            data.append([
                                                f"{i + 1}.",
                                                wd.get_id(),
                                                wd.get_room_type(),
                                                str(wd.check_availability())
                                            ])

                                    ss.bd.pp.hc.helper_functions.display_table(
                                        stdscr,
                                        6,
                                        "Current Wards:",
                                        headings,
                                        data,
                                        cols_width,
                                        stop
                                    )

                                    if stop:
                                        buildings_interface()

                                    win, ward_id = ss.bd.pp.hc.helper_functions.take_user_input(stdscr,
                                                                                                      "Enter Ward ID:",
                                                                                                      "Ward ID:",
                                                                                                      2 + len(data))

                                    wrd = None

                                    for wd in ss.bd.pp.buildings["wards"]:
                                        if wd.get_id() == ward_id:
                                            wrd = wd
                                            break

                                    if wrd is None:
                                        ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                   "Incorrect Ward ID")
                                        ss.tm.sleep(3)
                                        buildings_interface()

                                    else:
                                        def manage_ward():
                                            ss.bd.pp.hc.helper_functions.display_page_heading(
                                                "*** Manage Ward Page ***")

                                            option4 = ss.bd.pp.hc.helper_functions.display_get_options([
                                                "Reserve Room",
                                                "Discharge Patient",
                                                "Check Availability",
                                                "View Ward Information",
                                                "Go Back"
                                            ], "Select Option:")

                                            match option4:
                                                case 1:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Reserve Room page ***")
                                                    if not wrd.check_availability():
                                                        def run(stdscr):
                                                            rows, columns = stdscr.getmaxyx()
                                                            win = curses.newwin(1, columns // 2, rows // 4 - 1,
                                                                                columns // 4 - 1)
                                                            ss.bd.pp.hc.helper_functions.display_error(
                                                                win,
                                                                "Room is Currently Unavailable"
                                                            )
                                                            ss.tm.sleep(3)

                                                        wrapper(run)
                                                        manage_ward()

                                                    def run(stdscr):
                                                        win, patient_id = ss.bd.pp.hc.helper_functions.take_user_input(
                                                            stdscr, "Enter Patient ID:", "Patient ID:")

                                                        if "patients" not in ss.bd.pp.persons:
                                                            ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                       "Can't Find This Patient")
                                                            ss.tm.sleep(3)
                                                            manage_ward()
                                                            return

                                                        for patient in ss.bd.pp.persons["patients"]:
                                                            if patient.get_id() == patient_id:
                                                                wrd.assign_room(patient)
                                                                ss.bd.pp.hc.helper_functions.display_success_message(
                                                                    win,
                                                                    "Room Reserved Successfully"
                                                                )
                                                                ss.tm.sleep(3)
                                                                manage_ward()
                                                                return

                                                        ss.bd.pp.hc.helper_functions.display_error(win,
                                                                                                   "Can't Find This Patient")
                                                        ss.tm.sleep(3)
                                                        manage_ward()

                                                    wrapper(run)

                                                case 2:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Discharge Patient page ***")
                                                    wrd.discharge_patient()
                                                    def run(stdscr):
                                                        rows, columns = stdscr.getmaxyx()
                                                        win = curses.newwin(1, columns // 2, rows // 4 - 1,
                                                                            columns // 4 - 1)
                                                        ss.bd.pp.hc.helper_functions.display_success_message(
                                                            win,
                                                            "Patient Discharged Successfully"
                                                        )
                                                        ss.tm.sleep(3)

                                                    wrapper(run)
                                                    manage_ward()

                                                case 3:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Check Availability page ***")
                                                    is_free = wrd.check_availability()

                                                    def run(stdscr):
                                                        rows, columns = stdscr.getmaxyx()
                                                        win = curses.newwin(1, columns // 2, rows // 4 - 1,
                                                                            columns // 4 - 1)
                                                        if is_free:
                                                            ss.bd.pp.hc.helper_functions.display_success_message(
                                                                win,
                                                                "Room is Currently Available"
                                                            )
                                                        else:
                                                            ss.bd.pp.hc.helper_functions.display_error(
                                                                win,
                                                                "Room is Currently Unavailable"
                                                            )
                                                        ss.tm.sleep(3)

                                                    wrapper(run)
                                                    manage_ward()

                                                case 4:
                                                    ss.bd.pp.hc.helper_functions.display_page_heading(
                                                        "*** Ward Information Page ***")

                                                    wrd.view_information()
                                                    manage_ward()

                                                case _:
                                                    buildings_interface()

                                        manage_ward()

                                wrapper(run)


                            case _:
                                buildings_interface()

                    case _:
                        start_system()

            buildings_interface()

        case _:
            conn = ss.bd.pp.hc.sqf.DatabaseConnection.get_db_connection()
            conn.close()
            exit()


start_system()