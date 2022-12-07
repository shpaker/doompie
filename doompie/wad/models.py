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


class WADVertexes(
    NamedTuple,
):
    x: int
    y: int
