from pathlib import Path

from docgenerator.validator import validate_markdown


def generate_markdown(data, template_path=None):
    """Создаёт Markdown-документацию на основе данных парсера."""

    if template_path:
        template = Path(template_path).read_text(encoding="utf-8")
    else:
        template = Path("templates/default.md").read_text(encoding="utf-8")

    classes = []

    for class_info in data["classes"]:
        class_text = f"### {class_info['name']}\n\n"
        class_text += f"{class_info['description']}\n\n"

        for method in class_info["methods"]:
            parameters = ", ".join(method["parameters"])
            return_annotation = method.get("return_annotation", "")
            signature = f"{method['name']}({parameters}){return_annotation}"

            class_text += f"**{signature}**\n\n"
            class_text += f"{method['description']}\n\n"

        classes.append(class_text)

    functions = []

    for function in data["functions"]:
        parameters = ", ".join(function["parameters"])
        return_annotation = function.get("return_annotation", "")
        signature = f"{function['name']}({parameters}){return_annotation}"

        function_text = f"### {signature}\n\n"
        function_text += f"{function['description']}\n\n"
        functions.append(function_text)

    result = template.replace("{{ file }}", data["file"])
    result = result.replace("{{ classes }}", "".join(classes))
    result = result.replace("{{ functions }}", "".join(functions))

    errors = validate_markdown(result)

    if errors:
        raise ValueError("\n".join(errors))

    return result


def generate_project_markdown(files_data, template_path=None):
    """Создаёт общую документацию для нескольких Python-файлов."""

    documents = []

    for file_data in files_data:
        document = generate_markdown(file_data, template_path)
        documents.append(document)

    return "\n\n---\n\n".join(documents)
