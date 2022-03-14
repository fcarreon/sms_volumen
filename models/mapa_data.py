from pydantic import BaseModel

class Mapa_Data(BaseModel):
    date: str
    data: list

