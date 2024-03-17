from fastapi import FastAPI
from tanks.router import router as tank_router


app = FastAPI()


app.include_router(tank_router)
