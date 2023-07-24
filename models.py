import datetime

from typing import List
from typing import Optional

from sqlalchemy import func
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    creation_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
    modification_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


user_group = Table(
    "user_group",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("group_id", ForeignKey("group.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(320), unique=True)
    pass_hash: Mapped[str] = mapped_column(String(200))
    is_activated: Mapped[bool] = mapped_column(default=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deletion_date: Mapped[Optional[datetime.datetime]] = mapped_column(default=None)

    groups_admin: Mapped[List["Group"]] = relationship(back_populates="admin",
                                                       primaryjoin=lambda: User.id == Group.admin_id
                                                       )
    groups: Mapped[List["Group"]] = relationship(secondary=user_group, back_populates="users")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, " \
                f"first_name={self.first_name!r}, " \
                f"last_name={self.last_name!r}, " \
                f"email={self.email!r}, " \
                f"is_activated={self.is_activated!r}, " \
                f"is_deleted={self.is_deleted!r}, " \
                f"deletion_date={self.deletion_date!r}, " \
                f"creation_date={self.creation_date!r}, "\
                f"modification_date={self.modification_date!r}" \
               f")"


class Group(Base):
    __tablename__ = "group"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(200))

    admin: Mapped["User"] = relationship(back_populates="groups_admin", foreign_keys=[admin_id])
    users: Mapped[List["User"]] = relationship(secondary=user_group, back_populates="groups")
    events: Mapped[List["Event"]] = relationship(back_populates="group",
                                                 cascade="all, delete-orphan",
                                                 primaryjoin=lambda: Group.id == Event.group_id
                                                 )

    def __repr__(self) -> str:
        return f"Group(id={self.id!r}, " \
                f"admin={self.admin!r}, " \
                f"name={self.name!r}, " \
                f"description={self.description!r}, " \
                f"creation_date={self.creation_date!r}, "\
                f"modification_date={self.modification_date!r}" \
               f")"


class Event(Base):
    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey("group.id"))
    name: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(200))
    date: Mapped[datetime.datetime] = mapped_column()

    group: Mapped["Group"] = relationship(back_populates="events", foreign_keys=[group_id])

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, " \
                f"group={self.group!r}, " \
                f"name={self.name!r}, " \
                f"description={self.description!r}, " \
                f"date={self.date!r}, "\
                f"creation_date={self.creation_date!r}, "\
                f"modification_date={self.modification_date!r}" \
               f")"
