import curses
from curses import wrapper
import time as tm

import system as ss
import people as pp
import helper_classes as hc
import sqlfunctions as sqf
import sender


sqf.DBHandler.create_tables()
ss.LoadFromDB.load_patients()
ss.LoadFromDB.load_doctors()
ss.LoadFromDB.load_admins()
ss.LoadFromDB.load_records()


def start_system() -> None:
    wrapper(ss.HospitalManagementSystem.display_starting_page)

    option1 = hc.helper_functions.display_get_options([
        "Log In",
        "Register",
        "Buildings",
        "Exit"
    ], "Select Option:")
    match option1:
        case 1:
            hc.helper_functions.display_page_heading("*** Log In Page ***")

            option2 = hc.helper_functions.display_get_options([
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

                            sender.send_message(f"Admin [ID: {ss.current_user.get_id()}] Logged In")

                        hc.helper_functions.display_page_heading("*** Admin Page ***")
                        option3 = hc.helper_functions.display_get_options([
                            "Add Doctor",
                            "Remove Doctor",
                            "Generate Bill",
                            "Manage Hospital Operations",
                            "Log Out"
                        ], f"####  Welcome Back, Mr. {ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                hc.helper_functions.display_page_heading("*** Registration Page ***")
                                ss.current_user.add_doctor(
                                    ss.HospitalManagementSystem.register_user("doctor")
                                )
                                sender.send_message(f"Admin [ID: {ss.current_user.get_id()}] Added a Doctor")
                                admin_interface()

                            case 2:
                                hc.helper_functions.display_page_heading("*** Remove Doctor Page ***")

                                def run(stdscr):
                                    win, doctor_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Doctor ID:",
                                        "Doctor ID:"
                                    )
                                    ss.current_user.remove_doctor(win, doctor_id)

                                wrapper(run)
                                admin_interface()

                            case 3:
                                hc.helper_functions.display_page_heading("*** Generate Bill Page ***")
                                ss.HospitalManagementSystem.generate_bill()
                                admin_interface()

                            case 4:
                                hc.helper_functions.display_page_heading("*** Hospital Operations page ***")

                                def run(stdscr):
                                    rows, columns = stdscr.getmaxyx()
                                    win = curses.newwin(
                                        1,
                                        columns // 2,
                                        rows // 4 - 1,
                                        columns // 4 - 1
                                    )
                                    ss.current_user.manage_hospital_operations(win)

                                wrapper(run)
                                sender.send_message(
                                    f"Admin [ID: {ss.current_user.get_id()}] is Managing Hospital Operations"
                                )
                                admin_interface()

                            case _:
                                ss.current_user = None
                                start_system()

                    admin_interface()

                case 2:
                    def doctor_interface() -> None:
                        if ss.current_user is None:
                            is_logged = ss.HospitalManagementSystem.login_user("doctors")
                            if not is_logged:
                                start_system()

                            sender.send_message(f"Doctor [ID: {ss.current_user.get_id()}] Logged In")

                        hc.helper_functions.display_page_heading("*** Doctor Page ***")
                        option3 = hc.helper_functions.display_get_options([
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
                                hc.helper_functions.display_page_heading("*** Add Patient Page ***")
                                def run(stdscr):
                                    win, patient_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Patient ID:",
                                        "Patient ID:"
                                    )

                                    if "patients" not in pp.persons:
                                        hc.helper_functions.display_error(win, "Can't Find This Patient")
                                        tm.sleep(3)
                                        doctor_interface()
                                        return

                                    for patient in pp.persons["patients"]:
                                        if patient.get_id() == patient_id:
                                            ss.current_user.add_patient(patient)
                                            hc.helper_functions.display_success_message(
                                                win,
                                                "Patient Added Successfully"
                                            )
                                            sender.send_message(
                                                f"Doctor [ID: {ss.current_user.get_id()}] Added a Patient"
                                            )
                                            tm.sleep(3)
                                            doctor_interface()
                                            return

                                    hc.helper_functions.display_error(win, "Can't Find This Patient")
                                    tm.sleep(3)
                                    doctor_interface()

                                wrapper(run)

                            case 2:
                                hc.helper_functions.display_page_heading("*** Remove Patient Page ***")

                                def run(stdscr):
                                    win, patient_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Patient ID:",
                                        "Patient ID:"
                                    )
                                    ss.current_user.remove_patient(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 3:
                                ss.current_user.view_patients_list()
                                doctor_interface()

                            case 4:
                                hc.helper_functions.display_page_heading("*** Diagnose Patient Page ***")

                                def run(stdscr):
                                    win, patient_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Patient ID:",
                                        "Patient ID:"
                                    )
                                    ss.current_user.diagnose_patient(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 5:
                                hc.helper_functions.display_page_heading("*** Prescribe Medication Page ***")

                                def run(stdscr):
                                    win, patient_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Patient ID:",
                                        "Patient ID:"
                                    )
                                    ss.current_user.prescribe_medication(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 6:
                                hc.helper_functions.display_page_heading("*** Add Patient Record Page ***")

                                def run(stdscr):
                                    win, patient_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Patient ID:",
                                        "Patient ID:"
                                    )
                                    ss.current_user.add_patient_record(win, patient_id)
                                    doctor_interface()

                                wrapper(run)

                            case 7:
                                hc.helper_functions.display_page_heading("*** Patient Records Page ***")

                                def run(stdscr):
                                    win, patient_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Patient ID:",
                                        "Patient ID:"
                                    )
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

                            sender.send_message(f"Nurse [ID: {ss.current_user.get_id()}] Logged In")

                        title = "Mr. "
                        if ss.current_user.get_gender().lower() == "female":
                            title = "Mrs. "
                        hc.helper_functions.display_page_heading("*** Nurse Page ***")
                        option3 = hc.helper_functions.display_get_options([
                            "Update Patient Status",
                            "Assist Doctor",
                            "Manage Ward",
                            "Log Out"
                        ], f"####  Welcome Back, {title}{ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                hc.helper_functions.display_page_heading("*** Update Patient Status Page ***")

                                def run(stdscr):
                                    win, patient_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Patient ID:",
                                        "Patient ID:"
                                    )
                                    ss.current_user.update_patient_statues(win, patient_id)
                                    nurse_interface()

                                wrapper(run)

                            case 2:
                                hc.helper_functions.display_page_heading("*** Assist Doctor Page ***")

                                def run(stdscr):
                                    win, doctor_id = hc.helper_functions.take_user_input(
                                        stdscr,"Enter Doctor ID:",
                                        "Doctor ID:"
                                    )

                                    if "doctors" not in pp.persons:
                                        hc.helper_functions.display_error(win, "Can't Find This Doctor")
                                        tm.sleep(3)
                                        nurse_interface()
                                        return

                                    for doctor in pp.persons["doctors"]:
                                        if doctor.get_id() == doctor_id:
                                            ss.current_user.assist_doctor(doctor)
                                            hc.helper_functions.display_success_message(
                                                win,
                                                "Doctor Assisted Successfully"
                                            )
                                            sender.send_message(
                                                f"Nurse [ID: {ss.current_user.get_id()}] is Assisting a Doctor"
                                            )
                                            tm.sleep(3)
                                            nurse_interface()
                                            return

                                    hc.helper_functions.display_error(win, "Can't Find This Doctor")
                                    tm.sleep(3)
                                    nurse_interface()

                                wrapper(run)

                            case 3:
                                hc.helper_functions.display_page_heading("*** Manage Ward Page ***")

                                def run(stdscr):
                                    win, ward_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Ward ID:",
                                        "Ward ID:"
                                    )

                                    if "wards" not in pp.buildings:
                                        hc.helper_functions.display_error(win, "Can't Find This Ward")
                                        tm.sleep(3)
                                        nurse_interface()
                                        return

                                    for ward in pp.buildings["wards"]:
                                        if ward.get_id() == ward_id:
                                            ss.current_user.assign_ward(ward)
                                            hc.helper_functions.display_success_message(
                                                win,
                                                "Ward Managed Successfully"
                                            )
                                            sender.send_message(
                                                f"Nurse [ID: {ss.current_user.get_id()}] is Managing a Ward"
                                            )
                                            tm.sleep(3)
                                            nurse_interface()
                                            return

                                    hc.helper_functions.display_error(win, "Can't Find This Ward")
                                    tm.sleep(3)
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

                            sender.send_message(f"Patient [ID: {ss.current_user.get_id()}] Logged In")

                        title = "Mr. "
                        if ss.current_user.get_gender().lower() == "female":
                            title = "Mrs. "
                        hc.helper_functions.display_page_heading("*** Patient Page ***")
                        option3 = hc.helper_functions.display_get_options([
                            "Book Appointment",
                            "View Medical History",
                            "View & Pay Bills",
                            "Display Patient Information",
                            "Log Out"
                        ], f"####  Welcome Back, {title}{ss.current_user.get_name()}  ####")

                        match option3:
                            case 1:
                                hc.helper_functions.display_page_heading("*** Appointment Booking Page ***")
                                ss.current_user.book_appointment()
                                patient_interface()

                            case 2:
                                hc.helper_functions.display_page_heading("*** Patient Records Page ***")
                                ss.current_user.view_medical_history()
                                patient_interface()

                            case 3:
                                hc.helper_functions.display_page_heading("*** View & Pay Bills Page ***")

                                def run(stdscr):
                                    headings = [
                                        "NO.", "ID", "Treatment Cost", "Medicine Cost",
                                        "Total Cost", "Payment Status"
                                    ]
                                    cols_width = [5, 20, 20, 20, 20, 20]
                                    data = list()
                                    stop = True

                                    if len(hc.bills):
                                        for i, bll in enumerate(hc.bills):
                                            if bll.get_patient() == ss.current_user:
                                                if bll.get_payment_status() == "Pending":
                                                    stop = False
                                                data.append([
                                                    f"{i + 1}.",
                                                    bll.get_id(),
                                                    bll.get_treatment_cost(),
                                                    bll.get_medicine_cost(),
                                                    bll.get_total_cost(),
                                                    bll.get_payment_status()
                                                ])

                                    hc.helper_functions.display_table(
                                        stdscr,
                                        6,
                                        "All Bills:",
                                        headings,
                                        data,
                                        cols_width,
                                        stop
                                    )

                                    if stop:
                                        patient_interface()

                                    win, bill_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Bill ID:",
                                        "Bill ID:",
                                        2 + len(data)
                                    )

                                    bill = None

                                    for bll in hc.bills:
                                        if bll.get_id() == bill_id:
                                            bill = bll
                                            break

                                    if bill is None:
                                        hc.helper_functions.display_error(
                                            win,
                                            "Incorrect Bill ID"
                                        )

                                    else:
                                        bill.process_payment()
                                        hc.helper_functions.display_success_message(
                                            win,
                                            "Bill Paid Successfully"
                                        )
                                        sender.send_message(
                                            f"Patient [ID: {ss.current_user.get_id()}] Paid Bill"
                                        )

                                    tm.sleep(3)
                                    patient_interface()

                                wrapper(run)

                            case 4:
                                hc.helper_functions.display_page_heading("*** Patient Information Page ***")
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
                                    hc.helper_functions.display_table(
                                        stdscr,
                                        6,
                                        "Patient Information:",
                                        headings,
                                        data,
                                        cols_width
                                    )

                                wrapper(run)
                                patient_interface()

                            case 5:
                                ss.current_user = None
                                start_system()

                    patient_interface()

                case _:
                    start_system()




        case 2:
            hc.helper_functions.display_page_heading("*** Registration Page ***")

            option2 = hc.helper_functions.display_get_options([
                "Admin",
                "Doctor",
                "Nurse",
                "Patient",
                "Go Back"
            ], "Register As:")

            match option2:
                case 1:
                    hc.helper_functions.display_page_heading("*** Admin Registration Page ***")
                    admin = ss.HospitalManagementSystem.register_user("admin")
                    if "admins" not in pp.persons:
                        pp.persons["admins"] = list()
                    pp.persons["admins"].append(admin)
                    sender.send_message(
                        f"Admin [ID: {admin.get_id()}] was Registered"
                    )
                    sqf.DBHandler.insert_administrator(admin)

                    start_system()

                case 2:
                    hc.helper_functions.display_page_heading("*** Doctor Registration Page ***")
                    doctor = ss.HospitalManagementSystem.register_user("doctor")
                    if "doctors" not in pp.persons:
                        pp.persons["doctors"] = list()
                    pp.persons["doctors"].append(doctor)
                    sender.send_message(
                        f"Doctor [ID: {doctor.get_id()}] was Registered"
                    )
                    sqf.DBHandler.insert_doctor(doctor)

                    start_system()

                case 3:
                    hc.helper_functions.display_page_heading("*** Nurse Registration Page ***")
                    nurse = ss.HospitalManagementSystem.register_user("nurse")
                    if "nurses" not in pp.persons:
                        pp.persons["nurses"] = list()
                    pp.persons["nurses"].append(nurse)
                    sender.send_message(
                        f"Nurse [ID: {nurse.get_id()}] was Registered"
                    )

                    start_system()

                case 4:
                    hc.helper_functions.display_page_heading("*** Patient Registration Page ***")
                    patient = ss.HospitalManagementSystem.register_user("patient")
                    if "patients" not in pp.persons:
                        pp.persons["patients"] = list()
                    pp.persons["patients"].append(patient)
                    sender.send_message(
                        f"Patient [ID: {patient.get_id()}] was Registered"
                    )
                    sqf.DBHandler.insert_patient(patient)

                    start_system()

                case _:
                    start_system()

        case 3:
            def buildings_interface():
                hc.helper_functions.display_page_heading("*** Buildings Management Page ***")

                option2 = hc.helper_functions.display_get_options([
                    "Add Building",
                    "Remove Building",
                    "Manage Building",
                    "Go Back"
                ], "Select Option:")

                match option2:
                    case 1:
                        hc.helper_functions.display_page_heading("*** Add Building Page ***")

                        option3 = hc.helper_functions.display_get_options([
                            "Department",
                            "Pharmacy",
                            "Ward",
                            "Go Back"
                        ], "Add:")

                        match option3:
                            case 1:
                                hc.helper_functions.display_page_heading("*** Add Department Page ***")
                                department = ss.HospitalManagementSystem.add_building("department")
                                if "departments" not in pp.buildings:
                                    pp.buildings["departments"] = list()
                                pp.buildings["departments"].append(department)
                                sender.send_message(
                                    f"Department [ID: {department.get_id()}] was Added"
                                )

                                buildings_interface()

                            case 2:
                                hc.helper_functions.display_page_heading("*** Add Pharmacy Page ***")
                                pharmacy = ss.HospitalManagementSystem.add_building("pharmacy")
                                if "pharmacies" not in pp.buildings:
                                    pp.buildings["pharmacies"] = list()
                                pp.buildings["pharmacies"].append(pharmacy)
                                sender.send_message(
                                    f"Pharmacy [ID: {pharmacy.get_id()}] was Added"
                                )

                                buildings_interface()

                            case 3:
                                hc.helper_functions.display_page_heading("*** Add Ward Page ***")
                                ward = ss.HospitalManagementSystem.add_building("ward")
                                if "wards" not in pp.buildings:
                                    pp.buildings["wards"] = list()
                                pp.buildings["wards"].append(ward)
                                sender.send_message(
                                    f"Ward [ID: {ward.get_id()}] was Added"
                                )

                                buildings_interface()

                            case _:
                                buildings_interface()

                    case 2:
                        hc.helper_functions.display_page_heading("*** Remove Building Page ***")

                        option3 = hc.helper_functions.display_get_options([
                            "Department",
                            "Pharmacy",
                            "Ward",
                            "Go Back"
                        ], "Remove:")

                        match option3:
                            case 1:
                                hc.helper_functions.display_page_heading("*** Remove Department Page ***")

                                def run(stdscr):
                                    win, department_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Department ID:",
                                        "Department ID:"
                                    )

                                    idx = -1
                                    if "departments" not in pp.buildings:
                                        hc.helper_functions.display_error(
                                            win,
                                            "Can't Find This Department"
                                        )
                                        pp.tm.sleep(3)
                                        buildings_interface()

                                    for i, dep in enumerate(pp.buildings["departments"]):
                                        if dep.get_id() == department_id:
                                            idx = i
                                            break

                                    if idx == -1:
                                        hc.helper_functions.display_error(
                                            win,
                                            "Can't Find This Department"
                                        )
                                    else:
                                        del pp.buildings["departments"][idx]
                                        hc.helper_functions.display_success_message(
                                            win,
                                            "Department Removed Successfully"
                                        )
                                        sender.send_message(
                                            f"Department [ID: {department_id}] was Removed"
                                        )

                                    pp.tm.sleep(3)
                                    buildings_interface()

                                wrapper(run)

                            case 2:
                                hc.helper_functions.display_page_heading("*** Remove Pharmacy Page ***")

                                def run(stdscr):
                                    win, pharmacy_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Pharmacy ID:",
                                        "Pharmacy ID:"
                                    )

                                    idx = -1
                                    if "pharmacies" not in pp.buildings:
                                        hc.helper_functions.display_error(win, "Can't Find This Pharmacy")
                                        pp.tm.sleep(3)
                                        buildings_interface()

                                    for i, phr in enumerate(pp.buildings["pharmacies"]):
                                        if phr.get_id() == pharmacy_id:
                                            idx = i
                                            break

                                    if idx == -1:
                                        hc.helper_functions.display_error(win, "Can't Find This Pharmacy")
                                    else:
                                        del pp.buildings["pharmacies"][idx]
                                        hc.helper_functions.display_success_message(
                                            win,
                                            "Pharmacy Removed Successfully"
                                        )
                                        sender.send_message(
                                            f"Pharmacy [ID: {pharmacy_id}] was Removed"
                                        )

                                    pp.tm.sleep(3)
                                    buildings_interface()

                                wrapper(run)

                            case 3:
                                hc.helper_functions.display_page_heading("*** Remove Ward Page ***")

                                def run(stdscr):
                                    win, ward_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Ward ID:",
                                        "Ward ID:"
                                    )

                                    idx = -1
                                    if "wards" not in pp.buildings:
                                        hc.helper_functions.display_error(win, "Can't Find This Ward")
                                        pp.tm.sleep(3)
                                        buildings_interface()

                                    for i, wrd in enumerate(pp.buildings["wards"]):
                                        if wrd.get_id() == ward_id:
                                            idx = i
                                            break

                                    if idx == -1:
                                        hc.helper_functions.display_error(win, "Can't Find This Ward")
                                    else:
                                        del pp.buildings["wards"][idx]
                                        hc.helper_functions.display_success_message(
                                            win,
                                            "Ward Removed Successfully"
                                        )
                                        sender.send_message(
                                            f"Ward [ID: {ward_id}] was Removed"
                                        )

                                    pp.tm.sleep(3)
                                    buildings_interface()

                                wrapper(run)

                            case _:
                                buildings_interface()

                    case 3:
                        hc.helper_functions.display_page_heading("*** Manage Building Page ***")

                        option3 = hc.helper_functions.display_get_options([
                            "Department",
                            "Pharmacy",
                            "Ward",
                            "Go Back"
                        ], "Manage:")

                        match option3:
                            case 1:
                                hc.helper_functions.display_page_heading("*** Manage Department Page ***")

                                def run(stdscr):
                                    headings = ["NO.", "ID", "Name", "Services Offered"]
                                    cols_width = [5, 15, 20, 100]
                                    data = list()
                                    stop = True

                                    if "departments" in pp.buildings:
                                        stop = False
                                        for i, dep in enumerate(pp.buildings["departments"]):
                                            data.append([
                                                f"{i+1}.",
                                                dep.get_id(),
                                                dep.get_name(),
                                                str(dep.get_services_offered())[1:-1].replace(
                                                    "'",
                                                    ""
                                                )
                                            ])

                                    hc.helper_functions.display_table(
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

                                    win, department_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Department ID:",
                                        "Department ID:",
                                        2+len(data)
                                    )

                                    depart = None

                                    for dep in pp.buildings["departments"]:
                                        if dep.get_id() == department_id:
                                            depart = dep
                                            break

                                    if depart is None:
                                        hc.helper_functions.display_error(
                                            win,
                                            "Incorrect Department ID"
                                        )
                                        tm.sleep(3)
                                        buildings_interface()

                                    else:
                                        def manage_department():
                                            hc.helper_functions.display_page_heading(
                                                "*** Manage Department Page ***"
                                            )

                                            option4 = hc.helper_functions.display_get_options([
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
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Setting Head of Department Page ***"
                                                    )

                                                    def run(stdscr):
                                                        win, head_of_department = hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter The Head of Department:",
                                                            "Head of Department Name:"
                                                        )

                                                        head_of_department = head_of_department.strip()
                                                        if not head_of_department or head_of_department == "":
                                                            hc.helper_functions.display_error(
                                                                win,
                                                                "Enter a valid name"
                                                            )
                                                        else:
                                                            depart.set_head_of_department(head_of_department)
                                                            hc.helper_functions.display_success_message(
                                                                win,
                                                                "Head of Department Set Successfully"
                                                            )
                                                            sender.send_message(
                                                                f"Head of Department [ID: {depart.get_id()}] was Set"
                                                            )

                                                        pp.tm.sleep(3)
                                                        manage_department()

                                                    wrapper(run)

                                                case 2:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Add Doctor Page ***"
                                                    )

                                                    def run(stdscr):
                                                        win, doctor_id = hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter Doctor ID:",
                                                            "Doctor ID:"
                                                        )

                                                        if "doctors" not in pp.persons:
                                                            hc.helper_functions.display_error(
                                                                win,
                                                                "Can't Find This Doctor"
                                                            )
                                                            tm.sleep(3)
                                                            manage_department()
                                                            return

                                                        for doctor in pp.persons["doctors"]:
                                                            if doctor.get_id() == doctor_id:
                                                                depart.add_doctor(doctor)
                                                                hc.helper_functions.display_success_message(
                                                                    win,
                                                                    "Doctor Added Successfully"
                                                                )
                                                                sender.send_message(
                                                                    f"Doctor was Added to Department [ID: {depart.get_id()}]"
                                                                )
                                                                tm.sleep(3)
                                                                manage_department()
                                                                return

                                                        hc.helper_functions.display_error(
                                                            win,
                                                            "Can't Find This Doctor"
                                                        )
                                                        tm.sleep(3)
                                                        manage_department()

                                                    wrapper(run)

                                                case 3:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Remove Doctor Page ***"
                                                    )

                                                    def run(stdscr):
                                                        win, doctor_id = hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter Doctor ID:",
                                                            "Doctor ID:"
                                                        )
                                                        depart.remove_doctor(win, doctor_id)
                                                        manage_department()

                                                    wrapper(run)

                                                case 4:
                                                    depart.view_doctors_list()
                                                    manage_department()

                                                case 5:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Add Service Page ***"
                                                    )

                                                    def run(stdscr):
                                                        win, service = hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter Service:",
                                                            "Service:"
                                                        )

                                                        service = service.strip()
                                                        if not service or service == "":
                                                            hc.helper_functions.display_error(
                                                                win,
                                                                "Enter a valid service"
                                                            )
                                                        else:
                                                            depart.add_service(service)
                                                            hc.helper_functions.display_success_message(
                                                                win,
                                                                "Service Added Successfully"
                                                            )
                                                            sender.send_message(
                                                                f"A Service was Added to Department [ID: {depart.get_id()}]"
                                                            )

                                                        pp.tm.sleep(3)
                                                        manage_department()

                                                    wrapper(run)

                                                case 6:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Department Information Page ***"
                                                    )

                                                    depart.view_information()
                                                    manage_department()

                                                case _:
                                                    buildings_interface()

                                        manage_department()

                                wrapper(run)

                            case 2:
                                hc.helper_functions.display_page_heading("*** Manage Pharmacy Page ***")

                                def run(stdscr):
                                    headings = ["NO.", "ID", "Pharmacy Name", "Pharmacist Name"]
                                    cols_width = [5, 15, 30, 40]
                                    data = list()
                                    stop = True

                                    if "pharmacies" in pp.buildings:
                                        stop = False
                                        for i, phr in enumerate(pp.buildings["pharmacies"]):
                                            data.append([
                                                f"{i + 1}.",
                                                phr.get_id(),
                                                phr.get_pharmacy_name(),
                                                phr.get_pharmacist_name(),
                                            ])

                                    hc.helper_functions.display_table(
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

                                    win, pharmacy_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Pharmacy ID:",
                                        "Pharmacy ID:",
                                        2 + len(data)
                                    )

                                    pharma = None

                                    for phr in pp.buildings["pharmacies"]:
                                        if phr.get_id() == pharmacy_id:
                                            pharma = phr
                                            break

                                    if pharma is None:
                                        hc.helper_functions.display_error(
                                            win,
                                            "Incorrect Pharmacy ID"
                                        )
                                        tm.sleep(3)
                                        buildings_interface()

                                    else:
                                        def manage_pharmacy():
                                            hc.helper_functions.display_page_heading(
                                                "*** Manage Pharmacy Page ***"
                                            )

                                            option4 = hc.helper_functions.display_get_options([
                                                "Add Medicine Stock",
                                                "Check Medicine Stock",
                                                "Dispense Prescription",
                                                "View Current Stock",
                                                "View Pharmacy Information",
                                                "Go Back"
                                            ], "Select Option:")

                                            match option4:
                                                case 1:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Adding Medicine Stock Page ***"
                                                    )

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
                                                                win.addstr(
                                                                    3,
                                                                    5,
                                                                    f"Medicine Name:{(win_columns - len("Medicine Name:") - 5) * " "}",
                                                                    curses.A_BOLD
                                                                )
                                                                stdscr.move(rows // 4 + 2, columns // 4 + 26)
                                                                win.move(3, 27)
                                                                win.refresh()
                                                                val = hc.helper_functions.take_str(
                                                                    stdscr,
                                                                    win
                                                                ).strip()
                                                                if not val or val == "":
                                                                    raise ValueError
                                                            except ValueError:
                                                                win.addstr(
                                                                    win_rows - 1,
                                                                    0,
                                                                    "!!ERROR: Enter a valid medicine name!!",
                                                                    red_and_black
                                                                )
                                                                win.refresh()
                                                                return get_medicine_name()
                                                            except Exception as e:
                                                                win.addstr(
                                                                    win_rows - 1, 0,
                                                                    f"!!UNEXPECTED ERROR: {e}!!",
                                                                    red_and_black
                                                                )
                                                                win.refresh()
                                                                return get_medicine_name()
                                                            else:
                                                                win.addstr(
                                                                    win_rows - 1, 0,
                                                                    f"{(win_columns - 1) * " "}"
                                                                )
                                                                win.refresh()
                                                                return val
                                                        medicine_name = get_medicine_name()

                                                        def get_quantity():
                                                            try:
                                                                win.addstr(
                                                                    4,
                                                                    5,
                                                                    f"Quantity:{(win_columns - len("Quantity:") - 5) * " "}",
                                                                    curses.A_BOLD
                                                                )
                                                                stdscr.move(rows // 4 + 3, columns // 4 + 26)
                                                                win.move(4, 27)
                                                                win.refresh()
                                                                val = int(hc.helper_functions.take_str(
                                                                    stdscr,
                                                                    win
                                                                ).strip())
                                                                if val <= 0:
                                                                    raise ValueError
                                                            except ValueError:
                                                                win.addstr(
                                                                    win_rows - 1, 0,
                                                                    "!!ERROR: Enter a valid quantity!!",
                                                                    red_and_black
                                                                )
                                                                win.refresh()
                                                                return get_quantity()
                                                            except Exception as e:
                                                                win.addstr(
                                                                    win_rows - 1,
                                                                    0,
                                                                    f"!!UNEXPECTED ERROR: {e}!!", red_and_black
                                                                )
                                                                win.refresh()
                                                                return get_quantity()
                                                            else:
                                                                win.addstr(
                                                                    win_rows - 1,
                                                                    0,
                                                                    f"{(win_columns - 1) * " "}"
                                                                )
                                                                win.refresh()
                                                                return val
                                                        quantity = get_quantity()

                                                        hc.helper_functions.display_success_message(
                                                            win,
                                                            "Medicine Stock Added Successfully"
                                                        )
                                                        sender.send_message(
                                                            f"Medicine Stock was Added to Pharmacy [ID: {pharma.get_id()}]"
                                                        )
                                                        tm.sleep(3)

                                                        pharma.add_medicine_stock(medicine_name.lower(), quantity)
                                                        manage_pharmacy()

                                                    wrapper(run)

                                                case 2:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Check Medicine Stock Page ***"
                                                    )

                                                    def run(stdscr):
                                                        win, medicine_name = hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter Medicine Name:",
                                                            "Medicine Name:"
                                                        )

                                                        medicine_name = medicine_name.strip().lower()
                                                        if not medicine_name or medicine_name == "":
                                                            hc.helper_functions.display_error(
                                                                win,
                                                                "Enter a valid medicine name"
                                                            )
                                                        else:
                                                            quantity = pharma.check_stock(medicine_name)
                                                            if not quantity:
                                                                hc.helper_functions.display_error(
                                                                    win,
                                                                    f"{medicine_name} is out of stock!"
                                                                )
                                                            else:
                                                                hc.helper_functions.display_success_message(
                                                                    win,
                                                                    f"{medicine_name.capitalize()} is available in stock – {quantity} units."
                                                                )

                                                        pp.tm.sleep(3)
                                                        manage_pharmacy()

                                                    wrapper(run)

                                                case 3:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Dispense Prescription Page ***"
                                                    )

                                                    def run(stdscr):
                                                        win, prescription = hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter Prescription (Formatted [Name:Quantity,Name:Quantity,...])",
                                                            "Prescription:"
                                                        )

                                                        prescription = prescription.strip()
                                                        if not prescription or prescription == "":
                                                            hc.helper_functions.display_error(
                                                                win,
                                                                "Enter a valid Prescription"
                                                            )
                                                        else:
                                                            prescription = prescription.split(",")
                                                            for i in range(len(prescription)):
                                                                prescription[i] = prescription[i].split(":")
                                                                prescription[i][0] = prescription[i][0].lower()
                                                                prescription[i][1] = int(prescription[i][1])

                                                            can_dispense = pharma.dispense_medication(prescription)
                                                            if not can_dispense:
                                                                hc.helper_functions.display_error(
                                                                    win,
                                                                    "Some items in the prescription are out of stock"
                                                                )
                                                            else:
                                                                hc.helper_functions.display_success_message(
                                                                    win,
                                                                    "Prescription Dispensed Successfully"
                                                                )
                                                                sender.send_message(
                                                                    f"A Prescription was Dispensed from Pharmacy [ID: {pharma.get_id()}]"
                                                                )


                                                        pp.tm.sleep(3)
                                                        manage_pharmacy()

                                                    wrapper(run)

                                                case 4:
                                                    pharma.view_stock()
                                                    manage_pharmacy()

                                                case 5:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Pharmacy Information Page ***"
                                                    )

                                                    pharma.view_information()
                                                    manage_pharmacy()

                                                case _:
                                                    buildings_interface()

                                        manage_pharmacy()

                                wrapper(run)

                            case 3:
                                hc.helper_functions.display_page_heading("*** Manage Ward Page ***")

                                def run(stdscr):
                                    headings = ["NO.", "ID", "Room Type", "Availability"]
                                    cols_width = [5, 15, 15, 20]
                                    data = list()
                                    stop = True

                                    if "wards" in pp.buildings:
                                        stop = False
                                        for i, wd in enumerate(pp.buildings["wards"]):
                                            data.append([
                                                f"{i + 1}.",
                                                wd.get_id(),
                                                wd.get_room_type(),
                                                str(wd.check_availability())
                                            ])

                                    hc.helper_functions.display_table(
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

                                    win, ward_id = hc.helper_functions.take_user_input(
                                        stdscr,
                                        "Enter Ward ID:",
                                        "Ward ID:",
                                        2 + len(data)
                                    )

                                    wrd = None

                                    for wd in pp.buildings["wards"]:
                                        if wd.get_id() == ward_id:
                                            wrd = wd
                                            break

                                    if wrd is None:
                                        hc.helper_functions.display_error(
                                            win,
                                            "Incorrect Ward ID"
                                        )
                                        tm.sleep(3)
                                        buildings_interface()

                                    else:
                                        def manage_ward():
                                            hc.helper_functions.display_page_heading(
                                                "*** Manage Ward Page ***"
                                            )

                                            option4 = hc.helper_functions.display_get_options([
                                                "Reserve Room",
                                                "Discharge Patient",
                                                "Check Availability",
                                                "View Ward Information",
                                                "Go Back"
                                            ], "Select Option:")

                                            match option4:
                                                case 1:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Reserve Room page ***"
                                                    )
                                                    if not wrd.check_availability():
                                                        def run(stdscr):
                                                            rows, columns = stdscr.getmaxyx()
                                                            win = curses.newwin(
                                                                1,
                                                                columns // 2,
                                                                rows // 4 - 1,
                                                                columns // 4 - 1
                                                            )
                                                            hc.helper_functions.display_error(
                                                                win,
                                                                "Room is Currently Unavailable"
                                                            )
                                                            tm.sleep(3)

                                                        wrapper(run)
                                                        manage_ward()

                                                    def run(stdscr):
                                                        win, patient_id = hc.helper_functions.take_user_input(
                                                            stdscr,
                                                            "Enter Patient ID:", "Patient ID:"
                                                        )

                                                        if "patients" not in pp.persons:
                                                            hc.helper_functions.display_error(
                                                                win,
                                                                "Can't Find This Patient"
                                                            )
                                                            tm.sleep(3)
                                                            manage_ward()
                                                            return

                                                        for patient in pp.persons["patients"]:
                                                            if patient.get_id() == patient_id:
                                                                wrd.assign_room(patient)
                                                                hc.helper_functions.display_success_message(
                                                                    win,
                                                                    "Room Reserved Successfully"
                                                                )
                                                                sender.send_message(
                                                                    f"Ward [ID: {wrd.get_id()}] was Reserved"
                                                                )
                                                                tm.sleep(3)
                                                                manage_ward()
                                                                return

                                                        hc.helper_functions.display_error(
                                                            win,
                                                            "Can't Find This Patient"
                                                        )
                                                        tm.sleep(3)
                                                        manage_ward()

                                                    wrapper(run)

                                                case 2:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Discharge Patient page ***"
                                                    )
                                                    wrd.discharge_patient()
                                                    def run(stdscr):
                                                        rows, columns = stdscr.getmaxyx()
                                                        win = curses.newwin(
                                                            1,
                                                            columns // 2,
                                                            rows // 4 - 1,
                                                            columns // 4 - 1
                                                        )
                                                        hc.helper_functions.display_success_message(
                                                            win,
                                                            "Patient Discharged Successfully"
                                                        )
                                                        sender.send_message(
                                                            f"Patient Discharged From Ward [ID: {wrd.get_id()}]"
                                                        )
                                                        tm.sleep(3)

                                                    wrapper(run)
                                                    manage_ward()

                                                case 3:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Check Availability page ***"
                                                    )
                                                    is_free = wrd.check_availability()

                                                    def run(stdscr):
                                                        rows, columns = stdscr.getmaxyx()
                                                        win = curses.newwin(
                                                            1,
                                                            columns // 2,
                                                            rows // 4 - 1,
                                                            columns // 4 - 1
                                                        )
                                                        if is_free:
                                                            hc.helper_functions.display_success_message(
                                                                win,
                                                                "Room is Currently Available"
                                                            )
                                                        else:
                                                            hc.helper_functions.display_error(
                                                                win,
                                                                "Room is Currently Unavailable"
                                                            )
                                                        tm.sleep(3)

                                                    wrapper(run)
                                                    manage_ward()

                                                case 4:
                                                    hc.helper_functions.display_page_heading(
                                                        "*** Ward Information Page ***"
                                                    )

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
            conn = sqf.DatabaseConnection.get_db_connection()
            conn.close()
            sender.send_message("None")
            sender.sock.close()
            exit()


start_system()