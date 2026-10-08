import sys
from pathlib import Path


def ask_path(prompt: str, default: str = "") -> Path:
    hint = f" [{default}]" if default else ""
    value = input(f"{prompt}{hint}: ").strip() or default
    if not value:
        raise ValueError("Путь не должен быть пустым.")
    return Path(value).expanduser()


def confirm(prompt: str) -> bool:
    return input(f"{prompt} [да/нет]: ").strip().casefold() in {"да", "д", "yes", "y"}


def run(main) -> int:
    try:
        return main()
    except (OSError, ValueError) as error:
        print(f"Ошибка: {error}", file=sys.stderr)
        return 2
    except EOFError:
        print("Ошибка: ввод завершён до получения всех данных.", file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("\nОперация отменена.", file=sys.stderr)
        return 130
