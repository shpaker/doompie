from enum import Enum

WAD_HEADER_STRUCT = "4sII"
WAD_LUMP_STRUCT = "II8s"
WAD_VERTEXES_STRUCT = "hh"


class WADTypes(Enum):
    PWAD = b"PWAD"
    IWAD = b"IWAD"


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
