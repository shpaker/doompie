from doompie.wad.constants import WADMapLumpTypes, WADTypes
from doompie.wad.models import WADHeader
from doompie.wad.utils import (
    extract_map_lumps,
    extract_vertexes,
    wad_read_files,
    wad_read_header,
)


def test_wad_read_header_ok(
    doom_wad: bytes,
) -> None:
    header = wad_read_header(doom_wad)
    assert header == WADHeader(
        wad_type=WADTypes.IWAD,
        files_count=1270,
        files_offset=4187499,
    ), header


def test_wad_read_files_ok(
    doom_wad: bytes,
) -> None:
    files = wad_read_files(doom_wad)
    assert len(files) == 1270, len(files)


def test_extract_maps_lumps_pos_ok(
    doom_wad: bytes,
) -> None:
    files = wad_read_files(doom_wad)
    data = extract_map_lumps(files)
    assert data
    testing = extract_vertexes(
        doom_wad, data["E1M1"][WADMapLumpTypes.VERTEXES]
    )
    print(testing)
