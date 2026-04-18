"""CLI entry point: python -m src"""

import sys

from src.config.settings import PROJECT_ROOT
from src.extractors.docx_extractor import run_ingestion


def main() -> int:
    print(f"Project root: {PROJECT_ROOT}")
    print("Running DOCX ingestion...")
    result = run_ingestion()
    result.print_summary()
    return 1 if result.failed else 0


if __name__ == "__main__":
    sys.exit(main())
