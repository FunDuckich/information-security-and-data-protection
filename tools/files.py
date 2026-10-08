import tempfile
from pathlib import Path

from tools.console import confirm


def save_bytes(
    path: Path, data: bytes, source: Path | None = None, *, overwrite: bool = False
) -> bool:
    if source is not None and (
        source.resolve() == path.resolve() or path.exists() and source.samefile(path)
    ):
        raise ValueError("Входной и выходной файлы должны различаться.")
    if path.is_symlink() or path.is_junction():
        raise ValueError("Нельзя записывать результат по ссылке.")
    if path.exists():
        if not path.is_file():
            raise ValueError("Выходной путь должен указывать на файл.")
        if not overwrite and not confirm(f"Файл {path} существует. Перезаписать?"):
            print("Сохранение отменено.")
            return False
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = tempfile.NamedTemporaryFile(dir=path.parent, delete=False)
    try:
        with temporary:
            temporary.write(data)
        Path(temporary.name).replace(path)
    finally:
        Path(temporary.name).unlink(missing_ok=True)
    return True
