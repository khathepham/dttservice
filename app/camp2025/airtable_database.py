import os
import sys
import pyairtable
from infisical_sdk import InfisicalSDKClient
import datetime
import dotenv
import logging
from app.Registrant import Registrant

lg = logging.getLogger(__name__)

dotenv.load_dotenv("stack.env")



client = InfisicalSDKClient(host="https://infisical.khathepham.com")
infisical_client_secret = os.environ["INFISICAL_CLIENT_SECRET"]
infisical_client_id = os.environ["INFISICAL_CLIENT_ID"]

client.auth.universal_auth.login(infisical_client_id, infisical_client_secret)

airtable = pyairtable.Api(client.secrets.get_secret_by_name(
    secret_name="airtable-token",
    project_id=os.environ["INFISICAL_PROJECT_ID"],
    environment_slug="prod",
    secret_path="/Camp2025/"
).secretValue)

airtable_appid = client.secrets.get_secret_by_name(
    secret_name="airtable-appid",
    project_id=os.environ["INFISICAL_PROJECT_ID"],
    environment_slug="prod",
    secret_path="/Camp2025/"
).secretValue

airtable_tableid = client.secrets.get_secret_by_name(
    secret_name="airtable-tableid",
    project_id=os.environ["INFISICAL_PROJECT_ID"],
    environment_slug="prod",
    secret_path="/Camp2025/"
).secretValue



table = airtable.table(airtable_appid, airtable_tableid)



def create_new_registrant(registrant:Registrant):

    data = {
        "First Name": registrant.first_name,
        "Last Name": registrant.last_name,
        "Date of Birth": registrant.date_of_birth.isoformat(),
        "Gender": registrant.gender,
        "Ngành": registrant.nganh,
        "Special Needs": registrant.special_needs,
        "Parent/Guardian Name": registrant.guardian_name,
        "Parent/Guardian Phone": registrant.guardian_number,
        "Parent/Guardian Email": registrant.guardian_email,
        "Participant Photo": [{
            "url": registrant.photo_url,
        }]
    }

    table.create(data)

    logging.info(f"Created new registrant: {registrant.first_name} {registrant.last_name}")



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
        photo_url="https://api.doantomathien.org/camp2025/registrant_images/testimage.jpg"
    )

    create_new_registrant(kim)