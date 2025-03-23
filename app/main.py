from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}




app.mount("/camp2025/registrant_images", StaticFiles(directory="app/camp-2025/registrant_images"), name="registrant_images")
# async def say_hello(name: str):
#     return {"message": f"Hello {name}"}
