import time as tm
import curses
from curses import wrapper

from email_validator import validate_email, EmailNotValidError

import people as pp

current_user = None


class LoadFromDB:
    @staticmethod
    def load_patients():
        patient_info = pp.hc.sqf.DBHandler.get_table("Patient")
        for pat in patient_info:
            patient = pp.Patient(pat[2], pat[3], pat[4])
            contact_info = pat[5].split(",")
            patient.add_contact_info("email", contact_info[0])
            patient.add_contact_info("phone_number", contact_info[1])
            security_info = pat[6].split(",")
            patient.add_security_info("email", security_info[0])
            patient.add_security_info("password", security_info[1])
            patient.set_diagnosis(pat[7])
            patient.set_prescribed_treatment(pat[8])
            patient.set_assigned_doctor(pat[9])

            if "patients" not in pp.persons:
                pp.persons["patients"] = list()
            pp.persons["patients"].append(patient)

    @staticmethod
    def load_doctors():
        doctor_info = pp.hc.sqf.DBHandler.get_table("Doctor")
        for doc in doctor_info:
            doctor = pp.Doctor(doc[2], doc[3], doc[4], doc[7])
            contact_info = doc[5].split(",")
            doctor.add_contact_info("email", contact_info[0])
            doctor.add_contact_info("phone_number", contact_info[1])
            security_info = doc[6].split(",")
            doctor.add_security_info("email", security_info[0])
            doctor.add_security_info("password", security_info[1])
            patient_list = doc[8].split(":")
            for pat in pp.persons["patients"]:
                if pat.get_id() in patient_list:
                    doctor.add_patient(pat)

            if "doctors" not in pp.persons:
                pp.persons["doctors"] = list()
            pp.persons["doctors"].append(doctor)

    @staticmethod
    def load_admins():
        admin_info = pp.hc.sqf.DBHandler.get_table("Administrator")
        for adm in admin_info:
            admin = pp.Administrator(adm[2], adm[3], adm[4])
            contact_info = adm[5].split(",")
            admin.add_contact_info("email", contact_info[0])
            admin.add_contact_info("phone_number", contact_info[1])
            security_info = adm[6].split(",")
            admin.add_security_info("email", security_info[0])
            admin.add_security_info("password", security_info[1])

            if "admins" not in pp.persons:
                pp.persons["admins"] = list()
            pp.persons["admins"].append(admin)

    @staticmethod
    def load_records():
        record_info = pp.hc.sqf.DBHandler.get_table("MedicalRecord")
        for record in record_info:
            pat_id, doc_id = record[2], record[3]
            patient, doctor = None, None
            for pat in pp.persons["patients"]:
                if pat.get_id() == pat_id:
                    patient = pat
                    break
            for doc in pp.persons["doctors"]:
                if doc.get_id() == doc_id:
                    doctor = doc
                    break

            medical_record = pp.hc.MedicalRecord(patient, doctor, record[4], record[5], record[6], record[7], record[8])
            patient.add_medical_record(medical_record)



class HospitalManagementSystem:
    @staticmethod
    def display_starting_page(stdscr) -> None:
        pp.hc.helper_functions.display_page_heading("*** Welcome to Hospital Management System ***")

        blue_and_black = curses.color_pair(1)
        columns = curses.COLS
        date = f"Date: {str(pp.hc.datetime.now().date())}"
        time = f"Time: {str(pp.hc.datetime.now().time())[0:8]}"
        stdscr.addstr(f"{date}{(columns - len(date) - len(time)) * " "}{time}", blue_and_black)

        stdscr.refresh()


    @staticmethod
    def login_user(users: str) -> bool:
        pp.hc.helper_functions.display_page_heading("*** Log In Page ***")
        def run(stdscr):
            global current_user

            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            green_and_black = curses.color_pair(3)

            rows, columns = stdscr.getmaxyx()

            win = curses.newwin(rows // 2, columns // 2, rows // 4 - 1, columns // 4 - 1)
            win.clear()

            win.addstr(0, 0, "Enter email and password:", curses.A_BOLD | green_and_black)
            win.addstr(1, 0, "-------------------------", curses.A_BOLD | green_and_black)

            curses.curs_set(1)

            win.addstr(3, 5, f"Email:", curses.A_BOLD)
            stdscr.move(rows // 4 + 2, columns // 4 + 14)
            win.move(3, 15)
            win.refresh()
            email = pp.hc.helper_functions.take_str(stdscr, win)

            win.addstr(4, 5, f"Password:", curses.A_BOLD)
            stdscr.move(rows // 4 + 3, columns // 4 + 14)
            win.move(4, 15)
            win.refresh()
            password = pp.hc.helper_functions.take_str(stdscr, win)

            if users not in pp.persons:
                pp.hc.helper_functions.display_error(win, "Invalid Credentials Please Try again")
                tm.sleep(3)
                return False

            for user in pp.persons[users]:
                security_info = user.get_security_info()
                if security_info["email"] == email and security_info["password"] == password:
                    current_user = user
                    pp.hc.helper_functions.display_success_message(win, "Log In Completed Successfully")
                    tm.sleep(3)
                    return True

            pp.hc.helper_functions.display_error(win, "Invalid Credentials Please Try again")
            tm.sleep(3)
            return False

        return wrapper(run)


    @staticmethod
    def register_user(user: str):
        def run(stdscr):
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            red_and_black = curses.color_pair(2)
            green_and_black = curses.color_pair(3)

            rows, columns = stdscr.getmaxyx()

            win = curses.newwin(rows // 2, columns // 2, rows // 4 - 1, columns // 4 - 1)
            win_rows, win_columns = win.getmaxyx()
            win.clear()

            win.addstr(0, 0, "Complete the following data:", curses.A_BOLD | green_and_black)
            win.addstr(1, 0, "----------------------------", curses.A_BOLD | green_and_black)

            curses.curs_set(1)

            def get_name():
                try:
                    win.addstr(3, 5, f"Full Name:{(win_columns-len("Full Name:")-5) * " "}", curses.A_BOLD)
                    stdscr.move(rows // 4 + 2, columns // 4 + 26)
                    win.move(3, 27)
                    win.refresh()
                    val = pp.hc.helper_functions.take_str(stdscr, win).strip()
                    if not val or val == "":
                        raise ValueError
                except ValueError:
                    win.addstr(win_rows-1, 0, "!!ERROR: Enter a valid name!!", red_and_black)
                    win.refresh()
                    return get_name()
                except Exception as e:
                    win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                    win.refresh()
                    return get_name()
                else:
                    win.addstr(win_rows - 1, 0, f"{(win_columns-1) * " "}")
                    win.refresh()
                    return val
            name = get_name()

            def get_age():
                try:
                    win.addstr(4, 5, f"Age:{(win_columns-len("Age:")-5) * " "}", curses.A_BOLD)
                    stdscr.move(rows // 4 + 3, columns // 4 + 26)
                    win.move(4, 27)
                    win.refresh()
                    val = int(pp.hc.helper_functions.take_str(stdscr, win).strip())
                    if user == "patient":
                        if val < 0 or val > 150:
                            raise ValueError
                    else:
                        if val < 18 or val > 80:
                            raise ValueError
                except ValueError:
                    win.addstr(win_rows-1, 0, "!!ERROR: Enter a valid age!!", red_and_black)
                    win.refresh()
                    return get_age()
                except Exception as e:
                    win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                    win.refresh()
                    return get_age()
                else:
                    win.addstr(win_rows - 1, 0, f"{(win_columns-1) * " "}")
                    win.refresh()
                    return val
            age = get_age()

            def get_gender():
                try:
                    win.addstr(5, 5, f"Gender(Male/Female):{(win_columns-len("Gender(Male/Female):")-5) * " "}", curses.A_BOLD)
                    stdscr.move(rows // 4 + 4, columns // 4 + 26)
                    win.move(5, 27)
                    win.refresh()
                    val = pp.hc.helper_functions.take_str(stdscr, win).strip().lower()
                    if val != "male" and val != "female":
                        raise ValueError
                except ValueError:
                    win.addstr(win_rows-1, 0, "!!ERROR: Enter a valid gender!!", red_and_black)
                    win.refresh()
                    return get_gender()
                except Exception as e:
                    win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                    win.refresh()
                    return get_gender()
                else:
                    win.addstr(win_rows - 1, 0, f"{(win_columns-1) * " "}")
                    win.refresh()
                    return val
            gender = get_gender()

            def get_email():
                try:
                    win.addstr(6, 5, f"Email:{(win_columns-len("Email:")-5) * " "}", curses.A_BOLD)
                    stdscr.move(rows // 4 + 5, columns // 4 + 26)
                    win.move(6, 27)
                    win.refresh()
                    val = pp.hc.helper_functions.take_str(stdscr, win).strip()
                    v = validate_email(val)
                    val = v["email"]
                except EmailNotValidError:
                    win.addstr(win_rows-1, 0, "!!ERROR: Enter a valid email!!", red_and_black)
                    win.refresh()
                    return get_email()
                except Exception as e:
                    win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                    win.refresh()
                    return get_email()
                else:
                    win.addstr(win_rows - 1, 0, f"{(win_columns-1) * " "}")
                    win.refresh()
                    return val
            email = get_email()

            def get_password():
                try:
                    win.addstr(7, 5, f"Password:{(win_columns-len("Password:")-5) * " "}", curses.A_BOLD)
                    stdscr.move(rows // 4 + 6, columns // 4 + 26)
                    win.move(7, 27)
                    win.refresh()
                    val = pp.hc.helper_functions.take_str(stdscr, win)
                    if len(val) < 8:
                        raise ValueError
                except ValueError:
                    win.addstr(win_rows-1, 0, "!!ERROR: Enter a valid password!!", red_and_black)
                    win.refresh()
                    return get_password()
                except Exception as e:
                    win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                    win.refresh()
                    return get_password()
                else:
                    win.addstr(win_rows - 1, 0, f"{(win_columns-1) * " "}")
                    win.refresh()
                    return val
            password = get_password()

            def get_number():
                try:
                    win.addstr(8, 5, f"Phone Number:{(win_columns-len("Phone Number:")-5) * " "}", curses.A_BOLD)
                    stdscr.move(rows // 4 + 7, columns // 4 + 26)
                    win.move(8, 27)
                    win.refresh()
                    val = pp.hc.helper_functions.take_str(stdscr, win)
                    for char in val:
                        if char < "0" or char > "9":
                            raise ValueError
                except ValueError:
                    win.addstr(win_rows-1, 0, "!!ERROR: Enter a valid phone number!!", red_and_black)
                    win.refresh()
                    return get_number()
                except Exception as e:
                    win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                    win.refresh()
                    return get_number()
                else:
                    win.addstr(win_rows - 1, 0, f"{(win_columns-1) * " "}")
                    win.refresh()
                    return val
            number = get_number()

            if user == "doctor":
                def get_specialization():
                    try:
                        win.addstr(9, 5, f"Specialization:{(win_columns - len("Specialization:") - 5) * " "}", curses.A_BOLD)
                        stdscr.move(rows // 4 + 8, columns // 4 + 26)
                        win.move(9, 27)
                        win.refresh()
                        val = pp.hc.helper_functions.take_str(stdscr, win).strip()
                        if not val or val == "":
                            raise ValueError
                    except ValueError:
                        win.addstr(win_rows - 1, 0, "!!ERROR: Enter a valid specialization!!", red_and_black)
                        win.refresh()
                        return get_specialization()
                    except Exception as e:
                        win.addstr(win_rows - 1, 0, f"!!UNEXPECTED ERROR: {e}!!", red_and_black)
                        win.refresh()
                        return get_specialization()
                    else:
                        win.addstr(win_rows - 1, 0, f"{(win_columns - 1) * " "}")
                        win.refresh()
                        return val

                specialization = get_specialization()

                pp.hc.helper_functions.display_success_message(win, "Registration Completed Successfully")
                tm.sleep(3)

                doctor = pp.Doctor(name, age, gender, specialization)
                doctor.add_contact_info("email", email)
                doctor.add_contact_info("phone_number", number)
                doctor.add_security_info("id", doctor.get_id())
                doctor.add_security_info("email", email)
                doctor.add_security_info("password", password)
                return doctor

            pp.hc.helper_functions.display_success_message(win, "Registration Completed Successfully")
            tm.sleep(3)

            if user == "admin":
                admin = pp.Administrator(name, age, gender)
                admin.add_contact_info("email", email)
                admin.add_contact_info("phone_number", number)
                admin.add_security_info("id", admin.get_id())
                admin.add_security_info("email", email)
                admin.add_security_info("password", password)
                return admin

            elif user == "nurse":
                nurse = pp.Nurse(name, age, gender)
                nurse.add_contact_info("email", email)
                nurse.add_contact_info("phone_number", number)
                nurse.add_security_info("id", nurse.get_id())
                nurse.add_security_info("email", email)
                nurse.add_security_info("password", password)
                return nurse

            elif user == "patient":
                patient = pp.Patient(name, age, gender)
                patient.add_contact_info("email", email)
                patient.add_contact_info("phone_number", number)
                patient.add_security_info("id", patient.get_id())
                patient.add_security_info("email", email)
                patient.add_security_info("password", password)
                return patient

        return wrapper(run)