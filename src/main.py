from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api.tanks.router import router as tank_db_router
from api.scraping.router import router as tank_api_router
from web.tanks.router import router as tank_web_router

app = FastAPI()

app.mount("/web/static", StaticFiles(directory="web/static"), name="static")

app.include_router(tank_db_router)
app.include_router(tank_api_router)
app.include_router(tank_web_router)