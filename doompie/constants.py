from enum import Enum
from typing import Any, Type

from pydantic import BaseModel

from doompie.models import WADLindef, WADThing, WADVertex

WAD_HEADER_STRUCT = "4sII"
WAD_LUMP_STRUCT = "II8s"


class MapLumpTypes(Enum):
    VERTEXES = ("hh", WADVertex)
    LINEDEFS = ("HHHHHHH", WADLindef)
    THINGS = ("hhHHH", WADThing)

    def __eq__(
        self,
        other: Any,
    ) -> bool:
        if isinstance(other, self.__class__):
            return self.name == other.name
        return self.name == other

    def __hash__(
        self,
    ) -> int:
        return hash(self.name)

    def __init__(
        self,
        pack_format: str,
        model: Type[BaseModel],
    ) -> None:
        self.pack_format = pack_format
        self.model = model
