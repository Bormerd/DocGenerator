from docgenerator.validator import validate_markdown


def test_valid_markdown():
    markdown = "# Документация проекта\n\nОписание проекта."

    result = validate_markdown(markdown)

    assert result == []


def test_invalid_markdown():
    markdown = "Документация проекта\n\n```python\nprint('Hello')"

    result = validate_markdown(markdown)

    assert len(result) == 2
    assert "отсутствует заголовок первого уровня" in result[0]
    assert "незакрытая секция кода" in result[1]


def test_unfilled_template():
    markdown = "# Документация\n\n{{ description }}"

    result = validate_markdown(markdown)

    assert "незаполненные шаблонные переменные" in result[0]
