from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from tanks.schemas import TankAddScheme, TankShowScheme, GunScheme
from database import get_async_session
from tanks.queries import get_tank_info, add_new_tank, add_new_gun, get_guns_info as g, update_tank_gun
from scraping.wot_data_scraper import get_guns_info, get_tanks_info

router = APIRouter(
    prefix='/api/v1',
    tags=['tanks']
)


@router.get('/gun/list', response_model=dict[str, str | list[list[GunScheme]] | None])
async def get_all_guns():
    data = await get_guns_info()
    return {
        "status": "success",
        "data": data,
        "detail": None
    }


@router.get('/tank/list', response_model=dict[str, str | list[TankAddScheme] | None])
async def get_all_tanks():
    data = await get_tanks_info()
    return {
        "status": "success",
        "data": data,
        "detail": None
    }


@router.post('/guns/add')
async def add_guns(session: AsyncSession = Depends(get_async_session)):
    try:
        data: list[list[GunScheme]] = await get_guns_info()
        for item in data:
            await add_new_gun(item, session)
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "detail": str(e)
        }
    return {
        "status": "success",
        "data": None,
        "detail": None
    }


@router.post('/tanks/add')
async def add_tanks(session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_tanks_info()
        for item in data:
            await add_new_tank(item, session)
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "detail": str(e)
        }
    return {
        "status": "success",
        "data": None,
        "detail": None
    }


@router.get('/tank/{tank_id}', response_model=dict[str, str | TankShowScheme | None])
async def get_tank(tank_id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        tank = await get_tank_info(tank_id, session)
        return {
            "status": "success",
            "data": tank,
            "detail": None
        }
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "detail": str(e)
        }


@router.get("/tank/vision/update/{tank_id}")
async def update_vision(tank_id: int, session: AsyncSession = Depends(get_async_session)):
    pass







@router.post('/gun/update/{gun_id}')
async def update_gun(gun_id: int, data: GunScheme, session: AsyncSession = Depends(get_async_session)):
    await update_tank_gun(gun_id, data, session)
    return {
        "status": "success",
        "detail": None
    }


