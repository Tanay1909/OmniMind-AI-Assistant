"""
=========================================================
OmniMind AI Assistant
Export Service
=========================================================

Provides export functionality for:

- JSON
- TXT
- Markdown
- CSV
- HTML

Future:
- PDF
- DOCX
- Excel
"""

from __future__ import annotations

import csv
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any

# ==========================================================
# EXPORT REQUEST
# ==========================================================


@dataclass(slots=True)
class ExportRequest:
    """
    Standard export request.
    """

    data: Any

    output_path: str | Path


# ==========================================================
# BASE EXPORTER
# ==========================================================


class BaseExporter(ABC):
    """
    Base exporter.
    """

    @abstractmethod
    def export(
        self,
        request: ExportRequest,
    ) -> Path:
        raise NotImplementedError


# ==========================================================
# JSON EXPORTER
# ==========================================================


class JSONExporter(BaseExporter):

    def export(
        self,
        request: ExportRequest,
    ) -> Path:

        output = Path(request.output_path)

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                request.data,
                file,
                indent=4,
                ensure_ascii=False,
            )

        return output


# ==========================================================
# TEXT EXPORTER
# ==========================================================


class TextExporter(BaseExporter):

    def export(
        self,
        request: ExportRequest,
    ) -> Path:

        output = Path(request.output_path)

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            if isinstance(request.data, list):

                for item in request.data:

                    file.write(f"{item}\n")

            else:

                file.write(str(request.data))

        return output


# ==========================================================
# MARKDOWN EXPORTER
# ==========================================================


class MarkdownExporter(BaseExporter):

    def export(
        self,
        request: ExportRequest,
    ) -> Path:

        output = Path(request.output_path)

        with output.open(
            "w",
            encoding="utf-8",
        ) as file:

            file.write("# OmniMind Export\n\n")

            if isinstance(request.data, list):

                for item in request.data:

                    file.write(f"- {item}\n")

            else:

                file.write(str(request.data))

        return output


# ==========================================================
# HTML EXPORTER
# ==========================================================


class HTMLExporter(BaseExporter):

    def export(
        self,
        request: ExportRequest,
    ) -> Path:

        output = Path(request.output_path)

        html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>OmniMind Export</title>
</head>
<body>
<pre>
{request.data}
</pre>
</body>
</html>
"""

        output.write_text(
            html,
            encoding="utf-8",
        )

        return output


# ==========================================================
# CSV EXPORTER
# ==========================================================


class CSVExporter(BaseExporter):

    def export(
        self,
        request: ExportRequest,
    ) -> Path:

        output = Path(request.output_path)

        rows = request.data

        with output.open(
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.writer(file)

            if rows:

                writer.writerow(rows[0].keys())

                for row in rows:

                    writer.writerow(row.values())

        return output


# ==========================================================
# EXPORT SERVICE
# ==========================================================


class ExportService:
    """
    High-level export interface.
    """

    def __init__(self):

        self.exporters = {
            "json": JSONExporter(),
            "txt": TextExporter(),
            "md": MarkdownExporter(),
            "html": HTMLExporter(),
            "csv": CSVExporter(),
        }

    # ------------------------------------------------------

    def register_exporter(
        self,
        extension: str,
        exporter: BaseExporter,
    ) -> None:

        self.exporters[extension.lower()] = exporter

    # ------------------------------------------------------

    def export(
        self,
        data: Any,
        output_path: str | Path,
    ) -> Path:

        output = Path(output_path)

        extension = output.suffix.lower().replace(
            ".",
            "",
        )

        if extension not in self.exporters:

            raise ValueError(f"No exporter registered for '{extension}'.")

        request = ExportRequest(
            data=data,
            output_path=output,
        )

        return self.exporters[extension].export(request)
