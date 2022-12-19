from collections import defaultdict
from struct import calcsize, unpack

from doompie.wad.constants import (
    WAD_HEADER_STRUCT,
    WAD_LUMP_STRUCT,
    WADMapLumpTypes,
    WADTypes,
)
from doompie.wad.models import WADHeader, WADLump


class WAD:
    def __init__(
        self,
        data: bytes,
    ) -> None:
        self.data = data
        self._lumps: tuple[WADLump, ...] | None = None
        self._levels_lumps_pos = self._filter_maps_lumps_pos()

    @property
    def maps(
        self,
    ) -> tuple[str, ...]:
        return tuple(self._levels_lumps_pos.keys())

    @property
    def header(
        self,
    ) -> WADHeader:
        wad_header_length = calcsize(WAD_HEADER_STRUCT)
        unpacked = unpack(
            WAD_HEADER_STRUCT,
            self.data[:wad_header_length],
        )
        return WADHeader(
            wad_type=WADTypes(unpacked[0]),
            files_count=unpacked[1],
            files_offset=unpacked[2],
        )

    @property
    def lumps(
        self,
    ) -> tuple[WADLump, ...]:
        if self._lumps:
            return self._lumps
        header = self.header
        files = []
        wad_lump_length = calcsize(WAD_LUMP_STRUCT)
        for i in range(header.files_count):
            start_offset = header.files_offset + (i * wad_lump_length)
            unpacked = unpack(
                WAD_LUMP_STRUCT,
                self.data[start_offset: start_offset + wad_lump_length],
            )
            lump_name = unpacked[2].rstrip(b"\x00").decode()
            files.append(
                WADLump(
                    offset=unpacked[0],
                    size=unpacked[1],
                    name=lump_name,
                )
            )
        self._lumps = tuple(files)
        return self._lumps

    def _filter_maps_lumps_pos(
        self,
    ) -> dict[str, dict[WADMapLumpTypes, int]]:
        marker_lump_pos: int | None = None
        map_lumps = defaultdict(dict)
        for pos, lump in enumerate(self.lumps):
            if lump.size == 0:
                marker_lump_pos = pos
            try:
                lump_type = WADMapLumpTypes[lump.name]
            except KeyError:
                continue
            if marker_lump_pos is None:
                raise ValueError
            map_lumps[self.lumps[marker_lump_pos].name][lump_type] = pos
        return map_lumps

    def get_map_lumps(
        self,
        name: str,
    ) -> dict[WADMapLumpTypes, WADLump]:
        lumps_pos = self._levels_lumps_pos[name]
        return {name: self.lumps[pos] for name, pos in lumps_pos.items()}
