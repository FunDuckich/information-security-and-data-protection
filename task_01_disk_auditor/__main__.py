import json

from task_01_disk_auditor.auditor import MANIFEST_NAME, load_manifest, scan_directory
from tools.console import ask_path, confirm, run
from tools.files import save_bytes


def main() -> int:
    root = ask_path("Каталог для проверки").resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Нужно указать каталог.")
    manifest = root / MANIFEST_NAME
    exists = manifest.exists() or manifest.is_symlink()
    previous = load_manifest(manifest) if exists else {}
    current = scan_directory(root)
    print(f"Проверено файлов: {len(current)}")
    if exists:
        added = sorted(current.keys() - previous.keys())
        removed = sorted(previous.keys() - current.keys())
        changed = sorted(
            name for name in current.keys() & previous.keys() if current[name] != previous[name]
        )
        if not (added or removed or changed):
            print("Изменений не обнаружено.")
            return 0
        for title, names in (("Добавлены", added), ("Удалены", removed), ("Изменены", changed)):
            if names:
                print(f"{title}:")
                for name in names:
                    print(f"  {name}")
        if not confirm("Принять текущее состояние и обновить эталон?"):
            print("Эталон оставлен без изменений.")
            return 1
    data = json.dumps(current, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if save_bytes(manifest, data.encode("utf-8"), overwrite=exists):
        print("Эталон обновлён." if exists else "Эталон создан.")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(main))
