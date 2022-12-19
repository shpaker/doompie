from typing import NamedTuple

from doompie.wad.constants import WADTypes


class WADHeader(
    NamedTuple,
):
    wad_type: WADTypes
    files_count: int
    files_offset: int


class WADLump(
    NamedTuple,
):
    offset: int
    size: int
    name: str


class WADVertex(
    NamedTuple,
):
    x: int
    y: int


class WADLindef(
    NamedTuple,
):
    beginning_vertex: int
    ending_vertex: int
    flags: int
    line_type: int
    sector_tag: int
    right_sidedef: int | None
    left_sidedef: int | None


class WADThings(
    NamedTuple,
):
    x: int
    y: int
    angle: int
    type: int
    flags: int
