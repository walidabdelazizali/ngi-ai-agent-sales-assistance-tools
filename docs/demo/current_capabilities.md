# Current Capabilities

## Plan/Remedy Queries
- Field retrieval (annual limit, pharmacy, etc.)
- Plan comparison (all fields or specific field)
- Plan summary (structured)
- Free-text owner queries (English)
- Output packaging for business/WhatsApp/client

## Network Queries
- Provider lookup by name (English/Arabic)
- Tier, city, type, and network status
- Handles ambiguous/missing providers

## Data Handling
- Reads normalized CSV for network
- Reads JSON for plan extraction

## CLI Entry Points
- `python -m src.query` (field, compare, summary, ask)
- `python scripts/parse_remedy.py <json>`
- `PYTHONPATH=. python scripts/ask_network.py <query>`

## Test Coverage
- Plan/owner query logic
- Network lookup logic
- Extraction/normalization/validation
- CLI and business answer

## Not Supported / Not Demo-Ready
- DOCX ingestion (no input files)
- Web/bot/GUI interfaces
- RAG/AI/LLM features
- User-facing error handling
- Automated deployment/runbooks
