import re
from pathlib import Path


def parse_jsdoc_comment(comment):
    """Извлекает описание, параметры и возвращаемое значение из JSDoc."""

    lines = []

    for line in comment.splitlines():
        line = line.strip()
        line = line.lstrip("*").strip()

        if line:
            lines.append(line)

    description_lines = []
    parameters = []
    return_annotation = ""

    for line in lines:
        if line.startswith("@param"):
            match = re.match(
                r"@param\s+\{([^}]+)\}\s+(\[?[^\s\]]+\]?)",
                line,
            )

            if match:
                parameter_type = match.group(1)
                parameter_name = match.group(2).strip("[]")
                parameters.append(f"{parameter_name}: {parameter_type}")

        elif line.startswith(("@returns", "@return")):
            match = re.match(r"@returns?\s+\{([^}]+)\}", line)

            if match:
                return_annotation = f" -> {match.group(1)}"

        elif not line.startswith("@"):
            description_lines.append(line)

    description = " ".join(description_lines)

    if not description:
        description = "Описание отсутствует"

    return {
        "description": description,
        "parameters": parameters,
        "return_annotation": return_annotation,
    }


def parse_javascript_file(file_path):
    """Анализирует JavaScript-файл и извлекает данные из JSDoc."""

    file_path = Path(file_path)
    source_code = file_path.read_text(encoding="utf-8-sig")

    result = {
        "file": file_path.name,
        "classes": [],
        "functions": [],
    }

    pattern = re.compile(
        r"/\*\*(.*?)\*/\s*"
        r"((?:(?:export|default|async)\s+)*"
        r"(?:function\s+\w+\s*\([^)]*\)|class\s+\w+))",
        re.DOTALL,
    )

    for match in pattern.finditer(source_code):
        comment = match.group(1)
        declaration = match.group(2)

        jsdoc_info = parse_jsdoc_comment(comment)

        function_match = re.search(
            r"function\s+(\w+)\s*\(([^)]*)\)",
            declaration,
        )

        class_match = re.search(r"class\s+(\w+)", declaration)

        if function_match:
            name = function_match.group(1)
            declared_parameters = function_match.group(2)

            if not jsdoc_info["parameters"] and declared_parameters.strip():
                jsdoc_info["parameters"] = [
                    parameter.strip()
                    for parameter in declared_parameters.split(",")
                    if parameter.strip()
                ]

            result["functions"].append(
                {
                    "name": name,
                    "parameters": jsdoc_info["parameters"],
                    "return_annotation": jsdoc_info["return_annotation"],
                    "description": jsdoc_info["description"],
                }
            )

        elif class_match:
            result["classes"].append(
                {
                    "name": class_match.group(1),
                    "description": jsdoc_info["description"],
                    "methods": [],
                }
            )

    return result
