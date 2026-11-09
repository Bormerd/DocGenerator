from docgenerator.generator import generate_markdown


def test_generate_markdown(tmp_path):
    template_path = tmp_path / "template.md"

    template_path.write_text(
        "# Документация проекта\n\n"
        "Файл: {{ file }}\n\n"
        "## Классы\n\n"
        "{{ classes }}\n\n"
        "## Функции\n\n"
        "{{ functions }}",
        encoding="utf-8",
    )

    data = {
        "file": "example.py",
        "classes": [
            {
                "name": "Computer",
                "description": "Класс компьютера.",
                "methods": [
                    {
                        "name": "start",
                        "parameters": ["self"],
                        "return_annotation": "",
                        "description": "Запускает компьютер.",
                    }
                ],
            }
        ],
        "functions": [
            {
                "name": "hello",
                "parameters": ["name"],
                "return_annotation": "",
                "description": "Приветствует пользователя.",
            },
            {
                "name": "calculate",
                "parameters": ["price: float", "count: int = 1"],
                "return_annotation": " -> float",
                "description": "Рассчитывает стоимость.",
            },
        ],
    }

    result = generate_markdown(data, template_path)

    assert "# Документация проекта" in result
    assert "Файл: example.py" in result
    assert "### Computer" in result
    assert "Класс компьютера." in result
    assert "**start(self)**" in result
    assert "### hello(name)" in result
    assert "### calculate(price: float, count: int = 1) -> float" in result
    assert "Рассчитывает стоимость." in result
