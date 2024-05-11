from sqlalchemy import select, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.tanks.models import Tank, Gun, Stealth, Vision, Mobility, Survival, Firepower, Specification, gun_association_table
from api.tanks.schemas import TankAddScheme, GunScheme, TankShowScheme
from api.tanks.utils import get_slug, convert_data


async def get_tanks_slugs(session: AsyncSession):
    """Get all tanks slugs from database"""
    query = select(Tank.slug_field)
    result = await session.execute(query)
    return result.scalars().all()


async def get_tank_info(tank_slug: str, session: AsyncSession) -> TankShowScheme:
    """Get all tank information from database by tank_slug"""
    query = select(
        Tank.id, Tank.name, Tank.level, Tank.country, Tank.type, Tank.slug_field,
        Survival.hp, Survival.hull_armor, Survival.tower_armor,
        Mobility.weight, Mobility.power, Mobility.specific_power, Mobility.max_forward_speed,
        Mobility.max_backward_speed, Mobility.rotation_speed, Mobility.tower_rotation_speed,
        Vision.vision_range, Vision.communication_range,
        Stealth.standing_stealth, Stealth.moving_stealth,
        Gun.id.label('gun_id'), Gun.name.label('gun_name'), Gun.gun_type, Gun.shell_count, Gun.alpha, Gun.penetration, Gun.shell_type,
        Gun.reload, Gun.dpm, Gun.inside_reload, Gun.autoreload, Gun.spread, Gun.reduction_time,
        Gun.elevation_vertical_angles, Gun.elevation_horizontal_angles) \
    .join(
        Specification, Tank.specification_id == Specification.id
    ).join(
        Survival, Specification.survival_id == Survival.id
    ).join(
        Mobility, Specification.mobility_id == Mobility.id
    ).join(
        Vision, Specification.vision_id == Vision.id
    ).join(
        Stealth, Specification.stealth_id == Stealth.id
    ).join(
        Firepower, Specification.firepower_id == Firepower.id
    ).join(
        gun_association_table, Firepower.id == gun_association_table.c.firepower_id
    ).join(
        Gun, gun_association_table.c.gun_id == Gun.id
    ).where(Tank.slug_field == tank_slug)

    result = await session.execute(query)
    tank = result.mappings().all()
    if not tank:
        raise NoResultFound("Танка с таким названием не существует")
    result = await convert_data(tank)
    return result


async def add_new_tank(data: TankAddScheme, session: AsyncSession):
    """Add new tank to database"""
    spec_data = data.specification

    guns_query = select(Gun).where(Gun.id.in_(spec_data.firepower.tank_guns))
    guns = await session.execute(guns_query)
    guns = guns.scalars().all()

    if len(guns) == 0:
        raise NoResultFound("Орудия с таким id не существует")

    firepower = Firepower(guns=guns)
    stealth = Stealth(**spec_data.stealth.model_dump())
    vision = Vision(**spec_data.vision.model_dump())
    survival = Survival(**spec_data.survival.model_dump())
    mobility = Mobility(**spec_data.mobility.model_dump(),
                        specific_power=spec_data.mobility.power/spec_data.mobility.weight)

    specification = Specification(survival=survival,
                                  firepower=firepower,
                                  mobility=mobility,
                                  vision=vision,
                                  stealth=stealth)

    tank = Tank(name=data.name, level=data.level, country=data.country, type=data.type,
                slug_field=get_slug(data.name), specification=specification)

    session.add(tank)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        return e


async def get_gun_info(session: AsyncSession):
    """Get information about all guns from database"""
    query = select(Gun)
    result = await session.execute(query)
    return result.scalars().all()


async def add_new_gun(data: list[GunScheme], session: AsyncSession):
    """Add new gun to database"""
    for item in data:
        gun = Gun(**item.model_dump())
        session.add(gun)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        return e


async def update_tank_gun(gun_id: int, data: GunScheme, session: AsyncSession):
    """Update information about gun"""
    stmt = update(Gun).where(Gun.id == gun_id).values(**data.model_dump())
    await session.execute(stmt)
    await session.commit()


async def delete_tank_gun(gun_id: int, session: AsyncSession):
    """Delete gun from database"""
    stmt = delete(Gun).where(Gun.id == gun_id)
    await session.execute(stmt)
    await session.commit()



