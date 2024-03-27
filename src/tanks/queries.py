from sqlalchemy import select, update
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from tanks.models import Tank, Gun, Stealth, Vision, Mobility, Survival, Firepower, Specification, gun_association_table
from tanks.schemas import TankAddScheme, SurvivalScheme, SpecificationScheme, FirepowerScheme, \
    MobilityShowScheme, VisionScheme, StealthScheme, TankShowScheme, GunScheme


async def get_tanks_name(session: AsyncSession):
    query = select(Tank.name)
    result = await session.execute(query)
    return result.scalars().all()


async def get_tank_info(tank_name: str, session: AsyncSession):
    tank_slug: str = tank_name.replace(" ", "-").lower()
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
    return TankShowScheme(
        tank_id=tank[0]['id'],
        name=tank[0]['name'],
        level=tank[0]['level'],
        country=tank[0]['country'],
        type=tank[0]['type'],
        slug_field=tank[0]['slug_field'],
        specification=SpecificationScheme(
            survival=SurvivalScheme(
                hp=tank[0]['hp'],
                hull_armor=tank[0]['hull_armor'],
                tower_armor=tank[0]['tower_armor'],
            ),
            firepower=FirepowerScheme(
                tank_guns=[GunScheme(
                    id=tank[idx]['gun_id'],
                    name=tank[idx]['gun_name'],
                    gun_type=tank[idx]['gun_type'],
                    shell_count=tank[idx]['shell_count'],
                    alpha=tank[idx]['alpha'],
                    penetration=tank[idx]['penetration'],
                    shell_type=tank[idx]['shell_type'],
                    reload=tank[idx]['reload'],
                    dpm=tank[idx]['dpm'],
                    inside_reload=tank[idx]['inside_reload'],
                    autoreload=tank[idx]['autoreload'],
                    spread=tank[idx]['spread'],
                    reduction_time=tank[idx]['reduction_time'],
                    elevation_vertical_angles=tank[idx]['elevation_vertical_angles'],
                    elevation_horizontal_angles=tank[idx]['elevation_horizontal_angles'],
                ) for idx in range(len(tank))],
            ),
            mobility=MobilityShowScheme(
                weight=tank[0]['weight'],
                power=tank[0]['power'],
                specific_power=tank[0]['specific_power'],
                max_forward_speed=tank[0]['max_forward_speed'],
                max_backward_speed=tank[0]['max_backward_speed'],
                rotation_speed=tank[0]['rotation_speed'],
                tower_rotation_speed=tank[0]['tower_rotation_speed'],
            ),
            vision=VisionScheme(
                vision_range=tank[0]['vision_range'],
                communication_range=tank[0]['communication_range'],
            ),
            stealth=StealthScheme(
                standing_stealth=tank[0]['standing_stealth'],
                moving_stealth=tank[0]['moving_stealth'],
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
    slug_field = data.name.replace(" ", "-").lower()
    tank = Tank(name=data.name, level=data.level, country=data.country, type=data.type,
                slug_field=slug_field, specification_id=specification.id)
    session.add(tank)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        return e


async def get_gun_info(session: AsyncSession):
    query = select(Gun)
    result = await session.execute(query)
    return result.scalars().all()


async def add_new_gun(data: list[GunScheme], session: AsyncSession):
    for item in data:
        gun = Gun(**item.model_dump())
        session.add(gun)
    try:
        await session.commit()
    except IntegrityError as e:
        await session.rollback()
        return e


async def update_tank_gun(gun_id: int, data: GunScheme, session: AsyncSession):
    stmt = update(Gun).where(Gun.id == gun_id).values(**data.model_dump())
    await session.execute(stmt)
    await session.commit()



