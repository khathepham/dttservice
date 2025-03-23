from datetime import datetime


class Registrant:
    def __init__(self, first_name: str, last_name: str, date_of_birth:datetime.date, gender:str, nganh:str, special_needs:str,
                 guardian_name:str, guardian_number:str, guardian_email:str, photo_url):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.nganh = nganh
        self.gender = gender
        self.special_needs = special_needs
        self.guardian_name = guardian_name
        self.guardian_number = guardian_number
        self.guardian_email = guardian_email
        self.photo_url = photo_url