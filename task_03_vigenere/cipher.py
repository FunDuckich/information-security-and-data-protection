ALPHABET = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
INDEX = {character: index for index, character in enumerate(ALPHABET)}


def _transform(text: str, key: str, direction: int) -> str:
    if not key or any(character.lower() not in INDEX for character in key):
        raise ValueError("Ключ должен содержать только русские буквы и не быть пустым.")
    offsets = [INDEX[character.lower()] for character in key]
    result: list[str] = []
    position = 0
    for character in text:
        index = INDEX.get(character.lower())
        if index is None:
            result.append(character)
            continue
        offset = direction * offsets[position % len(offsets)]
        replacement = ALPHABET[(index + offset) % len(ALPHABET)]
        result.append(replacement.upper() if character.isupper() else replacement)
        position += 1
    return "".join(result)


def encrypt_text(text: str, key: str) -> str:
    return _transform(text, key, 1)


def decrypt_text(text: str, key: str) -> str:
    return _transform(text, key, -1)
