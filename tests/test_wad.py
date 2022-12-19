from doompie import WAD
from doompie.wad.constants import WADMapLumpTypes, WADTypes
from doompie.map import Map
from doompie.wad.models import WADHeader
from doompie.wad.utils import (
    filter_maps_lumps,
    extract_vertexes,
    wad_read_lumps,
    wad_read_header,
    extract_lindefs,
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
    files = wad_read_lumps(doom_wad)
    assert len(files) == 1270, len(files)


def test_extract_maps_lumps(
    doom_wad: bytes,
) -> None:
    lumps = wad_read_lumps(doom_wad)
    data = filter_maps_lumps(lumps)
    assert data
    vertexes = extract_vertexes(
        doom_wad, data["E1M1"][WADMapLumpTypes.VERTEXES]
    )
    assert vertexes
    linedefs = extract_lindefs(
        doom_wad, data["E1M1"][WADMapLumpTypes.LINEDEFS]
    )
    assert linedefs


def test_map(
    doom_wad: bytes,
) -> None:
    wad = WAD(doom_wad)
    map = Map(wad.maps[0], wad=wad)
    assert wad
