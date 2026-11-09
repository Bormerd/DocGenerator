import ast
import os
from pathlib import Path

from docgenerator.jsdoc_parser import parse_javascript_file


def get_function_info(node):
    """Получает информацию о функции или методе."""

    parameters = []

    positional_args = node.args.posonlyargs + node.args.args
    defaults = [None] * (len(positional_args) - len(node.args.defaults))
    defaults += node.args.defaults

    for arg, default in zip(positional_args, defaults):
        parameter = arg.arg

        if arg.annotation:
            parameter += f": {ast.unparse(arg.annotation)}"

        if default is not None:
            parameter += f" = {ast.unparse(default)}"

        parameters.append(parameter)

    for index, arg in enumerate(node.args.kwonlyargs):
        parameter = arg.arg

        if arg.annotation:
            parameter += f": {ast.unparse(arg.annotation)}"

        default = node.args.kw_defaults[index]

        if default is not None:
            parameter += f" = {ast.unparse(default)}"

        parameters.append(parameter)

    if node.args.vararg:
        parameters.append(f"*{node.args.vararg.arg}")

    if node.args.kwarg:
        parameters.append(f"**{node.args.kwarg.arg}")

    return_annotation = ""

    if node.returns:
        return_annotation = f" -> {ast.unparse(node.returns)}"

    return {
        "name": node.name,
        "parameters": parameters,
        "return_annotation": return_annotation,
        "description": ast.get_docstring(node) or "Описание отсутствует",
    }


def parse_python_file(file_path):
    """Анализирует Python-файл и возвращает найденные классы и функции."""

    file_path = Path(file_path)

    source_code = file_path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source_code)

    result = {
        "file": file_path.name,
        "classes": [],
        "functions": [],
    }

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            result["functions"].append(get_function_info(node))

        elif isinstance(node, ast.ClassDef):
            class_info = {
                "name": node.name,
                "description": ast.get_docstring(node) or "Описание отсутствует",
                "methods": [],
            }

            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    class_info["methods"].append(get_function_info(item))

            result["classes"].append(class_info)

    return result


def parse_python_directory(directory_path):
    """Анализирует все Python-файлы в указанной папке."""

    directory_path = Path(directory_path)
    results = []

    for file_path in sorted(directory_path.rglob("*.py")):
        if "__pycache__" in file_path.parts:
            continue

        results.append(parse_python_file(file_path))

    return results


def parse_project_directory(directory_path):
    """Анализирует Python- и JavaScript-файлы в указанной папке."""

    directory_path = Path(directory_path)
    excluded_directories = {
        ".venv",
        "venv",
        ".git",
        "__pycache__",
        "node_modules",
        ".pytest_cache",
        "build",
        "dist",
    }

    file_paths = []

    for current_directory, directories, filenames in os.walk(directory_path):
        directories[:] = [
            directory for directory in directories if directory not in excluded_directories
        ]

        for filename in filenames:
            file_path = Path(current_directory) / filename

            if file_path.suffix in (".py", ".js"):
                file_paths.append(file_path)

    results = []

    for file_path in sorted(file_paths):
        if file_path.suffix == ".py":
            results.append(parse_python_file(file_path))
        elif file_path.suffix == ".js":
            results.append(parse_javascript_file(file_path))

    return results
