from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.tanks.schemas import GunScheme
from database import get_async_session
from api.tanks.queries import get_gun_info, update_tank_gun, add_new_gun, \
    delete_tank_gun

router = APIRouter(
    prefix="/gun",
    tags=['Guns']
)


@router.get('/list', response_model=dict[str, str | list[GunScheme] | None])
async def get_all_guns_from_db(session: AsyncSession = Depends(get_async_session)):
    try:
        data: list[GunScheme] = await get_gun_info(session)
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "detail": str(e)
        }
    return {
        "status": "success",
        "data": data,
        "detail": None
    }


@router.post('/add')
async def add_gun(data: GunScheme, session: AsyncSession = Depends(get_async_session)):
    try:
        await add_new_gun([data], session)
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


@router.post('/update/{gun_id}')
async def update_gun(gun_id: int, data: GunScheme, session: AsyncSession = Depends(get_async_session)):
    await update_tank_gun(gun_id, data, session)
    return {
        "status": "success",
        "detail": None
    }


@router.post('/delete/{gun_id}')
async def delete_gun(gun_id: int, session: AsyncSession = Depends(get_async_session)):
    await delete_tank_gun(gun_id, session)
    return {
        "status": "success",
        "detail": None
    }
