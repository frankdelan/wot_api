from fastapi import FastAPI
from tanks.router import router as tank_db_router
from scraping.router import router as tank_api_router

app = FastAPI()


app.include_router(tank_db_router)
app.include_router(tank_api_router)
