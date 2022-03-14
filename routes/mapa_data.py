from fastapi import APIRouter

from models.mapa_data import Mapa_Data
from config.db import conn
from schemas.mapa_data import mapa_dataEntity, datasEntity

mapa_data = APIRouter()

@mapa_data.post('/mapa_data')
async def save_mapa_data(data: Mapa_Data):
    conn.local.mapa_data.insert_one(dict(data))
    return datasEntity(conn.local.mapa_data.find())
    

@mapa_data.get('/mapa_data')
async def get_mapa_data():
    print(conn.local.mapa_data.find())
    print(datasEntity(conn.local.mapa_data.find()))
    return datasEntity(conn.local.mapa_data.find()) 





