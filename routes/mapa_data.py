from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from models.mapa_data import Mapa_Data
from config.db import conn
from schemas.mapa_data import mapa_dataEntity, datasEntity

mapa_data = APIRouter()

views = Jinja2Templates(directory="views")

@mapa_data.post('/mapa_data')
async def save_mapa_data(data: Mapa_Data):
    conn.local.mapa_data.insert_one(dict(data))
    return datasEntity(conn.local.mapa_data.find())
    

@mapa_data.get('/mapa_data', response_class=HTMLResponse)
async def get_mapa_data(request: Request):
    #print(conn.local.mapa_data.find())
    #print(datasEntity(conn.local.mapa_data.find()))
    #return datasEntity(conn.local.mapa_data.find()) 
    
    data_wholesale = datasEntity(conn.local.mapa_data.find({"type":"Wholesale"}))
    data_retail = datasEntity(conn.local.mapa_data.find({"type":"Retail"}))
    return views.TemplateResponse("index.html", {"request":request, "data_wholesale": data_wholesale,"data_retail": data_retail})


@mapa_data.get('/process_data')
async def process_mapa_data():
    data_wholesale_query =  datasEntity(conn.local.mapa_data.find({"type":"Wholesale"}))
    for key, val in data_wholesale_query.item():
        print(val)
    return "Hola"







