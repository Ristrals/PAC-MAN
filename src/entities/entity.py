# PACMAN - 42Luxembourg 2026 - kmalfois

from typing import Annotated
from abc import ABC
from pydantic import BaseModel, Field


class EntityModel(ABC, BaseModel):
    _y: Annotated[int, Field(alias="y", description="Coordinate y")]
    _x: Annotated[int, Field(alias="x", description="Coordinate x")]
    _active: bool = Field(alias="active", description="Is this entity active?")