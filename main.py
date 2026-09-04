import curses
from curses import wrapper
import time as tm

import system as ss
import people as pp
import helper_classes as hc
import data_manager

# Load persistent application state into memory on startup
data_manager.load_app_state(pp.persons, pp.buildings, hc)

# --- Admin Interface ---
def admin_interface():
    # UI callback functions for admin actions
    def _remove_doctor_ui(stdscr):
        win, doctor_id = hc.helper_functions.take_user_input(
            stdscr,
            "Enter Doctor ID:",
            "Doctor ID:"
        )
        ss.current_user.remove_doctor(win, doctor_id)

    def _manage_ops_ui(stdscr):
        rows, columns = stdscr.getmaxyx()
        win = curses.newwin(
            1,
            columns // 2,
            rows // 4 - 1,
            columns // 4 - 1
        )
        ss.current_user.manage_hospital_operations(win)

    # Authenticate user before entering the interface loop
    if ss.current_user is None:
        is_logged = ss.HospitalManagementSystem.login_user("admins")
        if not is_logged:
            return

    # Main event loop for the Admin interface
    while True:
        hc.helper_functions.display_page_heading("*** Admin Page ***")
        option = hc.helper_functions.display_get_options([
            "Add Doctor",
            "Remove Doctor",
            "Generate Bill",
            "Manage Hospital Operations",
            "Log Out"
        ], f"####  Welcome Back, Mr. {ss.current_user.get_name()}  ####")

        match option:
            case 1:
                hc.helper_functions.display_page_heading("*** Registration Page ***")
                ss.current_user.add_doctor(
                    ss.HospitalManagementSystem.register_user("doctor")
                )

            case 2:
                hc.helper_functions.display_page_heading("*** Remove Doctor Page ***")
                wrapper(_remove_doctor_ui)

            case 3:
                hc.helper_functions.display_page_heading("*** Generate Bill Page ***")
                ss.HospitalManagementSystem.generate_bill()

            case 4:
                hc.helper_functions.display_page_heading("*** Hospital Operations page ***")
                wrapper(_manage_ops_ui)

            case _:
                ss.current_user = None
                return

# --- Doctor Interface ---
def doctor_interface():
    # UI callback functions for doctor actions
    def _add_patient_ui(stdscr):
        win, patient_id = hc.helper_functions.take_user_input(
            stdscr,
            "Enter Patient ID:",
            "Patient ID:"
        )

        if "patients" not in pp.persons:
            hc.helper_functions.display_error(win, "Can't Find This Patient")
            tm.sleep(3)
            return

        for patient in pp.persons["patients"]:
            if patient.get_id() == patient_id:
                ss.current_user.add_patient(patient)
                hc.helper_functions.display_success_message(win, "Patient Added Successfully")
                tm.sleep(3)
                return

        hc.helper_functions.display_error(win, "Can't Find This Patient")
        tm.sleep(3)

    def _remove_patient_ui(stdscr):
        win, patient_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Patient ID:", "Patient ID:"
        )
        ss.current_user.remove_patient(win, patient_id)

    def _diagnose_patient_ui(stdscr):
        win, patient_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Patient ID:", "Patient ID:"
        )
        ss.current_user.diagnose_patient(win, patient_id)

    def _prescribe_medication_ui(stdscr):
        win, patient_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Patient ID:", "Patient ID:"
        )
        ss.current_user.prescribe_medication(win, patient_id)

    def _add_patient_record_ui(stdscr):
        win, patient_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Patient ID:", "Patient ID:"
        )
        ss.current_user.add_patient_record(win, patient_id)

    def _view_patient_records_ui(stdscr):
        win, patient_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Patient ID:", "Patient ID:"
        )
        ss.current_user.view_patient_records(win, patient_id)


    if ss.current_user is None:
        is_logged = ss.HospitalManagementSystem.login_user("doctors")
        if not is_logged:
            return

    # Main event loop for the Doctor interface
    while True:
        hc.helper_functions.display_page_heading("*** Doctor Page ***")
        option = hc.helper_functions.display_get_options([
            "Add Patient",
            "Remove Patient",
            "View Patients List",
            "Diagnose Patient",
            "Prescribe Medication",
            "Add Patient Record",
            "View Patient Records",
            "Log Out"
        ], f"####  Welcome Back, Dr. {ss.current_user.get_name()}  ####")

        match option:
            case 1:
                hc.helper_functions.display_page_heading("*** Add Patient Page ***")
                wrapper(_add_patient_ui)
            case 2:
                hc.helper_functions.display_page_heading("*** Remove Patient Page ***")
                wrapper(_remove_patient_ui)
            case 3:
                ss.current_user.view_patients_list()
            case 4:
                hc.helper_functions.display_page_heading("*** Diagnose Patient Page ***")
                wrapper(_diagnose_patient_ui)
            case 5:
                hc.helper_functions.display_page_heading("*** Prescribe Medication Page ***")
                wrapper(_prescribe_medication_ui)
            case 6:
                hc.helper_functions.display_page_heading("*** Add Patient Record Page ***")
                wrapper(_add_patient_record_ui)
            case 7:
                hc.helper_functions.display_page_heading("*** Patient Records Page ***")
                wrapper(_view_patient_records_ui)
            case 8 | _:
                ss.current_user = None
                return

# --- Nurse Interface ---
def nurse_interface():
    # UI callback functions for nurse actions
    def _update_patient_status_ui(stdscr):
        win, patient_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Patient ID:", "Patient ID:"
        )
        ss.current_user.update_patient_statues(win, patient_id)

    def _assist_doctor_ui(stdscr):
        win, doctor_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Doctor ID:", "Doctor ID:"
        )

        if "doctors" not in pp.persons:
            hc.helper_functions.display_error(win, "Can't Find This Doctor")
            tm.sleep(3)
            return

        for doctor in pp.persons["doctors"]:
            if doctor.get_id() == doctor_id:
                ss.current_user.assist_doctor(doctor)
                hc.helper_functions.display_success_message(win, "Doctor Assisted Successfully")
                tm.sleep(3)
                return

        hc.helper_functions.display_error(win, "Can't Find This Doctor")
        tm.sleep(3)

    def _manage_ward_ui(stdscr):
        win, ward_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Ward ID:", "Ward ID:"
        )

        if "wards" not in pp.buildings:
            hc.helper_functions.display_error(win, "Can't Find This Ward")
            tm.sleep(3)
            return

        for ward in pp.buildings["wards"]:
            if ward.get_id() == ward_id:
                ss.current_user.assign_ward(ward)
                hc.helper_functions.display_success_message(win, "Ward Managed Successfully")
                tm.sleep(3)
                return

        hc.helper_functions.display_error(win, "Can't Find This Ward")
        tm.sleep(3)

    if ss.current_user is None:
        is_logged = ss.HospitalManagementSystem.login_user("nurses")
        if not is_logged:
            return

    # Main event loop for the Nurse interface
    while True:
        title = "Mr. "
        if ss.current_user.get_gender().lower() == "female":
            title = "Mrs. "
            
        hc.helper_functions.display_page_heading("*** Nurse Page ***")
        option = hc.helper_functions.display_get_options([
            "Update Patient Status",
            "Assist Doctor",
            "Manage Ward",
            "Log Out"
        ], f"####  Welcome Back, {title}{ss.current_user.get_name()}  ####")

        match option:
            case 1:
                hc.helper_functions.display_page_heading("*** Update Patient Status Page ***")
                wrapper(_update_patient_status_ui)
            case 2:
                hc.helper_functions.display_page_heading("*** Assist Doctor Page ***")
                wrapper(_assist_doctor_ui)
            case 3:
                hc.helper_functions.display_page_heading("*** Manage Ward Page ***")
                wrapper(_manage_ward_ui)
            case 4 | _:
                ss.current_user = None
                return

# --- Patient Interface ---
def patient_interface():
    # UI callback functions for patient actions
    def _view_and_pay_bills_ui(stdscr):
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
            stdscr, 6, "All Bills:", headings, data, cols_width, stop
        )

        if stop:
            return

        win, bill_id = hc.helper_functions.take_user_input(
            stdscr, "Enter Bill ID:", "Bill ID:", 2 + len(data)
        )

        bill = None
        for bll in hc.bills:
            if bll.get_id() == bill_id:
                bill = bll
                break

        if bill is None:
            hc.helper_functions.display_error(win, "Incorrect Bill ID")
        else:
            bill.process_payment()
            hc.helper_functions.display_success_message(win, "Bill Paid Successfully")

        tm.sleep(3)

    def _display_patient_info_ui(stdscr):
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
            stdscr, 6, "Patient Information:", headings, data, cols_width
        )

    if ss.current_user is None:
        is_logged = ss.HospitalManagementSystem.login_user("patients")
        if not is_logged:
            return

    # Main event loop for the Patient interface
    while True:
        title = "Mr. "
        if ss.current_user.get_gender().lower() == "female":
            title = "Mrs. "
            
        hc.helper_functions.display_page_heading("*** Patient Page ***")
        option = hc.helper_functions.display_get_options([
            "Book Appointment",
            "View Medical History",
            "View & Pay Bills",
            "Display Patient Information",
            "Log Out"
        ], f"####  Welcome Back, {title}{ss.current_user.get_name()}  ####")

        match option:
            case 1:
                hc.helper_functions.display_page_heading("*** Appointment Booking Page ***")
                ss.current_user.book_appointment()
            case 2:
                hc.helper_functions.display_page_heading("*** Patient Records Page ***")
                ss.current_user.view_patient_records()
            case 3:
                hc.helper_functions.display_page_heading("*** View & Pay Bills Page ***")
                wrapper(_view_and_pay_bills_ui)
            case 4:
                hc.helper_functions.display_page_heading("*** Patient Information Page ***")
                wrapper(_display_patient_info_ui)
            case 5 | _:
                ss.current_user = None
                return

# --- Main Login Routing ---
def handle_login():
    hc.helper_functions.display_page_heading("*** Log In Page ***")
    option = hc.helper_functions.display_get_options([
        "Admin", "Doctor", "Nurse", "Patient", "Go Back"
    ], "Log In As:")
    
    match option:
        case 1:
            admin_interface()
        case 2:
            doctor_interface()
        case 3:
            nurse_interface()
        case 4:
            patient_interface()
        case 5:
            return

# --- Registration Interface ---
def handle_registration():
    hc.helper_functions.display_page_heading("*** Registration Page ***")

    option = hc.helper_functions.display_get_options([
        "Admin",
        "Doctor",
        "Nurse",
        "Patient",
        "Go Back"
    ], "Register As:")

    match option:
        case 1:
            hc.helper_functions.display_page_heading("*** Admin Registration Page ***")
            admin = ss.HospitalManagementSystem.register_user("admin")
            pp.persons.setdefault("admins", []).append(admin)

        case 2:
            hc.helper_functions.display_page_heading("*** Doctor Registration Page ***")
            doctor = ss.HospitalManagementSystem.register_user("doctor")
            pp.persons.setdefault("doctors", []).append(doctor)

        case 3:
            hc.helper_functions.display_page_heading("*** Nurse Registration Page ***")
            nurse = ss.HospitalManagementSystem.register_user("nurse")
            pp.persons.setdefault("nurses", []).append(nurse)

        case 4:
            hc.helper_functions.display_page_heading("*** Patient Registration Page ***")
            patient = ss.HospitalManagementSystem.register_user("patient")
            pp.persons.setdefault("patients", []).append(patient)

        case 5 | _:
            return

# --- Buildings Interface & Sub-Loops ---
def handle_buildings():
    def _manage_department_loop(depart):
        def _set_head_ui(stdscr):
            win, head_of_department = hc.helper_functions.take_user_input(
                stdscr, "Enter The Head of Department:", "Head of Department Name:"
            )
            head_of_department = head_of_department.strip()
            if not head_of_department:
                hc.helper_functions.display_error(win, "Enter a valid name")
            else:
                depart.set_head_of_department(head_of_department)
                hc.helper_functions.display_success_message(win, "Head of Department Set Successfully")
            tm.sleep(3)

        def _add_doctor_ui(stdscr):
            win, doctor_id = hc.helper_functions.take_user_input(
                stdscr, "Enter Doctor ID:", "Doctor ID:"
            )
            if "doctors" not in pp.persons:
                hc.helper_functions.display_error(win, "Can't Find This Doctor")
                tm.sleep(3)
                return

            for doctor in pp.persons["doctors"]:
                if doctor.get_id() == doctor_id:
                    depart.add_doctor(doctor)
                    hc.helper_functions.display_success_message(win, "Doctor Added Successfully")
                    tm.sleep(3)
                    return

            hc.helper_functions.display_error(win, "Can't Find This Doctor")
            tm.sleep(3)

        def _remove_doctor_ui(stdscr):
            win, doctor_id = hc.helper_functions.take_user_input(
                stdscr, "Enter Doctor ID:", "Doctor ID:"
            )
            depart.remove_doctor(win, doctor_id)

        def _add_service_ui(stdscr):
            win, service = hc.helper_functions.take_user_input(
                stdscr, "Enter Service:", "Service:"
            )
            service = service.strip()
            if not service:
                hc.helper_functions.display_error(win, "Enter a valid service")
            else:
                depart.add_service(service)
                hc.helper_functions.display_success_message(win, "Service Added Successfully")
            tm.sleep(3)

        while True:
            hc.helper_functions.display_page_heading("*** Manage Department Page ***")
            option = hc.helper_functions.display_get_options([
                "Set Head of Department", "Add Doctor", "Remove Doctor",
                "View Doctors List", "Add Service", "View Department Information", "Go Back"
            ], "Select Option:")

            match option:
                case 1:
                    hc.helper_functions.display_page_heading("*** Setting Head of Department Page ***")
                    wrapper(_set_head_ui)
                case 2:
                    hc.helper_functions.display_page_heading("*** Add Doctor Page ***")
                    wrapper(_add_doctor_ui)
                case 3:
                    hc.helper_functions.display_page_heading("*** Remove Doctor Page ***")
                    wrapper(_remove_doctor_ui)
                case 4:
                    depart.view_doctors_list()
                case 5:
                    hc.helper_functions.display_page_heading("*** Add Service Page ***")
                    wrapper(_add_service_ui)
                case 6:
                    hc.helper_functions.display_page_heading("*** Department Information Page ***")
                    depart.view_information()
                case 7 | _:
                    return


    def _manage_pharmacy_loop(pharma):
        def _add_stock_ui(stdscr):
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            red_and_black = curses.color_pair(2)
            green_and_black = curses.color_pair(3)
            rows, columns = stdscr.getmaxyx()
            win = curses.newwin(rows // 2, columns // 2, rows // 4 - 1, columns // 4 - 1)
            win_rows, win_columns = win.getmaxyx()
            win.clear()

            win.addstr(0, 0, "Enter Medicine Name and Quantity:", curses.A_BOLD | green_and_black)
            win.addstr(1, 0, "---------------------------------", curses.A_BOLD | green_and_black)
            curses.curs_set(1)

            def get_medicine_name():
                try:
                    win.addstr(3, 5, f"Medicine Name:{(win_columns - len('Medicine Name:') - 5) * ' '}", curses.A_BOLD)
                    stdscr.move(rows // 4 + 2, columns // 4 + 26)
                    win.move(3, 27)
                    win.refresh()
                    val = hc.helper_functions.take_str(stdscr, win).strip()
                    if not val: raise ValueError
                    return val
                except ValueError:
                    win.addstr(win_rows - 1, 0, "!!ERROR: Enter a valid medicine name!!", red_and_black)
                    win.refresh()
                    return get_medicine_name()
                except Exception as e:
                    win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                    win.refresh()
                    return get_medicine_name()

            def get_quantity():
                try:
                    win.addstr(4, 5, f"Quantity:{(win_columns - len('Quantity:') - 5) * ' '}", curses.A_BOLD)
                    stdscr.move(rows // 4 + 3, columns // 4 + 26)
                    win.move(4, 27)
                    win.refresh()
                    val = int(hc.helper_functions.take_str(stdscr, win).strip())
                    if val <= 0: raise ValueError
                    return val
                except ValueError:
                    win.addstr(win_rows - 1, 0, "!!ERROR: Enter a valid quantity!!", red_and_black)
                    win.refresh()
                    return get_quantity()
                except Exception as e:
                    win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                    win.refresh()
                    return get_quantity()

            medicine_name = get_medicine_name()
            quantity = get_quantity()

            hc.helper_functions.display_success_message(win, "Medicine Stock Added Successfully")
            tm.sleep(3)
            pharma.add_medicine_stock(medicine_name.lower(), quantity)

        def _check_stock_ui(stdscr):
            win, medicine_name = hc.helper_functions.take_user_input(
                stdscr, "Enter Medicine Name:", "Medicine Name:"
            )
            medicine_name = medicine_name.strip().lower()
            if not medicine_name:
                hc.helper_functions.display_error(win, "Enter a valid medicine name")
            else:
                quantity = pharma.check_stock(medicine_name)
                if not quantity:
                    hc.helper_functions.display_error(win, f"{medicine_name} is out of stock!")
                else:
                    hc.helper_functions.display_success_message(win, f"{medicine_name.capitalize()} is available in stock – {quantity} units.")
            tm.sleep(3)

        def _dispense_prescription_ui(stdscr):
            win, prescription = hc.helper_functions.take_user_input(
                stdscr, "Enter Prescription (Formatted [Name:Quantity,Name:Quantity,...])", "Prescription:"
            )
            prescription = prescription.strip()
            if not prescription:
                hc.helper_functions.display_error(win, "Enter a valid Prescription")
            else:
                try:
                    prescription_list = []
                    for item in prescription.split(","):
                        name, qty = item.split(":")
                        prescription_list.append([name.lower(), int(qty)])
                    
                    if not pharma.dispense_medication(prescription_list):
                        hc.helper_functions.display_error(win, "Some items are out of stock")
                    else:
                        hc.helper_functions.display_success_message(win, "Prescription Dispensed Successfully")
                except:
                    hc.helper_functions.display_error(win, "Invalid format")
            tm.sleep(3)

        while True:
            hc.helper_functions.display_page_heading("*** Manage Pharmacy Page ***")
            option = hc.helper_functions.display_get_options([
                "Add Medicine Stock", "Check Medicine Stock", "Dispense Prescription",
                "View Current Stock", "View Pharmacy Information", "Go Back"
            ], "Select Option:")

            match option:
                case 1:
                    hc.helper_functions.display_page_heading("*** Adding Medicine Stock Page ***")
                    wrapper(_add_stock_ui)
                case 2:
                    hc.helper_functions.display_page_heading("*** Check Medicine Stock Page ***")
                    wrapper(_check_stock_ui)
                case 3:
                    hc.helper_functions.display_page_heading("*** Dispense Prescription Page ***")
                    wrapper(_dispense_prescription_ui)
                case 4:
                    pharma.view_stock()
                case 5:
                    hc.helper_functions.display_page_heading("*** Pharmacy Information Page ***")
                    pharma.view_information()
                case 6 | _:
                    return


    def _manage_ward_loop(wrd):
        def _reserve_room_ui(stdscr):
            rows, columns = stdscr.getmaxyx()
            win = curses.newwin(1, columns // 2, rows // 4 - 1, columns // 4 - 1)
            hc.helper_functions.display_error(win, "Room is Currently Unavailable")
            tm.sleep(3)

        def _assign_patient_ui(stdscr):
            win, patient_id = hc.helper_functions.take_user_input(stdscr, "Enter Patient ID:", "Patient ID:")
            if "patients" not in pp.persons:
                hc.helper_functions.display_error(win, "Can't Find This Patient")
                tm.sleep(3)
                return

            for patient in pp.persons["patients"]:
                if patient.get_id() == patient_id:
                    wrd.assign_room(patient)
                    hc.helper_functions.display_success_message(win, "Room Reserved Successfully")
                    tm.sleep(3)
                    return
            hc.helper_functions.display_error(win, "Can't Find This Patient")
            tm.sleep(3)

        def _discharge_patient_ui(stdscr):
            rows, columns = stdscr.getmaxyx()
            win = curses.newwin(1, columns // 2, rows // 4 - 1, columns // 4 - 1)
            hc.helper_functions.display_success_message(win, "Patient Discharged Successfully")
            tm.sleep(3)

        def _check_availability_ui(stdscr):
            rows, columns = stdscr.getmaxyx()
            win = curses.newwin(1, columns // 2, rows // 4 - 1, columns // 4 - 1)
            if wrd.check_availability():
                hc.helper_functions.display_success_message(win, "Room is Currently Available")
            else:
                hc.helper_functions.display_error(win, "Room is Currently Unavailable")
            tm.sleep(3)

        while True:
            hc.helper_functions.display_page_heading("*** Manage Ward Page ***")
            option = hc.helper_functions.display_get_options([
                "Reserve Room", "Discharge Patient", "Check Availability",
                "View Ward Information", "Go Back"
            ], "Select Option:")

            match option:
                case 1:
                    hc.helper_functions.display_page_heading("*** Reserve Room page ***")
                    if not wrd.check_availability():
                        wrapper(_reserve_room_ui)
                    else:
                        wrapper(_assign_patient_ui)
                case 2:
                    hc.helper_functions.display_page_heading("*** Discharge Patient page ***")
                    wrd.discharge_patient()
                    wrapper(_discharge_patient_ui)
                case 3:
                    hc.helper_functions.display_page_heading("*** Check Availability page ***")
                    wrapper(_check_availability_ui)
                case 4:
                    hc.helper_functions.display_page_heading("*** Ward Information Page ***")
                    wrd.view_information()
                case 5 | _:
                    return


    # Main event loop for building management
    while True:
        hc.helper_functions.display_page_heading("*** Buildings Management Page ***")
        option = hc.helper_functions.display_get_options([
            "Add Building", "Remove Building", "Manage Building", "Go Back"
        ], "Select Option:")

        match option:
            case 1:
                hc.helper_functions.display_page_heading("*** Add Building Page ***")
                opt_add = hc.helper_functions.display_get_options(["Department", "Pharmacy", "Ward", "Go Back"], "Add:")
                
                if opt_add == 1:
                    hc.helper_functions.display_page_heading("*** Add Department Page ***")
                    department = ss.HospitalManagementSystem.add_building("department")
                    pp.buildings.setdefault("departments", []).append(department)
                elif opt_add == 2:
                    hc.helper_functions.display_page_heading("*** Add Pharmacy Page ***")
                    pharmacy = ss.HospitalManagementSystem.add_building("pharmacy")
                    pp.buildings.setdefault("pharmacies", []).append(pharmacy)
                elif opt_add == 3:
                    hc.helper_functions.display_page_heading("*** Add Ward Page ***")
                    ward = ss.HospitalManagementSystem.add_building("ward")
                    pp.buildings.setdefault("wards", []).append(ward)

            case 2:
                hc.helper_functions.display_page_heading("*** Remove Building Page ***")
                opt_rm = hc.helper_functions.display_get_options(["Department", "Pharmacy", "Ward", "Go Back"], "Remove:")
                
                def _remove_building_ui(stdscr, building_type, key):
                    win, b_id = hc.helper_functions.take_user_input(stdscr, f"Enter {building_type} ID:", f"{building_type} ID:")
                    if key not in pp.buildings:
                        hc.helper_functions.display_error(win, f"Can't Find This {building_type}")
                        tm.sleep(3)
                        return
                    
                    for i, b in enumerate(pp.buildings[key]):
                        if b.get_id() == b_id:
                            del pp.buildings[key][i]
                            hc.helper_functions.display_success_message(win, f"{building_type} Removed Successfully")
                            tm.sleep(3)
                            return
                    hc.helper_functions.display_error(win, f"Can't Find This {building_type}")
                    tm.sleep(3)

                if opt_rm == 1:
                    hc.helper_functions.display_page_heading("*** Remove Department Page ***")
                    wrapper(lambda stdscr: _remove_building_ui(stdscr, "Department", "departments"))
                elif opt_rm == 2:
                    hc.helper_functions.display_page_heading("*** Remove Pharmacy Page ***")
                    wrapper(lambda stdscr: _remove_building_ui(stdscr, "Pharmacy", "pharmacies"))
                elif opt_rm == 3:
                    hc.helper_functions.display_page_heading("*** Remove Ward Page ***")
                    wrapper(lambda stdscr: _remove_building_ui(stdscr, "Ward", "wards"))

            case 3:
                hc.helper_functions.display_page_heading("*** Manage Building Page ***")
                opt_mng = hc.helper_functions.display_get_options(["Department", "Pharmacy", "Ward", "Go Back"], "Manage:")
                
                def _select_building_ui(stdscr, title, headings, cols_width, key):
                    if key not in pp.buildings or not pp.buildings[key]:
                        return None, True 
                    
                    data = []
                    for i, b in enumerate(pp.buildings[key]):
                        if key == "departments":
                            data.append([f"{i+1}.", b.get_id(), b.get_name(), str(b.get_services_offered())[1:-1].replace("'", "")])
                        elif key == "pharmacies":
                            data.append([f"{i+1}.", b.get_id(), b.get_pharmacy_name(), b.get_pharmacist_name()])
                        elif key == "wards":
                            data.append([f"{i+1}.", b.get_id(), b.get_room_type(), str(b.check_availability())])
                            
                    hc.helper_functions.display_table(stdscr, 6, title, headings, data, cols_width, False)
                    win, b_id = hc.helper_functions.take_user_input(stdscr, "Enter ID:", "ID:", 2+len(data))
                    
                    for b in pp.buildings[key]:
                        if b.get_id() == b_id:
                            return b, False
                    
                    hc.helper_functions.display_error(win, "Incorrect ID")
                    tm.sleep(3)
                    return None, False

                if opt_mng == 1:
                    hc.helper_functions.display_page_heading("*** Manage Department Page ***")
                    # Use a mutable list to extract the selection from the curses wrapper
                    result = []
                    wrapper(lambda stdscr: result.append(_select_building_ui(
                        stdscr, "Current Departments:", ["NO.", "ID", "Name", "Services Offered"], 
                        [5, 15, 20, 100], "departments"
                    )))
                    if result and result[0][0]:
                        _manage_department_loop(result[0][0])
                        
                elif opt_mng == 2:
                    hc.helper_functions.display_page_heading("*** Manage Pharmacy Page ***")
                    result = []
                    wrapper(lambda stdscr: result.append(_select_building_ui(
                        stdscr, "Current Pharmacies:", ["NO.", "ID", "Pharmacy Name", "Pharmacist Name"], 
                        [5, 15, 30, 40], "pharmacies"
                    )))
                    if result and result[0][0]:
                        _manage_pharmacy_loop(result[0][0])
                        
                elif opt_mng == 3:
                    hc.helper_functions.display_page_heading("*** Manage Ward Page ***")
                    result = []
                    wrapper(lambda stdscr: result.append(_select_building_ui(
                        stdscr, "Current Wards:", ["NO.", "ID", "Room Type", "Availability"], 
                        [5, 15, 15, 20], "wards"
                    )))
                    if result and result[0][0]:
                        _manage_ward_loop(result[0][0])

            case 4 | _:
                return

# --- Main Application Loop ---
def start_system() -> None:
    while True:
        wrapper(ss.HospitalManagementSystem.display_starting_page)

        option = hc.helper_functions.display_get_options([
            "Log In", 
            "Register", 
            "Buildings", 
            "Exit"
        ], "Select Option:")
        
        match option:
            case 1:
                handle_login()
            case 2:
                handle_registration()
            case 3:
                handle_buildings()
            case 4 | _:
                # Persist state before shutting down the application
                data_manager.save_app_state(pp.persons, pp.buildings, hc)
                break

if __name__ == "__main__":
    start_system()