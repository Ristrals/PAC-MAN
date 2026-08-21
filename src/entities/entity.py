# PACMAN - 42Luxembourg 2026 - kmalfois

from typing import Annotated
from abc import ABC
from pydantic import BaseModel, Field


class EntityModel(ABC, BaseModel):
    _coord_y: Annotated[int, Field(alias="coord_y", description="Coordinate y")]
    _coord_x: Annotated[int, Field(alias="coord_x", description="Coordinate x")]
    _active: bool = Field(alias="active", description="Is this entity active?")