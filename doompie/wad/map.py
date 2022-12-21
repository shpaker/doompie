from struct import calcsize, unpack
from typing import Union

from doompie.wad.constants import WADMapLumpTypes, WAPMapLumpStruct, WAPMapLumpModel
from doompie.wad.models import WADVertex, WADLump, WADLindef, WADThing
from doompie.wad.data import WADData


class WADMap:
    def __init__(
        self,
        name: str,
        *,
        wad: WADData,
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
        lump_type: WADMapLumpTypes,
    ) -> tuple[Union[WADVertex, WADLindef, WADThing], ...]:
        lump = self.lumps[WADMapLumpTypes.LINEDEFS]
        map_lump_structs = self._unpack_map_lump_structs(
            lump=lump,
            lump_struct=WAPMapLumpStruct[lump_type.name].value,
        )
        model = WAPMapLumpModel[lump_type.name].value
        return tuple(model(*unpacked) for unpacked in map_lump_structs)

    @property
    def vertexes(self) -> tuple[WADVertex, ...]:
        return self._read_lump_data(WADMapLumpTypes.VERTEXES)

    @property
    def linedefs(self) -> tuple[WADLindef, ...]:
        return self._read_lump_data(WADMapLumpTypes.LINEDEFS)

    @property
    def things(self) -> tuple[WADThing, ...]:
        return self._read_lump_data(WADMapLumpTypes.THINGS)
