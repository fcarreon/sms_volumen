from fastapi import FastAPI 
#from fastapi.staticfiles import StaticFiles 
from routes.user import user
from routes.mapa_data import mapa_data

app = FastAPI()


app.include_router(user)
app.include_router(mapa_data)





