from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from scraping.wot_data_scraper import get_guns_info, get_tanks_info
from tanks.queries import add_new_tank, add_new_gun
from tanks.schemas import GunScheme, TankAddScheme

router = APIRouter(
    prefix='/api/v1',
    tags=['Tanks from TANKS.GG API']
)


@router.get('/gun/list', response_model=dict[str, str | list[list[GunScheme]] | None])
async def get_all_guns_from_api():
    data = await get_guns_info()
    return {
        "status": "success",
        "data": data,
        "detail": None
    }


@router.get('/tank/list', response_model=dict[str, str | list[TankAddScheme] | None])
async def get_all_tanks_from_api():
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