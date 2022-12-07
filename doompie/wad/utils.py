from struct import unpack

from doompie.wad.constants import (
    WAD_DATA_HEADER_LENGTH,
    WAD_FILE_DATA_LENGTH,
    WAD_FILE_DATA_STRUCT,
    WAD_HEADER_DATA_STRUCT,
    WADMapLumps,
    WADTypes,
)
from doompie.wad.models import WADFile, WADHeader


def wad_read_header(
    data: bytes,
) -> WADHeader:
    unpacked = unpack(
        WAD_HEADER_DATA_STRUCT,
        data[:WAD_DATA_HEADER_LENGTH],
    )
    return WADHeader(
        wad_type=WADTypes(unpacked[0]),
        files_count=unpacked[1],
        files_offset=unpacked[2],
    )


def wad_read_files(
    data: bytes,
    header: WADHeader | None = None,
) -> list[WADFile]:
    header = header or wad_read_header(data)
    files = []
    for i in range(header.files_count):
        start_offset = header.files_offset + (i * WAD_FILE_DATA_LENGTH)
        unpacked = unpack(
            WAD_FILE_DATA_STRUCT,
            data[start_offset : start_offset + WAD_FILE_DATA_LENGTH],
        )
        filename = unpacked[2].rstrip(b"\x00").decode()
        files.append(
            WADFile(
                offset=unpacked[0],
                size=unpacked[1],
                name=filename,
            )
        )
    return files


def extract_maps_lumps_pos(
    lumps: list[WADFile],
) -> list[int]:
    marker_lump_pos: int | None = None
    map_markers = []
    for pos, lump in enumerate(lumps):
        if lump.size == 0:
            marker_lump_pos = pos
        try:
            WADMapLumps[lump.name]
        except KeyError:
            continue
        if marker_lump_pos is None:
            raise ValueError("Incorrect WAD file")
        if marker_lump_pos not in map_markers:
            map_markers.append(marker_lump_pos)
    return map_markers


# def extract_maps_lumps(
#     lumps: list[WADFile],
# ) -> list[int]:
#
#     while ():
#         ...
