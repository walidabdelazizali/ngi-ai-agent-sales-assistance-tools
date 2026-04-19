import subprocess
import sys
import os
import shlex

# Demo queries (English and Arabic)
DEMO_QUERIES = [
    # Network/Provider
    ("ask_network.py", "Is Accuracy Plus Medical Laboratory in the network?"),
    ("ask_network.py", "Which network tiers is Aster Hospital (Qusais) available in?"),
    ("ask_network.py", "What city is International Modern Hospital located in?"),
    ("ask_network.py", "What type of provider is Burjeel Specialty Hospital Sharjah?"),
    ("ask_network.py", "Is Ajman Specialty Hospital covered under HN Basic Plus?"),
    # Plan/Benefit
    ("-m src.query", "field \"Remedy 02\" \"annual limit\""),
    ("-m src.query", "field \"Remedy 02\" \"pharmacy\""),
    ("-m src.query", "compare \"Remedy 02\" \"Remedy 03\" --field maternity_cover"),
    ("-m src.query", "field \"Remedy 03\" \"outpatient_cover_summary\""),
    ("-m src.query", "field \"Remedy 02\" \"key_exclusions\""),
    # Arabic
    ("ask_network.py", "هل مختبر Accuracy Plus الطبي داخل الشبكة؟"),
    ("-m src.query", "field \"Remedy 02\" \"حدود التغطية السنوية\""),
    ("-m src.query", "field \"Remedy 03\" \"مزايا الصيدلية\""),
    ("ask_network.py", "هل مستشفى أستر (القصيص) مشمول في الشبكة؟"),
    ("ask_network.py", "ما هي المستشفيات المتاحة في شبكة HN Basic Plus؟"),
]

PYTHON = sys.executable

for idx, (entry, query) in enumerate(DEMO_QUERIES, 1):
    print(f"\n{'='*40}\nDemo Query {idx}: {query}\n{'='*40}")
    if entry == "ask_network.py":
        cmd = [PYTHON, "scripts/ask_network.py", query]
        env = dict(**os.environ, PYTHONPATH=".")
    else:
        # Use shlex.split to preserve quoted arguments
        cmd = [PYTHON, "-m", "src.query"] + shlex.split(query)
        env = None
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, env=env, check=True)
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Command failed: {' '.join(cmd)}")
        print(e.stderr.strip())
        sys.exit(1)
