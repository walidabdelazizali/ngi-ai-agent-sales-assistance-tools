"""CLI entry point: python -m src"""

from src.config.settings import PROJECT_ROOT


def main() -> None:
    print(f"Project root: {PROJECT_ROOT}")
    # TODO: Wire extraction pipeline here
    print("No pipeline configured yet. Exiting.")


if __name__ == "__main__":
    main()
