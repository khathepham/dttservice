import os
import sys
import pyairtable
from infisical_sdk import InfisicalSDKClient
import datetime
import dotenv

dotenv.load_dotenv("stack.env")



client = InfisicalSDKClient(host="https://infisical.khathepham.com")
infisical_client_secret = os.environ["INFISICAL_CLIENT_SECRET"]
infisical_client_id = os.environ["INFISICAL_CLIENT_ID"]

client.auth.universal_auth.login(infisical_client_id, infisical_client_secret)

airtable = pyairtable.Api(client.secrets.get_secret_by_name(
    secret_name="camp2025-airtable",
    project_id=os.environ["INFISICAL_PROJECT_ID"],
    environment_slug="prod",
    secret_path="/Camp2025/"
))

airtable_appid = client.secrets.get_secret_by_name(
    secret_name="airtable-appid",
    project_id=os.environ["INFISICAL_PROJECT_ID"],
    environment_slug="prod",
    secret_path="/Camp2025/"
)

airtable_tableid = client.secrets.get_secret_by_name(
    secret_name="airtable-tableid",
    project_id=os.environ["INFISICAL_PROJECT_ID"],
    environment_slug="prod",
    secret_path="/Camp2025/"
)



table = airtable.table(airtable_appid, airtable_tableid)


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




def create_new_registrant(registrant:Registrant):
    data = {
        "First Name": registrant.first_name,
        "Last Name": registrant.last_name,
        "Date of Birth": registrant.date_of_birth.isoformat(),
        "Gender": registrant.gender,
        "Ngành": registrant.nganh,
        "Special Needs": registrant.special_needs,
        "Parent/Guardian Name": registrant.guardian_name,
        "Parent/Guardian Phone Number": registrant.guardian_number,
        "Parent/Guardian Email": registrant.guardian_email,
        "Participant Photo": registrant.photo_url
    }

    table.create(data)



if __name__ == '__main__':
    """
    Test
    """

    kim = Registrant(
        first_name="Kim",
        last_name="Pham",
        date_of_birth=datetime.datetime(2010, 9, 10),
        gender="Female",
        nganh="Nghĩa Sĩ",
        special_needs="",
        guardian_name="Anh-Duyen Pham",
        guardian_email="giaoduyenus@yahoo.com",
        guardian_number="6513434037",
        photo_url="api.doantomathien.org/camp2025/registrant_images/testimage.jpg"

    )