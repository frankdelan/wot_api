from fastapi import APIRouter

from api.tanks.endpoints.tank import router as tank_router
from api.tanks.endpoints.gun import router as gun_router

router = APIRouter(
    prefix='/api/v2'
)

router.include_router(tank_router)
router.include_router(gun_router)




