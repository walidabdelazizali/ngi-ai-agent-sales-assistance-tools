import sys
from pathlib import Path
from src.parsers.network_workbook_parser import parse_network_workbook

SRC = Path("data/networks/raw/uae_network_feb_2026_source.xlsx")
OUTDIR = Path("runtime_data/networks")

if not SRC.exists():
    print(f"Source file not found: {SRC}")
    sys.exit(1)

OUTDIR.mkdir(parents=True, exist_ok=True)

print(f"Inspecting: {SRC}")
results = parse_network_workbook(SRC, OUTDIR)

print("\nSummary:")
for r in results:
    print(f"Sheet: {r['sheet']}")
    print(f"  Output: {r['output']}")
    print(f"  Row count: {r['row_count']}")
    print(f"  Headers: {r['headers']}")
    print("-"*40)
