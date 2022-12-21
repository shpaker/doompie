from struct import calcsize, unpack

from pydantic import BaseModel

from doompie.constants import (
    MapLumpTypes,
)
from doompie.wad import WAD
from doompie.models import WADLindef, WADLump, WADThing, WADVertex


class Map:
    def __init__(
        self,
        name: str,
        *,
        wad: WAD,
    ) -> None:
        assert name in wad.map_names
        self.wad = wad
        self.name = name
        self.lumps = wad.get_map_lumps(name)

    def _unpack_map_lump_structs(
        self,
        lump: WADLump,
        lump_struct: str,
    ):
        wad_vertexes_length = calcsize(lump_struct)
        lump_data = self.wad.read_lump(lump)
        start_offset = 0
        end_offset = wad_vertexes_length
        while end_offset <= lump.size:
            yield unpack(lump_struct, lump_data[start_offset:end_offset])
            start_offset += wad_vertexes_length
            end_offset = start_offset + wad_vertexes_length

    def _read_lump_data(
        self,
        lump_type: MapLumpTypes,
    ) -> tuple[BaseModel, ...]:
        lump = self.lumps[MapLumpTypes.LINEDEFS]
        map_lump_structs = self._unpack_map_lump_structs(
            lump=lump,
            lump_struct=MapLumpTypes[lump_type.name].pack_format,
        )
        model = MapLumpTypes[lump_type.name].model
        return tuple(model(*unpacked) for unpacked in map_lump_structs)

    @property
    def vertexes(self) -> tuple[WADVertex, ...]:
        return self._read_lump_data(MapLumpTypes.VERTEXES)

    @property
    def linedefs(self) -> tuple[WADLindef, ...]:
        return self._read_lump_data(MapLumpTypes.LINEDEFS)

    @property
    def things(self) -> tuple[WADThing, ...]:
        return self._read_lump_data(MapLumpTypes.THINGS)
