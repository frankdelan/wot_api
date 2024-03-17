from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from tanks.models import Tank, Gun, Stealth, Vision, Mobility, Survival, Firepower, Specification, gun_association_table
from tanks.schemas import TankAddScheme, SurvivalScheme, SpecificationScheme, FirepowerScheme, \
    MobilityShowScheme, VisionScheme, StealthScheme, TankShowScheme, GunScheme


async def get_tank_info(tank_id: int, session: AsyncSession):
    query = select(
        Tank.name, Tank.level, Tank.country, Tank.type,
        Survival.hp, Survival.hull_armor, Survival.tower_armor,
        Mobility.weight, Mobility.power, Mobility.specific_power, Mobility.max_forward_speed,
        Mobility.max_backward_speed, Mobility.rotation_speed, Mobility.tower_rotation_speed,
        Vision.vision_range, Vision.communication_range,
        Stealth.standing_stealth, Stealth.moving_stealth,
        Gun.id, Gun.name.label('gun_name'), Gun.alpha, Gun.penetration, Gun.shell_type,
        Gun.reload, Gun.spread, Gun.reduction_time,
        Gun.dpm, Gun.elevation_vertical_angles, Gun.elevation_horizontal_angles) \
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
    ).where(Tank.id == tank_id)

    result = await session.execute(query)
    tank = result.mappings().first()

    return TankShowScheme(
        tank_id=tank_id,
        name=tank['name'],
        level=tank['level'],
        country=tank['country'],
        type=tank['type'],
        specification=SpecificationScheme(
            survival=SurvivalScheme(
                hp=tank['hp'],
                hull_armor=tank['hull_armor'],
                tower_armor=tank['tower_armor'],
            ),
            firepower=FirepowerScheme(
                tank_guns=[GunScheme(
                    id=tank['id'],
                    name=tank['gun_name'],
                    alpha=tank['alpha'],
                    penetration=tank['penetration'],
                    shell_type=tank['shell_type'],
                    reload=tank['reload'],
                    spread=tank['spread'],
                    reduction_time=tank['reduction_time'],
                    dpm=tank['dpm'],
                    elevation_vertical_angles=tank['elevation_vertical_angles'],
                    elevation_horizontal_angles=tank['elevation_horizontal_angles'],
                )],
            ),
            mobility=MobilityShowScheme(
                weight=tank['weight'],
                power=tank['power'],
                specific_power=tank['specific_power'],
                max_forward_speed=tank['max_forward_speed'],
                max_backward_speed=tank['max_backward_speed'],
                rotation_speed=tank['rotation_speed'],
                tower_rotation_speed=tank['tower_rotation_speed'],
            ),
            vision=VisionScheme(
                vision_range=tank['vision_range'],
                communication_range=tank['communication_range'],
            ),
            stealth=StealthScheme(
                standing_stealth=tank['standing_stealth'],
                moving_stealth=tank['moving_stealth'],
            ),
        )
    )


async def add_new_tank(data: TankAddScheme, session: AsyncSession):
    spec_data = data.specification

    stealth = Stealth(**spec_data.stealth.model_dump())
    vision = Vision(**spec_data.vision.model_dump())
    survival = Survival(**spec_data.survival.model_dump())
    mobility = Mobility(**spec_data.mobility.model_dump())

    guns_query = select(Gun).where(Gun.id.in_(spec_data.firepower.tank_guns))
    guns = await session.execute(guns_query)
    guns = guns.scalars().all()
    if not len(guns):
        raise NoResultFound("Орудия с таким id не существует")
    firepower = Firepower(guns=guns)

    for item in [stealth, vision, mobility, survival, firepower]:
        session.add(item)
    await session.flush()

    specification = Specification(survival_id=survival.id,
                                  firepower_id=firepower.id,
                                  mobility_id=mobility.id,
                                  vision_id=vision.id,
                                  stealth_id=stealth.id)
    session.add(specification)
    await session.flush()

    tank = Tank(name=data.name, level=data.level, country=data.country, type=data.type,
                slug_field=data.slug_field, specification_id=specification.id)
    session.add(tank)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        return e


async def get_guns_info(session: AsyncSession):
    query = select(Gun)
    result = await session.execute(query)
    return result.scalars().all()


async def add_new_gun(data: list[GunScheme], session: AsyncSession):
    for item in data:
        print(item)
        gun = Gun(**item.model_dump())
        session.add(gun)
    await session.commit()


async def update_tank_gun(gun_id: int, data: GunScheme, session: AsyncSession):
    stmt = update(Gun).where(Gun.id == gun_id).values(**data.model_dump())
    await session.execute(stmt)
    await session.commit()



