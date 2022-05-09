from cgitb import reset
from contextlib import nullcontext
from unittest import result
from fastapi import APIRouter, Request, File, UploadFile, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from models.mapa_data import Mapa_Data
from config.db import conn
from schemas.mapa_data import mapa_dataEntity, datasEntity
from io import BytesIO
import pandas as pd
import csv
import os

mapa_data = APIRouter()

views = Jinja2Templates(directory="views")


@mapa_data.get('/save_data', response_class=HTMLResponse)
async def save_data_template(request: Request):
    data_wholesale = datasEntity(conn.local.mapa_data.find({"type_data":"Wholesale"}))
    data_retail = datasEntity(conn.local.mapa_data.find({"type_data":"Retail"}))
    return views.TemplateResponse("save_data.html", {"request":request, "data_wholesale": data_wholesale,"data_retail": data_retail})


# @mapa_data.post('/mapa_data')
# async def save_mapa_data(data: Mapa_Data):
#     conn.local.mapa_data.insert_one(dict(data))
#     return datasEntity(conn.local.mapa_data.find())
    


@mapa_data.post('/mapa_data')
async def save_mapa_data(request: Request, date: str = Form(...), type_data: str = Form(...), file: UploadFile = File(...)):
    contents = await file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer)
    buffer.close()
    data_done = df.to_dict(orient='records')

    data = {
        "date": date,
        "type_data": type_data,
        "data": data_done

    }
    
    conn.local.mapa_data.insert_one(dict(data))
    return RedirectResponse('/save_data',status_code=303)




@mapa_data.get('/mapa_data', response_class=HTMLResponse)
async def get_mapa_data(request: Request):
    #print(conn.localw.mapa_data.find())
    #print(datasEntity(conn.local.mapa_data.find()))
    #return datasEntity(conn.local.mapa_data.find()) 
    
    data_wholesale = datasEntity(conn.local.mapa_data.find({"type_data":"Wholesale"}))
    data_retail = datasEntity(conn.local.mapa_data.find({"type_data":"Retail"}))
    return views.TemplateResponse("index.html", {"request":request, "data_wholesale": data_wholesale,"data_retail": data_retail})


@mapa_data.get('/process_data')
async def gen_report(request: Request):
    data_filtered = [];
    data_wholesale = datasEntity(conn.local.mapa_data.find({"type_data":"Wholesale"}))
    for item in data_wholesale:
        obj_data = item['data']
        data_filtered.extend(obj_data)

    # Wholesale

    df = pd.DataFrame(data_filtered)
    table2 = pd.pivot_table(df, index='CustomerName', values='SMSsNumber', columns='Day', aggfunc='sum', margins=True).reset_index().rename_axis(None, axis=1)
    table2 = table2.fillna(0)
    table_special = table2
    table2 = table2.set_index(['CustomerName'])
    table2 = table2.drop(['All'])
    table2.index.names = [None]
    
    #pd.options.display.float_format = '{:,}'.format
    columntosort = table2.columns[6]
    table2 = table2.sort_values(by=columntosort, ascending=False)
    html_table = table2.head(10).to_html(classes="table table-bordered text-center", border="0" , table_id="wholesale1")  
    
    # special carriers

    special_carriers = ['ALC', 'ALK', 'BLG', 'CHM', 'DET', 'IDT', 'LNK', 'ORS', 'QXT', 'TTA', 'TTA2']
    table_special = table_special[table_special['CustomerName'].isin(special_carriers)]
    table_special = table_special.set_index(['CustomerName'])
    table_special.index.names = [None]
    table_special =  table_special.sort_values(by=columntosort, ascending=False)

    html_table2 = table_special.to_html(classes="table table-striped table-hover", border="0", table_id="wholesale2")

    return views.TemplateResponse("index.html", {"request":request, "table_wholesale": html_table, "table_wholesale2": html_table2})

