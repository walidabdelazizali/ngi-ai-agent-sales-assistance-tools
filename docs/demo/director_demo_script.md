# Director Demo Script

## 5-Minute Live Demo Flow

### Opening Query
1. Is Accuracy Plus Medical Laboratory in the network?
   - (Shows instant provider lookup and network status)

### Core Proof Queries
2. What is the annual limit for Remedy 02?
   - (Demonstrates plan field extraction)
3. What is the pharmacy benefit for Remedy 02?
   - (Shows benefit detail extraction)
4. Compare Remedy 02 and Remedy 03 for maternity cover.
   - (Highlights plan comparison)
5. What city is International Modern Hospital located in?
   - (Provider location proof)
6. What type of provider is Burjeel Specialty Hospital Sharjah?
   - (Provider type proof)
7. Which network tiers is Aster Hospital (Qusais) available in?
   - (Shows tiered network access)
8. Is Ajman Specialty Hospital covered under HN Basic Plus?
   - (Plan-aware network proof)
9. What is the co-pay for outpatient services in Remedy 03?
   - (Out-of-pocket cost proof)
10. Summarize the key exclusions for Remedy 02.
   - (Risk/compliance proof)

### Arabic Proof
11. هل مختبر Accuracy Plus الطبي داخل الشبكة؟
    - (Arabic provider lookup)
12. ما هي حدود التغطية السنوية لخطة Remedy 02؟
    - (Arabic plan field)
13. ما هي مزايا الصيدلية في Remedy 03؟
    - (Arabic benefit detail)
14. هل مستشفى أستر (القصيص) مشمول في الشبكة؟
    - (Arabic provider + network)
15. ما هي المستشفيات المتاحة في شبكة HN Basic Plus؟
    - (Arabic network listing)

## Entrypoints for Live Demo
- Plan/benefit queries: `python -m src.query ...` or `python scripts/parse_remedy.py ...`
- Network/provider queries: `PYTHONPATH=. python scripts/ask_network.py ...`
- Arabic queries: Use same entrypoints with Arabic input

## Notes
- Use only provided sample data/outputs
- If a query fails, show fallback message as expected
- Do not attempt DOCX ingestion or unsupported features live
