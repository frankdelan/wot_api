from api.tanks.schemas import TankShowScheme, StealthScheme, VisionScheme, MobilityShowScheme, FirepowerScheme, \
    GunScheme, SpecificationScheme, SurvivalScheme


def get_slug(tank_name: str) -> str:
    """Form slug from tank_name"""
    tank_slug = tank_name.replace("/", "").replace(".", "")
    return tank_slug.replace(" ", "-").lower()


async def convert_data(data) -> TankShowScheme:
    """Convert list[dict] to TankShowScheme"""
    return TankShowScheme(
        tank_id=data[0]['id'],
        name=data[0]['name'],
        level=data[0]['level'],
        country=data[0]['country'],
        type=data[0]['type'],
        slug_field=data[0]['slug_field'],
        specification=SpecificationScheme(
            survival=SurvivalScheme(
                hp=data[0]['hp'],
                hull_armor=data[0]['hull_armor'],
                tower_armor=data[0]['tower_armor'],
            ),
            firepower=FirepowerScheme(
                tank_guns=[GunScheme(
                    id=data[idx]['gun_id'],
                    name=data[idx]['gun_name'],
                    gun_type=data[idx]['gun_type'],
                    shell_count=data[idx]['shell_count'],
                    alpha=data[idx]['alpha'],
                    penetration=data[idx]['penetration'],
                    shell_type=data[idx]['shell_type'],
                    reload=data[idx]['reload'],
                    dpm=data[idx]['dpm'],
                    inside_reload=data[idx]['inside_reload'],
                    autoreload=data[idx]['autoreload'],
                    spread=data[idx]['spread'],
                    reduction_time=data[idx]['reduction_time'],
                    elevation_vertical_angles=data[idx]['elevation_vertical_angles'],
                    elevation_horizontal_angles=data[idx]['elevation_horizontal_angles'],
                ) for idx in range(len(data))],
            ),
            mobility=MobilityShowScheme(
                weight=data[0]['weight'],
                power=data[0]['power'],
                specific_power=data[0]['specific_power'],
                max_forward_speed=data[0]['max_forward_speed'],
                max_backward_speed=data[0]['max_backward_speed'],
                rotation_speed=data[0]['rotation_speed'],
                tower_rotation_speed=data[0]['tower_rotation_speed'],
            ),
            vision=VisionScheme(
                vision_range=data[0]['vision_range'],
                communication_range=data[0]['communication_range'],
            ),
            stealth=StealthScheme(
                standing_stealth=data[0]['standing_stealth'],
                moving_stealth=data[0]['moving_stealth'],
            ),
        )
    )