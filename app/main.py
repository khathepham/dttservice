import datetime
import os
from typing import Annotated

from fastapi import FastAPI, Form, UploadFile, File
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from app.Registrant import Registrant
from app.camp2025 import airtable_database
import uuid
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# For Static images
app.mount("/camp2025/registrant_images", StaticFiles(directory="app/camp2025/registrant_images"), name="registrant_images")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}


class Registration(BaseModel):
    firstName: str
    lastName: str
    birthdate: datetime.date
    gender: str
    nganh: str
    specialNeeds: str
    parentName: str
    parentPhone: str
    parentEmail: str
    childPhoto: Annotated[UploadFile, File()]


@app.post("/camp2025/register")
async def register( firstName: Annotated[str, Form()],
                    lastName: Annotated[str, Form()],
                    birthdate: Annotated[str, Form()],
                    gender: Annotated[str, Form()],
                    nganh: Annotated[str, Form()],
                    parentName: Annotated[str, Form()],
                    parentPhone: Annotated[str, Form()],
                    parentEmail: Annotated[str, Form()],
                    childPhoto: Annotated[UploadFile, File()],
                    specialNeeds: Annotated[str | None, Form()] = None,
                    ):
    print(firstName, lastName, birthdate, gender, nganh, specialNeeds, parentName, parentPhone, parentEmail, childPhoto)

    out_file = childPhoto.filename

    if os.path.exists(f"app/camp2025/registrant_images/{out_file}"):
        out_file_split = os.path.splitext(out_file)
        out_file = out_file_split[0] + "-%s" + out_file_split[1]

        i = 0
        while os.path.exists(out_file % i):
            i += 1

        out_file = out_file % i

    contents = await childPhoto.read()

    with open(f"app/camp2025/registrant_images/{out_file}", "wb") as file:
        file.write(contents)


    registrant = Registrant(
        first_name=firstName,
        last_name=lastName,
        date_of_birth=birthdate,
        gender=gender,
        nganh=nganh,
        special_needs=specialNeeds,
        guardian_name=parentName,
        guardian_number=parentPhone,
        guardian_email=parentEmail,
        photo_url=f"https://api.doantomathien.org/camp2025/registrant_images/{out_file}",
    )

    airtable_database.create_new_registrant(registrant)



