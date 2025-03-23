import datetime
import enum
import os
import traceback
from typing import Annotated

from fastapi import FastAPI, Form, UploadFile, File, HTTPException
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel
from camp2025.Registrant import Registrant
from camp2025 import airtable_database
from fastapi.middleware.cors import CORSMiddleware
import logging

lg = logging.getLogger(__name__)

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://doantomathien.org",
    "https://www.doantomathien.org",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

# For Static images
app.mount("/camp2025/registrant_images", StaticFiles(directory="app/camp2025/registrant_images"), name="registrant_images")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}

class Nganh(enum.Enum):
    AU_NHI = "Ấu Nhi"
    THIEU_NHI = "Thiếu Nhi"
    NGHIA_SI = "Nghĩa Sĩ"
    HIEP_SI = "Hiệp Sĩ"


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

    try:
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
            date_of_birth=datetime.datetime.fromisoformat(birthdate),
            gender=gender.capitalize(),
            nganh=find_nganh(nganh),
            special_needs=specialNeeds,
            guardian_name=parentName,
            guardian_number=parentPhone,
            guardian_email=parentEmail,
            photo_url=f"https://api.doantomathien.org/camp2025/registrant_images/{out_file}",
        )

        airtable_database.create_new_registrant(registrant)
        return {"message": "Successfully registered!"}
    except Exception as error:
        lg.error(error)
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(error))


def find_nganh(n: str) -> None | str:
    n.lower().strip()

    match n:
        case "au nhi":
            return Nganh.AU_NHI.value
        case "thieu nhi":
            return Nganh.THIEU_NHI.value
        case "nghia si":
            return Nganh.NGHIA_SI.value
        case "hiep si":
            return Nganh.HIEP_SI.value
        case _:
            return None
