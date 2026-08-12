"""
=========================================================
OmniMind AI Assistant
Documentation Generator
=========================================================

Automatically generates project documentation.

Features
--------
✓ Project structure
✓ Python module listing
✓ Function extraction
✓ Class extraction
✓ Markdown documentation

Usage

python scripts/generate_docs.py
"""

from pathlib import Path
import ast
from datetime import datetime

# ==========================================================
# CONFIGURATION
# ==========================================================

PROJECT_ROOT = Path(".")

OUTPUT_DIR = Path("generated_docs")

OUTPUT_FILE = OUTPUT_DIR / "PROJECT_DOCUMENTATION.md"

EXCLUDED = {

    ".git",

    "__pycache__",

    ".pytest_cache",

    "venv",

    ".venv",

    "generated_docs",

}


# ==========================================================
# DIRECTORY TREE
# ==========================================================

def build_tree(path, indent=""):

    lines = []

    items = sorted(

        path.iterdir(),

        key=lambda x: (x.is_file(), x.name.lower())

    )

    for item in items:

        if item.name in EXCLUDED:

            continue

        lines.append(

            f"{indent}- {item.name}"

        )

        if item.is_dir():

            lines.extend(

                build_tree(

                    item,

                    indent + "  "

                )

            )

    return lines


# ==========================================================
# PYTHON ANALYSIS
# ==========================================================

def analyze_python(file_path):

    with open(

        file_path,

        "r",

        encoding="utf-8"

    ) as file:

        tree = ast.parse(

            file.read()

        )

    classes = []

    functions = []

    for node in ast.walk(tree):

        if isinstance(

            node,

            ast.ClassDef

        ):

            classes.append(

                node.name

            )

        elif isinstance(

            node,

            ast.FunctionDef

        ):

            functions.append(

                node.name

            )

    return classes, functions


# ==========================================================
# GENERATE DOCUMENTATION
# ==========================================================

def generate():

    OUTPUT_DIR.mkdir(

        exist_ok=True

    )

    with open(

        OUTPUT_FILE,

        "w",

        encoding="utf-8"

    ) as document:

        document.write(

            "# OmniMind AI Assistant\n\n"

        )

        document.write(

            "## Auto Generated Documentation\n\n"

        )

        document.write(

            f"Generated: {datetime.now()}\n\n"

        )

        document.write(

            "---\n\n"

        )

        document.write(

            "# Project Structure\n\n"

        )

        for line in build_tree(

            PROJECT_ROOT

        ):

            document.write(

                line + "\n"

            )

        document.write(

            "\n---\n\n"

        )

        document.write(

            "# Python Modules\n\n"

        )

        for py_file in sorted(

            PROJECT_ROOT.rglob("*.py")

        ):

            if any(

                part in EXCLUDED

                for part in py_file.parts

            ):

                continue

            document.write(

                f"## {py_file}\n\n"

            )

            try:

                classes, functions = analyze_python(

                    py_file

                )

                document.write(

                    "**Classes**\n\n"

                )

                if classes:

                    for cls in classes:

                        document.write(

                            f"- {cls}\n"

                        )

                else:

                    document.write(

                        "- None\n"

                    )

                document.write(

                    "\n**Functions**\n\n"

                )

                if functions:

                    for func in functions:

                        document.write(

                            f"- {func}\n"

                        )

                else:

                    document.write(

                        "- None\n"

                    )

                document.write(

                    "\n---\n\n"

                )

            except Exception as error:

                document.write(

                    f"Unable to analyze: {error}\n\n"

                )


# ==========================================================
# MAIN
# ==========================================================

def main():

    print("=" * 60)

    print("Generating Project Documentation")

    print("=" * 60)

    generate()

    print(

        f"\nDocumentation generated successfully."

    )

    print(

        f"Location: {OUTPUT_FILE}"

    )


if __name__ == "__main__":

    main()