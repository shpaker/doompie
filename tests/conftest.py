from pathlib import Path

from pytest import fixture

_TEST_DIR = Path(__file__).parent.resolve()


@fixture(name="tests_root_dir")
def _tests_root_dir() -> Path:
    return _TEST_DIR


@fixture
def doom_wad(
    tests_root_dir: Path,
) -> bytes:
    path = tests_root_dir / "DOOM1.WAD"
    with open(path, "rb") as fh:
        return fh.read()
