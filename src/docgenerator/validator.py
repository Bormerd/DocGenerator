def validate_markdown(markdown):
    """Проверяет корректность сгенерированного Markdown."""

    errors = []

    if not markdown.strip():
        errors.append("Документ пустой")

    if not markdown.startswith("# "):
        errors.append("В документе отсутствует заголовок первого уровня")

    if markdown.count("```") % 2 != 0:
        errors.append("Найдена незакрытая секция кода")

    if "{{" in markdown or "}}" in markdown:
        errors.append("В документе остались незаполненные шаблонные переменные")

    return errors
