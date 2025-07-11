import curses
from curses import wrapper
from curses.textpad import rectangle
from datetime import datetime


appointments = list()
bills = list()

class helper_functions:
    @staticmethod
    def generate_id(prefix, counter) -> str:
        """
        Generate a unique ID based on person type.
        Format: [TYPE]-[YEAR]-[SEQUENCE]
        """
        year = datetime.now().year

        return f"{prefix}-{year}-{counter:04d}"

    @staticmethod
    def display_error(win, error: str) -> None:
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
        red_and_black = curses.color_pair(2)
        win_rows, win_columns = win.getmaxyx()
        curses.curs_set(0)
        message = f"!!ERROR: {error}!!"
        win.addstr(win_rows - 1, (win_columns - len(message)) // 2, message, red_and_black)
        win.refresh()

    @staticmethod
    def display_success_message(win, message: str) -> None:
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        green_and_black = curses.color_pair(3)
        win_rows, win_columns = win.getmaxyx()
        curses.curs_set(0)
        message = f"##### {message} #####"
        win.addstr(win_rows - 1, (win_columns - len(message)) // 2, message, green_and_black)
        win.refresh()

    @staticmethod
    def display_page_heading(message):
        def run(stdscr):
            curses.curs_set(0)
            stdscr.clear()
            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
            blue_and_black = curses.color_pair(1)

            rows, columns = stdscr.getmaxyx()

            num_spaces = (columns - len(message)) // 2

            stdscr.addstr(0, 0, columns * "=", blue_and_black)
            stdscr.addstr(1, 0, f"{num_spaces * " "}{message}", blue_and_black)
            stdscr.addstr(2, 0, columns * "=", blue_and_black)

            stdscr.refresh()

        wrapper(run)

    @staticmethod
    def display_get_options(options: list, prefix_message="") -> int:
        def run(stdscr):
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
            red_and_black = curses.color_pair(2)
            green_and_black = curses.color_pair(3)

            rows, columns = stdscr.getmaxyx()

            win = curses.newwin(rows // 2, columns // 2, rows * 2 // 5 - 1, columns // 3 - 1)
            if prefix_message != "":
                win.addstr(0, 0, prefix_message, green_and_black)
            win.addstr(len(options) + 3, 0, "Use ↑ ↓ to navigate, Enter to select", red_and_black)

            def display_options():
                for i in range(len(options)):
                    win.addstr(2 + i, 5, f"{options[i]}{(27-len(options[i])) * " "}")

            option = 0
            while True:
                display_options()
                win.addstr(2 + option, 5, f"{options[option]}{(27-len(options[option])) * " "}", curses.A_REVERSE)
                win.refresh()

                key = stdscr.getkey()
                if key == "KEY_UP":
                    option -= 1
                    option = (option + len(options)) % len(options)
                elif key == "KEY_DOWN":
                    option += 1
                    option %= len(options)
                elif key == "\n":
                    break
                else:
                    continue

            return option + 1

        return wrapper(run)

    @staticmethod
    def take_str(stdscr, win):
        curses.cbreak()
        stdscr.keypad(True)
        result = ""
        while True:
            try:
                char = stdscr.getkey()

                if char == "\b":
                    if len(result) > 0:
                        y, x = win.getyx()
                        sy, sx = win.getbegyx()
                        win.move(y, max(0, x - 1))
                        win.addstr(" ")
                        win.move(y, max(0, x - 1))
                        stdscr.move(y + sy, max(0, x - 1) + sx)
                        win.refresh()
                        result = result[:-1]
                    continue

                if char == "\n":
                    return result

                if len(char) == 1 and 32 <= ord(char) <= 126:
                    win.addstr(char)
                    y, x = win.getyx()
                    sy, sx = win.getbegyx()
                    stdscr.move(y + sy, x + sx)
                    result += char

                win.refresh()

            except curses.error:
                pass

    @staticmethod
    def take_user_input(stdscr, message: str, label: str, strt=0) -> tuple[curses, str]:
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        green_and_black = curses.color_pair(3)

        rows, columns = stdscr.getmaxyx()

        win = curses.newwin(
            min(rows // 4,(rows - (rows // 4 + strt))-1),
            columns // 2,
            rows // 4 + strt,
            columns // 4 - 1
        )
        win.clear()

        win.addstr(0, 0, message, curses.A_BOLD | green_and_black)
        win.addstr(1, 0, f"{len(message) * "-"}", curses.A_BOLD | green_and_black)

        curses.curs_set(1)

        win.addstr(3, 5, label, curses.A_BOLD)
        stdscr.move(rows // 4 + strt + 3, columns // 4 + len(label) + 5)
        win.move(3, len(label) + 6)
        win.refresh()

        person_id = helper_functions.take_str(stdscr, win)
        return win, person_id

    @staticmethod
    def display_table(stdscr, start_row, label, headings, data, cols_width, stop=True):
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        green_and_black = curses.color_pair(3)
        yellow_and_black = curses.color_pair(5)

        rows, columns = stdscr.getmaxyx()
        width = sum(cols_width) + 2
        height = 4 + len(data)

        if len(data) == 0:
            height += 1

        yb, xb, ye, xe = start_row, (columns - width) // 2, 6 + height - 1, (columns - width) // 2 + width - 1
        stdscr.addstr(yb - 2, xb, label, green_and_black | curses.A_BOLD)
        rectangle(stdscr, yb, xb, ye, xe)
        stdscr.hline(yb + 2, xb + 1, curses.ACS_HLINE, width - 2)

        temp = xb + 1
        for i in range(len(headings)):
            stdscr.addstr(yb + 1, temp, headings[i], curses.A_BOLD)
            temp += cols_width[i]

        if len(data) == 0:
            message = "NO Data YET!"
            stdscr.addstr(yb + 3, xb + (width - len(message)) // 2, message)

        else:
            line = yb + 3
            for row in data:
                col = xb + 1
                for i in range(len(row)):
                    stdscr.addstr(line, col, str(row[i]))
                    col += cols_width[i]
                line += 1

        if stop:
            stdscr.addstr(
                yb + height + 1,
                xb + (width - len("Press any key to continue...")) // 2,
                "Press any key to continue...",
                yellow_and_black | curses.A_BOLD
            )
            curses.curs_set(1)
            stdscr.refresh()
            stdscr.getch()


class Appointment:
    __number_of_appointments = 0

    def __init__(self, patient, symptoms) -> None:
        Appointment.__number_of_appointments += 1
        self._id = helper_functions.generate_id("APP", Appointment.get_number_of_appointments())
        self._patient = patient
        self._doctor = None
        self._symptoms = symptoms
        self._date = datetime.now().date()
        self._time = str(datetime.now().time())[0:8]
        self._status = "Pending"

    def get_patient(self):
        return self._patient
    def set_doctor(self, doctor):
        self._doctor = doctor
    def set_status(self, status):
        self._status = status

    @staticmethod
    def get_number_of_appointments() -> int:
        return Appointment.__number_of_appointments

    def schedule_appointment(self):
        appointments.append(self)

    def cancel_appointment(self) -> None:
        appointments.remove(self)


class MedicalRecord:
    __number_of_records = 0

    def __init__(self, patient, doctor, diagnosis, prescribed_treatment, test_results, date, time) -> None:
        MedicalRecord.__number_of_records += 1
        self._id = helper_functions.generate_id("MDR", MedicalRecord.get_number_of_records())
        self._patient = patient
        self._doctor = doctor
        self._diagnosis = diagnosis
        self._prescribed_treatment = prescribed_treatment
        self._test_results = test_results
        self._date = date
        self._time = time

    def get_record_id(self):
        return self._id
    def get_patient(self):
        return self._patient
    def get_doctor(self):
        return self._doctor
    def get_diagnosis(self):
        return self._diagnosis
    def get_prescribed_treatment(self):
        return self._prescribed_treatment
    def get_test_results(self):
        return self._test_results
    def get_date(self):
        return self._date
    def get_time(self):
        return self._time

    @staticmethod
    def get_number_of_records() -> int:
        return MedicalRecord.__number_of_records


class Billing:
    __number_of_bills = 0

    def __init__(self, patient, treatment_cost, medicine_cost) -> None:
        Billing.__number_of_bills += 1
        self._id = helper_functions.generate_id("BIL", Billing.get_number_of_bills())
        self._patient = patient
        self._treatment_cost = treatment_cost
        self._medicine_cost = medicine_cost
        self._total_cost = treatment_cost + medicine_cost
        self._payment_status = "Pending"

    def get_id(self):
        return self._id
    def get_patient(self):
        return self._patient
    def get_treatment_cost(self):
        return self._treatment_cost
    def get_medicine_cost(self):
        return self._medicine_cost
    def get_total_cost(self):
        return self._total_cost
    def get_payment_status(self):
        return self._payment_status

    def process_payment(self):
        self._payment_status = "Completed"

    @staticmethod
    def get_number_of_bills() -> int:
        return Billing.__number_of_bills