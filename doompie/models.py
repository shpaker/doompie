from enum import Enum
from typing import NamedTuple

from pydantic.dataclasses import dataclass


class WADTypes(Enum):
    PWAD = b"PWAD"
    IWAD = b"IWAD"


@dataclass(frozen=True)
class WADHeader:
    wad_type: WADTypes
    files_count: int
    files_offset: int


class WADLump(
    NamedTuple,
):
    offset: int
    size: int
    name: str


@dataclass(frozen=True)
class WADVertex:
    x: int
    y: int


@dataclass(frozen=True)
class WADLindef:
    beginning_vertex: int
    ending_vertex: int
    flags: int
    line_type: int
    sector_tag: int
    right_sidedef: int | None
    left_sidedef: int | None


@dataclass(frozen=True)
class WADThing:
    x: int
    y: int
    angle: int
    type: int
    flags: int
