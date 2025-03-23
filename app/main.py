import datetime
from typing import Annotated

from fastapi import FastAPI, Form, UploadFile, File
from starlette.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# For Static images
app.mount("/camp2025/registrant_images", StaticFiles(directory="app/camp-2025/registrant_images"), name="registrant_images")
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
async def register(data: Annotated[Registration, Form()], image: Annotated[UploadFile, File()]):
    print(data)
    pass

