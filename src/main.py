from fastapi import FastAPI
from api.tanks.router import router as tank_db_router
from api.scraping.router import router as tank_api_router
from web.tanks.router import router as tank_web_router

app = FastAPI()


app.include_router(tank_db_router)
app.include_router(tank_api_router)
app.include_router(tank_web_router)