from pydantic import BaseModel, Field
from enum import Enum


class GunScheme(BaseModel):
    id: int
    name: str
    gun_type: str
    shell_count: int
    alpha: str
    penetration: str
    shell_type: str
    reload: float
    dpm: float
    inside_reload: float
    autoreload: str
    spread: float
    reduction_time: float
    elevation_vertical_angles: str
    elevation_horizontal_angles: int = Field(ge=0, le=360)


class SurvivalScheme(BaseModel):
    hp: int
    hull_armor: str
    tower_armor: str


class FirepowerScheme(BaseModel):
    tank_guns: list[int] | list[GunScheme]


class MobilityAddScheme(BaseModel):
    weight: float
    power: int
    max_forward_speed: float
    max_backward_speed: float
    rotation_speed: float
    tower_rotation_speed: float


class MobilityShowScheme(MobilityAddScheme):
    specific_power: float


class StealthScheme(BaseModel):
    standing_stealth: str = "0 / 0"
    moving_stealth: str = "0 / 0"


class VisionScheme(BaseModel):
    vision_range: int
    communication_range: int


class SpecificationScheme(BaseModel):
    survival: SurvivalScheme
    firepower: FirepowerScheme
    mobility: MobilityAddScheme | MobilityShowScheme
    vision: VisionScheme
    stealth: StealthScheme


class TankTypeScheme(str, Enum):
    heavy: str = 'Тяжелый'
    medium: str = 'Средний'
    light: str = 'Лёгкий'
    sau: str = 'САУ'
    pt_sau: str = 'ПТ-САУ'


class TankCountryScheme(str, Enum):
    ussr: str = 'СССР'
    germany: str = 'Германия'
    france: str = 'Франция'
    usa: str = 'США'
    china: str = 'Китай'
    uk: str = 'Великобритания'
    poland: str = 'Польша'
    japan: str = 'Япония'
    czech: str = 'Чехословакия'
    sweden: str = 'Швеция'
    italy: str = 'Италия'


class TankAddScheme(BaseModel):
    name: str
    level: int = Field(ge=1, le=10)
    country: TankCountryScheme
    type: TankTypeScheme
    specification: SpecificationScheme | None


class TankShowScheme(TankAddScheme):
    tank_id: int
    slug_field: str
