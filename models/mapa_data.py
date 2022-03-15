from pydantic import BaseModel

class Mapa_Data(BaseModel):
    date: str
    type: str
    data: list

