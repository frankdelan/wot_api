from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.tanks.schemas import TankAddScheme, TankShowScheme
from database import get_async_session
from api.tanks.queries import get_tank_info, add_new_tank, get_tanks_slugs

router = APIRouter(
    prefix="/tank",
    tags=['Tanks']
)


@router.get('/list', response_model=dict[str, str | list[TankShowScheme] | None])
async def get_all_tanks_from_db(session: AsyncSession = Depends(get_async_session)):
    data: list[TankShowScheme] = []
    slugs: list[str] = await get_tanks_slugs(session)
    try:
        for item in slugs:
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


@router.get('/{tank_slug}', response_model=dict[str, str | TankShowScheme | None])
async def get_tank(tank_slug: str, session: AsyncSession = Depends(get_async_session)):
    try:
        tank: TankShowScheme = await get_tank_info(tank_slug, session)
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


@router.post('/add')
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
