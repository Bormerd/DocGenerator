import argparse
from pathlib import Path

from docgenerator.generator import (
    generate_markdown,
    generate_project_markdown,
)
from docgenerator.jsdoc_parser import parse_javascript_file
from docgenerator.parser import (
    parse_project_directory,
    parse_python_file,
)


def main():
    """Запускает программу генерации документации."""

    parser = argparse.ArgumentParser(
        description="Генератор документации Python и JavaScript проектов"
    )

    parser.add_argument(
        "path",
        help="Путь к файлу или папке проекта",
    )

    parser.add_argument(
        "-t",
        "--template",
        help="Путь к Markdown-шаблону",
    )

    parser.add_argument(
        "-o",
        "--output",
        default="README.md",
        help="Имя выходного файла",
    )

    args = parser.parse_args()

    input_path = Path(args.path)

    if not input_path.exists():
        print("Указанный путь не найден.")
        return

    if input_path.is_file():
        if input_path.suffix == ".py":
            data = parse_python_file(input_path)
        elif input_path.suffix == ".js":
            data = parse_javascript_file(input_path)
        else:
            print("Можно обрабатывать только файлы .py и .js.")
            return

        markdown = generate_markdown(data, args.template)

    elif input_path.is_dir():
        files_data = parse_project_directory(input_path)

        if not files_data:
            print("В указанной папке не найдены файлы .py или .js.")
            return

        markdown = generate_project_markdown(
            files_data,
            args.template,
        )

    else:
        print("Указанный путь не является файлом или папкой.")
        return

    Path(args.output).write_text(markdown, encoding="utf-8")

    print(f"Документация успешно создана: {args.output}")


if __name__ == "__main__":
    main()
