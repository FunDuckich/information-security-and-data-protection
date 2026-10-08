import json

from task_04_gamma.cipher import apply_gamma
from tools.console import ask_path, confirm, run
from tools.files import save_bytes


def main() -> int:
    source = ask_path("Файл с шифротекстом", "output/gamma.bin")
    with source.open("rb") as stream:
        header = json.loads(stream.readline().decode("utf-8"))
        encrypted = stream.read()
    if (
        not isinstance(header, dict)
        or set(header) != {"salt", "encoding"}
        or header["encoding"] not in ("utf-8", "cp1251")
    ):
        raise ValueError("В файле должны быть соль и кодировка utf-8 или cp1251.")
    data = apply_gamma(encrypted, header["salt"])
    text = data.decode(header["encoding"])
    print(f"Соль: {header['salt']}")
    print("Расшифрованный текст:")
    print(text)
    if confirm("Сохранить текст в файл?"):
        destination = ask_path("Файл для текста", "output/gamma_restored.txt")
        if save_bytes(destination, data, source):
            print(f"Текст сохранён: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(main))
