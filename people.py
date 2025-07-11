import curses
from curses import wrapper
import time as tm

import helper_classes as hc
import sqlfunctions as sqf
import sender

persons = dict()
buildings = dict()


class Person:
    __number_of_persons: int = 0

    def __init__(self, name: str, age: int, gender: str) -> None:
        self._name: str = name
        self._age: int = age
        self._gender: str = gender
        self._contact_info = dict()
        self._security_info = dict()
        self._id: str = str()
        Person.__number_of_persons += 1

    def get_name(self) -> str:
        return self._name
    def get_age(self) -> int:
        return self._age
    def get_gender(self) -> str:
        return self._gender
    def get_contact_info(self) -> dict:
        return self._contact_info
    def get_security_info(self) -> dict:
        return self._security_info
    def get_id(self) -> str:
        return self._id

    @staticmethod
    def get_number_of_persons() -> int:
        return Person.__number_of_persons

    def set_name(self, name: str) -> None:
        self._name = name
    def set_age(self, age: int) -> None:
        self._age = age if age >= 0 else ValueError('Age not valid')
    def set_gender(self, gender: str) -> None:
        self._gender = gender
    def add_contact_info(self, key: str, value: str) -> None:
        self._contact_info[key] = value
    def add_security_info(self, key: str, value: str) -> None:
        self._security_info[key] = value


class Patient(Person):
    __number_of_patients: int = 0

    def __init__(self, name: str, age: int, gender: str):
        super().__init__(name, age, gender)
        Patient.__number_of_patients += 1
        self._id: str = hc.helper_functions.generate_id("PAT", Patient.get_number_of_patients())
        self._diagnosis = str()
        self._prescribed_treatment = str()
        self._assigned_doctor = str()
        self._medical_history = list()

    @staticmethod
    def get_number_of_patients() -> int:
        return Patient.__number_of_patients

    def get_diagnosis(self) -> str:
        return self._diagnosis
    def get_prescribed_treatment(self) -> str:
        return self._prescribed_treatment
    def get_assigned_doctor(self) -> str:
        return self._assigned_doctor

    def view_medical_history(self) -> None:
        hc.helper_functions.display_page_heading("Patient Records Page")

        def run(stdscr):
            headings = ["Name", "Age", "Gender", "Doctor", "Diagnosis", "Treatment", "Results", "Date", "Time"]
            cols_width = [30, 6, 8, 30, 20, 20, 11, 12, 10]
            data = list()

            for record in self._medical_history:
                data.append([
                    record.get_patient().get_name(),
                    record.get_patient().get_age(),
                    record.get_patient().get_gender(),
                    record.get_doctor().get_name(),
                    record.get_diagnosis(),
                    record.get_prescribed_treatment(),
                    record.get_test_results(),
                    record.get_date(),
                    record.get_time()
                ])
            hc.helper_functions.display_table(
                stdscr,
                6,
                "Patient Medical Records:",
                headings,
                data,
                cols_width
            )

        wrapper(run)

    def book_appointment(self) -> None:
        def run(stdscr):
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            green_and_black = curses.color_pair(3)

            rows, columns = stdscr.getmaxyx()

            win = curses.newwin(rows // 4, columns // 2, rows // 4 - 1, columns // 4 - 1)
            win.clear()

            win.addstr(0, 0, "Enter The Symptoms:", curses.A_BOLD | green_and_black)
            win.addstr(2, 0, f"{len("Enter The Symptoms:") * "-"}", curses.A_BOLD | green_and_black)

            curses.curs_set(1)

            label = "Symptoms:"
            win.addstr(4, 5, label, curses.A_BOLD)
            stdscr.move(rows // 4 + 3, columns // 4 + len(label) + 5)
            win.move(4, len(label) + 6)
            win.refresh()

            symptoms = hc.helper_functions.take_str(stdscr, win)
            appointment = hc.Appointment(self, symptoms)
            appointment.schedule_appointment()

            hc.helper_functions.display_success_message(win, "Appointment Booked Successfully")
            sender.send_message(
                f"Patient [ID: {self.get_id()}] Booked an Appointment"
            )
            tm.sleep(3)

        wrapper(run)

    def set_diagnosis(self, diagnosis: str) -> None:
        self._diagnosis = diagnosis
    def set_prescribed_treatment(self, prescribed_treatment: str) -> None:
        self._prescribed_treatment = prescribed_treatment
    def set_assigned_doctor(self, doctor) -> None:
        self._assigned_doctor = doctor
    def add_medical_record(self, record):
        self._medical_history.append(record)


class Doctor(Person):
    __number_of_doctors: int = 0

    def __init__(self, name: str, age: int, gender: str, specialization: str) -> None:
        super().__init__(name, age, gender)
        Doctor.__number_of_doctors += 1
        self._id: str = hc.helper_functions.generate_id("DOC", Doctor.get_number_of_doctors())
        self._specialization: str = specialization
        self._patients_list = list()

    def get_specialization(self) -> str:
        return self._specialization
    def get_patient_list(self) -> list:
        return self._patients_list

    @staticmethod
    def get_number_of_doctors() -> int:
        return Doctor.__number_of_doctors

    def add_patient(self, patient) -> None:
        if patient not in self._patients_list:
            self._patients_list.append(patient)
            patient.set_assigned_doctor(self.get_name())

            appointment = None
            for app in hc.appointments:
                if app.get_patient() == patient:
                    appointment = app
                    break
            if appointment is not None:
                appointment.set_doctor(self)

            conn = sqf.DatabaseConnection.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT patient_list FROM Doctor WHERE app_id = ?", (self.get_id(),))
            result = cursor.fetchone()[0]

            result += f":{patient.get_id()}"
            if result[0] == ":":
                result = result[1:]
            cursor.execute("UPDATE Doctor SET patient_list = ? WHERE app_id = ?", (result, self.get_id(),))
            conn.commit()

    def remove_patient(self, win, patient_id) -> None:
        idx = -1

        for i, patient in enumerate(self._patients_list):
            if patient.get_id() == patient_id:
                idx = i
                break

        if idx == -1:
            hc.helper_functions.display_error(win, "Can't Find This Patient")
            tm.sleep(3)
        else:
            conn = sqf.DatabaseConnection.get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT patient_list FROM Doctor WHERE app_id = ?", (self.get_id(),))
            pat_list = cursor.fetchone()[0].split(":")
            pat_list.remove(patient_id)
            result = ""
            for p in pat_list:
                result += f"{p}:"
            result = result[:-1]

            cursor.execute("UPDATE Doctor SET patient_list = ? WHERE app_id = ?", (result, self.get_id(),))
            conn.commit()

            self._patients_list[idx].set_assigned_doctor(str())
            del self._patients_list[idx]
            hc.helper_functions.display_success_message(win, "Patient Removed Successfully")
            sender.send_message(
                f"Doctor [ID: {self.get_id()}] Removed a Patient"
            )
            tm.sleep(3)

    def view_patients_list(self):
        hc.helper_functions.display_page_heading("Patients List Page")

        def run(stdscr):
            headings = ["Name", "Age", "Gender"]
            cols_width = [30, 6, 8]
            data = list()
            for patient in self._patients_list:
                data.append([patient.get_name(), patient.get_age(), patient.get_gender()])
            hc.helper_functions.display_table(
                stdscr,
                6,
                "Patients List:",
                headings,
                data,
                cols_width
            )

        wrapper(run)

    def diagnose_patient(self, win, patient_id: str) -> None:
        for patient in self._patients_list:
            if patient.get_id() == patient_id:
                def run(stdscr):
                    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
                    green_and_black = curses.color_pair(3)

                    rows, columns = stdscr.getmaxyx()

                    win.addstr(5, 0, "Enter Diagnosis:", curses.A_BOLD | green_and_black)
                    win.addstr(6, 0, f"{len("Enter Diagnosis:") * "-"}", curses.A_BOLD | green_and_black)

                    curses.curs_set(1)

                    label = "Diagnosis:"
                    win.addstr(8, 5, label, curses.A_BOLD)
                    stdscr.move(rows // 4 + 8, columns // 4 + len(label) + 5)
                    win.move(8, len(label) + 6)
                    win.refresh()

                    diagnosis = hc.helper_functions.take_str(stdscr, win)
                    patient.set_diagnosis(diagnosis)

                    conn = sqf.DatabaseConnection.get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Patient SET diagnosis = ? WHERE app_id = ?", (diagnosis, patient_id,))
                    conn.commit()

                    hc.helper_functions.display_success_message(win, "Patient Diagnosed Successfully")
                    sender.send_message(
                        f"Doctor [ID: {self.get_id()}] Diagnosed a Patient"
                    )
                    tm.sleep(3)

                wrapper(run)
                return

        hc.helper_functions.display_error(win, "Can't Find This Patient")
        tm.sleep(3)

    def prescribe_medication(self, win, patient_id: str):
        for patient in self._patients_list:
            if patient.get_id() == patient_id:
                def run(stdscr):
                    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
                    green_and_black = curses.color_pair(3)

                    rows, columns = stdscr.getmaxyx()

                    win.addstr(5, 0, "Enter Treatment:", curses.A_BOLD | green_and_black)
                    win.addstr(6, 0, f"{len("Enter Treatment:") * "-"}", curses.A_BOLD | green_and_black)

                    curses.curs_set(1)

                    label = "Treatment:"
                    win.addstr(8, 5, label, curses.A_BOLD)
                    stdscr.move(rows // 4 + 8, columns // 4 + len(label) + 5)
                    win.move(8, len(label) + 6)
                    win.refresh()

                    treatment = hc.helper_functions.take_str(stdscr, win)
                    patient.set_prescribed_treatment(treatment)

                    conn = sqf.DatabaseConnection.get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE Patient SET prescribed_treatment = ? WHERE app_id = ?",
                        (treatment, patient_id,)
                    )
                    conn.commit()

                    hc.helper_functions.display_success_message(
                        win,
                        "Treatment Prescribed Successfully"
                    )
                    sender.send_message(
                        f"Doctor [ID: {self.get_id()}] Prescribed Medication"
                    )
                    tm.sleep(3)

                wrapper(run)
                return

        hc.helper_functions.display_error(win, "Can't Find This Patient")
        tm.sleep(3)

    def add_patient_record(self, win, patient_id: str):
        for patient in self._patients_list:
            if patient.get_id() == patient_id:
                def run(stdscr):
                    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
                    green_and_black = curses.color_pair(3)

                    rows, columns = stdscr.getmaxyx()

                    win.addstr(5, 0, "Enter Test Results:", curses.A_BOLD | green_and_black)
                    win.addstr(6, 0, f"{len("Enter Test Results:") * "-"}", curses.A_BOLD | green_and_black)

                    curses.curs_set(1)

                    label = "Test Results:"
                    win.addstr(8, 5, label, curses.A_BOLD)
                    stdscr.move(rows // 4 + 8, columns // 4 + len(label) + 5)
                    win.move(8, len(label) + 6)
                    win.refresh()

                    test_results = hc.helper_functions.take_str(stdscr, win)
                    date = f"{str(hc.datetime.now().date())}"
                    time = f"{str(hc.datetime.now().time())[0:8]}"
                    record = hc.MedicalRecord(
                        patient,
                        self,
                        patient.get_diagnosis(),
                        patient.get_prescribed_treatment(),
                        test_results,
                        date,
                        time
                    )
                    patient.add_medical_record(record)
                    sqf.DBHandler.insert_medical_record(record, patient_id)

                    hc.helper_functions.display_success_message(
                        win,
                        "Patient Record Added Successfully"
                    )
                    sender.send_message(
                        f"Doctor [ID: {self.get_id()}] Added a Patient Record"
                    )
                    tm.sleep(3)

                wrapper(run)
                return

        hc.helper_functions.display_error(win, "Can't Find This Patient")
        tm.sleep(3)

    def view_patient_records(self, win, patient_id: str):
        for patient in self._patients_list:
            if patient.get_id() == patient_id:
                patient.view_medical_history()
                return

        hc.helper_functions.display_error(win, "Can't Find This Patient")
        tm.sleep(3)


class Nurse(Person):
    __number_of_nurses: int = 0

    def __init__(self, name: str, age: int, gender: str):
        super().__init__(name, age, gender)
        Nurse.__number_of_nurses += 1
        self._id: str = hc.helper_functions.generate_id("NUR", Nurse.get_number_of_nurses())
        self._assigned_ward = None
        self._assisted_doctor = None

    @staticmethod
    def get_number_of_nurses() -> int:
        return Nurse.__number_of_nurses

    def assign_ward(self, ward) -> None:
        self._assigned_ward = ward

    def assist_doctor(self, doctor):
        self._assisted_doctor = doctor

    def update_patient_statues(self, win, patient_id):
        appointment = None
        for app in hc.appointments:
            if app.get_patient().get_id() == patient_id:
                appointment = app
                break

        if appointment is not None:
            def run(stdscr):
                curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
                green_and_black = curses.color_pair(3)

                rows, columns = stdscr.getmaxyx()

                win.addstr(5, 0, "Enter Status:", curses.A_BOLD | green_and_black)
                win.addstr(6, 0, f"{len("Enter Status:") * "-"}", curses.A_BOLD | green_and_black)

                curses.curs_set(1)

                label = "Status:"
                win.addstr(8, 5, label, curses.A_BOLD)
                stdscr.move(rows // 4 + 7, columns // 4 + len(label) + 5)
                win.move(8, len(label) + 6)
                win.refresh()

                status = hc.helper_functions.take_str(stdscr, win)
                appointment.set_status(status)

                hc.helper_functions.display_success_message(win, "Status Updated Successfully")
                sender.send_message(
                    f"Nurse [ID: {self.get_id()}] Updated a Patient Status"
                )
                tm.sleep(3)

            wrapper(run)
            return

        hc.helper_functions.display_error(win, "Can't Find This Patient")
        tm.sleep(3)


class Administrator(Person):
    __number_of_administrator: int = 0

    def __init__(self, name: str, age: int, gender: str):
        super().__init__(name, age, gender)
        Administrator.__number_of_administrator += 1
        self._id: str = hc.helper_functions.generate_id(
            "ADM",
            Administrator.get_number_of_administrators()
        )

    @staticmethod
    def get_number_of_administrators() -> int:
        return Administrator.__number_of_administrator

    @staticmethod
    def add_doctor(doctor) -> None:
        if "doctors" not in persons:
            persons["doctors"] = list()
        persons["doctors"].append(doctor)
        sqf.DBHandler.insert_doctor(doctor)

    def remove_doctor(self, win, doctor_id) -> None:
        idx = -1
        if "doctors" not in persons:
            hc.helper_functions.display_error(win, "Can't Find This Doctor")
            tm.sleep(3)
            return

        for i, doctor in enumerate(persons["doctors"]):
            if doctor.get_id() == doctor_id:
                idx = i
                break

        if idx == -1:
            hc.helper_functions.display_error(win, "Can't Find This Doctor")
        else:
            del persons["doctors"][idx]
            hc.helper_functions.display_success_message(win, "Doctor Removed Successfully")
            sender.send_message(f"Admin [ID: {self.get_id()}] Removed a Doctor")

        tm.sleep(3)

    def manage_hospital_operations(self, win) -> None:
        hc.helper_functions.display_success_message(
            win,
            f"{self.get_name()} is managing hospital operations."
        )
        tm.sleep(3)