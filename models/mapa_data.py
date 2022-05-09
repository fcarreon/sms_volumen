from ast import For
from pydantic import BaseModel
from fastapi import Form, UploadFile  , File

class Mapa_Data(BaseModel):
    date: str
    type_data: str
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        date: str = Form(...),
        type_data: str = Form(...),
        file: UploadFile = File(...)
    ):
        return cls(
            date=date,
            type_data=type_data,
            file=file
        )