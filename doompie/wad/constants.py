from enum import Enum

from doompie.wad.models import WADThing, WADLindef, WADVertex

WAD_HEADER_STRUCT = "4sII"
WAD_LUMP_STRUCT = "II8s"


class WAPMapLumpStruct(Enum):
    VERTEXES = "hh"
    LINEDEFS = 'HHHHHHH'
    THINGS = 'hhHHH'


class WAPMapLumpModel(Enum):
    VERTEXES = WADVertex
    LINEDEFS = WADLindef
    THINGS = WADThing


class WADMapLumpTypes(Enum):
    VERTEXES = "VERTEXES"
    LINEDEFS = "LINEDEFS"
    SIDEDDEFS = "SIDEDDEFS"
    SECTORS = "SECTORS"
    SSECTORS = "SSECTORS"
    SEGS = "SEGS"
    NODES = "NODES"
    THINGS = "THINGS"
    REJECT = "REJECT"
    BLOCKMAP = "BLOCKMAP"
