from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.tanks.schemas import TankAddScheme, TankShowScheme, GunScheme
from database import get_async_session
from api.tanks.queries import get_tank_info, get_gun_info, update_tank_gun, get_tanks_name, add_new_tank, add_new_gun, \
    delete_tank_gun

router = APIRouter(
    prefix='/api/v2',
    tags=['Tanks from database']
)


@router.get('/tank/list', response_model=dict[str, str | list[TankShowScheme] | None])
async def get_all_tanks_from_db(session: AsyncSession = Depends(get_async_session)):
    data = []
    names = await get_tanks_name(session)
    try:
        for item in names:
            data.append(await get_tank_info(item, session))
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


@router.get('/gun/list', response_model=dict[str, str | list[GunScheme] | None])
async def get_all_guns_from_db(session: AsyncSession = Depends(get_async_session)):
    try:
        data = await get_gun_info(session)
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


@router.get('/tank/{tank_name}', response_model=dict[str, str | TankShowScheme | None])
async def get_tank(tank_name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        tank = await get_tank_info(tank_name, session)
    except Exception as e:
        return {
            "status": "error",
            "data": None,
            "detail": str(e)
        }
    return {
        "status": "success",
        "data": tank,
        "detail": None
    }


@router.post('/tank/add')
async def add_tank(data: TankAddScheme, session: AsyncSession = Depends(get_async_session)):
    try:
        await add_new_tank(data, session)
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


@router.post('/gun/add')
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


@router.post('/gun/update/{gun_id}')
async def update_gun(gun_id: int, data: GunScheme, session: AsyncSession = Depends(get_async_session)):
    await update_tank_gun(gun_id, data, session)
    return {
        "status": "success",
        "detail": None
    }


@router.post('/gun/delete/{gun_id}')
async def delete_gun(gun_id: int, session: AsyncSession = Depends(get_async_session)):
    await delete_tank_gun(gun_id, session)
    return {
        "status": "success",
        "detail": None
    }

# TODO: add tank delete
