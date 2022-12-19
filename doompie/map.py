from doompie.wad.constants import WADMapLumpTypes
from doompie.wad.models import WADVertex
from doompie.wad.utils import extract_lindefs, extract_vertexes, extract_things
from doompie.wad.wad import WAD


class Map:
    def __init__(
        self,
        name: str,
        *,
        wad: WAD,
    ) -> None:
        assert name in wad.maps
        self.name = name
        lumps = wad.get_map_lumps(name)
        self.vertexes: tuple[WADVertex, ...] = extract_vertexes(wad.data, lumps[WADMapLumpTypes.VERTEXES])
        self.linedefs = extract_lindefs(wad.data, lumps[WADMapLumpTypes.LINEDEFS])
        self.things = extract_things(wad.data, lumps[WADMapLumpTypes.THINGS])
