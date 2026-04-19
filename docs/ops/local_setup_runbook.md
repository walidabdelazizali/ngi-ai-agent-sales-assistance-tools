# Local Setup Runbook

## 1. Clone the repository
```
git clone https://github.com/walidabdelazizali/ngi-ai-agent-sales-assistance-tools.git
cd NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS
```

## 2. Create and activate virtual environment
```
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On bash (Windows):
source .venv/Scripts/activate
```

## 3. Install dependencies
```
pip install -r requirements.txt
```

## 4. Validate environment
```
python --version
pip list
```

## 5. Run demo runner
```
c:/Projects/NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS/.venv/Scripts/python.exe scripts/run_demo_pack.py
```

## 6. Run smoke test
```
c:/Projects/NGI-AI-AGENT-SALES-ASSISTANCE-TOOLS/.venv/Scripts/python.exe scripts/smoke_test.py
```
