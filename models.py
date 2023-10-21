import random
import string
from datetime import datetime
from typing import List, Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, JSON, ForeignKey
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    ...


db = SQLAlchemy(model_class=Base)


def generate_binds_label():
    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    while db.session.get(Binding, name):
        name = ''.join(random.choice(string.ascii_lowercase) for _ in range(6))
    return name


class Binding(db.Model):
    raw_file: Mapped[str]
    label: Mapped[str] = mapped_column(primary_key=True, default=generate_binds_label)
    description: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(insert_default=func.now())
    color_by: Mapped[str]
    categories = mapped_column(JSON)
    # TODO investigate AssociationProxy once we know how things should be queried
    commands: Mapped[List["BindingCommand"]] = relationship(back_populates="binding")
    modifiers = relationship('Modifier', order_by='Modifier.index',
                             collection_class=ordering_list('index', count_from=1))


class BindingCommand(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    binding_id: Mapped[str] = mapped_column(ForeignKey("binding.label"))
    binding: Mapped["Binding"] = relationship(back_populates="commands")
    command_id: Mapped[str] = mapped_column(ForeignKey("command.label"))
    command: Mapped["Command"] = relationship()
    device: Mapped[str]  # not an FK as we want to store unknown devices
    key: Mapped[str]
    modifiers = mapped_column(JSON)  # keys for keyboard, indexes for others


class Modifier(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    binding_id: Mapped[str] = mapped_column(ForeignKey("binding.label"))
    binding: Mapped["Binding"] = relationship(back_populates='modifiers')
    index: Mapped[int]
    device: Mapped[str]
    key: Mapped[str]


class Command(db.Model):
    label: Mapped[str] = mapped_column(primary_key=True)
    category: Mapped[str]
    order: Mapped[int]
    name: Mapped[str]
    overridden_by: Mapped[Optional[str]]


class Device(db.Model):
    label: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
    filename: Mapped[str]
