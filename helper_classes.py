from datetime import datetime

class ID_Generator:
    @staticmethod
    def generate_id(prefix, counter) -> str:
        """
        Generate a unique ID based on person type.
        Format: [TYPE]-[YEAR]-[SEQUENCE]
        """
        year = datetime.now().year

        return f"{prefix}-{year}-{counter:04d}"

class Appointment():
    __number_of_appointments = 0
    __appointments = {}
    def __init__(self, patient, doctor, time, statues) -> None:
        Appointment.__number_of_appointments += 1
        self._id = ID_Generator.generate_id("APP", Appointment.get_number_of_appointments()) 
        self._patient = patient
        self._doctor = doctor
        self._date = datetime.now()
        self._time = time
        self._statues = statues
        self._data = {'patient':self._patient, 'doctor':self._doctor, 'time':self._time}
    @staticmethod
    def get_number_of_appointments() -> int:
        return Appointment.__number_of_appointments
    @staticmethod
    def schedule_appointment(self) -> None:
        Appointment.__appointments.update({self._id: self._data})
    @staticmethod
    def cancel_appointment(self) -> None:
        del Appointment.__appointments[self._id]
        """
        Appointment.__number_of_appointments -= 1
        this cause a problem with the ids because now multiple appointments can have the same id
        """
    @staticmethod
    def reschedule_appointment(self, new_time) -> None:
        Appointment.__appointments[self._id[self._time]] = new_time
        
class MedicalRecord():
    __number_of_records = 0
    def __init__(self, patient, doctor, diagnosis, prescribed_treatment, test_results) -> None:
        MedicalRecord.__number_of_records += 1
        self._id = ID_Generator.generate_id("MDR", Appointment.get_number_of_records()) 
        self._patient = patient
        self._doctor = doctor
        self._diagnosis = diagnosis
        self._prescribed_treatment = prescribed_treatment
        self._test_results = test_results
        self._data = {
            "record_id": self._id,
            "patient": self._patient,
            "doctor": self._doctor,
            "diagnosis": self._diagnosis,
            "prescribed_treatment": self._prescribed_treatment,
            "test_results": self._test_results
        }
    @staticmethod
    def get_number_of_records() -> int:
        return MedicalRecord.__number_of_records
    def update_record(self, diagnosis=None, prescribed_treatment=None, test_results=None) -> None:
        if diagnosis:
            self._diagnosis = diagnosis
        if prescribed_treatment:
            self._prescribed_treatment = prescribed_treatment
        if test_results:
            self._test_results = test_results
    def view_record(self):
        return self._data
    def delete_record(self) -> None:
        del self._data
        self._record_id = None
        self._patient = None
        self._doctor = None
        self._diagnosis = None
        self._prescribed_treatment = None
        self._test_results = None


class Billing():
    __number_of_bills = 0
    def __init__(self, patient, treatment_cost, medicine_cost, total_amount, payment_status) -> None:
        Billing.__number_of_bills += 1
        self._id = ID_Generator.generate_id("BIL", Appointment.get_number_of_bills()) 
        self._patient = patient
        self._treatment_cost = treatment_cost
        self._medicine_cost = medicine_cost
        self._total_amount = total_amount
        self._payment_status = payment_status
        self._data = {
            "bill_id": self._id,
            "patient": self._patient,
            "treatment_cost": self._treatment_cost,
            "medicine_cost": self._medicine_cost,
            "total_amount": self._total_amount,
            "payment_status": self._payment_status
        }
    @staticmethod
    def get_number_of_bills() -> int:
        return Billing.__number_of_bills
    def generate_bill(self) -> float:
        self._total_amount = self._treatment_cost + self._medicine_cost
        return self._total_amount
    def process_payment(self, amount):
        if amount >= self._total_amount:
            self._payment_status = "Paid"
            return "Payment successful"
        else:
            return "Insufficient payment"
    def view_bill_details(self):
        return self._data