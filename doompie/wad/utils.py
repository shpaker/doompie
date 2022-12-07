from collections import defaultdict
from struct import calcsize, unpack

from doompie.wad.constants import (
    WAD_HEADER_STRUCT,
    WAD_LUMP_STRUCT,
    WAD_VERTEXES_STRUCT,
    WADMapLumpTypes,
    WADTypes,
)
from doompie.wad.models import WADHeader, WADLump, WADVertexes


def wad_read_header(
    data: bytes,
) -> WADHeader:
    wad_header_length = calcsize(WAD_HEADER_STRUCT)
    unpacked = unpack(
        WAD_HEADER_STRUCT,
        data[:wad_header_length],
    )
    return WADHeader(
        wad_type=WADTypes(unpacked[0]),
        files_count=unpacked[1],
        files_offset=unpacked[2],
    )


def wad_read_files(
    data: bytes,
    header: WADHeader | None = None,
) -> list[WADLump]:
    header = header or wad_read_header(data)
    files = []
    wad_lump_length = calcsize(WAD_LUMP_STRUCT)
    for i in range(header.files_count):
        start_offset = header.files_offset + (i * wad_lump_length)
        unpacked = unpack(
            WAD_LUMP_STRUCT,
            data[start_offset : start_offset + wad_lump_length],
        )
        filename = unpacked[2].rstrip(b"\x00").decode()
        files.append(
            WADLump(
                offset=unpacked[0],
                size=unpacked[1],
                name=filename,
            )
        )
    return files


def extract_map_lumps(
    lumps: list[WADLump],
) -> dict[str, dict[WADMapLumpTypes, WADLump]]:
    marker_lump_pos: int | None = None
    map_lumps = defaultdict(dict)
    for pos, lump in enumerate(lumps):
        if lump.size == 0:
            marker_lump_pos = pos
        try:
            lump_type = WADMapLumpTypes[lump.name]
        except KeyError:
            continue
        if marker_lump_pos is None:
            raise ValueError("Incorrect WAD file")
        map_lumps[lumps[marker_lump_pos].name][lump_type] = lump
    return map_lumps


def read_lump_data(
    data: bytes,
    lump: WADLump,
):
    return data[lump.offset : lump.offset + lump.size]


def extract_map_lump_structs(
    data: bytes,
    lump: WADLump,
    lump_struct: str,
):
    wad_vertexes_length = calcsize(lump_struct)
    lump_data = read_lump_data(data, lump)
    start_offset = 0
    end_offset = wad_vertexes_length
    while end_offset <= lump.size:
        yield unpack(WAD_VERTEXES_STRUCT, lump_data[start_offset:end_offset])
        start_offset += wad_vertexes_length
        end_offset = start_offset + wad_vertexes_length


def extract_vertexes(
    data: bytes,
    lump: WADLump,
) -> tuple[WADVertexes, ...]:
    assert lump.name == WADMapLumpTypes.VERTEXES.value, lump
    map_lump_structs = extract_map_lump_structs(
        data, lump, WAD_VERTEXES_STRUCT
    )
    return tuple(WADVertexes(*unpacked) for unpacked in map_lump_structs)
