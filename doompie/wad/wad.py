from doompie.wad.utils import wad_read_files, wad_read_header


class WAD:
    def __init__(
        self,
        data: bytes,
    ) -> None:
        self.header = wad_read_header(data)
        self.files = wad_read_files(data, self.header)
