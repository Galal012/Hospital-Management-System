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
    ...
    

class MedicalHistory():
    ...

class Billing():
    ...