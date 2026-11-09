from docgenerator.jsdoc_parser import parse_javascript_file
from docgenerator.parser import (
    parse_project_directory,
    parse_python_directory,
    parse_python_file,
)


def test_parse_function(tmp_path):
    file_path = tmp_path / "example.py"

    file_path.write_text(
        'def hello(name):\n    """Приветствует пользователя."""\n    print(name)\n',
        encoding="utf-8",
    )

    result = parse_python_file(file_path)

    assert len(result["functions"]) == 1
    assert result["functions"][0]["name"] == "hello"
    assert result["functions"][0]["parameters"] == ["name"]
    assert result["functions"][0]["description"] == "Приветствует пользователя."


def test_parse_class(tmp_path):
    file_path = tmp_path / "example.py"

    file_path.write_text(
        "class Computer:\n"
        '    """Класс компьютера."""\n'
        "    def start(self):\n"
        '        """Запускает компьютер."""\n'
        "        pass\n",
        encoding="utf-8",
    )

    result = parse_python_file(file_path)

    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "Computer"
    assert result["classes"][0]["description"] == "Класс компьютера."
    assert result["classes"][0]["methods"][0]["name"] == "start"


def test_parse_function_signature(tmp_path):
    file_path = tmp_path / "example.py"

    file_path.write_text(
        "def calculate(price: float, count: int = 1) -> float:\n"
        '    """Рассчитывает стоимость."""\n'
        "    return price * count\n",
        encoding="utf-8",
    )

    result = parse_python_file(file_path)

    function = result["functions"][0]

    assert function["name"] == "calculate"
    assert function["parameters"] == [
        "price: float",
        "count: int = 1",
    ]
    assert function["return_annotation"] == " -> float"


def test_parse_python_directory(tmp_path):
    first_file = tmp_path / "first.py"
    second_file = tmp_path / "second.py"

    first_file.write_text(
        'def hello():\n    """Приветствует пользователя."""\n    pass\n',
        encoding="utf-8",
    )

    second_file.write_text(
        'class Computer:\n    """Класс компьютера."""\n    pass\n',
        encoding="utf-8",
    )

    result = parse_python_directory(tmp_path)

    assert len(result) == 2
    assert result[0]["file"] == "first.py"
    assert result[0]["functions"][0]["name"] == "hello"
    assert result[1]["file"] == "second.py"
    assert result[1]["classes"][0]["name"] == "Computer"


def test_parse_javascript_function(tmp_path):
    file_path = tmp_path / "example.js"

    file_path.write_text(
        "/**\n"
        " * Рассчитывает стоимость оборудования.\n"
        " * @param {number} price Цена оборудования.\n"
        " * @param {number} count Количество.\n"
        " * @returns {number} Итоговая стоимость.\n"
        " */\n"
        "function calculate(price, count) {\n"
        "    return price * count;\n"
        "}\n",
        encoding="utf-8",
    )

    result = parse_javascript_file(file_path)

    function = result["functions"][0]

    assert function["name"] == "calculate"
    assert function["parameters"] == [
        "price: number",
        "count: number",
    ]
    assert function["return_annotation"] == " -> number"
    assert function["description"] == "Рассчитывает стоимость оборудования."


def test_parse_javascript_class(tmp_path):
    file_path = tmp_path / "example.js"

    file_path.write_text(
        "/**\n * Класс компьютерного оборудования.\n */\nclass Computer {\n}\n",
        encoding="utf-8",
    )

    result = parse_javascript_file(file_path)

    assert len(result["classes"]) == 1
    assert result["classes"][0]["name"] == "Computer"
    assert result["classes"][0]["description"] == "Класс компьютерного оборудования."


def test_parse_mixed_project_directory(tmp_path):
    python_file = tmp_path / "example.py"
    javascript_file = tmp_path / "example.js"

    python_file.write_text(
        'def hello():\n    """Приветствует пользователя."""\n    pass\n',
        encoding="utf-8",
    )

    javascript_file.write_text(
        "/**\n * Приветствует пользователя.\n */\nfunction hello() {\n    return true;\n}\n",
        encoding="utf-8",
    )

    result = parse_project_directory(tmp_path)

    assert len(result) == 2
    assert result[0]["file"] == "example.js"
    assert result[1]["file"] == "example.py"

    assert result[0]["functions"][0]["name"] == "hello"
    assert result[1]["functions"][0]["name"] == "hello"


def test_parse_project_skips_venv(tmp_path):
    project_directory = tmp_path / "project"
    virtual_environment = project_directory / ".venv"

    project_directory.mkdir()
    virtual_environment.mkdir()

    (project_directory / "main.py").write_text(
        "def main():\n    pass\n",
        encoding="utf-8",
    )

    (virtual_environment / "library.py").write_text(
        "def library_function():\n    pass\n",
        encoding="utf-8",
    )

    result = parse_project_directory(project_directory)

    assert len(result) == 1
    assert result[0]["file"] == "main.py"
