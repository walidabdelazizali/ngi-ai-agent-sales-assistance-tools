"""
Smoke test for NGI AI Agent Sales Assistance Tools
Validates environment, imports, and demo runner.
"""
import sys
import subprocess

REQUIRED_MODULES = [
    "openpyxl",
    "pandas",
    "lxml",
    "pytest",
    "docx",  # correct import name for python-docx
]

def check_imports():
    failed = []
    for mod in REQUIRED_MODULES:
        try:
            __import__(mod)
        except ImportError:
            failed.append(mod)
    if failed:
        print(f"[FAIL] Missing modules: {', '.join(failed)}")
        return False
    print("[OK] All required modules import successfully.")
    return True

def run_demo_runner():
    try:
        result = subprocess.run([
            sys.executable, "scripts/run_demo_pack.py"
        ], capture_output=True, text=True, check=True)
        print("[OK] Demo runner executed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print("[FAIL] Demo runner failed:")
        print(e.stdout)
        print(e.stderr)
        return False

def main():
    print("== Smoke Test Start ==")
    ok = check_imports()
    if not ok:
        sys.exit(1)
    ok = run_demo_runner()
    if not ok:
        sys.exit(2)
    print("== Smoke Test PASSED ==")

if __name__ == "__main__":
    main()
