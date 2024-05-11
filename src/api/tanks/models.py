from typing import Optional

from sqlalchemy import Table
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Gun(Base):
    __tablename__ = 'gun'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    gun_type: Mapped[str]
    shell_count: Mapped[int]
    alpha: Mapped[str]
    penetration: Mapped[str]
    shell_type: Mapped[str]
    reload: Mapped[float]
    inside_reload: Mapped[float]
    autoreload: Mapped[str]
    spread: Mapped[float]
    reduction_time: Mapped[float]
    dpm: Mapped[int]
    elevation_vertical_angles: Mapped[str]
    elevation_horizontal_angles: Mapped[int]


class Survival(Base):
    __tablename__ = 'survival'
    id: Mapped[int] = mapped_column(primary_key=True)
    hp: Mapped[int]
    hull_armor: Mapped[str]
    tower_armor: Mapped[str]

    specification: Mapped["Specification"] = relationship(back_populates="survival")


class Firepower(Base):
    __tablename__ = 'firepower'
    id: Mapped[int] = mapped_column(primary_key=True)
    guns = relationship(Gun, secondary='gun_association_table')

    specification: Mapped["Specification"] = relationship(back_populates="firepower")


class Mobility(Base):
    __tablename__ = 'mobility'
    id: Mapped[int] = mapped_column(primary_key=True)
    weight: Mapped[float] = mapped_column(unique=True)
    power: Mapped[int]
    specific_power: Mapped[float]  # power / weight
    max_forward_speed: Mapped[float]
    max_backward_speed: Mapped[float]
    rotation_speed: Mapped[float]
    tower_rotation_speed: Mapped[float]

    specification: Mapped["Specification"] = relationship(back_populates="mobility")


class Vision(Base):
    __tablename__ = 'vision'
    id: Mapped[int] = mapped_column(primary_key=True)
    vision_range: Mapped[int]
    communication_range: Mapped[int]

    specification: Mapped["Specification"] = relationship(back_populates="vision")


class Stealth(Base):
    __tablename__ = 'stealth'
    id: Mapped[int] = mapped_column(primary_key=True)
    standing_stealth: Mapped[str]
    moving_stealth: Mapped[str]

    specification: Mapped["Specification"] = relationship(back_populates="stealth")


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
    survival: Mapped[Survival] = relationship(Survival, back_populates="specification")

    firepower_id: Mapped[int] = mapped_column(ForeignKey('firepower.id'))
    firepower: Mapped[Firepower] = relationship(Firepower, back_populates="specification")

    mobility_id: Mapped[int] = mapped_column(ForeignKey('mobility.id'))
    mobility: Mapped[Mobility] = relationship(Mobility, back_populates="specification")

    vision_id: Mapped[int] = mapped_column(ForeignKey('vision.id'))
    vision: Mapped[Vision] = relationship(Vision, back_populates="specification")

    stealth_id: Mapped[int] = mapped_column(ForeignKey('stealth.id'))
    stealth: Mapped[Stealth] = relationship(Stealth, back_populates="specification")

    tank: Mapped["Tank"] = relationship(back_populates="specification")


class Tank(Base):
    __tablename__ = 'tank'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    level: Mapped[int]
    country: Mapped[str]
    type: Mapped[str]
    slug_field: Mapped[str]
    specification_id: Mapped[Optional[int]] = mapped_column(ForeignKey('specification.id'))
    specification: Mapped[Specification] = relationship(Specification, back_populates="tank")
