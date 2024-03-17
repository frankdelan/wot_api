from tanks.schemas import SurvivalScheme, SpecificationScheme, FirepowerScheme, \
    MobilityShowScheme, VisionScheme, StealthScheme, GunScheme, TankAddScheme

from .config import countries, tank_types, shell_types


def calculate_tank_weight(tank_json: dict) -> float:
    full_weight = sum([tank_json['tank']['weight'],
                       tank_json['tank']['chassis'][-1]['weight'],
                       tank_json['tank']['turrets'][-1]['weight'],
                       tank_json['tank']['guns'][-1]['weight'],
                       tank_json['tank']['engines'][-1]['weight'],
                       tank_json['tank']['radios'][-1]['weight']]) / 1000
    return full_weight


def parse_tank_specification(tank_json: dict):
    full_weight = calculate_tank_weight(tank_json)
    data = TankAddScheme(
        name=tank_json['tank']['short_name'],
        level=tank_json['tank']['tier'],
        type=tank_types[tank_json['tank']['type']],
        country=countries[tank_json['tank']['nation']],
        slug_field=tank_json['tank']['short_name'].lower().replace(" ", "-"),
        specification=SpecificationScheme(
            survival=SurvivalScheme(
                hp=tank_json['tank']['health'],
                hull_armor=f"{tank_json['tank']['armor_front']} / "
                           f"{tank_json['tank']['armor_side']} / "
                           f"{tank_json['tank']['armor_rear']}",
                tower_armor=f"{tank_json['tank']['turrets'][-1]['armor_front']} / "
                            f"{tank_json['tank']['turrets'][-1]['armor_side']} / "
                            f"{tank_json['tank']['turrets'][-1]['armor_rear']}",
            ),
            firepower=FirepowerScheme(
                tank_guns=[item['id'] for item in tank_json['tank']['guns']],
            ),
            mobility=MobilityShowScheme(
                weight=full_weight,
                power=tank_json['tank']['engines'][-1]['power'],
                specific_power=round(tank_json['tank']['engines'][-1]['power'] / full_weight, 2),
                max_forward_speed=tank_json['tank']['forward_speed'],
                max_backward_speed=tank_json['tank']['reverse_speed'],
                rotation_speed=tank_json['tank']['turrets'][-1]['rotation_speed'],
                tower_rotation_speed=tank_json['tank']['turrets'][-1]['rotation_speed'],
            ),
            vision=VisionScheme(
                vision_range=tank_json['tank']['radios'][-1]['range'],
                communication_range=tank_json['tank']['turrets'][-1]['view_range'],
            ),
            stealth=StealthScheme(
                standing_stealth="",
                moving_stealth="",
            ),
        )
    )
    return data


def parse_shells(tank_json: dict) -> dict[str, list[str]]:
    shell_info = {'shell_type': [],
                  'penetration': [],
                  'alpha': []}
    for gun_idx in range(0, len(tank_json['tank']['guns']) + 2, 3):
        shell_type: str = (shell_types[tank_json['tank']['shells'][gun_idx]['type']] + ' / ' +
                           shell_types[tank_json['tank']['shells'][gun_idx + 1]['type']] + ' / ' +
                           shell_types[tank_json['tank']['shells'][gun_idx + 2]['type']])
        penetration: str = (
            f"{tank_json['tank']['shells'][gun_idx]['penetration']} / "
            f"{tank_json['tank']['shells'][gun_idx + 1]['penetration']} / "
            f"{tank_json['tank']['shells'][gun_idx + 2]['penetration']}")

        alpha: str = (
            f"{tank_json['tank']['shells'][gun_idx]['damage']} / {tank_json['tank']['shells'][gun_idx + 1]['damage']} / "
            f" {tank_json['tank']['shells'][gun_idx + 2]['damage']}")
        shell_info['shell_type'] += [shell_type]
        shell_info['alpha'] += [alpha]
        shell_info['penetration'] += [penetration]
    return shell_info


def parse_guns(tank_json: dict):
    shell_info: dict[str, list[str]] = parse_shells(tank_json)

    data = [GunScheme(
        id=tank_json['tank']['guns'][gun_idx]['id'],
        name=tank_json['tank']['guns'][gun_idx]['name'],
        gun_type='cycle' if tank_json['tank']['guns'][gun_idx]['clip_size'] == 0 else 'autoreload'
        if tank_json['tank']['guns'][gun_idx]['autoreload_time'] else 'drum',

        shell_count=tank_json['tank']['guns'][gun_idx]['clip_size'],
        alpha=shell_info['alpha'][gun_idx],
        penetration=shell_info['penetration'][gun_idx],
        shell_type=shell_info['shell_type'][gun_idx],
        reload=tank_json['tank']['guns'][gun_idx]['reload_time'],
        inside_reload=round(tank_json['tank']['guns'][gun_idx]['clip_reload'], 1),
        autoreload=tank_json['tank']['guns'][gun_idx]['autoreload_time'],
        spread=tank_json['tank']['guns'][gun_idx]['dispersion'],
        reduction_time=tank_json['tank']['guns'][gun_idx]['aim_time'],

        elevation_vertical_angles=f"-{tank_json['tank']['guns'][gun_idx]['depression']}.."
                                  f"+{tank_json['tank']['guns'][gun_idx]['elevation']}",

        elevation_horizontal_angles=abs(tank_json['tank']['guns'][gun_idx]['yaw_left']) +
                                    abs(tank_json['tank']['guns'][gun_idx]['yaw_right']),

        dpm=round((60 / tank_json['tank']['guns'][gun_idx]['reload_time']) *
                  tank_json['tank']['shells'][gun_idx]['damage'], 2),

    ) for gun_idx in range(len(tank_json['tank']['guns']))]
    return data
