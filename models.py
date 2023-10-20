from datetime import datetime
from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


db = SQLAlchemy(model_class=Base)


class Binding(db.Model):
    label: Mapped[str] = mapped_column(primary_key=True)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    color_by: Mapped[str]
    # TODO investigate AssociationProxy once we know how things should be queried
    commands: Mapped[List["BindingCommand"]] = relationship(back_populates="binding")


class BindingCommand(db.Model):
    binding_id = mapped_column(ForeignKey("binding.label"), primary_key=True)
    command_id = mapped_column(ForeignKey("command.label"), primary_key=True)

    binding: Mapped["Binding"] = relationship(back_populates="commands")
    command: Mapped["Command"] = relationship()
    # TODO modifiers list their own devices; should we take it into account or assume they're the same as the keys'?
    primary_device: Mapped[str]  # not an FK as we want to store unknown devices
    primary_key: Mapped[str]
    primary_modifier: Mapped[Optional[str]]
    secondary_device: Mapped[Optional[str]]
    secondary_key: Mapped[Optional[str]]
    secondary_modifier: Mapped[Optional[str]]


class Command(db.Model):
    label: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str]


class Device(db.Model):
    label: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    filename: Mapped[str]
