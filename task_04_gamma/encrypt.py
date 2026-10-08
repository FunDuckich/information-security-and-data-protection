import json

from task_04_gamma.cipher import apply_gamma
from tools.console import ask_path, run
from tools.files import save_bytes


def main() -> int:
    source = ask_path("Исходный текстовый файл")
    salt = input("Соль (непустая строка): ")
    encoding = input("Кодировка [utf-8/cp1251, Enter — utf-8]: ").strip().lower() or "utf-8"
    if encoding not in {"utf-8", "cp1251"}:
        raise ValueError("Выберите utf-8 или cp1251.")
    data = source.read_bytes()
    data.decode(encoding)
    encrypted = apply_gamma(data, salt)
    header = json.dumps({"salt": salt, "encoding": encoding}, ensure_ascii=False)
    destination = ask_path("Файл для шифротекста", "output/gamma.bin")
    if save_bytes(destination, header.encode("utf-8") + b"\n" + encrypted, source):
        print(f"Зашифровано байтов: {len(data)}")
        print(f"Шифротекст сохранён: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(main))
