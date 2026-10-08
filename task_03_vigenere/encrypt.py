from task_03_vigenere.cipher import encrypt_text
from tools.console import ask_path, run
from tools.files import save_bytes


def main() -> int:
    text = input("Текст для шифрования: ")
    key = input("Ключ (русские буквы): ")
    encrypted = encrypt_text(text, key)
    destination = ask_path("Файл для шифротекста", "output/vigenere.txt")
    if save_bytes(destination, encrypted.encode("utf-8")):
        print(f"Шифротекст сохранён: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(main))
