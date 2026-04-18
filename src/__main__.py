"""CLI entry point: python -m src"""

from src.config.settings import PROJECT_ROOT
from src.extractors.docx_extractor import run_ingestion


def main() -> None:
    print(f"Project root: {PROJECT_ROOT}")
    print("Running DOCX ingestion...")
    written = run_ingestion()
    print(f"Done. {len(written)} file(s) written.")


if __name__ == "__main__":
    main()
