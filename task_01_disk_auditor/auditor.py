import json
import os
from pathlib import Path

MANIFEST_NAME = ".integrity.json"


def checksum_file(path: Path) -> str:
    checksum = 0
    with path.open("rb") as stream:
        while block := stream.read(64 * 1024):
            if len(block) % 2:
                block += b"\x00"
            for index in range(0, len(block), 2):
                checksum ^= (block[index] << 8) | block[index + 1]
    return f"{checksum:04x}"


def _raise_error(error: OSError) -> None:
    raise error


def scan_directory(root: Path) -> dict[str, str]:
    files = {}
    for directory, folders, names in os.walk(root, onerror=_raise_error, followlinks=False):
        directory = Path(directory)
        for name in folders[:]:
            path = directory / name
            if path.is_symlink() or path.is_junction():
                folders.remove(name)
                print(f"Пропущена ссылка: {path.relative_to(root)}")
        for name in sorted(names):
            path = directory / name
            if path == root / MANIFEST_NAME:
                continue
            if path.is_symlink() or not path.is_file():
                print(f"Пропущен нестандартный файл: {path.relative_to(root)}")
                continue
            files[path.relative_to(root).as_posix()] = checksum_file(path)
    return files


def load_manifest(path: Path) -> dict[str, str]:
    if path.is_symlink() or path.is_junction():
        raise ValueError("Файл эталона не должен быть ссылкой.")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or any(
        not name
        or not isinstance(checksum, str)
        or len(checksum) != 4
        or any(character not in "0123456789abcdef" for character in checksum)
        for name, checksum in data.items()
    ):
        raise ValueError("Неверный формат эталона: ожидается словарь путей и XOR-16 сумм.")
    return data
