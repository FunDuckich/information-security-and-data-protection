from task_03_vigenere.cipher import decrypt_text
from tools.console import ask_path, confirm, run
from tools.files import save_bytes


def main() -> int:
    source = ask_path("Файл с шифротекстом", "output/vigenere.txt")
    key = input("Ключ (русские буквы): ")
    text = decrypt_text(source.read_bytes().decode("utf-8"), key)
    print("Расшифрованный текст:")
    print(text)
    if confirm("Сохранить текст в файл?"):
        destination = ask_path("Файл для текста", "output/vigenere_restored.txt")
        if save_bytes(destination, text.encode("utf-8"), source):
            print(f"Текст сохранён: {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run(main))
