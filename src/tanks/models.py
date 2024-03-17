from sqlalchemy import Table, select
from sqlalchemy_utils import create_view
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Gun(Base):
    __tablename__ = 'gun'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    gun_type: Mapped[str] = mapped_column(nullable=False)
    shell_count: Mapped[int] = mapped_column()
    alpha: Mapped[str] = mapped_column(nullable=False)
    penetration: Mapped[str] = mapped_column(nullable=False)
    shell_type: Mapped[str] = mapped_column(nullable=False)
    reload: Mapped[float] = mapped_column(nullable=False)
    inside_reload: Mapped[float] = mapped_column()
    autoreload: Mapped[str] = mapped_column()
    spread: Mapped[float] = mapped_column(nullable=False)
    reduction_time: Mapped[float] = mapped_column(nullable=False)
    dpm: Mapped[int] = mapped_column(nullable=False)
    elevation_vertical_angles: Mapped[str] = mapped_column(nullable=False)
    elevation_horizontal_angles: Mapped[int] = mapped_column(nullable=False)


class Survival(Base):
    __tablename__ = 'survival'
    id: Mapped[int] = mapped_column(primary_key=True)
    hp: Mapped[int] = mapped_column(nullable=False)
    hull_armor: Mapped[str] = mapped_column(nullable=False)
    tower_armor: Mapped[str] = mapped_column(nullable=False)


class Firepower(Base):
    __tablename__ = 'firepower'
    id: Mapped[int] = mapped_column(primary_key=True)
    guns = relationship(Gun, secondary='gun_association_table')


class Mobility(Base):
    __tablename__ = 'mobility'
    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[float] = mapped_column(nullable=False)
    power: Mapped[int] = mapped_column(nullable=False)
    specific_power: Mapped[float] = mapped_column(nullable=False)  # power / weight
    max_forward_speed: Mapped[float] = mapped_column(nullable=False)
    max_backward_speed: Mapped[float] = mapped_column(nullable=False)
    rotation_speed: Mapped[float] = mapped_column(nullable=False)
    tower_rotation_speed: Mapped[float] = mapped_column(nullable=False)


class Vision(Base):
    __tablename__ = 'vision'
    id: Mapped[int] = mapped_column(primary_key=True)
    vision_range: Mapped[int] = mapped_column(nullable=False)
    communication_range: Mapped[int] = mapped_column(nullable=False)


class Stealth(Base):
    __tablename__ = 'stealth'
    id: Mapped[int] = mapped_column(primary_key=True)
    standing_stealth: Mapped[str] = mapped_column(nullable=False)
    moving_stealth: Mapped[str] = mapped_column(nullable=False)


gun_association_table = Table(
    "gun_association_table",
    Base.metadata,
    Column("firepower_id", ForeignKey("firepower.id")),
    Column("gun_id", ForeignKey("gun.id"))
)


class Specification(Base):
    __tablename__ = 'specification'
    id: Mapped[int] = mapped_column(primary_key=True)

    survival_id: Mapped[int] = mapped_column(ForeignKey('survival.id'))
    survival: Mapped[Survival] = relationship(Survival)

    firepower_id: Mapped[int] = mapped_column(ForeignKey('firepower.id'))
    firepower: Mapped[Firepower] = relationship(Firepower)

    mobility_id: Mapped[int] = mapped_column(ForeignKey('mobility.id'))
    mobility: Mapped[Mobility] = relationship(Mobility)

    vision_id: Mapped[int] = mapped_column(ForeignKey('vision.id'))
    vision: Mapped[Vision] = relationship(Vision)

    stealth_id: Mapped[int] = mapped_column(ForeignKey('stealth.id'))
    stealth: Mapped[Stealth] = relationship(Stealth)


class Tank(Base):
    __tablename__ = 'tank'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    level: Mapped[int] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    slug_field: Mapped[str] = mapped_column(nullable=False)
    specification_id: Mapped[int] = mapped_column(ForeignKey('specification.id'), nullable=True)
    specification: Mapped[Specification] = relationship(Specification)

